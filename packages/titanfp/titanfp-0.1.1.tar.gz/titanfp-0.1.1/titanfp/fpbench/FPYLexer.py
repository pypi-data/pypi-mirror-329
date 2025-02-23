# Generated from FPY.g4 by ANTLR 4.9.3
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from antlr4.Token import CommonToken
import re
import importlib

# Pre-compile re
only_spaces = re.compile("[^\r\n\f]+")
only_newlines = re.compile("[\r\n\f]+")

# Allow languages to extend the lexer and parser, by loading the parser dynamically
module_path = __name__[:-5]
language_name = __name__.split('.')[-1]
language_name = language_name[:-5]  # Remove Lexer from name
LanguageParser = getattr(importlib.import_module('{}Parser'.format(module_path)), '{}Parser'.format(language_name))



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2/")
        buf.write("\u019c\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\5")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\13\3")
        buf.write("\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22\3\22\3\23")
        buf.write("\3\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3\30")
        buf.write("\3\30\3\31\3\31\3\31\3\32\3\32\3\33\3\33\3\33\3\34\3\34")
        buf.write("\3\35\3\35\3\35\3\36\3\36\3\36\3\37\3\37\3 \3 \3!\3!\3")
        buf.write("\"\3\"\3#\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3$\3$\3%\3%\3")
        buf.write("%\3%\3%\3%\3%\3&\5&\u00ec\n&\3&\6&\u00ef\n&\r&\16&\u00f0")
        buf.write("\3&\3&\6&\u00f5\n&\r&\16&\u00f6\5&\u00f9\n&\3&\3&\6&\u00fd")
        buf.write("\n&\r&\16&\u00fe\5&\u0101\n&\3&\3&\5&\u0105\n&\3&\6&\u0108")
        buf.write("\n&\r&\16&\u0109\5&\u010c\n&\3\'\5\'\u010f\n\'\3\'\3\'")
        buf.write("\3\'\6\'\u0114\n\'\r\'\16\'\u0115\3\'\3\'\6\'\u011a\n")
        buf.write("\'\r\'\16\'\u011b\5\'\u011e\n\'\3\'\3\'\6\'\u0122\n\'")
        buf.write("\r\'\16\'\u0123\5\'\u0126\n\'\3\'\3\'\5\'\u012a\n\'\3")
        buf.write("\'\6\'\u012d\n\'\r\'\16\'\u012e\5\'\u0131\n\'\3(\5(\u0134")
        buf.write("\n(\3(\6(\u0137\n(\r(\16(\u0138\3(\3(\7(\u013d\n(\f(\16")
        buf.write("(\u0140\13(\3(\3(\7(\u0144\n(\f(\16(\u0147\13(\3)\3)\7")
        buf.write(")\u014b\n)\f)\16)\u014e\13)\3*\3*\3*\3*\7*\u0154\n*\f")
        buf.write("*\16*\u0157\13*\3*\3*\3+\3+\7+\u015d\n+\f+\16+\u0160\13")
        buf.write("+\3+\3+\3,\3,\3,\5,\u0167\n,\3,\3,\5,\u016b\n,\3,\5,\u016e")
        buf.write("\n,\5,\u0170\n,\3,\3,\3-\3-\3-\5-\u0177\n-\3-\3-\3.\3")
        buf.write(".\3/\6/\u017e\n/\r/\16/\u017f\3\60\3\60\7\60\u0184\n\60")
        buf.write("\f\60\16\60\u0187\13\60\3\61\3\61\5\61\u018b\n\61\3\61")
        buf.write("\5\61\u018e\n\61\3\61\3\61\5\61\u0192\n\61\3\62\3\62\3")
        buf.write("\63\3\63\3\64\3\64\3\64\5\64\u019b\n\64\2\2\65\3\3\5\4")
        buf.write("\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17")
        buf.write("\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63")
        buf.write("\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-")
        buf.write("Y.[/]\2_\2a\2c\2e\2g\2\3\2\17\4\2--//\3\2\62;\4\2GGgg")
        buf.write("\4\2ZZzz\5\2\62;CHch\4\2RRrr\3\2\63;\4\2\13\13\"\"\4\2")
        buf.write("\f\f\16\17\t\2&&((\60\60A\\`ac|\u0080\u0080\n\2&&((\60")
        buf.write("\60\62;A\\`ac|\u0080\u0080\6\2\n\17\"#%]_\u0080\n\2$$")
        buf.write("^^ddhhppttvvxx\2\u01ba\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2")
        buf.write("\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2")
        buf.write("\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2")
        buf.write("\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!")
        buf.write("\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2")
        buf.write("\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3")
        buf.write("\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2")
        buf.write("\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2")
        buf.write("\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2")
        buf.write("\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3")
        buf.write("\2\2\2\2[\3\2\2\2\3i\3\2\2\2\5l\3\2\2\2\7o\3\2\2\2\tr")
        buf.write("\3\2\2\2\13u\3\2\2\2\r|\3\2\2\2\17\177\3\2\2\2\21\u0084")
        buf.write("\3\2\2\2\23\u0089\3\2\2\2\25\u008e\3\2\2\2\27\u0092\3")
        buf.write("\2\2\2\31\u0098\3\2\2\2\33\u009c\3\2\2\2\35\u00a3\3\2")
        buf.write("\2\2\37\u00a8\3\2\2\2!\u00ab\3\2\2\2#\u00ae\3\2\2\2%\u00b1")
        buf.write("\3\2\2\2\'\u00b4\3\2\2\2)\u00b6\3\2\2\2+\u00b8\3\2\2\2")
        buf.write("-\u00ba\3\2\2\2/\u00bc\3\2\2\2\61\u00be\3\2\2\2\63\u00c1")
        buf.write("\3\2\2\2\65\u00c3\3\2\2\2\67\u00c6\3\2\2\29\u00c8\3\2")
        buf.write("\2\2;\u00cb\3\2\2\2=\u00ce\3\2\2\2?\u00d0\3\2\2\2A\u00d2")
        buf.write("\3\2\2\2C\u00d4\3\2\2\2E\u00d6\3\2\2\2G\u00dc\3\2\2\2")
        buf.write("I\u00e3\3\2\2\2K\u00eb\3\2\2\2M\u010e\3\2\2\2O\u0133\3")
        buf.write("\2\2\2Q\u0148\3\2\2\2S\u014f\3\2\2\2U\u015a\3\2\2\2W\u016f")
        buf.write("\3\2\2\2Y\u0176\3\2\2\2[\u017a\3\2\2\2]\u017d\3\2\2\2")
        buf.write("_\u0181\3\2\2\2a\u0188\3\2\2\2c\u0193\3\2\2\2e\u0195\3")
        buf.write("\2\2\2g\u019a\3\2\2\2ij\7*\2\2jk\b\2\2\2k\4\3\2\2\2lm")
        buf.write("\7+\2\2mn\b\3\3\2n\6\3\2\2\2op\7]\2\2pq\b\4\4\2q\b\3\2")
        buf.write("\2\2rs\7_\2\2st\b\5\5\2t\n\3\2\2\2uv\7H\2\2vw\7R\2\2w")
        buf.write("x\7E\2\2xy\7q\2\2yz\7t\2\2z{\7g\2\2{\f\3\2\2\2|}\7k\2")
        buf.write("\2}~\7h\2\2~\16\3\2\2\2\177\u0080\7v\2\2\u0080\u0081\7")
        buf.write("j\2\2\u0081\u0082\7g\2\2\u0082\u0083\7p\2\2\u0083\20\3")
        buf.write("\2\2\2\u0084\u0085\7g\2\2\u0085\u0086\7n\2\2\u0086\u0087")
        buf.write("\7k\2\2\u0087\u0088\7h\2\2\u0088\22\3\2\2\2\u0089\u008a")
        buf.write("\7g\2\2\u008a\u008b\7n\2\2\u008b\u008c\7u\2\2\u008c\u008d")
        buf.write("\7g\2\2\u008d\24\3\2\2\2\u008e\u008f\7n\2\2\u008f\u0090")
        buf.write("\7g\2\2\u0090\u0091\7v\2\2\u0091\26\3\2\2\2\u0092\u0093")
        buf.write("\7y\2\2\u0093\u0094\7j\2\2\u0094\u0095\7k\2\2\u0095\u0096")
        buf.write("\7n\2\2\u0096\u0097\7g\2\2\u0097\30\3\2\2\2\u0098\u0099")
        buf.write("\7h\2\2\u0099\u009a\7q\2\2\u009a\u009b\7t\2\2\u009b\32")
        buf.write("\3\2\2\2\u009c\u009d\7v\2\2\u009d\u009e\7g\2\2\u009e\u009f")
        buf.write("\7p\2\2\u009f\u00a0\7u\2\2\u00a0\u00a1\7q\2\2\u00a1\u00a2")
        buf.write("\7t\2\2\u00a2\34\3\2\2\2\u00a3\u00a4\7y\2\2\u00a4\u00a5")
        buf.write("\7k\2\2\u00a5\u00a6\7v\2\2\u00a6\u00a7\7j\2\2\u00a7\36")
        buf.write("\3\2\2\2\u00a8\u00a9\7f\2\2\u00a9\u00aa\7q\2\2\u00aa ")
        buf.write("\3\2\2\2\u00ab\u00ac\7k\2\2\u00ac\u00ad\7p\2\2\u00ad\"")
        buf.write("\3\2\2\2\u00ae\u00af\7q\2\2\u00af\u00b0\7h\2\2\u00b0$")
        buf.write("\3\2\2\2\u00b1\u00b2\7,\2\2\u00b2\u00b3\7,\2\2\u00b3&")
        buf.write("\3\2\2\2\u00b4\u00b5\7-\2\2\u00b5(\3\2\2\2\u00b6\u00b7")
        buf.write("\7/\2\2\u00b7*\3\2\2\2\u00b8\u00b9\7,\2\2\u00b9,\3\2\2")
        buf.write("\2\u00ba\u00bb\7\61\2\2\u00bb.\3\2\2\2\u00bc\u00bd\7\'")
        buf.write("\2\2\u00bd\60\3\2\2\2\u00be\u00bf\7>\2\2\u00bf\u00c0\7")
        buf.write("?\2\2\u00c0\62\3\2\2\2\u00c1\u00c2\7>\2\2\u00c2\64\3\2")
        buf.write("\2\2\u00c3\u00c4\7@\2\2\u00c4\u00c5\7?\2\2\u00c5\66\3")
        buf.write("\2\2\2\u00c6\u00c7\7@\2\2\u00c78\3\2\2\2\u00c8\u00c9\7")
        buf.write("?\2\2\u00c9\u00ca\7?\2\2\u00ca:\3\2\2\2\u00cb\u00cc\7")
        buf.write("#\2\2\u00cc\u00cd\7?\2\2\u00cd<\3\2\2\2\u00ce\u00cf\7")
        buf.write("?\2\2\u00cf>\3\2\2\2\u00d0\u00d1\7<\2\2\u00d1@\3\2\2\2")
        buf.write("\u00d2\u00d3\7.\2\2\u00d3B\3\2\2\2\u00d4\u00d5\7#\2\2")
        buf.write("\u00d5D\3\2\2\2\u00d6\u00d7\7c\2\2\u00d7\u00d8\7d\2\2")
        buf.write("\u00d8\u00d9\7q\2\2\u00d9\u00da\7t\2\2\u00da\u00db\7v")
        buf.write("\2\2\u00dbF\3\2\2\2\u00dc\u00dd\7u\2\2\u00dd\u00de\7{")
        buf.write("\2\2\u00de\u00df\7o\2\2\u00df\u00e0\7d\2\2\u00e0\u00e1")
        buf.write("\7q\2\2\u00e1\u00e2\7n\2\2\u00e2H\3\2\2\2\u00e3\u00e4")
        buf.write("\7f\2\2\u00e4\u00e5\7k\2\2\u00e5\u00e6\7i\2\2\u00e6\u00e7")
        buf.write("\7k\2\2\u00e7\u00e8\7v\2\2\u00e8\u00e9\7u\2\2\u00e9J\3")
        buf.write("\2\2\2\u00ea\u00ec\t\2\2\2\u00eb\u00ea\3\2\2\2\u00eb\u00ec")
        buf.write("\3\2\2\2\u00ec\u0100\3\2\2\2\u00ed\u00ef\t\3\2\2\u00ee")
        buf.write("\u00ed\3\2\2\2\u00ef\u00f0\3\2\2\2\u00f0\u00ee\3\2\2\2")
        buf.write("\u00f0\u00f1\3\2\2\2\u00f1\u00f8\3\2\2\2\u00f2\u00f4\7")
        buf.write("\60\2\2\u00f3\u00f5\t\3\2\2\u00f4\u00f3\3\2\2\2\u00f5")
        buf.write("\u00f6\3\2\2\2\u00f6\u00f4\3\2\2\2\u00f6\u00f7\3\2\2\2")
        buf.write("\u00f7\u00f9\3\2\2\2\u00f8\u00f2\3\2\2\2\u00f8\u00f9\3")
        buf.write("\2\2\2\u00f9\u0101\3\2\2\2\u00fa\u00fc\7\60\2\2\u00fb")
        buf.write("\u00fd\t\3\2\2\u00fc\u00fb\3\2\2\2\u00fd\u00fe\3\2\2\2")
        buf.write("\u00fe\u00fc\3\2\2\2\u00fe\u00ff\3\2\2\2\u00ff\u0101\3")
        buf.write("\2\2\2\u0100\u00ee\3\2\2\2\u0100\u00fa\3\2\2\2\u0101\u010b")
        buf.write("\3\2\2\2\u0102\u0104\t\4\2\2\u0103\u0105\t\2\2\2\u0104")
        buf.write("\u0103\3\2\2\2\u0104\u0105\3\2\2\2\u0105\u0107\3\2\2\2")
        buf.write("\u0106\u0108\t\3\2\2\u0107\u0106\3\2\2\2\u0108\u0109\3")
        buf.write("\2\2\2\u0109\u0107\3\2\2\2\u0109\u010a\3\2\2\2\u010a\u010c")
        buf.write("\3\2\2\2\u010b\u0102\3\2\2\2\u010b\u010c\3\2\2\2\u010c")
        buf.write("L\3\2\2\2\u010d\u010f\t\2\2\2\u010e\u010d\3\2\2\2\u010e")
        buf.write("\u010f\3\2\2\2\u010f\u0110\3\2\2\2\u0110\u0111\7\62\2")
        buf.write("\2\u0111\u0125\t\5\2\2\u0112\u0114\t\6\2\2\u0113\u0112")
        buf.write("\3\2\2\2\u0114\u0115\3\2\2\2\u0115\u0113\3\2\2\2\u0115")
        buf.write("\u0116\3\2\2\2\u0116\u011d\3\2\2\2\u0117\u0119\7\60\2")
        buf.write("\2\u0118\u011a\t\6\2\2\u0119\u0118\3\2\2\2\u011a\u011b")
        buf.write("\3\2\2\2\u011b\u0119\3\2\2\2\u011b\u011c\3\2\2\2\u011c")
        buf.write("\u011e\3\2\2\2\u011d\u0117\3\2\2\2\u011d\u011e\3\2\2\2")
        buf.write("\u011e\u0126\3\2\2\2\u011f\u0121\7\60\2\2\u0120\u0122")
        buf.write("\t\6\2\2\u0121\u0120\3\2\2\2\u0122\u0123\3\2\2\2\u0123")
        buf.write("\u0121\3\2\2\2\u0123\u0124\3\2\2\2\u0124\u0126\3\2\2\2")
        buf.write("\u0125\u0113\3\2\2\2\u0125\u011f\3\2\2\2\u0126\u0130\3")
        buf.write("\2\2\2\u0127\u0129\t\7\2\2\u0128\u012a\t\2\2\2\u0129\u0128")
        buf.write("\3\2\2\2\u0129\u012a\3\2\2\2\u012a\u012c\3\2\2\2\u012b")
        buf.write("\u012d\t\3\2\2\u012c\u012b\3\2\2\2\u012d\u012e\3\2\2\2")
        buf.write("\u012e\u012c\3\2\2\2\u012e\u012f\3\2\2\2\u012f\u0131\3")
        buf.write("\2\2\2\u0130\u0127\3\2\2\2\u0130\u0131\3\2\2\2\u0131N")
        buf.write("\3\2\2\2\u0132\u0134\t\2\2\2\u0133\u0132\3\2\2\2\u0133")
        buf.write("\u0134\3\2\2\2\u0134\u0136\3\2\2\2\u0135\u0137\t\3\2\2")
        buf.write("\u0136\u0135\3\2\2\2\u0137\u0138\3\2\2\2\u0138\u0136\3")
        buf.write("\2\2\2\u0138\u0139\3\2\2\2\u0139\u013a\3\2\2\2\u013a\u013e")
        buf.write("\7\61\2\2\u013b\u013d\t\3\2\2\u013c\u013b\3\2\2\2\u013d")
        buf.write("\u0140\3\2\2\2\u013e\u013c\3\2\2\2\u013e\u013f\3\2\2\2")
        buf.write("\u013f\u0141\3\2\2\2\u0140\u013e\3\2\2\2\u0141\u0145\t")
        buf.write("\b\2\2\u0142\u0144\t\3\2\2\u0143\u0142\3\2\2\2\u0144\u0147")
        buf.write("\3\2\2\2\u0145\u0143\3\2\2\2\u0145\u0146\3\2\2\2\u0146")
        buf.write("P\3\2\2\2\u0147\u0145\3\2\2\2\u0148\u014c\5c\62\2\u0149")
        buf.write("\u014b\5e\63\2\u014a\u0149\3\2\2\2\u014b\u014e\3\2\2\2")
        buf.write("\u014c\u014a\3\2\2\2\u014c\u014d\3\2\2\2\u014dR\3\2\2")
        buf.write("\2\u014e\u014c\3\2\2\2\u014f\u0150\7u\2\2\u0150\u0151")
        buf.write("\7$\2\2\u0151\u0155\3\2\2\2\u0152\u0154\5g\64\2\u0153")
        buf.write("\u0152\3\2\2\2\u0154\u0157\3\2\2\2\u0155\u0153\3\2\2\2")
        buf.write("\u0155\u0156\3\2\2\2\u0156\u0158\3\2\2\2\u0157\u0155\3")
        buf.write("\2\2\2\u0158\u0159\7$\2\2\u0159T\3\2\2\2\u015a\u015e\7")
        buf.write("$\2\2\u015b\u015d\5g\64\2\u015c\u015b\3\2\2\2\u015d\u0160")
        buf.write("\3\2\2\2\u015e\u015c\3\2\2\2\u015e\u015f\3\2\2\2\u015f")
        buf.write("\u0161\3\2\2\2\u0160\u015e\3\2\2\2\u0161\u0162\7$\2\2")
        buf.write("\u0162V\3\2\2\2\u0163\u0164\6,\2\2\u0164\u0170\5]/\2\u0165")
        buf.write("\u0167\7\17\2\2\u0166\u0165\3\2\2\2\u0166\u0167\3\2\2")
        buf.write("\2\u0167\u0168\3\2\2\2\u0168\u016b\7\f\2\2\u0169\u016b")
        buf.write("\4\16\17\2\u016a\u0166\3\2\2\2\u016a\u0169\3\2\2\2\u016b")
        buf.write("\u016d\3\2\2\2\u016c\u016e\5]/\2\u016d\u016c\3\2\2\2\u016d")
        buf.write("\u016e\3\2\2\2\u016e\u0170\3\2\2\2\u016f\u0163\3\2\2\2")
        buf.write("\u016f\u016a\3\2\2\2\u0170\u0171\3\2\2\2\u0171\u0172\b")
        buf.write(",\6\2\u0172X\3\2\2\2\u0173\u0177\5]/\2\u0174\u0177\5_")
        buf.write("\60\2\u0175\u0177\5a\61\2\u0176\u0173\3\2\2\2\u0176\u0174")
        buf.write("\3\2\2\2\u0176\u0175\3\2\2\2\u0177\u0178\3\2\2\2\u0178")
        buf.write("\u0179\b-\7\2\u0179Z\3\2\2\2\u017a\u017b\13\2\2\2\u017b")
        buf.write("\\\3\2\2\2\u017c\u017e\t\t\2\2\u017d\u017c\3\2\2\2\u017e")
        buf.write("\u017f\3\2\2\2\u017f\u017d\3\2\2\2\u017f\u0180\3\2\2\2")
        buf.write("\u0180^\3\2\2\2\u0181\u0185\7%\2\2\u0182\u0184\n\n\2\2")
        buf.write("\u0183\u0182\3\2\2\2\u0184\u0187\3\2\2\2\u0185\u0183\3")
        buf.write("\2\2\2\u0185\u0186\3\2\2\2\u0186`\3\2\2\2\u0187\u0185")
        buf.write("\3\2\2\2\u0188\u018a\7^\2\2\u0189\u018b\5]/\2\u018a\u0189")
        buf.write("\3\2\2\2\u018a\u018b\3\2\2\2\u018b\u0191\3\2\2\2\u018c")
        buf.write("\u018e\7\17\2\2\u018d\u018c\3\2\2\2\u018d\u018e\3\2\2")
        buf.write("\2\u018e\u018f\3\2\2\2\u018f\u0192\7\f\2\2\u0190\u0192")
        buf.write("\4\16\17\2\u0191\u018d\3\2\2\2\u0191\u0190\3\2\2\2\u0192")
        buf.write("b\3\2\2\2\u0193\u0194\t\13\2\2\u0194d\3\2\2\2\u0195\u0196")
        buf.write("\t\f\2\2\u0196f\3\2\2\2\u0197\u019b\t\r\2\2\u0198\u0199")
        buf.write("\7^\2\2\u0199\u019b\t\16\2\2\u019a\u0197\3\2\2\2\u019a")
        buf.write("\u0198\3\2\2\2\u019bh\3\2\2\2\'\2\u00eb\u00f0\u00f6\u00f8")
        buf.write("\u00fe\u0100\u0104\u0109\u010b\u010e\u0115\u011b\u011d")
        buf.write("\u0123\u0125\u0129\u012e\u0130\u0133\u0138\u013e\u0145")
        buf.write("\u014c\u0155\u015e\u0166\u016a\u016d\u016f\u0176\u017f")
        buf.write("\u0185\u018a\u018d\u0191\u019a\b\3\2\2\3\3\3\3\4\4\3\5")
        buf.write("\5\3,\6\b\2\2")
        return buf.getvalue()


class FPYLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    OPEN_PAREN = 1
    CLOSE_PAREN = 2
    OPEN_BRACK = 3
    CLOSE_BRACK = 4
    FPCORE = 5
    IF = 6
    THEN = 7
    ELIF = 8
    ELSE = 9
    LET = 10
    WHILE = 11
    FOR = 12
    TENSOR = 13
    WITH = 14
    DO = 15
    IN = 16
    OF = 17
    POWER = 18
    PLUS = 19
    MINUS = 20
    TIMES = 21
    DIVIDE = 22
    MOD = 23
    LE = 24
    LT = 25
    GE = 26
    GT = 27
    EQ = 28
    NE = 29
    IS = 30
    COLON = 31
    COMMA = 32
    BANG = 33
    ABORT = 34
    SYM = 35
    DIG = 36
    DECNUM = 37
    HEXNUM = 38
    RATIONAL = 39
    SYMBOL = 40
    S_STRING = 41
    STRING = 42
    NEWLINE = 43
    SKIP_ = 44
    UNK_ = 45

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'['", "']'", "'FPCore'", "'if'", "'then'", "'elif'", 
            "'else'", "'let'", "'while'", "'for'", "'tensor'", "'with'", 
            "'do'", "'in'", "'of'", "'**'", "'+'", "'-'", "'*'", "'/'", 
            "'%'", "'<='", "'<'", "'>='", "'>'", "'=='", "'!='", "'='", 
            "':'", "','", "'!'", "'abort'", "'symbol'", "'digits'" ]

    symbolicNames = [ "<INVALID>",
            "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACK", "CLOSE_BRACK", "FPCORE", 
            "IF", "THEN", "ELIF", "ELSE", "LET", "WHILE", "FOR", "TENSOR", 
            "WITH", "DO", "IN", "OF", "POWER", "PLUS", "MINUS", "TIMES", 
            "DIVIDE", "MOD", "LE", "LT", "GE", "GT", "EQ", "NE", "IS", "COLON", 
            "COMMA", "BANG", "ABORT", "SYM", "DIG", "DECNUM", "HEXNUM", 
            "RATIONAL", "SYMBOL", "S_STRING", "STRING", "NEWLINE", "SKIP_", 
            "UNK_" ]

    ruleNames = [ "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACK", "CLOSE_BRACK", 
                  "FPCORE", "IF", "THEN", "ELIF", "ELSE", "LET", "WHILE", 
                  "FOR", "TENSOR", "WITH", "DO", "IN", "OF", "POWER", "PLUS", 
                  "MINUS", "TIMES", "DIVIDE", "MOD", "LE", "LT", "GE", "GT", 
                  "EQ", "NE", "IS", "COLON", "COMMA", "BANG", "ABORT", "SYM", 
                  "DIG", "DECNUM", "HEXNUM", "RATIONAL", "SYMBOL", "S_STRING", 
                  "STRING", "NEWLINE", "SKIP_", "UNK_", "SPACES", "COMMENT", 
                  "LINE_JOINING", "SIMPLE_SYMBOL_START", "SIMPLE_SYMBOL_CHAR", 
                  "STRING_CHAR" ]

    grammarFileName = "FPY.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    @property
    def tokens(self):
        try:
            return self._tokens
        except AttributeError:
            self._tokens = []
            return self._tokens

    @property
    def indents(self):
        try:
            return self._indents
        except AttributeError:
            self._indents = []
            return self._indents

    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    @property
    def lastToken(self):
        try:
            return self._lastToken
        except AttributeError:
            self._lastToken = None
            return self._lastToken

    @lastToken.setter
    def lastToken(self, value):
        self._lastToken = value

    def reset(self):
        super().reset()
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.lastToken = None

    def emitToken(self, t):
        super().emitToken(t)
        self.tokens.append(t)

    def nextToken(self):
        if self._input.LA(1) == Token.EOF and self.indents:
            for i in range(len(self.tokens)-1,-1,-1):
                if self.tokens[i].type == Token.EOF:
                    self.tokens.pop(i)

            self.emitToken(self.commonToken(LanguageParser.NEWLINE, '\n'))
            while self.indents:
                self.emitToken(self.createDedent())
                self.indents.pop()

            self.emitToken(self.commonToken(LanguageParser.EOF, "<EOF>"))
        next = super().nextToken()
        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next
        return next if not self.tokens else self.tokens.pop(0)

    def createDedent(self):
        dedent = self.commonToken(LanguageParser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent

    def commonToken(self, type, text, indent=0):
        stop = self.getCharIndex()-1-indent
        start = (stop - len(text) + 1) if text else stop
        return CommonToken(self._tokenFactorySourcePair, type, super().DEFAULT_TOKEN_CHANNEL, start, stop)

    @staticmethod
    def getIndentationCount(spaces):
        count = 0
        for ch in spaces:
            if ch == '\t':
                count += 8 - (count % 8)
            else:
                count += 1
        return count

    def atStartOfInput(self):
        return Lexer.column.fget(self) == 0 and Lexer.line.fget(self) == 1


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[0] = self.OPEN_PAREN_action 
            actions[1] = self.CLOSE_PAREN_action 
            actions[2] = self.OPEN_BRACK_action 
            actions[3] = self.CLOSE_BRACK_action 
            actions[42] = self.NEWLINE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened -= 1
     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened -= 1
     

    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:

            tempt = Lexer.text.fget(self)
            newLine = only_spaces.sub("", tempt)
            spaces = only_newlines.sub("", tempt)
            la_char = ""
            try:
                la = self._input.LA(1)
                la_char = chr(la)
            except ValueError: # End of file
                pass

            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to
            # satisfy the final newline needed by the single_put rule used by the REPL.
            try:
                nextnext_la = self._input.LA(2)
                nextnext_la_char = chr(nextnext_la)
            except ValueError:
                nextnext_eof = True
            else:
                nextnext_eof = False

            if self.opened > 0 or nextnext_eof is False and (la_char == '\r' or la_char == '\n' or la_char == '\f' or la_char == '#'):
                self.skip()
            else:
                indent = self.getIndentationCount(spaces)
                previous = self.indents[-1] if self.indents else 0
                self.emitToken(self.commonToken(self.NEWLINE, newLine, indent=indent))      # NEWLINE is actually the '\n' char
                if indent == previous:
                    self.skip()
                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[42] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


