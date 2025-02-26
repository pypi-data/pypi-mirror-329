from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cocas.object_module import CodeLocation, ExternalEntry, ObjectSectionRecord

from ...ast_nodes import LabelNode, RelocatableExpressionNode, TemplateFieldNode
from ...exceptions import AssemblerException, AssemblerExceptionTag
from .. import ICodeSegment, IVaryingLengthSegment
from .branches import check_inverse_branch
from .instruction_codes import simple_instructions

TAG = AssemblerExceptionTag.ASM

if TYPE_CHECKING:
    from ...code_block import Section


class CodeSegment(ICodeSegment, ABC):
    _location = CodeLocation()

    @property
    def location(self) -> CodeLocation:
        return self._location

    @location.setter
    def location(self, value):
        self._location = value


@dataclass
class RelocatableExpressionSegment(CodeSegment, ABC):
    expr: RelocatableExpressionNode = field(init=True)


@dataclass
class VaryingLengthSegment(IVaryingLengthSegment, CodeSegment, ABC):
    is_expanded: bool = field(init=False, default=False)
    expanded_size: int = field(init=False)


class BytesSegment(CodeSegment):
    data: bytearray

    def __init__(self, data: bytearray):
        self.data = data
        self._size = len(data)

    @property
    def size(self) -> int:
        return self._size

    def fill(self, object_record: "ObjectSectionRecord", section: "Section", labels: dict[str, int],
             templates: dict[str, dict[str, int]]):
        object_record.data += self.data


@dataclass
class ShortExpressionSegment(RelocatableExpressionSegment):
    size = 1

    def fill(self, object_record: "ObjectSectionRecord", section: "Section", labels: dict[str, int],
             templates: dict[str, dict[str, int]]):
        val, val_long, val_sect, ext = eval_rel_expr_seg(self, section, labels, templates)

        is_rel = (val_sect == section.name != '$abs')
        if self.expr.byte_specifier is None and (is_rel or ext is not None):
            _error(self, 'Expected a 1-byte expression')
        if not -2 ** 7 <= val < 2 ** 8:
            _error(self, 'Number out of range')

        if is_rel:
            add_rel_record(object_record, section, val_long, self)
        if ext is not None:
            add_ext_record(object_record, ext, section, val_long, self)
        object_record.data.extend(val.to_bytes(self.size, 'little', signed=(val < 0)))


@dataclass
class ConstExpressionSegment(RelocatableExpressionSegment):
    positive: bool = False
    size = 1

    def fill(self, object_record: "ObjectSectionRecord", section: "Section", labels: dict[str, int],
             templates: dict[str, dict[str, int]]):
        val, _, val_sect, ext = eval_rel_expr_seg(self, section, labels, templates)
        if val_sect is not None or ext is not None:
            _error(self, 'Number expected but label found')
        if not -2 ** 7 <= val < 2 ** 8 or (self.positive and val < 0):
            _error(self, 'Number out of range')
        object_record.data.extend(val.to_bytes(self.size, 'little', signed=(val < 0)))


@dataclass
class LongExpressionSegment(RelocatableExpressionSegment):
    size = 2

    def fill(self, object_record: "ObjectSectionRecord", section: "Section", labels: dict[str, int],
             templates: dict[str, dict[str, int]]):
        val, val_long, val_sect, ext = eval_rel_expr_seg(self, section, labels, templates)

        if not -2 ** 15 <= val < 2 ** 16:
            _error(self, 'Number out of range')

        if val_sect:
            add_rel_record(object_record, section, val_long, self)
        if ext is not None:
            add_ext_record(object_record, ext, section, val_long, self)
        object_record.data.extend(val.to_bytes(self.size, 'little', signed=(val < 0)))


@dataclass
class OffsetExpressionSegment(RelocatableExpressionSegment):
    size = 1

    def fill(self, object_record: "ObjectSectionRecord", section: "Section", labels: dict[str, int],
             templates: dict[str, dict[str, int]]):
        val, _, val_sect, ext = eval_rel_expr_seg(self, section, labels, templates)

        is_rel = (val_sect == section.name != '$abs')
        if ext is not None:
            _error(self, 'Invalid destination address (external label used)')
        if section.name != '$abs' and not is_rel:
            _error(self, 'Invalid destination address (absolute address from rsect)')
        if self.expr.byte_specifier is not None and is_rel:
            _error(self, 'Invalid destination address (byte of relocatable address)')

        val -= section.address + len(object_record.data)
        if not -2 ** 7 <= val < 2 ** 7:
            _error(self, 'Destination address is too far')

        object_record.data.extend(val.to_bytes(self.size, 'little', signed=(val < 0)))


