# Generated from assembler/grammar/AsmParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from base64 import b64decode

def serializedATN():
    return [
        4,1,41,398,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,1,0,5,0,86,8,0,10,0,12,0,89,9,0,1,0,5,0,92,8,
        0,10,0,12,0,95,9,0,1,0,5,0,98,8,0,10,0,12,0,101,9,0,1,0,1,0,1,1,
        5,1,106,8,1,10,1,12,1,109,9,1,1,1,4,1,112,8,1,11,1,12,1,113,1,1,
        5,1,117,8,1,10,1,12,1,120,9,1,1,1,5,1,123,8,1,10,1,12,1,126,9,1,
        1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,139,8,2,1,3,1,3,
        1,3,4,3,144,8,3,11,3,12,3,145,1,4,1,4,1,4,4,4,151,8,4,11,4,12,4,
        152,1,5,1,5,1,5,4,5,158,8,5,11,5,12,5,159,1,6,1,6,1,7,1,7,1,7,1,
        7,1,7,1,7,1,7,5,7,171,8,7,10,7,12,7,174,9,7,1,8,1,8,1,8,1,8,3,8,
        180,8,8,1,8,4,8,183,8,8,11,8,12,8,184,1,8,1,8,1,8,1,8,1,8,1,8,1,
        9,1,9,1,10,1,10,1,11,1,11,4,11,199,8,11,11,11,12,11,200,1,12,1,12,
        4,12,205,8,12,11,12,12,12,206,1,13,1,13,1,14,1,14,3,14,213,8,14,
        1,14,4,14,216,8,14,11,14,12,14,217,1,14,3,14,221,8,14,1,14,1,14,
        3,14,225,8,14,1,14,4,14,228,8,14,11,14,12,14,229,3,14,232,8,14,1,
        15,1,15,1,15,1,16,1,16,1,16,5,16,240,8,16,10,16,12,16,243,9,16,1,
        17,1,17,1,17,5,17,248,8,17,10,17,12,17,251,9,17,1,18,1,18,4,18,255,
        8,18,11,18,12,18,256,1,18,1,18,1,18,3,18,262,8,18,1,18,1,18,4,18,
        266,8,18,11,18,12,18,267,1,19,5,19,271,8,19,10,19,12,19,274,9,19,
        1,19,1,19,4,19,278,8,19,11,19,12,19,279,1,19,1,19,4,19,284,8,19,
        11,19,12,19,285,3,19,288,8,19,1,20,1,20,1,20,1,20,4,20,294,8,20,
        11,20,12,20,295,1,21,1,21,1,21,1,21,1,22,1,22,4,22,304,8,22,11,22,
        12,22,305,1,22,1,22,1,23,1,23,1,24,1,24,1,25,1,25,4,25,316,8,25,
        11,25,12,25,317,1,25,1,25,1,25,1,25,4,25,324,8,25,11,25,12,25,325,
        1,25,1,25,1,25,4,25,331,8,25,11,25,12,25,332,1,26,1,26,1,27,1,27,
        4,27,339,8,27,11,27,12,27,340,1,27,1,27,1,27,1,27,4,27,347,8,27,
        11,27,12,27,348,1,28,1,28,1,28,1,28,1,28,3,28,356,8,28,1,29,1,29,
        1,29,1,29,1,29,1,30,1,30,5,30,365,8,30,10,30,12,30,368,9,30,1,31,
        3,31,371,8,31,1,31,1,31,1,32,1,32,1,32,1,33,1,33,3,33,380,8,33,1,
        34,1,34,1,35,1,35,1,36,1,36,1,37,1,37,1,38,1,38,1,39,1,39,1,40,1,
        40,1,41,1,41,1,41,0,0,42,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,
        30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
        74,76,78,80,82,0,4,2,0,23,23,25,25,1,0,21,22,1,0,32,34,2,0,1,18,
        30,31,407,0,87,1,0,0,0,2,107,1,0,0,0,4,138,1,0,0,0,6,140,1,0,0,0,
        8,147,1,0,0,0,10,154,1,0,0,0,12,161,1,0,0,0,14,172,1,0,0,0,16,175,
        1,0,0,0,18,192,1,0,0,0,20,194,1,0,0,0,22,196,1,0,0,0,24,202,1,0,
        0,0,26,208,1,0,0,0,28,231,1,0,0,0,30,233,1,0,0,0,32,236,1,0,0,0,
        34,244,1,0,0,0,36,252,1,0,0,0,38,272,1,0,0,0,40,289,1,0,0,0,42,297,
        1,0,0,0,44,301,1,0,0,0,46,309,1,0,0,0,48,311,1,0,0,0,50,313,1,0,
        0,0,52,334,1,0,0,0,54,336,1,0,0,0,56,355,1,0,0,0,58,357,1,0,0,0,
        60,362,1,0,0,0,62,370,1,0,0,0,64,374,1,0,0,0,66,379,1,0,0,0,68,381,
        1,0,0,0,70,383,1,0,0,0,72,385,1,0,0,0,74,387,1,0,0,0,76,389,1,0,
        0,0,78,391,1,0,0,0,80,393,1,0,0,0,82,395,1,0,0,0,84,86,5,37,0,0,
        85,84,1,0,0,0,86,89,1,0,0,0,87,85,1,0,0,0,87,88,1,0,0,0,88,93,1,
        0,0,0,89,87,1,0,0,0,90,92,3,26,13,0,91,90,1,0,0,0,92,95,1,0,0,0,
        93,91,1,0,0,0,93,94,1,0,0,0,94,99,1,0,0,0,95,93,1,0,0,0,96,98,3,
        4,2,0,97,96,1,0,0,0,98,101,1,0,0,0,99,97,1,0,0,0,99,100,1,0,0,0,
        100,102,1,0,0,0,101,99,1,0,0,0,102,103,5,6,0,0,103,1,1,0,0,0,104,
        106,5,37,0,0,105,104,1,0,0,0,106,109,1,0,0,0,107,105,1,0,0,0,107,
        108,1,0,0,0,108,111,1,0,0,0,109,107,1,0,0,0,110,112,3,16,8,0,111,
        110,1,0,0,0,112,113,1,0,0,0,113,111,1,0,0,0,113,114,1,0,0,0,114,
        118,1,0,0,0,115,117,3,26,13,0,116,115,1,0,0,0,117,120,1,0,0,0,118,
        116,1,0,0,0,118,119,1,0,0,0,119,124,1,0,0,0,120,118,1,0,0,0,121,
        123,3,4,2,0,122,121,1,0,0,0,123,126,1,0,0,0,124,122,1,0,0,0,124,
        125,1,0,0,0,125,127,1,0,0,0,126,124,1,0,0,0,127,128,5,6,0,0,128,
        3,1,0,0,0,129,130,3,6,3,0,130,131,3,12,6,0,131,139,1,0,0,0,132,133,
        3,8,4,0,133,134,3,12,6,0,134,139,1,0,0,0,135,136,3,10,5,0,136,137,
        3,12,6,0,137,139,1,0,0,0,138,129,1,0,0,0,138,132,1,0,0,0,138,135,
        1,0,0,0,139,5,1,0,0,0,140,141,5,1,0,0,141,143,3,80,40,0,142,144,
        5,37,0,0,143,142,1,0,0,0,144,145,1,0,0,0,145,143,1,0,0,0,145,146,
        1,0,0,0,146,7,1,0,0,0,147,148,5,12,0,0,148,150,3,82,41,0,149,151,
        5,37,0,0,150,149,1,0,0,0,151,152,1,0,0,0,152,150,1,0,0,0,152,153,
        1,0,0,0,153,9,1,0,0,0,154,155,5,15,0,0,155,157,3,82,41,0,156,158,
        5,37,0,0,157,156,1,0,0,0,158,159,1,0,0,0,159,157,1,0,0,0,159,160,
        1,0,0,0,160,11,1,0,0,0,161,162,3,14,7,0,162,13,1,0,0,0,163,171,3,
        22,11,0,164,171,3,24,12,0,165,171,3,28,14,0,166,171,3,36,18,0,167,
        171,3,50,25,0,168,171,3,54,27,0,169,171,3,16,8,0,170,163,1,0,0,0,
        170,164,1,0,0,0,170,165,1,0,0,0,170,166,1,0,0,0,170,167,1,0,0,0,
        170,168,1,0,0,0,170,169,1,0,0,0,171,174,1,0,0,0,172,170,1,0,0,0,
        172,173,1,0,0,0,173,15,1,0,0,0,174,172,1,0,0,0,175,176,5,28,0,0,
        176,177,3,18,9,0,177,179,3,20,10,0,178,180,5,30,0,0,179,178,1,0,
        0,0,179,180,1,0,0,0,180,182,1,0,0,0,181,183,5,37,0,0,182,181,1,0,
        0,0,183,184,1,0,0,0,184,182,1,0,0,0,184,185,1,0,0,0,185,186,1,0,
        0,0,186,187,6,8,-1,0,187,188,6,8,-1,0,188,189,6,8,-1,0,189,190,6,
        8,-1,0,190,191,6,8,-1,0,191,17,1,0,0,0,192,193,5,32,0,0,193,19,1,
        0,0,0,194,195,5,40,0,0,195,21,1,0,0,0,196,198,5,2,0,0,197,199,5,
        37,0,0,198,197,1,0,0,0,199,200,1,0,0,0,200,198,1,0,0,0,200,201,1,
        0,0,0,201,23,1,0,0,0,202,204,5,3,0,0,203,205,5,37,0,0,204,203,1,
        0,0,0,205,206,1,0,0,0,206,204,1,0,0,0,206,207,1,0,0,0,207,25,1,0,
        0,0,208,209,3,28,14,0,209,27,1,0,0,0,210,212,3,30,15,0,211,213,5,
        7,0,0,212,211,1,0,0,0,212,213,1,0,0,0,213,215,1,0,0,0,214,216,5,
        37,0,0,215,214,1,0,0,0,216,217,1,0,0,0,217,215,1,0,0,0,217,218,1,
        0,0,0,218,232,1,0,0,0,219,221,3,30,15,0,220,219,1,0,0,0,220,221,
        1,0,0,0,221,222,1,0,0,0,222,224,3,72,36,0,223,225,3,34,17,0,224,
        223,1,0,0,0,224,225,1,0,0,0,225,227,1,0,0,0,226,228,5,37,0,0,227,
        226,1,0,0,0,228,229,1,0,0,0,229,227,1,0,0,0,229,230,1,0,0,0,230,
        232,1,0,0,0,231,210,1,0,0,0,231,220,1,0,0,0,232,29,1,0,0,0,233,234,
        3,32,16,0,234,235,7,0,0,0,235,31,1,0,0,0,236,241,3,70,35,0,237,238,
        5,20,0,0,238,240,3,70,35,0,239,237,1,0,0,0,240,243,1,0,0,0,241,239,
        1,0,0,0,241,242,1,0,0,0,242,33,1,0,0,0,243,241,1,0,0,0,244,249,3,
        56,28,0,245,246,5,20,0,0,246,248,3,56,28,0,247,245,1,0,0,0,248,251,
        1,0,0,0,249,247,1,0,0,0,249,250,1,0,0,0,250,35,1,0,0,0,251,249,1,
        0,0,0,252,254,5,9,0,0,253,255,5,37,0,0,254,253,1,0,0,0,255,256,1,
        0,0,0,256,254,1,0,0,0,256,257,1,0,0,0,257,258,1,0,0,0,258,259,3,
        38,19,0,259,261,3,14,7,0,260,262,3,44,22,0,261,260,1,0,0,0,261,262,
        1,0,0,0,262,263,1,0,0,0,263,265,5,8,0,0,264,266,5,37,0,0,265,264,
        1,0,0,0,266,267,1,0,0,0,267,265,1,0,0,0,267,268,1,0,0,0,268,37,1,
        0,0,0,269,271,3,40,20,0,270,269,1,0,0,0,271,274,1,0,0,0,272,270,
        1,0,0,0,272,273,1,0,0,0,273,275,1,0,0,0,274,272,1,0,0,0,275,277,
        3,42,21,0,276,278,5,37,0,0,277,276,1,0,0,0,278,279,1,0,0,0,279,277,
        1,0,0,0,279,280,1,0,0,0,280,287,1,0,0,0,281,283,5,14,0,0,282,284,
        5,37,0,0,283,282,1,0,0,0,284,285,1,0,0,0,285,283,1,0,0,0,285,286,
        1,0,0,0,286,288,1,0,0,0,287,281,1,0,0,0,287,288,1,0,0,0,288,39,1,
        0,0,0,289,290,3,42,21,0,290,291,5,20,0,0,291,293,3,48,24,0,292,294,
        5,37,0,0,293,292,1,0,0,0,294,295,1,0,0,0,295,293,1,0,0,0,295,296,
        1,0,0,0,296,41,1,0,0,0,297,298,3,14,7,0,298,299,5,10,0,0,299,300,
        3,46,23,0,300,43,1,0,0,0,301,303,5,5,0,0,302,304,5,37,0,0,303,302,
        1,0,0,0,304,305,1,0,0,0,305,303,1,0,0,0,305,306,1,0,0,0,306,307,
        1,0,0,0,307,308,3,14,7,0,308,45,1,0,0,0,309,310,5,30,0,0,310,47,
        1,0,0,0,311,312,5,30,0,0,312,49,1,0,0,0,313,315,5,18,0,0,314,316,
        5,37,0,0,315,314,1,0,0,0,316,317,1,0,0,0,317,315,1,0,0,0,317,318,
        1,0,0,0,318,319,1,0,0,0,319,320,3,52,26,0,320,321,5,13,0,0,321,323,
        3,46,23,0,322,324,5,37,0,0,323,322,1,0,0,0,324,325,1,0,0,0,325,323,
        1,0,0,0,325,326,1,0,0,0,326,327,1,0,0,0,327,328,3,14,7,0,328,330,
        5,17,0,0,329,331,5,37,0,0,330,329,1,0,0,0,331,332,1,0,0,0,332,330,
        1,0,0,0,332,333,1,0,0,0,333,51,1,0,0,0,334,335,3,14,7,0,335,53,1,
        0,0,0,336,338,5,4,0,0,337,339,5,37,0,0,338,337,1,0,0,0,339,340,1,
        0,0,0,340,338,1,0,0,0,340,341,1,0,0,0,341,342,1,0,0,0,342,343,3,
        14,7,0,343,344,5,16,0,0,344,346,3,46,23,0,345,347,5,37,0,0,346,345,
        1,0,0,0,347,348,1,0,0,0,348,346,1,0,0,0,348,349,1,0,0,0,349,55,1,
        0,0,0,350,356,3,78,39,0,351,356,3,74,37,0,352,356,3,76,38,0,353,
        356,3,60,30,0,354,356,3,58,29,0,355,350,1,0,0,0,355,351,1,0,0,0,
        355,352,1,0,0,0,355,353,1,0,0,0,355,354,1,0,0,0,356,57,1,0,0,0,357,
        358,3,68,34,0,358,359,5,26,0,0,359,360,3,60,30,0,360,361,5,27,0,
        0,361,59,1,0,0,0,362,366,3,62,31,0,363,365,3,64,32,0,364,363,1,0,
        0,0,365,368,1,0,0,0,366,364,1,0,0,0,366,367,1,0,0,0,367,61,1,0,0,
        0,368,366,1,0,0,0,369,371,7,1,0,0,370,369,1,0,0,0,370,371,1,0,0,
        0,371,372,1,0,0,0,372,373,3,66,33,0,373,63,1,0,0,0,374,375,7,1,0,
        0,375,376,3,66,33,0,376,65,1,0,0,0,377,380,3,80,40,0,378,380,3,70,
        35,0,379,377,1,0,0,0,379,378,1,0,0,0,380,67,1,0,0,0,381,382,3,82,
        41,0,382,69,1,0,0,0,383,384,3,82,41,0,384,71,1,0,0,0,385,386,5,30,
        0,0,386,73,1,0,0,0,387,388,5,35,0,0,388,75,1,0,0,0,389,390,5,29,
        0,0,390,77,1,0,0,0,391,392,5,36,0,0,392,79,1,0,0,0,393,394,7,2,0,
        0,394,81,1,0,0,0,395,396,7,3,0,0,396,83,1,0,0,0,43,87,93,99,107,
        113,118,124,138,145,152,159,170,172,179,184,200,206,212,217,220,
        224,229,231,241,249,256,261,267,272,279,285,287,295,305,317,325,
        332,340,348,355,366,370,379
    ]

