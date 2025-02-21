""" Python Character Mapping Codec generated from 'VENDORS/MICSFT/PC/CP869.TXT' with gencodec.py.

"""#"

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,encoding_map)

    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input,self.errors,encoding_map)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input,self.errors,decoding_table)[0]

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():
    return codecs.CodecInfo(
        name='cp869',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

### Decoding Map

decoding_map = codecs.make_identity_dict(range(256))
decoding_map.update({
    0x0080: None,       #  UNDEFINED
    0x0081: None,       #  UNDEFINED
    0x0082: None,       #  UNDEFINED
    0x0083: None,       #  UNDEFINED
    0x0084: None,       #  UNDEFINED
    0x0085: None,       #  UNDEFINED
    0x0086: 0x0386,     #  GREEK CAPITAL LETTER ALPHA WITH TONOS
    0x0087: None,       #  UNDEFINED
    0x0088: 0x00b7,     #  MIDDLE DOT
    0x0089: 0x00ac,     #  NOT SIGN
    0x008a: 0x00a6,     #  BROKEN BAR
    0x008b: 0x2018,     #  LEFT SINGLE QUOTATION MARK
    0x008c: 0x2019,     #  RIGHT SINGLE QUOTATION MARK
    0x008d: 0x0388,     #  GREEK CAPITAL LETTER EPSILON WITH TONOS
    0x008e: 0x2015,     #  HORIZONTAL BAR
    0x008f: 0x0389,     #  GREEK CAPITAL LETTER ETA WITH TONOS
    0x0090: 0x038a,     #  GREEK CAPITAL LETTER IOTA WITH TONOS
    0x0091: 0x03aa,     #  GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
    0x0092: 0x038c,     #  GREEK CAPITAL LETTER OMICRON WITH TONOS
    0x0093: None,       #  UNDEFINED
    0x0094: None,       #  UNDEFINED
    0x0095: 0x038e,     #  GREEK CAPITAL LETTER UPSILON WITH TONOS
    0x0096: 0x03ab,     #  GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA
    0x0097: 0x00a9,     #  COPYRIGHT SIGN
    0x0098: 0x038f,     #  GREEK CAPITAL LETTER OMEGA WITH TONOS
    0x0099: 0x00b2,     #  SUPERSCRIPT TWO
    0x009a: 0x00b3,     #  SUPERSCRIPT THREE
    0x009b: 0x03ac,     #  GREEK SMALL LETTER ALPHA WITH TONOS
    0x009c: 0x00a3,     #  POUND SIGN
    0x009d: 0x03ad,     #  GREEK SMALL LETTER EPSILON WITH TONOS
    0x009e: 0x03ae,     #  GREEK SMALL LETTER ETA WITH TONOS
    0x009f: 0x03af,     #  GREEK SMALL LETTER IOTA WITH TONOS
    0x00a0: 0x03ca,     #  GREEK SMALL LETTER IOTA WITH DIALYTIKA
    0x00a1: 0x0390,     #  GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
    0x00a2: 0x03cc,     #  GREEK SMALL LETTER OMICRON WITH TONOS
    0x00a3: 0x03cd,     #  GREEK SMALL LETTER UPSILON WITH TONOS
    0x00a4: 0x0391,     #  GREEK CAPITAL LETTER ALPHA
    0x00a5: 0x0392,     #  GREEK CAPITAL LETTER BETA
    0x00a6: 0x0393,     #  GREEK CAPITAL LETTER GAMMA
    0x00a7: 0x0394,     #  GREEK CAPITAL LETTER DELTA
    0x00a8: 0x0395,     #  GREEK CAPITAL LETTER EPSILON
    0x00a9: 0x0396,     #  GREEK CAPITAL LETTER ZETA
    0x00aa: 0x0397,     #  GREEK CAPITAL LETTER ETA
    0x00ab: 0x00bd,     #  VULGAR FRACTION ONE HALF
    0x00ac: 0x0398,     #  GREEK CAPITAL LETTER THETA
    0x00ad: 0x0399,     #  GREEK CAPITAL LETTER IOTA
    0x00ae: 0x00ab,     #  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00af: 0x00bb,     #  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00b0: 0x2591,     #  LIGHT SHADE
    0x00b1: 0x2592,     #  MEDIUM SHADE
    0x00b2: 0x2593,     #  DARK SHADE
    0x00b3: 0x2502,     #  BOX DRAWINGS LIGHT VERTICAL
    0x00b4: 0x2524,     #  BOX DRAWINGS LIGHT VERTICAL AND LEFT
    0x00b5: 0x039a,     #  GREEK CAPITAL LETTER KAPPA
    0x00b6: 0x039b,     #  GREEK CAPITAL LETTER LAMDA
    0x00b7: 0x039c,     #  GREEK CAPITAL LETTER MU
    0x00b8: 0x039d,     #  GREEK CAPITAL LETTER NU
    0x00b9: 0x2563,     #  BOX DRAWINGS DOUBLE VERTICAL AND LEFT
    0x00ba: 0x2551,     #  BOX DRAWINGS DOUBLE VERTICAL
    0x00bb: 0x2557,     #  BOX DRAWINGS DOUBLE DOWN AND LEFT
    0x00bc: 0x255d,     #  BOX DRAWINGS DOUBLE UP AND LEFT
    0x00bd: 0x039e,     #  GREEK CAPITAL LETTER XI
    0x00be: 0x039f,     #  GREEK CAPITAL LETTER OMICRON
    0x00bf: 0x2510,     #  BOX DRAWINGS LIGHT DOWN AND LEFT
    0x00c0: 0x2514,     #  BOX DRAWINGS LIGHT UP AND RIGHT
    0x00c1: 0x2534,     #  BOX DRAWINGS LIGHT UP AND HORIZONTAL
    0x00c2: 0x252c,     #  BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
    0x00c3: 0x251c,     #  BOX DRAWINGS LIGHT VERTICAL AND RIGHT
    0x00c4: 0x2500,     #  BOX DRAWINGS LIGHT HORIZONTAL
    0x00c5: 0x253c,     #  BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
    0x00c6: 0x03a0,     #  GREEK CAPITAL LETTER PI
    0x00c7: 0x03a1,     #  GREEK CAPITAL LETTER RHO
    0x00c8: 0x255a,     #  BOX DRAWINGS DOUBLE UP AND RIGHT
    0x00c9: 0x2554,     #  BOX DRAWINGS DOUBLE DOWN AND RIGHT
    0x00ca: 0x2569,     #  BOX DRAWINGS DOUBLE UP AND HORIZONTAL
    0x00cb: 0x2566,     #  BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
    0x00cc: 0x2560,     #  BOX DRAWINGS DOUBLE VERTICAL AND RIGHT
    0x00cd: 0x2550,     #  BOX DRAWINGS DOUBLE HORIZONTAL
    0x00ce: 0x256c,     #  BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
    0x00cf: 0x03a3,     #  GREEK CAPITAL LETTER SIGMA
    0x00d0: 0x03a4,     #  GREEK CAPITAL LETTER TAU
    0x00d1: 0x03a5,     #  GREEK CAPITAL LETTER UPSILON
    0x00d2: 0x03a6,     #  GREEK CAPITAL LETTER PHI
    0x00d3: 0x03a7,     #  GREEK CAPITAL LETTER CHI
    0x00d4: 0x03a8,     #  GREEK CAPITAL LETTER PSI
    0x00d5: 0x03a9,     #  GREEK CAPITAL LETTER OMEGA
    0x00d6: 0x03b1,     #  GREEK SMALL LETTER ALPHA
    0x00d7: 0x03b2,     #  GREEK SMALL LETTER BETA
    0x00d8: 0x03b3,     #  GREEK SMALL LETTER GAMMA
    0x00d9: 0x2518,     #  BOX DRAWINGS LIGHT UP AND LEFT
    0x00da: 0x250c,     #  BOX DRAWINGS LIGHT DOWN AND RIGHT
    0x00db: 0x2588,     #  FULL BLOCK
    0x00dc: 0x2584,     #  LOWER HALF BLOCK
    0x00dd: 0x03b4,     #  GREEK SMALL LETTER DELTA
    0x00de: 0x03b5,     #  GREEK SMALL LETTER EPSILON
    0x00df: 0x2580,     #  UPPER HALF BLOCK
    0x00e0: 0x03b6,     #  GREEK SMALL LETTER ZETA
    0x00e1: 0x03b7,     #  GREEK SMALL LETTER ETA
    0x00e2: 0x03b8,     #  GREEK SMALL LETTER THETA
    0x00e3: 0x03b9,     #  GREEK SMALL LETTER IOTA
    0x00e4: 0x03ba,     #  GREEK SMALL LETTER KAPPA
    0x00e5: 0x03bb,     #  GREEK SMALL LETTER LAMDA
    0x00e6: 0x03bc,     #  GREEK SMALL LETTER MU
    0x00e7: 0x03bd,     #  GREEK SMALL LETTER NU
    0x00e8: 0x03be,     #  GREEK SMALL LETTER XI
    0x00e9: 0x03bf,     #  GREEK SMALL LETTER OMICRON
    0x00ea: 0x03c0,     #  GREEK SMALL LETTER PI
    0x00eb: 0x03c1,     #  GREEK SMALL LETTER RHO
    0x00ec: 0x03c3,     #  GREEK SMALL LETTER SIGMA
    0x00ed: 0x03c2,     #  GREEK SMALL LETTER FINAL SIGMA
    0x00ee: 0x03c4,     #  GREEK SMALL LETTER TAU
    0x00ef: 0x0384,     #  GREEK TONOS
    0x00f0: 0x00ad,     #  SOFT HYPHEN
    0x00f1: 0x00b1,     #  PLUS-MINUS SIGN
    0x00f2: 0x03c5,     #  GREEK SMALL LETTER UPSILON
    0x00f3: 0x03c6,     #  GREEK SMALL LETTER PHI
    0x00f4: 0x03c7,     #  GREEK SMALL LETTER CHI
    0x00f5: 0x00a7,     #  SECTION SIGN
    0x00f6: 0x03c8,     #  GREEK SMALL LETTER PSI
    0x00f7: 0x0385,     #  GREEK DIALYTIKA TONOS
    0x00f8: 0x00b0,     #  DEGREE SIGN
    0x00f9: 0x00a8,     #  DIAERESIS
    0x00fa: 0x03c9,     #  GREEK SMALL LETTER OMEGA
    0x00fb: 0x03cb,     #  GREEK SMALL LETTER UPSILON WITH DIALYTIKA
    0x00fc: 0x03b0,     #  GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
    0x00fd: 0x03ce,     #  GREEK SMALL LETTER OMEGA WITH TONOS
    0x00fe: 0x25a0,     #  BLACK SQUARE
    0x00ff: 0x00a0,     #  NO-BREAK SPACE
})

### Decoding Table

decoding_table = (
    '\x00'     #  0x0000 -> NULL
    '\x01'     #  0x0001 -> START OF HEADING
    '\x02'     #  0x0002 -> START OF TEXT
    '\x03'     #  0x0003 -> END OF TEXT
    '\x04'     #  0x0004 -> END OF TRANSMISSION
    '\x05'     #  0x0005 -> ENQUIRY
    '\x06'     #  0x0006 -> ACKNOWLEDGE
    '\x07'     #  0x0007 -> BELL
    '\x08'     #  0x0008 -> BACKSPACE
    '\t'       #  0x0009 -> HORIZONTAL TABULATION
    '\n'       #  0x000a -> LINE FEED
    '\x0b'     #  0x000b -> VERTICAL TABULATION
    '\x0c'     #  0x000c -> FORM FEED
    '\r'       #  0x000d -> CARRIAGE RETURN
    '\x0e'     #  0x000e -> SHIFT OUT
    '\x0f'     #  0x000f -> SHIFT IN
    '\x10'     #  0x0010 -> DATA LINK ESCAPE
    '\x11'     #  0x0011 -> DEVICE CONTROL ONE
    '\x12'     #  0x0012 -> DEVICE CONTROL TWO
    '\x13'     #  0x0013 -> DEVICE CONTROL THREE
    '\x14'     #  0x0014 -> DEVICE CONTROL FOUR
    '\x15'     #  0x0015 -> NEGATIVE ACKNOWLEDGE
    '\x16'     #  0x0016 -> SYNCHRONOUS IDLE
    '\x17'     #  0x0017 -> END OF TRANSMISSION BLOCK
    '\x18'     #  0x0018 -> CANCEL
    '\x19'     #  0x0019 -> END OF MEDIUM
    '\x1a'     #  0x001a -> SUBSTITUTE
    '\x1b'     #  0x001b -> ESCAPE
    '\x1c'     #  0x001c -> FILE SEPARATOR
    '\x1d'     #  0x001d -> GROUP SEPARATOR
    '\x1e'     #  0x001e -> RECORD SEPARATOR
    '\x1f'     #  0x001f -> UNIT SEPARATOR
    ' '        #  0x0020 -> SPACE
    '!'        #  0x0021 -> EXCLAMATION MARK
    '"'        #  0x0022 -> QUOTATION MARK
    '#'        #  0x0023 -> NUMBER SIGN
    '$'        #  0x0024 -> DOLLAR SIGN
    '%'        #  0x0025 -> PERCENT SIGN
    '&'        #  0x0026 -> AMPERSAND
    "'"        #  0x0027 -> APOSTROPHE
    '('        #  0x0028 -> LEFT PARENTHESIS
    ')'        #  0x0029 -> RIGHT PARENTHESIS
    '*'        #  0x002a -> ASTERISK
    '+'        #  0x002b -> PLUS SIGN
    ','        #  0x002c -> COMMA
    '-'        #  0x002d -> HYPHEN-MINUS
    '.'        #  0x002e -> FULL STOP
    '/'        #  0x002f -> SOLIDUS
    '0'        #  0x0030 -> DIGIT ZERO
    '1'        #  0x0031 -> DIGIT ONE
    '2'        #  0x0032 -> DIGIT TWO
    '3'        #  0x0033 -> DIGIT THREE
    '4'        #  0x0034 -> DIGIT FOUR
    '5'        #  0x0035 -> DIGIT FIVE
    '6'        #  0x0036 -> DIGIT SIX
    '7'        #  0x0037 -> DIGIT SEVEN
    '8'        #  0x0038 -> DIGIT EIGHT
    '9'        #  0x0039 -> DIGIT NINE
    ':'        #  0x003a -> COLON
    ';'        #  0x003b -> SEMICOLON
    '<'        #  0x003c -> LESS-THAN SIGN
    '='        #  0x003d -> EQUALS SIGN
    '>'        #  0x003e -> GREATER-THAN SIGN
    '?'        #  0x003f -> QUESTION MARK
    '@'        #  0x0040 -> COMMERCIAL AT
    'A'        #  0x0041 -> LATIN CAPITAL LETTER A
    'B'        #  0x0042 -> LATIN CAPITAL LETTER B
    'C'        #  0x0043 -> LATIN CAPITAL LETTER C
    'D'        #  0x0044 -> LATIN CAPITAL LETTER D
    'E'        #  0x0045 -> LATIN CAPITAL LETTER E
    'F'        #  0x0046 -> LATIN CAPITAL LETTER F
    'G'        #  0x0047 -> LATIN CAPITAL LETTER G
    'H'        #  0x0048 -> LATIN CAPITAL LETTER H
    'I'        #  0x0049 -> LATIN CAPITAL LETTER I
    'J'        #  0x004a -> LATIN CAPITAL LETTER J
    'K'        #  0x004b -> LATIN CAPITAL LETTER K
    'L'        #  0x004c -> LATIN CAPITAL LETTER L
    'M'        #  0x004d -> LATIN CAPITAL LETTER M
    'N'        #  0x004e -> LATIN CAPITAL LETTER N
    'O'        #  0x004f -> LATIN CAPITAL LETTER O
    'P'        #  0x0050 -> LATIN CAPITAL LETTER P
    'Q'        #  0x0051 -> LATIN CAPITAL LETTER Q
    'R'        #  0x0052 -> LATIN CAPITAL LETTER R
    'S'        #  0x0053 -> LATIN CAPITAL LETTER S
    'T'        #  0x0054 -> LATIN CAPITAL LETTER T
    'U'        #  0x0055 -> LATIN CAPITAL LETTER U
    'V'        #  0x0056 -> LATIN CAPITAL LETTER V
    'W'        #  0x0057 -> LATIN CAPITAL LETTER W
    'X'        #  0x0058 -> LATIN CAPITAL LETTER X
    'Y'        #  0x0059 -> LATIN CAPITAL LETTER Y
    'Z'        #  0x005a -> LATIN CAPITAL LETTER Z
    '['        #  0x005b -> LEFT SQUARE BRACKET
    '\\'       #  0x005c -> REVERSE SOLIDUS
    ']'        #  0x005d -> RIGHT SQUARE BRACKET
    '^'        #  0x005e -> CIRCUMFLEX ACCENT
    '_'        #  0x005f -> LOW LINE
    '`'        #  0x0060 -> GRAVE ACCENT
    'a'        #  0x0061 -> LATIN SMALL LETTER A
    'b'        #  0x0062 -> LATIN SMALL LETTER B
    'c'        #  0x0063 -> LATIN SMALL LETTER C
    'd'        #  0x0064 -> LATIN SMALL LETTER D
    'e'        #  0x0065 -> LATIN SMALL LETTER E
    'f'        #  0x0066 -> LATIN SMALL LETTER F
    'g'        #  0x0067 -> LATIN SMALL LETTER G
    'h'        #  0x0068 -> LATIN SMALL LETTER H
    'i'        #  0x0069 -> LATIN SMALL LETTER I
    'j'        #  0x006a -> LATIN SMALL LETTER J
    'k'        #  0x006b -> LATIN SMALL LETTER K
    'l'        #  0x006c -> LATIN SMALL LETTER L
    'm'        #  0x006d -> LATIN SMALL LETTER M
    'n'        #  0x006e -> LATIN SMALL LETTER N
    'o'        #  0x006f -> LATIN SMALL LETTER O
    'p'        #  0x0070 -> LATIN SMALL LETTER P
    'q'        #  0x0071 -> LATIN SMALL LETTER Q
    'r'        #  0x0072 -> LATIN SMALL LETTER R
    's'        #  0x0073 -> LATIN SMALL LETTER S
    't'        #  0x0074 -> LATIN SMALL LETTER T
    'u'        #  0x0075 -> LATIN SMALL LETTER U
    'v'        #  0x0076 -> LATIN SMALL LETTER V
    'w'        #  0x0077 -> LATIN SMALL LETTER W
    'x'        #  0x0078 -> LATIN SMALL LETTER X
    'y'        #  0x0079 -> LATIN SMALL LETTER Y
    'z'        #  0x007a -> LATIN SMALL LETTER Z
    '{'        #  0x007b -> LEFT CURLY BRACKET
    '|'        #  0x007c -> VERTICAL LINE
    '}'        #  0x007d -> RIGHT CURLY BRACKET
    '~'        #  0x007e -> TILDE
    '\x7f'     #  0x007f -> DELETE
    '\ufffe'   #  0x0080 -> UNDEFINED
    '\ufffe'   #  0x0081 -> UNDEFINED
    '\ufffe'   #  0x0082 -> UNDEFINED
    '\ufffe'   #  0x0083 -> UNDEFINED
    '\ufffe'   #  0x0084 -> UNDEFINED
    '\ufffe'   #  0x0085 -> UNDEFINED
    '\u0386'   #  0x0086 -> GREEK CAPITAL LETTER ALPHA WITH TONOS
    '\ufffe'   #  0x0087 -> UNDEFINED
    '\xb7'     #  0x0088 -> MIDDLE DOT
    '\xac'     #  0x0089 -> NOT SIGN
    '\xa6'     #  0x008a -> BROKEN BAR
    '\u2018'   #  0x008b -> LEFT SINGLE QUOTATION MARK
    '\u2019'   #  0x008c -> RIGHT SINGLE QUOTATION MARK
    '\u0388'   #  0x008d -> GREEK CAPITAL LETTER EPSILON WITH TONOS
    '\u2015'   #  0x008e -> HORIZONTAL BAR
    '\u0389'   #  0x008f -> GREEK CAPITAL LETTER ETA WITH TONOS
    '\u038a'   #  0x0090 -> GREEK CAPITAL LETTER IOTA WITH TONOS
    '\u03aa'   #  0x0091 -> GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
    '\u038c'   #  0x0092 -> GREEK CAPITAL LETTER OMICRON WITH TONOS
    '\ufffe'   #  0x0093 -> UNDEFINED
    '\ufffe'   #  0x0094 -> UNDEFINED
    '\u038e'   #  0x0095 -> GREEK CAPITAL LETTER UPSILON WITH TONOS
    '\u03ab'   #  0x0096 -> GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA
    '\xa9'     #  0x0097 -> COPYRIGHT SIGN
    '\u038f'   #  0x0098 -> GREEK CAPITAL LETTER OMEGA WITH TONOS
    '\xb2'     #  0x0099 -> SUPERSCRIPT TWO
    '\xb3'     #  0x009a -> SUPERSCRIPT THREE
    '\u03ac'   #  0x009b -> GREEK SMALL LETTER ALPHA WITH TONOS
    '\xa3'     #  0x009c -> POUND SIGN
    '\u03ad'   #  0x009d -> GREEK SMALL LETTER EPSILON WITH TONOS
    '\u03ae'   #  0x009e -> GREEK SMALL LETTER ETA WITH TONOS
    '\u03af'   #  0x009f -> GREEK SMALL LETTER IOTA WITH TONOS
    '\u03ca'   #  0x00a0 -> GREEK SMALL LETTER IOTA WITH DIALYTIKA
    '\u0390'   #  0x00a1 -> GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
    '\u03cc'   #  0x00a2 -> GREEK SMALL LETTER OMICRON WITH TONOS
    '\u03cd'   #  0x00a3 -> GREEK SMALL LETTER UPSILON WITH TONOS
    '\u0391'   #  0x00a4 -> GREEK CAPITAL LETTER ALPHA
    '\u0392'   #  0x00a5 -> GREEK CAPITAL LETTER BETA
    '\u0393'   #  0x00a6 -> GREEK CAPITAL LETTER GAMMA
    '\u0394'   #  0x00a7 -> GREEK CAPITAL LETTER DELTA
    '\u0395'   #  0x00a8 -> GREEK CAPITAL LETTER EPSILON
    '\u0396'   #  0x00a9 -> GREEK CAPITAL LETTER ZETA
    '\u0397'   #  0x00aa -> GREEK CAPITAL LETTER ETA
    '\xbd'     #  0x00ab -> VULGAR FRACTION ONE HALF
    '\u0398'   #  0x00ac -> GREEK CAPITAL LETTER THETA
    '\u0399'   #  0x00ad -> GREEK CAPITAL LETTER IOTA
    '\xab'     #  0x00ae -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    '\xbb'     #  0x00af -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    '\u2591'   #  0x00b0 -> LIGHT SHADE
    '\u2592'   #  0x00b1 -> MEDIUM SHADE
    '\u2593'   #  0x00b2 -> DARK SHADE
    '\u2502'   #  0x00b3 -> BOX DRAWINGS LIGHT VERTICAL
    '\u2524'   #  0x00b4 -> BOX DRAWINGS LIGHT VERTICAL AND LEFT
    '\u039a'   #  0x00b5 -> GREEK CAPITAL LETTER KAPPA
    '\u039b'   #  0x00b6 -> GREEK CAPITAL LETTER LAMDA
    '\u039c'   #  0x00b7 -> GREEK CAPITAL LETTER MU
    '\u039d'   #  0x00b8 -> GREEK CAPITAL LETTER NU
    '\u2563'   #  0x00b9 -> BOX DRAWINGS DOUBLE VERTICAL AND LEFT
    '\u2551'   #  0x00ba -> BOX DRAWINGS DOUBLE VERTICAL
    '\u2557'   #  0x00bb -> BOX DRAWINGS DOUBLE DOWN AND LEFT
    '\u255d'   #  0x00bc -> BOX DRAWINGS DOUBLE UP AND LEFT
    '\u039e'   #  0x00bd -> GREEK CAPITAL LETTER XI
    '\u039f'   #  0x00be -> GREEK CAPITAL LETTER OMICRON
    '\u2510'   #  0x00bf -> BOX DRAWINGS LIGHT DOWN AND LEFT
    '\u2514'   #  0x00c0 -> BOX DRAWINGS LIGHT UP AND RIGHT
    '\u2534'   #  0x00c1 -> BOX DRAWINGS LIGHT UP AND HORIZONTAL
    '\u252c'   #  0x00c2 -> BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
    '\u251c'   #  0x00c3 -> BOX DRAWINGS LIGHT VERTICAL AND RIGHT
    '\u2500'   #  0x00c4 -> BOX DRAWINGS LIGHT HORIZONTAL
    '\u253c'   #  0x00c5 -> BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
    '\u03a0'   #  0x00c6 -> GREEK CAPITAL LETTER PI
    '\u03a1'   #  0x00c7 -> GREEK CAPITAL LETTER RHO
    '\u255a'   #  0x00c8 -> BOX DRAWINGS DOUBLE UP AND RIGHT
    '\u2554'   #  0x00c9 -> BOX DRAWINGS DOUBLE DOWN AND RIGHT
    '\u2569'   #  0x00ca -> BOX DRAWINGS DOUBLE UP AND HORIZONTAL
    '\u2566'   #  0x00cb -> BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
    '\u2560'   #  0x00cc -> BOX DRAWINGS DOUBLE VERTICAL AND RIGHT
    '\u2550'   #  0x00cd -> BOX DRAWINGS DOUBLE HORIZONTAL
    '\u256c'   #  0x00ce -> BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
    '\u03a3'   #  0x00cf -> GREEK CAPITAL LETTER SIGMA
    '\u03a4'   #  0x00d0 -> GREEK CAPITAL LETTER TAU
    '\u03a5'   #  0x00d1 -> GREEK CAPITAL LETTER UPSILON
    '\u03a6'   #  0x00d2 -> GREEK CAPITAL LETTER PHI
    '\u03a7'   #  0x00d3 -> GREEK CAPITAL LETTER CHI
    '\u03a8'   #  0x00d4 -> GREEK CAPITAL LETTER PSI
    '\u03a9'   #  0x00d5 -> GREEK CAPITAL LETTER OMEGA
    '\u03b1'   #  0x00d6 -> GREEK SMALL LETTER ALPHA
    '\u03b2'   #  0x00d7 -> GREEK SMALL LETTER BETA
    '\u03b3'   #  0x00d8 -> GREEK SMALL LETTER GAMMA
    '\u2518'   #  0x00d9 -> BOX DRAWINGS LIGHT UP AND LEFT
    '\u250c'   #  0x00da -> BOX DRAWINGS LIGHT DOWN AND RIGHT
    '\u2588'   #  0x00db -> FULL BLOCK
    '\u2584'   #  0x00dc -> LOWER HALF BLOCK
    '\u03b4'   #  0x00dd -> GREEK SMALL LETTER DELTA
    '\u03b5'   #  0x00de -> GREEK SMALL LETTER EPSILON
    '\u2580'   #  0x00df -> UPPER HALF BLOCK
    '\u03b6'   #  0x00e0 -> GREEK SMALL LETTER ZETA
    '\u03b7'   #  0x00e1 -> GREEK SMALL LETTER ETA
    '\u03b8'   #  0x00e2 -> GREEK SMALL LETTER THETA
    '\u03b9'   #  0x00e3 -> GREEK SMALL LETTER IOTA
    '\u03ba'   #  0x00e4 -> GREEK SMALL LETTER KAPPA
    '\u03bb'   #  0x00e5 -> GREEK SMALL LETTER LAMDA
    '\u03bc'   #  0x00e6 -> GREEK SMALL LETTER MU
    '\u03bd'   #  0x00e7 -> GREEK SMALL LETTER NU
    '\u03be'   #  0x00e8 -> GREEK SMALL LETTER XI
    '\u03bf'   #  0x00e9 -> GREEK SMALL LETTER OMICRON
    '\u03c0'   #  0x00ea -> GREEK SMALL LETTER PI
    '\u03c1'   #  0x00eb -> GREEK SMALL LETTER RHO
    '\u03c3'   #  0x00ec -> GREEK SMALL LETTER SIGMA
    '\u03c2'   #  0x00ed -> GREEK SMALL LETTER FINAL SIGMA
    '\u03c4'   #  0x00ee -> GREEK SMALL LETTER TAU
    '\u0384'   #  0x00ef -> GREEK TONOS
    '\xad'     #  0x00f0 -> SOFT HYPHEN
    '\xb1'     #  0x00f1 -> PLUS-MINUS SIGN
    '\u03c5'   #  0x00f2 -> GREEK SMALL LETTER UPSILON
    '\u03c6'   #  0x00f3 -> GREEK SMALL LETTER PHI
    '\u03c7'   #  0x00f4 -> GREEK SMALL LETTER CHI
    '\xa7'     #  0x00f5 -> SECTION SIGN
    '\u03c8'   #  0x00f6 -> GREEK SMALL LETTER PSI
    '\u0385'   #  0x00f7 -> GREEK DIALYTIKA TONOS
    '\xb0'     #  0x00f8 -> DEGREE SIGN
    '\xa8'     #  0x00f9 -> DIAERESIS
    '\u03c9'   #  0x00fa -> GREEK SMALL LETTER OMEGA
    '\u03cb'   #  0x00fb -> GREEK SMALL LETTER UPSILON WITH DIALYTIKA
    '\u03b0'   #  0x00fc -> GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
    '\u03ce'   #  0x00fd -> GREEK SMALL LETTER OMEGA WITH TONOS
    '\u25a0'   #  0x00fe -> BLACK SQUARE
    '\xa0'     #  0x00ff -> NO-BREAK SPACE
)

### Encoding Map

encoding_map = {
    0x0000: 0x0000,     #  NULL
    0x0001: 0x0001,     #  START OF HEADING
    0x0002: 0x0002,     #  START OF TEXT
    0x0003: 0x0003,     #  END OF TEXT
    0x0004: 0x0004,     #  END OF TRANSMISSION
    0x0005: 0x0005,     #  ENQUIRY
    0x0006: 0x0006,     #  ACKNOWLEDGE
    0x0007: 0x0007,     #  BELL
    0x0008: 0x0008,     #  BACKSPACE
    0x0009: 0x0009,     #  HORIZONTAL TABULATION
    0x000a: 0x000a,     #  LINE FEED
    0x000b: 0x000b,     #  VERTICAL TABULATION
    0x000c: 0x000c,     #  FORM FEED
    0x000d: 0x000d,     #  CARRIAGE RETURN
    0x000e: 0x000e,     #  SHIFT OUT
    0x000f: 0x000f,     #  SHIFT IN
    0x0010: 0x0010,     #  DATA LINK ESCAPE
    0x0011: 0x0011,     #  DEVICE CONTROL ONE
    0x0012: 0x0012,     #  DEVICE CONTROL TWO
    0x0013: 0x0013,     #  DEVICE CONTROL THREE
    0x0014: 0x0014,     #  DEVICE CONTROL FOUR
    0x0015: 0x0015,     #  NEGATIVE ACKNOWLEDGE
    0x0016: 0x0016,     #  SYNCHRONOUS IDLE
    0x0017: 0x0017,     #  END OF TRANSMISSION BLOCK
    0x0018: 0x0018,     #  CANCEL
    0x0019: 0x0019,     #  END OF MEDIUM
    0x001a: 0x001a,     #  SUBSTITUTE
    0x001b: 0x001b,     #  ESCAPE
    0x001c: 0x001c,     #  FILE SEPARATOR
    0x001d: 0x001d,     #  GROUP SEPARATOR
    0x001e: 0x001e,     #  RECORD SEPARATOR
    0x001f: 0x001f,     #  UNIT SEPARATOR
    0x0020: 0x0020,     #  SPACE
    0x0021: 0x0021,     #  EXCLAMATION MARK
    0x0022: 0x0022,     #  QUOTATION MARK
    0x0023: 0x0023,     #  NUMBER SIGN
    0x0024: 0x0024,     #  DOLLAR SIGN
    0x0025: 0x0025,     #  PERCENT SIGN
    0x0026: 0x0026,     #  AMPERSAND
    0x0027: 0x0027,     #  APOSTROPHE
    0x0028: 0x0028,     #  LEFT PARENTHESIS
    0x0029: 0x0029,     #  RIGHT PARENTHESIS
    0x002a: 0x002a,     #  ASTERISK
    0x002b: 0x002b,     #  PLUS SIGN
    0x002c: 0x002c,     #  COMMA
    0x002d: 0x002d,     #  HYPHEN-MINUS
    0x002e: 0x002e,     #  FULL STOP
    0x002f: 0x002f,     #  SOLIDUS
    0x0030: 0x0030,     #  DIGIT ZERO
    0x0031: 0x0031,     #  DIGIT ONE
    0x0032: 0x0032,     #  DIGIT TWO
    0x0033: 0x0033,     #  DIGIT THREE
    0x0034: 0x0034,     #  DIGIT FOUR
    0x0035: 0x0035,     #  DIGIT FIVE
    0x0036: 0x0036,     #  DIGIT SIX
    0x0037: 0x0037,     #  DIGIT SEVEN
    0x0038: 0x0038,     #  DIGIT EIGHT
    0x0039: 0x0039,     #  DIGIT NINE
    0x003a: 0x003a,     #  COLON
    0x003b: 0x003b,     #  SEMICOLON
    0x003c: 0x003c,     #  LESS-THAN SIGN
    0x003d: 0x003d,     #  EQUALS SIGN
    0x003e: 0x003e,     #  GREATER-THAN SIGN
    0x003f: 0x003f,     #  QUESTION MARK
    0x0040: 0x0040,     #  COMMERCIAL AT
    0x0041: 0x0041,     #  LATIN CAPITAL LETTER A
    0x0042: 0x0042,     #  LATIN CAPITAL LETTER B
    0x0043: 0x0043,     #  LATIN CAPITAL LETTER C
    0x0044: 0x0044,     #  LATIN CAPITAL LETTER D
    0x0045: 0x0045,     #  LATIN CAPITAL LETTER E
    0x0046: 0x0046,     #  LATIN CAPITAL LETTER F
    0x0047: 0x0047,     #  LATIN CAPITAL LETTER G
    0x0048: 0x0048,     #  LATIN CAPITAL LETTER H
    0x0049: 0x0049,     #  LATIN CAPITAL LETTER I
    0x004a: 0x004a,     #  LATIN CAPITAL LETTER J
    0x004b: 0x004b,     #  LATIN CAPITAL LETTER K
    0x004c: 0x004c,     #  LATIN CAPITAL LETTER L
    0x004d: 0x004d,     #  LATIN CAPITAL LETTER M
    0x004e: 0x004e,     #  LATIN CAPITAL LETTER N
    0x004f: 0x004f,     #  LATIN CAPITAL LETTER O
    0x0050: 0x0050,     #  LATIN CAPITAL LETTER P
    0x0051: 0x0051,     #  LATIN CAPITAL LETTER Q
    0x0052: 0x0052,     #  LATIN CAPITAL LETTER R
    0x0053: 0x0053,     #  LATIN CAPITAL LETTER S
    0x0054: 0x0054,     #  LATIN CAPITAL LETTER T
    0x0055: 0x0055,     #  LATIN CAPITAL LETTER U
    0x0056: 0x0056,     #  LATIN CAPITAL LETTER V
    0x0057: 0x0057,     #  LATIN CAPITAL LETTER W
    0x0058: 0x0058,     #  LATIN CAPITAL LETTER X
    0x0059: 0x0059,     #  LATIN CAPITAL LETTER Y
    0x005a: 0x005a,     #  LATIN CAPITAL LETTER Z
    0x005b: 0x005b,     #  LEFT SQUARE BRACKET
    0x005c: 0x005c,     #  REVERSE SOLIDUS
    0x005d: 0x005d,     #  RIGHT SQUARE BRACKET
    0x005e: 0x005e,     #  CIRCUMFLEX ACCENT
    0x005f: 0x005f,     #  LOW LINE
    0x0060: 0x0060,     #  GRAVE ACCENT
    0x0061: 0x0061,     #  LATIN SMALL LETTER A
    0x0062: 0x0062,     #  LATIN SMALL LETTER B
    0x0063: 0x0063,     #  LATIN SMALL LETTER C
    0x0064: 0x0064,     #  LATIN SMALL LETTER D
    0x0065: 0x0065,     #  LATIN SMALL LETTER E
    0x0066: 0x0066,     #  LATIN SMALL LETTER F
    0x0067: 0x0067,     #  LATIN SMALL LETTER G
    0x0068: 0x0068,     #  LATIN SMALL LETTER H
    0x0069: 0x0069,     #  LATIN SMALL LETTER I
    0x006a: 0x006a,     #  LATIN SMALL LETTER J
    0x006b: 0x006b,     #  LATIN SMALL LETTER K
    0x006c: 0x006c,     #  LATIN SMALL LETTER L
    0x006d: 0x006d,     #  LATIN SMALL LETTER M
    0x006e: 0x006e,     #  LATIN SMALL LETTER N
    0x006f: 0x006f,     #  LATIN SMALL LETTER O
    0x0070: 0x0070,     #  LATIN SMALL LETTER P
    0x0071: 0x0071,     #  LATIN SMALL LETTER Q
    0x0072: 0x0072,     #  LATIN SMALL LETTER R
    0x0073: 0x0073,     #  LATIN SMALL LETTER S
    0x0074: 0x0074,     #  LATIN SMALL LETTER T
    0x0075: 0x0075,     #  LATIN SMALL LETTER U
    0x0076: 0x0076,     #  LATIN SMALL LETTER V
    0x0077: 0x0077,     #  LATIN SMALL LETTER W
    0x0078: 0x0078,     #  LATIN SMALL LETTER X
    0x0079: 0x0079,     #  LATIN SMALL LETTER Y
    0x007a: 0x007a,     #  LATIN SMALL LETTER Z
    0x007b: 0x007b,     #  LEFT CURLY BRACKET
    0x007c: 0x007c,     #  VERTICAL LINE
    0x007d: 0x007d,     #  RIGHT CURLY BRACKET
    0x007e: 0x007e,     #  TILDE
    0x007f: 0x007f,     #  DELETE
    0x00a0: 0x00ff,     #  NO-BREAK SPACE
    0x00a3: 0x009c,     #  POUND SIGN
    0x00a6: 0x008a,     #  BROKEN BAR
    0x00a7: 0x00f5,     #  SECTION SIGN
    0x00a8: 0x00f9,     #  DIAERESIS
    0x00a9: 0x0097,     #  COPYRIGHT SIGN
    0x00ab: 0x00ae,     #  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00ac: 0x0089,     #  NOT SIGN
    0x00ad: 0x00f0,     #  SOFT HYPHEN
    0x00b0: 0x00f8,     #  DEGREE SIGN
    0x00b1: 0x00f1,     #  PLUS-MINUS SIGN
    0x00b2: 0x0099,     #  SUPERSCRIPT TWO
    0x00b3: 0x009a,     #  SUPERSCRIPT THREE
    0x00b7: 0x0088,     #  MIDDLE DOT
    0x00bb: 0x00af,     #  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00bd: 0x00ab,     #  VULGAR FRACTION ONE HALF
    0x0384: 0x00ef,     #  GREEK TONOS
    0x0385: 0x00f7,     #  GREEK DIALYTIKA TONOS
    0x0386: 0x0086,     #  GREEK CAPITAL LETTER ALPHA WITH TONOS
    0x0388: 0x008d,     #  GREEK CAPITAL LETTER EPSILON WITH TONOS
    0x0389: 0x008f,     #  GREEK CAPITAL LETTER ETA WITH TONOS
    0x038a: 0x0090,     #  GREEK CAPITAL LETTER IOTA WITH TONOS
    0x038c: 0x0092,     #  GREEK CAPITAL LETTER OMICRON WITH TONOS
    0x038e: 0x0095,     #  GREEK CAPITAL LETTER UPSILON WITH TONOS
    0x038f: 0x0098,     #  GREEK CAPITAL LETTER OMEGA WITH TONOS
    0x0390: 0x00a1,     #  GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
    0x0391: 0x00a4,     #  GREEK CAPITAL LETTER ALPHA
    0x0392: 0x00a5,     #  GREEK CAPITAL LETTER BETA
    0x0393: 0x00a6,     #  GREEK CAPITAL LETTER GAMMA
    0x0394: 0x00a7,     #  GREEK CAPITAL LETTER DELTA
    0x0395: 0x00a8,     #  GREEK CAPITAL LETTER EPSILON
    0x0396: 0x00a9,     #  GREEK CAPITAL LETTER ZETA
    0x0397: 0x00aa,     #  GREEK CAPITAL LETTER ETA
    0x0398: 0x00ac,     #  GREEK CAPITAL LETTER THETA
    0x0399: 0x00ad,     #  GREEK CAPITAL LETTER IOTA
    0x039a: 0x00b5,     #  GREEK CAPITAL LETTER KAPPA
    0x039b: 0x00b6,     #  GREEK CAPITAL LETTER LAMDA
    0x039c: 0x00b7,     #  GREEK CAPITAL LETTER MU
    0x039d: 0x00b8,     #  GREEK CAPITAL LETTER NU
    0x039e: 0x00bd,     #  GREEK CAPITAL LETTER XI
    0x039f: 0x00be,     #  GREEK CAPITAL LETTER OMICRON
    0x03a0: 0x00c6,     #  GREEK CAPITAL LETTER PI
    0x03a1: 0x00c7,     #  GREEK CAPITAL LETTER RHO
    0x03a3: 0x00cf,     #  GREEK CAPITAL LETTER SIGMA
    0x03a4: 0x00d0,     #  GREEK CAPITAL LETTER TAU
    0x03a5: 0x00d1,     #  GREEK CAPITAL LETTER UPSILON
    0x03a6: 0x00d2,     #  GREEK CAPITAL LETTER PHI
    0x03a7: 0x00d3,     #  GREEK CAPITAL LETTER CHI
    0x03a8: 0x00d4,     #  GREEK CAPITAL LETTER PSI
    0x03a9: 0x00d5,     #  GREEK CAPITAL LETTER OMEGA
    0x03aa: 0x0091,     #  GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
    0x03ab: 0x0096,     #  GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA
    0x03ac: 0x009b,     #  GREEK SMALL LETTER ALPHA WITH TONOS
    0x03ad: 0x009d,     #  GREEK SMALL LETTER EPSILON WITH TONOS
    0x03ae: 0x009e,     #  GREEK SMALL LETTER ETA WITH TONOS
    0x03af: 0x009f,     #  GREEK SMALL LETTER IOTA WITH TONOS
    0x03b0: 0x00fc,     #  GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
    0x03b1: 0x00d6,     #  GREEK SMALL LETTER ALPHA
    0x03b2: 0x00d7,     #  GREEK SMALL LETTER BETA
    0x03b3: 0x00d8,     #  GREEK SMALL LETTER GAMMA
    0x03b4: 0x00dd,     #  GREEK SMALL LETTER DELTA
    0x03b5: 0x00de,     #  GREEK SMALL LETTER EPSILON
    0x03b6: 0x00e0,     #  GREEK SMALL LETTER ZETA
    0x03b7: 0x00e1,     #  GREEK SMALL LETTER ETA
    0x03b8: 0x00e2,     #  GREEK SMALL LETTER THETA
    0x03b9: 0x00e3,     #  GREEK SMALL LETTER IOTA
    0x03ba: 0x00e4,     #  GREEK SMALL LETTER KAPPA
    0x03bb: 0x00e5,     #  GREEK SMALL LETTER LAMDA
    0x03bc: 0x00e6,     #  GREEK SMALL LETTER MU
    0x03bd: 0x00e7,     #  GREEK SMALL LETTER NU
    0x03be: 0x00e8,     #  GREEK SMALL LETTER XI
    0x03bf: 0x00e9,     #  GREEK SMALL LETTER OMICRON
    0x03c0: 0x00ea,     #  GREEK SMALL LETTER PI
    0x03c1: 0x00eb,     #  GREEK SMALL LETTER RHO
    0x03c2: 0x00ed,     #  GREEK SMALL LETTER FINAL SIGMA
    0x03c3: 0x00ec,     #  GREEK SMALL LETTER SIGMA
    0x03c4: 0x00ee,     #  GREEK SMALL LETTER TAU
    0x03c5: 0x00f2,     #  GREEK SMALL LETTER UPSILON
    0x03c6: 0x00f3,     #  GREEK SMALL LETTER PHI
    0x03c7: 0x00f4,     #  GREEK SMALL LETTER CHI
    0x03c8: 0x00f6,     #  GREEK SMALL LETTER PSI
    0x03c9: 0x00fa,     #  GREEK SMALL LETTER OMEGA
    0x03ca: 0x00a0,     #  GREEK SMALL LETTER IOTA WITH DIALYTIKA
    0x03cb: 0x00fb,     #  GREEK SMALL LETTER UPSILON WITH DIALYTIKA
    0x03cc: 0x00a2,     #  GREEK SMALL LETTER OMICRON WITH TONOS
    0x03cd: 0x00a3,     #  GREEK SMALL LETTER UPSILON WITH TONOS
    0x03ce: 0x00fd,     #  GREEK SMALL LETTER OMEGA WITH TONOS
    0x2015: 0x008e,     #  HORIZONTAL BAR
    0x2018: 0x008b,     #  LEFT SINGLE QUOTATION MARK
    0x2019: 0x008c,     #  RIGHT SINGLE QUOTATION MARK
    0x2500: 0x00c4,     #  BOX DRAWINGS LIGHT HORIZONTAL
    0x2502: 0x00b3,     #  BOX DRAWINGS LIGHT VERTICAL
    0x250c: 0x00da,     #  BOX DRAWINGS LIGHT DOWN AND RIGHT
    0x2510: 0x00bf,     #  BOX DRAWINGS LIGHT DOWN AND LEFT
    0x2514: 0x00c0,     #  BOX DRAWINGS LIGHT UP AND RIGHT
    0x2518: 0x00d9,     #  BOX DRAWINGS LIGHT UP AND LEFT
    0x251c: 0x00c3,     #  BOX DRAWINGS LIGHT VERTICAL AND RIGHT
    0x2524: 0x00b4,     #  BOX DRAWINGS LIGHT VERTICAL AND LEFT
    0x252c: 0x00c2,     #  BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
    0x2534: 0x00c1,     #  BOX DRAWINGS LIGHT UP AND HORIZONTAL
    0x253c: 0x00c5,     #  BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
    0x2550: 0x00cd,     #  BOX DRAWINGS DOUBLE HORIZONTAL
    0x2551: 0x00ba,     #  BOX DRAWINGS DOUBLE VERTICAL
    0x2554: 0x00c9,     #  BOX DRAWINGS DOUBLE DOWN AND RIGHT
    0x2557: 0x00bb,     #  BOX DRAWINGS DOUBLE DOWN AND LEFT
    0x255a: 0x00c8,     #  BOX DRAWINGS DOUBLE UP AND RIGHT
    0x255d: 0x00bc,     #  BOX DRAWINGS DOUBLE UP AND LEFT
    0x2560: 0x00cc,     #  BOX DRAWINGS DOUBLE VERTICAL AND RIGHT
    0x2563: 0x00b9,     #  BOX DRAWINGS DOUBLE VERTICAL AND LEFT
    0x2566: 0x00cb,     #  BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
    0x2569: 0x00ca,     #  BOX DRAWINGS DOUBLE UP AND HORIZONTAL
    0x256c: 0x00ce,     #  BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
    0x2580: 0x00df,     #  UPPER HALF BLOCK
    0x2584: 0x00dc,     #  LOWER HALF BLOCK
    0x2588: 0x00db,     #  FULL BLOCK
    0x2591: 0x00b0,     #  LIGHT SHADE
    0x2592: 0x00b1,     #  MEDIUM SHADE
    0x2593: 0x00b2,     #  DARK SHADE
    0x25a0: 0x00fe,     #  BLACK SQUARE
}