class GotoSegment(RelocatableExpressionSegment, VaryingLengthSegment):
    def __init__(self, branch_mnemonic: str, expr: RelocatableExpressionNode):
        # noinspection PyArgumentList
        RelocatableExpressionSegment.__init__(self, expr)
        VaryingLengthSegment.__init__(self)
        self.branch_mnemonic = branch_mnemonic

    base_size = 2
    expanded_size = 5

    @property
    def size(self) -> int:
        if self.is_expanded:
            return self.expanded_size
        else:
            return self.base_size

    def update_varying_length(self, pos: int, section: "Section", labels: dict[str, int],
                              templates: dict[str, dict[str, int]]):
        try:
            if self.is_expanded:
                return

            addr, _, res_sect, ext = eval_rel_expr_seg(self, section, labels, templates)
            is_rel = (res_sect == section.name != '$abs')
            if (not -2 ** 7 <= addr - (pos + 1) < 2 ** 7
                    or (section.name != '$abs' and not is_rel)
                    or (self.expr.byte_specifier is not None and is_rel)
                    or (ext is not None)):

                shift_length = self.expanded_size - self.base_size
                self.is_expanded = True
                old_locations = section.code_locations
                section.code_locations = dict()
                for PC, location in old_locations.items():
                    if PC > pos:
                        PC += shift_length
                    section.code_locations[PC] = location

                for label_name in section.labels:
                    if section.labels[label_name] > pos:
                        section.labels[label_name] += shift_length
                        if label_name in labels:
                            labels[label_name] += shift_length
                return shift_length
        except AssemblerException as e:
            raise e
        except Exception as e:
            raise AssemblerException(TAG, self.location.file, self.location.line, str(e))

    def fill(self, object_record: "ObjectSectionRecord", section: "Section", labels: dict[str, int],
             templates: dict[str, dict[str, int]]):
        mnemonic = f'b{self.branch_mnemonic}'
        if mnemonic not in simple_instructions['branch']:
            _error(self, f'Invalid branch mnemonic: {mnemonic}')
        if self.is_expanded:

            branch_opcode = simple_instructions['branch'][
                f'b{check_inverse_branch(self.branch_mnemonic, inverse=True)}']
            jmp_opcode = simple_instructions['long']['jmp']
            object_record.data += bytearray([branch_opcode, 4, jmp_opcode])
            LongExpressionSegment(self.expr).fill(object_record, section, labels, templates)
        else:
            branch_opcode = simple_instructions['branch'][mnemonic]
            object_record.data += bytearray([branch_opcode])
            OffsetExpressionSegment(self.expr).fill(object_record, section, labels, templates)


def _error(segment: ICodeSegment, message: str):
    raise AssemblerException(TAG, segment.location.file, segment.location.line, message)


def eval_rel_expr_seg(seg: RelocatableExpressionSegment, s: "Section",
                      labels: dict[str, int], templates: dict[str, dict[str, int]]):
    val_long = seg.expr.const_term
    used_exts = dict()
    s_dim = 0
    local_dim = 0
    for term, m in [(t, 1) for t in seg.expr.add_terms] + [(t, -1) for t in seg.expr.sub_terms]:
        if isinstance(term, LabelNode):
            if term.name in labels:
                local_dim += m
                val_long += labels[term.name] * m
            elif term.name in s.labels:
                s_dim += m
                val_long += s.labels[term.name] * m
            elif term.name in s.exts:
                used_exts.setdefault(term.name, 0)
                used_exts[term.name] += m
            else:
                _error(seg, f'Label "{term.name}" not found')
        elif isinstance(term, TemplateFieldNode):
            val_long += templates[term.template_name][term.field_name] * m

    val_lo, val_hi = val_long.to_bytes(2, 'little', signed=(val_long < 0))
    if seg.expr.byte_specifier == 'low':
        val = val_lo
    elif seg.expr.byte_specifier == 'high':
        val = val_hi
    elif seg.expr.byte_specifier is not None:
        _error(seg, f'Invalid byte specifier "{seg.expr.byte_specifier}". Possible options are "low" and "high"')
        return
    else:
        val = val_long

    used_exts = dict(filter(lambda x: x[1] != 0, used_exts.items()))
    if len(used_exts) > 1:
        _error(seg, 'Cannot use multiple external labels in an address expression')

    if len(used_exts) == 0:
        if s_dim == 0 and local_dim == 0:
            return val, val_long, None, None
        elif s_dim == 0 and local_dim == 1:
            return val, val_long, '$abs', None
        elif s_dim == 1 and local_dim == 0:
            return val, val_long, s.name, None
    else:
        ext, ext_dim = used_exts.popitem()
        if local_dim == 0 and s_dim == 0 and ext_dim == 1:
            return val, val_long, None, ext

    _error(seg, 'Result is not a label or a number')


def add_ext_record(obj_rec: "ObjectSectionRecord", ext: str, s: "Section", val: int,
                   seg: RelocatableExpressionSegment):
    val %= 65536
    val_lo, _ = val.to_bytes(2, 'little', signed=False)
    offset = s.address + len(obj_rec.data)
    if seg.expr.byte_specifier == 'low':
        obj_rec.external.setdefault(ext, []).append(ExternalEntry(offset, range(0, 1), full_bytes=False))
    elif seg.expr.byte_specifier == 'high':
        entry = ExternalEntry(offset, range(1, 2), full_bytes=False, lower_part=val_lo)
        obj_rec.external.setdefault(ext, []).append(entry)
    else:
        obj_rec.external.setdefault(ext, []).append(ExternalEntry(offset, range(0, 2), full_bytes=True))


def add_rel_record(obj_rec: "ObjectSectionRecord", s: "Section", val: int,
                   seg: RelocatableExpressionSegment):
    val %= 65536
    val_lo, _ = val.to_bytes(2, 'little', signed=False)
    offset = s.address + len(obj_rec.data)
    if seg.expr.byte_specifier == 'low':
        obj_rec.relocatable.append(ExternalEntry(offset, range(0, 1), full_bytes=False))
    elif seg.expr.byte_specifier == 'high':
        entry = ExternalEntry(offset, range(1, 2), full_bytes=False, lower_part=val_lo)
        obj_rec.relocatable.append(entry)
    else:
        obj_rec.relocatable.append(ExternalEntry(offset, range(0, 2), full_bytes=True))