class AsmParser ( Parser ):

    grammarFileName = "AsmParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'asect'", "'break'", "'continue'", "'do'", 
                     "'else'", "'end'", "'ext'", "'fi'", "'if'", "'is'", 
                     "'macro'", "'rsect'", "'stays'", "'then'", "'tplate'", 
                     "'until'", "'wend'", "'while'", "'.'", "','", "'+'", 
                     "'-'", "':'", "'*'", "'>'", "'('", "')'", "'-|'" ]

    symbolicNames = [ "<INVALID>", "Asect", "Break", "Continue", "Do", "Else", 
                      "End", "Ext", "Fi", "If", "Is", "Macro", "Rsect", 
                      "Stays", "Then", "Tplate", "Until", "Wend", "While", 
                      "DOT", "COMMA", "PLUS", "MINUS", "COLON", "ASTERISK", 
                      "ANGLE_BRACKET", "OPEN_PAREN", "CLOSE_PAREN", "LINE_MARK_MARKER", 
                      "REGISTER", "WORD", "WORD_WITH_DOTS", "DECIMAL_NUMBER", 
                      "BINARY_NUMBER", "HEX_NUMBER", "STRING", "CHAR", "NEWLINE", 
                      "COMMENT", "WS", "BASE64", "UNEXPECTED_TOKEN" ]

    RULE_program_nomacros = 0
    RULE_program = 1
    RULE_section = 2
    RULE_asect_header = 3
    RULE_rsect_header = 4
    RULE_tplate_header = 5
    RULE_section_body = 6
    RULE_code_block = 7
    RULE_line_mark = 8
    RULE_line_number = 9
    RULE_filepath = 10
    RULE_break_statement = 11
    RULE_continue_statement = 12
    RULE_top_line = 13
    RULE_line = 14
    RULE_labels_declaration = 15
    RULE_labels = 16
    RULE_arguments = 17
    RULE_conditional = 18
    RULE_conditions = 19
    RULE_connective_condition = 20
    RULE_condition = 21
    RULE_else_clause = 22
    RULE_branch_mnemonic = 23
    RULE_conjunction = 24
    RULE_while_loop = 25
    RULE_while_condition = 26
    RULE_until_loop = 27
    RULE_argument = 28
    RULE_byte_expr = 29
    RULE_addr_expr = 30
    RULE_first_term = 31
    RULE_add_term = 32
    RULE_term = 33
    RULE_byte_specifier = 34
    RULE_label = 35
    RULE_instruction = 36
    RULE_string = 37
    RULE_register = 38
    RULE_character = 39
    RULE_number = 40
    RULE_name = 41

    ruleNames =  [ "program_nomacros", "program", "section", "asect_header", 
                   "rsect_header", "tplate_header", "section_body", "code_block", 
                   "line_mark", "line_number", "filepath", "break_statement", 
                   "continue_statement", "top_line", "line", "labels_declaration", 
                   "labels", "arguments", "conditional", "conditions", "connective_condition", 
                   "condition", "else_clause", "branch_mnemonic", "conjunction", 
                   "while_loop", "while_condition", "until_loop", "argument", 
                   "byte_expr", "addr_expr", "first_term", "add_term", "term", 
                   "byte_specifier", "label", "instruction", "string", "register", 
                   "character", "number", "name" ]

    EOF = Token.EOF
    Asect=1
    Break=2
    Continue=3
    Do=4
    Else=5
    End=6
    Ext=7
    Fi=8
    If=9
    Is=10
    Macro=11
    Rsect=12
    Stays=13
    Then=14
    Tplate=15
    Until=16
    Wend=17
    While=18
    DOT=19
    COMMA=20
    PLUS=21
    MINUS=22
    COLON=23
    ASTERISK=24
    ANGLE_BRACKET=25
    OPEN_PAREN=26
    CLOSE_PAREN=27
    LINE_MARK_MARKER=28
    REGISTER=29
    WORD=30
    WORD_WITH_DOTS=31
    DECIMAL_NUMBER=32
    BINARY_NUMBER=33
    HEX_NUMBER=34
    STRING=35
    CHAR=36
    NEWLINE=37
    COMMENT=38
    WS=39
    BASE64=40
    UNEXPECTED_TOKEN=41

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



        self.current_file = ''
        self.current_line = 0
        self.current_offset = 0



    class Program_nomacrosContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def End(self):
            return self.getToken(AsmParser.End, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def top_line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Top_lineContext)
            else:
                return self.getTypedRuleContext(AsmParser.Top_lineContext,i)


        def section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.SectionContext)
            else:
                return self.getTypedRuleContext(AsmParser.SectionContext,i)


        def getRuleIndex(self):
            return AsmParser.RULE_program_nomacros

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram_nomacros" ):
                return visitor.visitProgram_nomacros(self)
            else:
                return visitor.visitChildren(self)




    def program_nomacros(self):

        localctx = AsmParser.Program_nomacrosContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program_nomacros)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==37:
                self.state = 84
                self.match(AsmParser.NEWLINE)
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 93
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 90
                    self.top_line() 
                self.state = 95
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 36866) != 0):
                self.state = 96
                self.section()
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 102
            self.match(AsmParser.End)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def End(self):
            return self.getToken(AsmParser.End, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def line_mark(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Line_markContext)
            else:
                return self.getTypedRuleContext(AsmParser.Line_markContext,i)


        def top_line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Top_lineContext)
            else:
                return self.getTypedRuleContext(AsmParser.Top_lineContext,i)


        def section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.SectionContext)
            else:
                return self.getTypedRuleContext(AsmParser.SectionContext,i)


        def getRuleIndex(self):
            return AsmParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = AsmParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==37:
                self.state = 104
                self.match(AsmParser.NEWLINE)
                self.state = 109
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 111 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 110
                self.line_mark()
                self.state = 113 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==28):
                    break

            self.state = 118
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 115
                    self.top_line() 
                self.state = 120
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 36866) != 0):
                self.state = 121
                self.section()
                self.state = 126
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 127
            self.match(AsmParser.End)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return AsmParser.RULE_section

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AbsoluteSectionContext(SectionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AsmParser.SectionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def asect_header(self):
            return self.getTypedRuleContext(AsmParser.Asect_headerContext,0)

        def section_body(self):
            return self.getTypedRuleContext(AsmParser.Section_bodyContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbsoluteSection" ):
                return visitor.visitAbsoluteSection(self)
            else:
                return visitor.visitChildren(self)


    class TemplateSectionContext(SectionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AsmParser.SectionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def tplate_header(self):
            return self.getTypedRuleContext(AsmParser.Tplate_headerContext,0)

        def section_body(self):
            return self.getTypedRuleContext(AsmParser.Section_bodyContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemplateSection" ):
                return visitor.visitTemplateSection(self)
            else:
                return visitor.visitChildren(self)


    class RelocatableSectionContext(SectionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AsmParser.SectionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def rsect_header(self):
            return self.getTypedRuleContext(AsmParser.Rsect_headerContext,0)

        def section_body(self):
            return self.getTypedRuleContext(AsmParser.Section_bodyContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelocatableSection" ):
                return visitor.visitRelocatableSection(self)
            else:
                return visitor.visitChildren(self)



    def section(self):

        localctx = AsmParser.SectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_section)
        try:
            self.state = 138
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = AsmParser.AbsoluteSectionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 129
                self.asect_header()
                self.state = 130
                self.section_body()
                pass
            elif token in [12]:
                localctx = AsmParser.RelocatableSectionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 132
                self.rsect_header()
                self.state = 133
                self.section_body()
                pass
            elif token in [15]:
                localctx = AsmParser.TemplateSectionContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 135
                self.tplate_header()
                self.state = 136
                self.section_body()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Asect_headerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Asect(self):
            return self.getToken(AsmParser.Asect, 0)

        def number(self):
            return self.getTypedRuleContext(AsmParser.NumberContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_asect_header

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAsect_header" ):
                return visitor.visitAsect_header(self)
            else:
                return visitor.visitChildren(self)




    def asect_header(self):

        localctx = AsmParser.Asect_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_asect_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.match(AsmParser.Asect)
            self.state = 141
            self.number()
            self.state = 143 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 142
                self.match(AsmParser.NEWLINE)
                self.state = 145 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rsect_headerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Rsect(self):
            return self.getToken(AsmParser.Rsect, 0)

        def name(self):
            return self.getTypedRuleContext(AsmParser.NameContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_rsect_header

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRsect_header" ):
                return visitor.visitRsect_header(self)
            else:
                return visitor.visitChildren(self)




    def rsect_header(self):

        localctx = AsmParser.Rsect_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_rsect_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.match(AsmParser.Rsect)
            self.state = 148
            self.name()
            self.state = 150 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 149
                self.match(AsmParser.NEWLINE)
                self.state = 152 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tplate_headerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Tplate(self):
            return self.getToken(AsmParser.Tplate, 0)

        def name(self):
            return self.getTypedRuleContext(AsmParser.NameContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_tplate_header

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTplate_header" ):
                return visitor.visitTplate_header(self)
            else:
                return visitor.visitChildren(self)




    def tplate_header(self):

        localctx = AsmParser.Tplate_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_tplate_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self.match(AsmParser.Tplate)
            self.state = 155
            self.name()
            self.state = 157 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 156
                self.match(AsmParser.NEWLINE)
                self.state = 159 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Section_bodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_section_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSection_body" ):
                return visitor.visitSection_body(self)
            else:
                return visitor.visitChildren(self)




    def section_body(self):

        localctx = AsmParser.Section_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_section_body)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Code_blockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def break_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Break_statementContext)
            else:
                return self.getTypedRuleContext(AsmParser.Break_statementContext,i)


        def continue_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Continue_statementContext)
            else:
                return self.getTypedRuleContext(AsmParser.Continue_statementContext,i)


        def line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.LineContext)
            else:
                return self.getTypedRuleContext(AsmParser.LineContext,i)


        def conditional(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.ConditionalContext)
            else:
                return self.getTypedRuleContext(AsmParser.ConditionalContext,i)


        def while_loop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.While_loopContext)
            else:
                return self.getTypedRuleContext(AsmParser.While_loopContext,i)


        def until_loop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Until_loopContext)
            else:
                return self.getTypedRuleContext(AsmParser.Until_loopContext,i)


        def line_mark(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Line_markContext)
            else:
                return self.getTypedRuleContext(AsmParser.Line_markContext,i)


        def getRuleIndex(self):
            return AsmParser.RULE_code_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCode_block" ):
                return visitor.visitCode_block(self)
            else:
                return visitor.visitChildren(self)




    def code_block(self):

        localctx = AsmParser.Code_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_code_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 170
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
                    if la_ == 1:
                        self.state = 163
                        self.break_statement()
                        pass

                    elif la_ == 2:
                        self.state = 164
                        self.continue_statement()
                        pass

                    elif la_ == 3:
                        self.state = 165
                        self.line()
                        pass

                    elif la_ == 4:
                        self.state = 166
                        self.conditional()
                        pass

                    elif la_ == 5:
                        self.state = 167
                        self.while_loop()
                        pass

                    elif la_ == 6:
                        self.state = 168
                        self.until_loop()
                        pass

                    elif la_ == 7:
                        self.state = 169
                        self.line_mark()
                        pass

             
                self.state = 174
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Line_markContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.source_file = ''
            self.source_line = 0
            self._line_number = None # Line_numberContext
            self._filepath = None # FilepathContext

        def LINE_MARK_MARKER(self):
            return self.getToken(AsmParser.LINE_MARK_MARKER, 0)

        def line_number(self):
            return self.getTypedRuleContext(AsmParser.Line_numberContext,0)


        def filepath(self):
            return self.getTypedRuleContext(AsmParser.FilepathContext,0)


        def WORD(self):
            return self.getToken(AsmParser.WORD, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_line_mark

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLine_mark" ):
                return visitor.visitLine_mark(self)
            else:
                return visitor.visitChildren(self)




    def line_mark(self):

        localctx = AsmParser.Line_markContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_line_mark)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.match(AsmParser.LINE_MARK_MARKER)
            self.state = 176
            localctx._line_number = self.line_number()
            self.state = 177
            localctx._filepath = self.filepath()
            self.state = 179
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 178
                self.match(AsmParser.WORD)


            self.state = 182 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 181
                self.match(AsmParser.NEWLINE)
                self.state = 184 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.current_line = int((None if localctx._line_number is None else self._input.getText(localctx._line_number.start,localctx._line_number.stop)))
            self.current_file =  b64decode((None if localctx._filepath is None else self._input.getText(localctx._filepath.start,localctx._filepath.stop))[3:]).decode()
            localctx.source_file = self.current_file
            localctx.source_line = self.current_line
            self.current_offset = (None if localctx._line_number is None else localctx._line_number.start).line - self.current_line + 1
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Line_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL_NUMBER(self):
            return self.getToken(AsmParser.DECIMAL_NUMBER, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_line_number

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLine_number" ):
                return visitor.visitLine_number(self)
            else:
                return visitor.visitChildren(self)




    def line_number(self):

        localctx = AsmParser.Line_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_line_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.match(AsmParser.DECIMAL_NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FilepathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASE64(self):
            return self.getToken(AsmParser.BASE64, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_filepath

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFilepath" ):
                return visitor.visitFilepath(self)
            else:
                return visitor.visitChildren(self)




    def filepath(self):

        localctx = AsmParser.FilepathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_filepath)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.match(AsmParser.BASE64)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Break_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Break(self):
            return self.getToken(AsmParser.Break, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_break_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak_statement" ):
                return visitor.visitBreak_statement(self)
            else:
                return visitor.visitChildren(self)




    def break_statement(self):

        localctx = AsmParser.Break_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_break_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.match(AsmParser.Break)
            self.state = 198 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 197
                self.match(AsmParser.NEWLINE)
                self.state = 200 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Continue_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Continue(self):
            return self.getToken(AsmParser.Continue, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_continue_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue_statement" ):
                return visitor.visitContinue_statement(self)
            else:
                return visitor.visitChildren(self)




    def continue_statement(self):

        localctx = AsmParser.Continue_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_continue_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            self.match(AsmParser.Continue)
            self.state = 204 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 203
                self.match(AsmParser.NEWLINE)
                self.state = 206 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Top_lineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def line(self):
            return self.getTypedRuleContext(AsmParser.LineContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_top_line

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTop_line" ):
                return visitor.visitTop_line(self)
            else:
                return visitor.visitChildren(self)




    def top_line(self):

        localctx = AsmParser.Top_lineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_top_line)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 208
            self.line()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return AsmParser.RULE_line

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class InstructionLineContext(LineContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AsmParser.LineContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def instruction(self):
            return self.getTypedRuleContext(AsmParser.InstructionContext,0)

        def labels_declaration(self):
            return self.getTypedRuleContext(AsmParser.Labels_declarationContext,0)

        def arguments(self):
            return self.getTypedRuleContext(AsmParser.ArgumentsContext,0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstructionLine" ):
                return visitor.visitInstructionLine(self)
            else:
                return visitor.visitChildren(self)


    class StandaloneLabelsContext(LineContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AsmParser.LineContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def labels_declaration(self):
            return self.getTypedRuleContext(AsmParser.Labels_declarationContext,0)

        def Ext(self):
            return self.getToken(AsmParser.Ext, 0)
        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStandaloneLabels" ):
                return visitor.visitStandaloneLabels(self)
            else:
                return visitor.visitChildren(self)



    def line(self):

        localctx = AsmParser.LineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_line)
        self._la = 0 # Token type
        try:
            self.state = 231
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                localctx = AsmParser.StandaloneLabelsContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 210
                self.labels_declaration()
                self.state = 212
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 211
                    self.match(AsmParser.Ext)


                self.state = 215 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 214
                    self.match(AsmParser.NEWLINE)
                    self.state = 217 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==37):
                        break

                pass

            elif la_ == 2:
                localctx = AsmParser.InstructionLineContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 220
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
                if la_ == 1:
                    self.state = 219
                    self.labels_declaration()


                self.state = 222
                self.instruction()
                self.state = 224
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 136908898302) != 0):
                    self.state = 223
                    self.arguments()


                self.state = 227 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 226
                    self.match(AsmParser.NEWLINE)
                    self.state = 229 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==37):
                        break

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Labels_declarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def labels(self):
            return self.getTypedRuleContext(AsmParser.LabelsContext,0)


        def COLON(self):
            return self.getToken(AsmParser.COLON, 0)

        def ANGLE_BRACKET(self):
            return self.getToken(AsmParser.ANGLE_BRACKET, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_labels_declaration

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLabels_declaration" ):
                return visitor.visitLabels_declaration(self)
            else:
                return visitor.visitChildren(self)




    def labels_declaration(self):

        localctx = AsmParser.Labels_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_labels_declaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 233
            self.labels()
            self.state = 234
            _la = self._input.LA(1)
            if not(_la==23 or _la==25):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LabelsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def label(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.LabelContext)
            else:
                return self.getTypedRuleContext(AsmParser.LabelContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.COMMA)
            else:
                return self.getToken(AsmParser.COMMA, i)

        def getRuleIndex(self):
            return AsmParser.RULE_labels

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLabels" ):
                return visitor.visitLabels(self)
            else:
                return visitor.visitChildren(self)




    def labels(self):

        localctx = AsmParser.LabelsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_labels)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self.label()
            self.state = 241
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 237
                self.match(AsmParser.COMMA)
                self.state = 238
                self.label()
                self.state = 243
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(AsmParser.ArgumentContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.COMMA)
            else:
                return self.getToken(AsmParser.COMMA, i)

        def getRuleIndex(self):
            return AsmParser.RULE_arguments

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArguments" ):
                return visitor.visitArguments(self)
            else:
                return visitor.visitChildren(self)




    def arguments(self):

        localctx = AsmParser.ArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_arguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 244
            self.argument()
            self.state = 249
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 245
                self.match(AsmParser.COMMA)
                self.state = 246
                self.argument()
                self.state = 251
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def If(self):
            return self.getToken(AsmParser.If, 0)

        def conditions(self):
            return self.getTypedRuleContext(AsmParser.ConditionsContext,0)


        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def Fi(self):
            return self.getToken(AsmParser.Fi, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def else_clause(self):
            return self.getTypedRuleContext(AsmParser.Else_clauseContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_conditional

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConditional" ):
                return visitor.visitConditional(self)
            else:
                return visitor.visitChildren(self)




    def conditional(self):

        localctx = AsmParser.ConditionalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_conditional)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.match(AsmParser.If)
            self.state = 254 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 253
                self.match(AsmParser.NEWLINE)
                self.state = 256 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.state = 258
            self.conditions()
            self.state = 259
            self.code_block()
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 260
                self.else_clause()


            self.state = 263
            self.match(AsmParser.Fi)
            self.state = 265 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 264
                self.match(AsmParser.NEWLINE)
                self.state = 267 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(AsmParser.ConditionContext,0)


        def connective_condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Connective_conditionContext)
            else:
                return self.getTypedRuleContext(AsmParser.Connective_conditionContext,i)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def Then(self):
            return self.getToken(AsmParser.Then, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_conditions

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConditions" ):
                return visitor.visitConditions(self)
            else:
                return visitor.visitChildren(self)




    def conditions(self):

        localctx = AsmParser.ConditionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_conditions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 272
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,28,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 269
                    self.connective_condition() 
                self.state = 274
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,28,self._ctx)

            self.state = 275
            self.condition()
            self.state = 277 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 276
                self.match(AsmParser.NEWLINE)
                self.state = 279 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.state = 287
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                self.state = 281
                self.match(AsmParser.Then)
                self.state = 283 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 282
                    self.match(AsmParser.NEWLINE)
                    self.state = 285 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==37):
                        break



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Connective_conditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(AsmParser.ConditionContext,0)


        def COMMA(self):
            return self.getToken(AsmParser.COMMA, 0)

        def conjunction(self):
            return self.getTypedRuleContext(AsmParser.ConjunctionContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_connective_condition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConnective_condition" ):
                return visitor.visitConnective_condition(self)
            else:
                return visitor.visitChildren(self)




    def connective_condition(self):

        localctx = AsmParser.Connective_conditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_connective_condition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 289
            self.condition()
            self.state = 290
            self.match(AsmParser.COMMA)
            self.state = 291
            self.conjunction()
            self.state = 293 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 292
                self.match(AsmParser.NEWLINE)
                self.state = 295 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def Is(self):
            return self.getToken(AsmParser.Is, 0)

        def branch_mnemonic(self):
            return self.getTypedRuleContext(AsmParser.Branch_mnemonicContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_condition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = AsmParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 297
            self.code_block()
            self.state = 298
            self.match(AsmParser.Is)
            self.state = 299
            self.branch_mnemonic()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Else_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Else(self):
            return self.getToken(AsmParser.Else, 0)

        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_else_clause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElse_clause" ):
                return visitor.visitElse_clause(self)
            else:
                return visitor.visitChildren(self)




    def else_clause(self):

        localctx = AsmParser.Else_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_else_clause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 301
            self.match(AsmParser.Else)
            self.state = 303 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 302
                self.match(AsmParser.NEWLINE)
                self.state = 305 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.state = 307
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Branch_mnemonicContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(AsmParser.WORD, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_branch_mnemonic

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBranch_mnemonic" ):
                return visitor.visitBranch_mnemonic(self)
            else:
                return visitor.visitChildren(self)




    def branch_mnemonic(self):

        localctx = AsmParser.Branch_mnemonicContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_branch_mnemonic)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 309
            self.match(AsmParser.WORD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConjunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(AsmParser.WORD, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_conjunction

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConjunction" ):
                return visitor.visitConjunction(self)
            else:
                return visitor.visitChildren(self)




    def conjunction(self):

        localctx = AsmParser.ConjunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_conjunction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 311
            self.match(AsmParser.WORD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_loopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def While(self):
            return self.getToken(AsmParser.While, 0)

        def while_condition(self):
            return self.getTypedRuleContext(AsmParser.While_conditionContext,0)


        def Stays(self):
            return self.getToken(AsmParser.Stays, 0)

        def branch_mnemonic(self):
            return self.getTypedRuleContext(AsmParser.Branch_mnemonicContext,0)


        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def Wend(self):
            return self.getToken(AsmParser.Wend, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_while_loop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile_loop" ):
                return visitor.visitWhile_loop(self)
            else:
                return visitor.visitChildren(self)




    def while_loop(self):

        localctx = AsmParser.While_loopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_while_loop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 313
            self.match(AsmParser.While)
            self.state = 315 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 314
                self.match(AsmParser.NEWLINE)
                self.state = 317 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.state = 319
            self.while_condition()
            self.state = 320
            self.match(AsmParser.Stays)
            self.state = 321
            self.branch_mnemonic()
            self.state = 323 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 322
                self.match(AsmParser.NEWLINE)
                self.state = 325 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.state = 327
            self.code_block()
            self.state = 328
            self.match(AsmParser.Wend)
            self.state = 330 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 329
                self.match(AsmParser.NEWLINE)
                self.state = 332 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_conditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_while_condition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile_condition" ):
                return visitor.visitWhile_condition(self)
            else:
                return visitor.visitChildren(self)




    def while_condition(self):

        localctx = AsmParser.While_conditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_while_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 334
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Until_loopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Do(self):
            return self.getToken(AsmParser.Do, 0)

        def code_block(self):
            return self.getTypedRuleContext(AsmParser.Code_blockContext,0)


        def Until(self):
            return self.getToken(AsmParser.Until, 0)

        def branch_mnemonic(self):
            return self.getTypedRuleContext(AsmParser.Branch_mnemonicContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AsmParser.NEWLINE)
            else:
                return self.getToken(AsmParser.NEWLINE, i)

        def getRuleIndex(self):
            return AsmParser.RULE_until_loop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUntil_loop" ):
                return visitor.visitUntil_loop(self)
            else:
                return visitor.visitChildren(self)




    def until_loop(self):

        localctx = AsmParser.Until_loopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_until_loop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 336
            self.match(AsmParser.Do)
            self.state = 338 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 337
                self.match(AsmParser.NEWLINE)
                self.state = 340 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

            self.state = 342
            self.code_block()
            self.state = 343
            self.match(AsmParser.Until)
            self.state = 344
            self.branch_mnemonic()
            self.state = 346 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 345
                self.match(AsmParser.NEWLINE)
                self.state = 348 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def character(self):
            return self.getTypedRuleContext(AsmParser.CharacterContext,0)


        def string(self):
            return self.getTypedRuleContext(AsmParser.StringContext,0)


        def register(self):
            return self.getTypedRuleContext(AsmParser.RegisterContext,0)


        def addr_expr(self):
            return self.getTypedRuleContext(AsmParser.Addr_exprContext,0)


        def byte_expr(self):
            return self.getTypedRuleContext(AsmParser.Byte_exprContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_argument

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgument" ):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = AsmParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_argument)
        try:
            self.state = 355
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 350
                self.character()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 351
                self.string()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 352
                self.register()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 353
                self.addr_expr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 354
                self.byte_expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Byte_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def byte_specifier(self):
            return self.getTypedRuleContext(AsmParser.Byte_specifierContext,0)


        def OPEN_PAREN(self):
            return self.getToken(AsmParser.OPEN_PAREN, 0)

        def addr_expr(self):
            return self.getTypedRuleContext(AsmParser.Addr_exprContext,0)


        def CLOSE_PAREN(self):
            return self.getToken(AsmParser.CLOSE_PAREN, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_byte_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitByte_expr" ):
                return visitor.visitByte_expr(self)
            else:
                return visitor.visitChildren(self)




    def byte_expr(self):

        localctx = AsmParser.Byte_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_byte_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 357
            self.byte_specifier()
            self.state = 358
            self.match(AsmParser.OPEN_PAREN)
            self.state = 359
            self.addr_expr()
            self.state = 360
            self.match(AsmParser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Addr_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def first_term(self):
            return self.getTypedRuleContext(AsmParser.First_termContext,0)


        def add_term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AsmParser.Add_termContext)
            else:
                return self.getTypedRuleContext(AsmParser.Add_termContext,i)


        def getRuleIndex(self):
            return AsmParser.RULE_addr_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddr_expr" ):
                return visitor.visitAddr_expr(self)
            else:
                return visitor.visitChildren(self)




    def addr_expr(self):

        localctx = AsmParser.Addr_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_addr_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 362
            self.first_term()
            self.state = 366
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==21 or _la==22:
                self.state = 363
                self.add_term()
                self.state = 368
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class First_termContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(AsmParser.TermContext,0)


        def PLUS(self):
            return self.getToken(AsmParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(AsmParser.MINUS, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_first_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFirst_term" ):
                return visitor.visitFirst_term(self)
            else:
                return visitor.visitChildren(self)




    def first_term(self):

        localctx = AsmParser.First_termContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_first_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21 or _la==22:
                self.state = 369
                _la = self._input.LA(1)
                if not(_la==21 or _la==22):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 372
            self.term()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Add_termContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(AsmParser.TermContext,0)


        def PLUS(self):
            return self.getToken(AsmParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(AsmParser.MINUS, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_add_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdd_term" ):
                return visitor.visitAdd_term(self)
            else:
                return visitor.visitChildren(self)




    def add_term(self):

        localctx = AsmParser.Add_termContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_add_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 374
            _la = self._input.LA(1)
            if not(_la==21 or _la==22):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 375
            self.term()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(AsmParser.NumberContext,0)


        def label(self):
            return self.getTypedRuleContext(AsmParser.LabelContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = AsmParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_term)
        try:
            self.state = 379
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32, 33, 34]:
                self.enterOuterAlt(localctx, 1)
                self.state = 377
                self.number()
                pass
            elif token in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 30, 31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 378
                self.label()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Byte_specifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(AsmParser.NameContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_byte_specifier

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitByte_specifier" ):
                return visitor.visitByte_specifier(self)
            else:
                return visitor.visitChildren(self)




    def byte_specifier(self):

        localctx = AsmParser.Byte_specifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_byte_specifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LabelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(AsmParser.NameContext,0)


        def getRuleIndex(self):
            return AsmParser.RULE_label

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLabel" ):
                return visitor.visitLabel(self)
            else:
                return visitor.visitChildren(self)




    def label(self):

        localctx = AsmParser.LabelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_label)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 383
            self.name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstructionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(AsmParser.WORD, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_instruction

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstruction" ):
                return visitor.visitInstruction(self)
            else:
                return visitor.visitChildren(self)




    def instruction(self):

        localctx = AsmParser.InstructionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_instruction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 385
            self.match(AsmParser.WORD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AsmParser.STRING, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_string

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = AsmParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 387
            self.match(AsmParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RegisterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REGISTER(self):
            return self.getToken(AsmParser.REGISTER, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_register

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRegister" ):
                return visitor.visitRegister(self)
            else:
                return visitor.visitChildren(self)




    def register(self):

        localctx = AsmParser.RegisterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_register)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 389
            self.match(AsmParser.REGISTER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHAR(self):
            return self.getToken(AsmParser.CHAR, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_character

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharacter" ):
                return visitor.visitCharacter(self)
            else:
                return visitor.visitChildren(self)




    def character(self):

        localctx = AsmParser.CharacterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_character)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 391
            self.match(AsmParser.CHAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL_NUMBER(self):
            return self.getToken(AsmParser.DECIMAL_NUMBER, 0)

        def HEX_NUMBER(self):
            return self.getToken(AsmParser.HEX_NUMBER, 0)

        def BINARY_NUMBER(self):
            return self.getToken(AsmParser.BINARY_NUMBER, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_number

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)




    def number(self):

        localctx = AsmParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 393
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30064771072) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Asect(self):
            return self.getToken(AsmParser.Asect, 0)

        def Break(self):
            return self.getToken(AsmParser.Break, 0)

        def Continue(self):
            return self.getToken(AsmParser.Continue, 0)

        def Do(self):
            return self.getToken(AsmParser.Do, 0)

        def Else(self):
            return self.getToken(AsmParser.Else, 0)

        def End(self):
            return self.getToken(AsmParser.End, 0)

        def Ext(self):
            return self.getToken(AsmParser.Ext, 0)

        def Fi(self):
            return self.getToken(AsmParser.Fi, 0)

        def If(self):
            return self.getToken(AsmParser.If, 0)

        def Is(self):
            return self.getToken(AsmParser.Is, 0)

        def Macro(self):
            return self.getToken(AsmParser.Macro, 0)

        def Rsect(self):
            return self.getToken(AsmParser.Rsect, 0)

        def Stays(self):
            return self.getToken(AsmParser.Stays, 0)

        def Then(self):
            return self.getToken(AsmParser.Then, 0)

        def Tplate(self):
            return self.getToken(AsmParser.Tplate, 0)

        def Until(self):
            return self.getToken(AsmParser.Until, 0)

        def Wend(self):
            return self.getToken(AsmParser.Wend, 0)

        def While(self):
            return self.getToken(AsmParser.While, 0)

        def WORD(self):
            return self.getToken(AsmParser.WORD, 0)

        def WORD_WITH_DOTS(self):
            return self.getToken(AsmParser.WORD_WITH_DOTS, 0)

        def getRuleIndex(self):
            return AsmParser.RULE_name

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitName" ):
                return visitor.visitName(self)
            else:
                return visitor.visitChildren(self)




    def name(self):

        localctx = AsmParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 395
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3221749758) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





