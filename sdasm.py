"""
ToDo:
    * allow strings in instructions:
        lda "A"-$4b
    * create large test .asm
    * text mapping
    * option to automatically localize labels in macros
"""


import math, os, sys
from . import include
Cfg = include.Cfg
import time
from datetime import datetime

import pathlib
import operator

#try: import numpy as np
#except: np = False

# need better code for slicing with numpy.
# just disable for now.
np = False

def inScriptFolder(f):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),f)



operations = {
#    '-':operator.sub,
#    '+':operator.add,
    '/':operator.truediv,
    '&':operator.and_,
    '^':operator.xor,
    '~':operator.invert,
    '|':operator.or_,
    '**':operator.pow,
    '<<':operator.lshift,
    '>>':operator.rshift,
    '%':operator.mod,
    '*':operator.mul,
}


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


#directives = [
#    'if', 'elseif', 'else', 'endif', 'ifdef', 'ifndef', 'equ', 'org', 'base', 'pad',
#    'include', 'incsrc', 'incbin', 'bin', 'hex', 'word', 'dw', 'dcw', 'dc.w', 'byte',
#    'db', 'dcb', 'dc.b', 'dsw', 'ds.w', 'dsb', 'ds.b', 'align', 'macro', 'rept',
#    'endm', 'endr', 'enum', 'ende', 'ignorenl', 'endinl', 'fillvalue', 'dl', 'dh',
#    'error', 'inesprg', 'ineschr', 'inesmir', 'inesmap', 'nes2chrram', 'nes2prgram',
#    'nes2sub', 'nes2tv', 'nes2vs', 'nes2bram', 'nes2chrbram', 'unstable', 'hunstable'
#]

directives = [
    'org','base','pad','align',
    'include','incsrc','includeall','incbin','bin',
    'db','dw','byte','byt','word','hex',
    'enum','ende','endenum','fillvalue',
    'print','warning','error',
    'setincludefolder',
    'macro','endm','endmacro',
    'if','ifdef','ifndef','else','elseif','endif','iffileexist','iffile',
    'arch',
]

directives = directives + [
'index','mem','bank','banksize','header','define',
]

asm=[
Map(opcode = 'adc', mode = 'Immediate', byte = 105, length = 2),
Map(opcode = 'adc', mode = 'Zero Page', byte = 101, length = 2),
Map(opcode = 'adc', mode = 'Zero Page, X', byte = 117, length = 2),
Map(opcode = 'adc', mode = 'Absolute', byte = 109, length = 3),
Map(opcode = 'adc', mode = 'Absolute, X', byte = 125, length = 3),
Map(opcode = 'adc', mode = 'Absolute, Y', byte = 121, length = 3),
Map(opcode = 'adc', mode = '(Indirect, X)', byte = 97, length = 2),
Map(opcode = 'adc', mode = '(Indirect), Y', byte = 113, length = 2),
Map(opcode = 'and', mode = 'Immediate', byte = 41, length = 2),
Map(opcode = 'and', mode = 'Zero Page', byte = 37, length = 2),
Map(opcode = 'and', mode = 'Zero Page, X', byte = 53, length = 2),
Map(opcode = 'and', mode = 'Absolute', byte = 45, length = 3),
Map(opcode = 'and', mode = 'Absolute, X', byte = 61, length = 3),
Map(opcode = 'and', mode = 'Absolute, Y', byte = 57, length = 3),
Map(opcode = 'and', mode = '(Indirect, X)', byte = 33, length = 2),
Map(opcode = 'and', mode = '(Indirect), Y', byte = 49, length = 2),
Map(opcode = 'asl', mode = 'Accumulator', byte = 10, length = 1),
Map(opcode = 'asl', mode = 'Zero Page', byte = 6, length = 2),
Map(opcode = 'asl', mode = 'Zero Page, X', byte = 22, length = 2),
Map(opcode = 'asl', mode = 'Absolute', byte = 14, length = 3),
Map(opcode = 'asl', mode = 'Absolute, X', byte = 30, length = 3),
Map(opcode = 'bcc', mode = 'Relative', byte = 144, length = 2),
Map(opcode = 'bcs', mode = 'Relative', byte = 176, length = 2),
Map(opcode = 'beq', mode = 'Relative', byte = 240, length = 2),
Map(opcode = 'bit', mode = 'Zero Page', byte = 36, length = 2),
Map(opcode = 'bit', mode = 'Absolute', byte = 44, length = 3),
Map(opcode = 'bmi', mode = 'Relative', byte = 48, length = 2),
Map(opcode = 'bne', mode = 'Relative', byte = 208, length = 2),
Map(opcode = 'bpl', mode = 'Relative', byte = 16, length = 2),
Map(opcode = 'brk', mode = 'Implied', byte = 0, length = 1),
Map(opcode = 'bvc', mode = 'Relative', byte = 80, length = 2),
Map(opcode = 'bvs', mode = 'Relative', byte = 112, length = 2),
Map(opcode = 'clc', mode = 'Implied', byte = 24, length = 1),
Map(opcode = 'cld', mode = 'Implied', byte = 216, length = 1),
Map(opcode = 'cli', mode = 'Implied', byte = 88, length = 1),
Map(opcode = 'clv', mode = 'Implied', byte = 184, length = 1),
Map(opcode = 'cmp', mode = 'Immediate', byte = 201, length = 2),
Map(opcode = 'cmp', mode = 'Zero Page', byte = 197, length = 2),
Map(opcode = 'cmp', mode = 'Zero Page, X', byte = 213, length = 2),
Map(opcode = 'cmp', mode = 'Absolute', byte = 205, length = 3),
Map(opcode = 'cmp', mode = 'Absolute, X', byte = 221, length = 3),
Map(opcode = 'cmp', mode = 'Absolute, Y', byte = 217, length = 3),
Map(opcode = 'cmp', mode = '(Indirect, X)', byte = 193, length = 2),
Map(opcode = 'cmp', mode = '(Indirect), Y', byte = 209, length = 2),
Map(opcode = 'cpx', mode = 'Immediate', byte = 224, length = 2),
Map(opcode = 'cpx', mode = 'Zero Page', byte = 228, length = 2),
Map(opcode = 'cpx', mode = 'Absolute', byte = 236, length = 3),
Map(opcode = 'cpy', mode = 'Immediate', byte = 192, length = 2),
Map(opcode = 'cpy', mode = 'Zero Page', byte = 196, length = 2),
Map(opcode = 'cpy', mode = 'Absolute', byte = 204, length = 3),
Map(opcode = 'dec', mode = 'Zero Page', byte = 198, length = 2),
Map(opcode = 'dec', mode = 'Zero Page, X', byte = 214, length = 2),
Map(opcode = 'dec', mode = 'Absolute', byte = 206, length = 3),
Map(opcode = 'dec', mode = 'Absolute, X', byte = 222, length = 3),
Map(opcode = 'dex', mode = 'Implied', byte = 202, length = 1),
Map(opcode = 'dey', mode = 'Implied', byte = 136, length = 1),
Map(opcode = 'eor', mode = 'Immediate', byte = 73, length = 2),
Map(opcode = 'eor', mode = 'Zero Page', byte = 69, length = 2),
Map(opcode = 'eor', mode = 'Zero Page, X', byte = 85, length = 2),
Map(opcode = 'eor', mode = 'Absolute', byte = 77, length = 3),
Map(opcode = 'eor', mode = 'Absolute, X', byte = 93, length = 3),
Map(opcode = 'eor', mode = 'Absolute, Y', byte = 89, length = 3),
Map(opcode = 'eor', mode = '(Indirect, X)', byte = 65, length = 2),
Map(opcode = 'eor', mode = '(Indirect), Y', byte = 81, length = 2),
Map(opcode = 'inc', mode = 'Zero Page', byte = 230, length = 2),
Map(opcode = 'inc', mode = 'Zero Page, X', byte = 246, length = 2),
Map(opcode = 'inc', mode = 'Absolute', byte = 238, length = 3),
Map(opcode = 'inc', mode = 'Absolute, X', byte = 254, length = 3),
Map(opcode = 'inx', mode = 'Implied', byte = 232, length = 1),
Map(opcode = 'iny', mode = 'Implied', byte = 200, length = 1),
Map(opcode = 'jmp', mode = 'Indirect', byte = 108, length = 3),
Map(opcode = 'jmp', mode = 'Absolute', byte = 76, length = 3),
Map(opcode = 'jsr', mode = 'Absolute', byte = 32, length = 3),
Map(opcode = 'lda', mode = 'Immediate', byte = 169, length = 2),
Map(opcode = 'lda', mode = 'Zero Page', byte = 165, length = 2),
Map(opcode = 'lda', mode = 'Zero Page, X', byte = 181, length = 2),
Map(opcode = 'lda', mode = 'Absolute', byte = 173, length = 3),
Map(opcode = 'lda', mode = 'Absolute, X', byte = 189, length = 3),
Map(opcode = 'lda', mode = 'Absolute, Y', byte = 185, length = 3),
Map(opcode = 'lda', mode = '(Indirect, X)', byte = 161, length = 2),
Map(opcode = 'lda', mode = '(Indirect), Y', byte = 177, length = 2),
Map(opcode = 'ldx', mode = 'Zero Page', byte = 166, length = 2),
Map(opcode = 'ldx', mode = 'Zero Page, Y', byte = 182, length = 2),
Map(opcode = 'ldx', mode = 'Absolute', byte = 174, length = 3),
Map(opcode = 'ldx', mode = 'Absolute, Y', byte = 190, length = 3),
Map(opcode = 'ldx', mode = 'Immediate', byte = 162, length = 2),
Map(opcode = 'ldy', mode = 'Immediate', byte = 160, length = 2),
Map(opcode = 'ldy', mode = 'Zero Page', byte = 164, length = 2),
Map(opcode = 'ldy', mode = 'Zero Page, X', byte = 180, length = 2),
Map(opcode = 'ldy', mode = 'Absolute', byte = 172, length = 3),
Map(opcode = 'ldy', mode = 'Absolute, X', byte = 188, length = 3),
Map(opcode = 'lsr', mode = 'Accumulator', byte = 74, length = 1),
Map(opcode = 'lsr', mode = 'Zero Page', byte = 70, length = 2),
Map(opcode = 'lsr', mode = 'Zero Page, X', byte = 86, length = 2),
Map(opcode = 'lsr', mode = 'Absolute', byte = 78, length = 3),
Map(opcode = 'lsr', mode = 'Absolute, X', byte = 94, length = 3),
Map(opcode = 'nop', mode = 'Implied', byte = 234, length = 1),
Map(opcode = 'ora', mode = 'Immediate', byte = 9, length = 2),
Map(opcode = 'ora', mode = 'Zero Page', byte = 5, length = 2),
Map(opcode = 'ora', mode = 'Zero Page, X', byte = 21, length = 2),
Map(opcode = 'ora', mode = 'Absolute', byte = 13, length = 3),
Map(opcode = 'ora', mode = 'Absolute, X', byte = 29, length = 3),
Map(opcode = 'ora', mode = 'Absolute, Y', byte = 25, length = 3),
Map(opcode = 'ora', mode = '(Indirect, X)', byte = 1, length = 2),
Map(opcode = 'ora', mode = '(Indirect), Y', byte = 17, length = 2),
Map(opcode = 'pha', mode = 'Implied', byte = 72, length = 1),
Map(opcode = 'php', mode = 'Implied', byte = 8, length = 1),
Map(opcode = 'pla', mode = 'Implied', byte = 104, length = 1),
Map(opcode = 'plp', mode = 'Implied', byte = 40, length = 1),
Map(opcode = 'rol', mode = 'Accumulator', byte = 42, length = 1),
Map(opcode = 'rol', mode = 'Zero Page', byte = 38, length = 2),
Map(opcode = 'rol', mode = 'Zero Page, X', byte = 54, length = 2),
Map(opcode = 'rol', mode = 'Absolute', byte = 46, length = 3),
Map(opcode = 'rol', mode = 'Absolute, X', byte = 62, length = 3),
Map(opcode = 'ror', mode = 'Accumulator', byte = 106, length = 1),
Map(opcode = 'ror', mode = 'Zero Page', byte = 102, length = 2),
Map(opcode = 'ror', mode = 'Zero Page, X', byte = 118, length = 2),
Map(opcode = 'ror', mode = 'Absolute', byte = 110, length = 3),
Map(opcode = 'ror', mode = 'Absolute, X', byte = 126, length = 3),
Map(opcode = 'rti', mode = 'Implied', byte = 64, length = 1),
Map(opcode = 'rts', mode = 'Implied', byte = 96, length = 1),
Map(opcode = 'sbc', mode = 'Immediate', byte = 233, length = 2),
Map(opcode = 'sbc', mode = 'Zero Page', byte = 229, length = 2),
Map(opcode = 'sbc', mode = 'Zero Page, X', byte = 245, length = 2),
Map(opcode = 'sbc', mode = 'Absolute', byte = 237, length = 3),
Map(opcode = 'sbc', mode = 'Absolute, X', byte = 253, length = 3),
Map(opcode = 'sbc', mode = 'Absolute, Y', byte = 249, length = 3),
Map(opcode = 'sbc', mode = '(Indirect, X)', byte = 225, length = 2),
Map(opcode = 'sbc', mode = '(Indirect), Y', byte = 241, length = 2),
Map(opcode = 'sec', mode = 'Implied', byte = 56, length = 1),
Map(opcode = 'sed', mode = 'Implied', byte = 248, length = 1),
Map(opcode = 'sei', mode = 'Implied', byte = 120, length = 1),
Map(opcode = 'sta', mode = 'Zero Page', byte = 133, length = 2),
Map(opcode = 'sta', mode = 'Zero Page, X', byte = 149, length = 2),
Map(opcode = 'sta', mode = 'Absolute', byte = 141, length = 3),
Map(opcode = 'sta', mode = 'Absolute, X', byte = 157, length = 3),
Map(opcode = 'sta', mode = 'Absolute, Y', byte = 153, length = 3),
Map(opcode = 'sta', mode = '(Indirect, X)', byte = 129, length = 2),
Map(opcode = 'sta', mode = '(Indirect), Y', byte = 145, length = 2),
Map(opcode = 'stx', mode = 'Zero Page', byte = 134, length = 2),
Map(opcode = 'stx', mode = 'Zero Page, Y', byte = 150, length = 2),
Map(opcode = 'stx', mode = 'Absolute', byte = 142, length = 3),
Map(opcode = 'sty', mode = 'Zero Page', byte = 132, length = 2),
Map(opcode = 'sty', mode = 'Zero Page, X', byte = 148, length = 2),
Map(opcode = 'sty', mode = 'Absolute', byte = 140, length = 3),
Map(opcode = 'tax', mode = 'Implied', byte = 170, length = 1),
Map(opcode = 'tay', mode = 'Implied', byte = 168, length = 1),
Map(opcode = 'tsx', mode = 'Implied', byte = 186, length = 1),
Map(opcode = 'txa', mode = 'Implied', byte = 138, length = 1),
Map(opcode = 'txs', mode = 'Implied', byte = 154, length = 1),
Map(opcode = 'tya', mode = 'Implied', byte = 152, length = 1),
]

# Converting to dictionary removes duplicates
opcodes = list(dict.fromkeys([x.opcode for x in asm]))

implied = [x.opcode for x in asm if x.mode=='Implied']
accumulator = [x.opcode for x in asm if x.mode=="Accumulator"]
ifDirectives = ['if','endif','else','elseif','ifdef','ifndef','iffileexist','iffile']

mergeList = lambda a,b: [(a[i], b[i]) for i in range(0, len(a))]
makeHex = lambda x: '$'+x.to_bytes(((x.bit_length()|1  + 7) // 8),"big").hex()

specialSymbols = ['sdasm','bank']
timeSymbols = ['year','month','day','hour','minute','second']

specialSymbols+= timeSymbols

def assemble(filename, outputFilename = 'output.bin', listFilename = 'output.txt', configFile=False):
    if not configFile:
        configFile = inScriptFolder('config.ini')
    
    cfg = False
#    try:
    # create our config parser
    cfg = Cfg(configFile)

    # read config file if it exists
    cfg.load()

    # number of bytes to show when generating list
    cfg.setDefault('main', 'list_nBytes', 8)
    cfg.setDefault('main', 'comment', ';,//')
    cfg.setDefault('main', 'commentBlockOpen', '/*')
    cfg.setDefault('main', 'commentBlockClose', '*/')
    cfg.setDefault('main', 'nestedComments', True)
    cfg.setDefault('main', 'fillValue', '$00')
    cfg.setDefault('main', 'localPrefix', '@')
    cfg.setDefault('main', 'debug', False)
    cfg.setDefault('main', 'varOpen', '{')
    cfg.setDefault('main', 'varClose', '}')
    cfg.setDefault('main', 'labelSuffix', ':')

    # save configuration so our defaults can be changed
    cfg.save()

    _assemble(filename, outputFilename, listFilename, cfg=cfg)
#    except:
#        print("sdasm Error")
#        return False
#    return True

def _assemble(filename, outputFilename, listFilename, cfg):
    def getSpecial(s):
        if s == 'sdasm':
            v = 1
        elif s == 'bank':
            if bank == None:
                return ''
            else:
                #print(makeHex(bank))
                return makeHex(bank)
        elif s in timeSymbols:
            v = list(datetime.now().timetuple())[timeSymbols.index(s)]
        if type(v) in (int,float):
            return makeHex(v)
        else:
            return v
    def findFile(filename):
        
        # Search for files in this order:
        #   Exact match
        #   Relative to current script folder
        #   Relative to initial script folder
        #   Relative to current working folder
        #   Relative to top level of initial script folder
        #   Relative to executable folder
        files = [
            filename,
            os.path.join(currentFolder,filename),
            os.path.join(initialFolder,filename),
            os.path.join(os.getcwd(),filename),
            os.path.join(str(pathlib.Path(*pathlib.Path(initialFolder).parts[:1])),filename),
            os.path.join(os.path.dirname(os.path.realpath(__file__)),filename),
        ]
        
        for f in files:
            if os.path.isfile(f): return f
        
        return False
    
    def makeList(item):
        if type(item)!=list:
            return [item]
        else:
            return item
    
    def isImmediate(v):
        if v.startswith("#"):
            return True
        else:
            return False

    def isNumber(v):
        return all([x in "0123456789" for x in str(v)])

    def getValueAndLength(v):
        v = v.strip()
        l = False
        
        v=v.replace(", ",",").replace(" ,",",")
        if v.startswith("(") and v.endswith(")"):
            v = v[1:-1]
        if v.endswith(",x"):
            v = v.split(",x")[0]
        if v.endswith(",y"):
            v = v.split(",y")[0]
        if v.startswith("(") and v.endswith(")"):
            v = v[1:-1]
        
        if v=='':
            return 0,0
        
        if v.startswith('-'):
            label = v.split(' ',1)[0]
            if len(aLabels) > 0:
                return [x[1] for x in aLabels if x[0]==label and x[1]<addr][-1], 2
            else:
                # negative number?
                return -1, 0
        if v.startswith('+'):
            label = v.split(' ',1)[0]
            try:
                return [x[1] for x in aLabels if x[0]==label and x[1]>=addr][0], 2
            except:
                return 0,0
        
        if v.startswith('"') and v.endswith('"'):
            v = list(bytes(v[1:-1], 'utf-8'))
            l=len(v)
            return v, l
        # ToDo: tokenize, allow (), implement proper order of operations.
        if '+' in v:
            v = v.split('+')
            left, right = getValue(v[0]), getValue(v[1])
            if type(left)==type(right):
                v = left + right
            elif type(left)==list:
                v = [x+right for x in left]
                return v,len(v)
            else:
                return 0, 1
            l = 1 if v <=256 else 2
            return v,l
        if '-' in v:
            v = v.split('-')
            left, right = getValue(v[0]), getValue(v[1])
            if type(left)==type(right):
                v = left - right
            elif type(left)==list:
                v = [x-right for x in left]
                return v,len(v)
            else:
                return 0, 1
            l = 1 if v <=256 else 2
            return v,l
        
        if v.startswith("<"):
            v = getValue(v[1:]) % 0x100
            l = 1
            return v,l
        if v.startswith(">"):
            v = getValue(v[1:]) >> 8
            l = 1
            return v,l
        
        if v == '$' or v.lower() == 'pc':
            v = addr
            l = 1 if v <=256 else 2
            l=2
        elif v.startswith("$"):
            l = 1 if len(v)-1<=2 else 2
            v = int(v[1:],16)
        elif v.startswith("%"):
            l = 1
            v = int(v[1:],2)
        elif any(x in v for x in operations):
            for op in operations:
                if op in v:
                    v = v.split(op)
                    v = operations[op](getValue(v[0]), getValue(v[1]))
                    l = 1 if v <=256 else 2
                    return v,l
        elif isNumber(v):
            l = 1 if int(v,10) <=256 else 2
            v = int(v,10)
        elif v.lower() in symbols:
            v, l = getValueAndLength(symbols[v.lower()])
        elif v.lower() in specialSymbols:
            v, l = getValueAndLength(getSpecial(v.lower()))
        else:
            v = 0
            l = -1
        return v, l

    def getValue(v):
        return getValueAndLength(v)[0]
    def getLength(v):
        return getValueAndLength(v)[1]

    def getOpWithMode(opcode,mode):
        ops = [x for x in asm if x.opcode==opcode]
        if mode in [x.mode for x in ops]:
            return [x for x in ops if x.mode==mode][0]
        else:
            return False

    commentSep = makeList(cfg.getValue('main', 'comment'))
    commentBlockOpen = makeList(cfg.getValue('main', 'commentBlockOpen'))
    commentBlockClose = makeList(cfg.getValue('main', 'commentBlockClose'))
    fillValue = getValue(cfg.getValue('main', 'fillValue'))
    localPrefix = makeList(cfg.getValue('main', 'localPrefix'))
    debug = cfg.isTrue(cfg.getValue('main', 'debug'))
    varOpen = makeList(cfg.getValue('main', 'varOpen'))
    varClose = makeList(cfg.getValue('main', 'varClose'))
    varOpenClose = mergeList(varOpen,varClose)
    labelSuffix = makeList(cfg.getValue('main', 'labelSuffix'))
    
    try:
        file = open(filename, "r")
    except:
        print("Error: could not open file.")
        exit()

    initialFolder = os.path.split(filename)[0]

    # Doing it this way removes the line endings
    lines = file.read().splitlines()
    originalLines = lines

    symbols = Map()
    equ = Map()
    aLabels = []
    lLabels = []
    macros = Map()
    blockComment = 0
    
    if debug and (not np):
        print('no numpy')
    
    for passNum in (1,2):
        lines = originalLines
        addr = 0
        oldAddr = 0
        
        noOutput = False
        
        macro = False
        currentAddress = addr
        mode = ""
        showAddress = False
        out = []
        
        if np:
            out = np.array([],dtype="B")
        
        outputText = ''
        startAddress = False
        currentFolder = ''
        currentFolder = os.path.split(filename)[0]
        currentFolder = initialFolder
        ifLevel = 0
        ifData = Map()
        arch = 'nes.cpu'
        headerSize = 0
        bankSize = 0x10000
        bank = None
        
        print('pass {}...'.format(passNum))
        
        for i in range(10000000):
            if i>len(lines)-1:
                break
            line = lines[i]
            
            hide = False
            
            currentAddress = addr
            originalLine = line
            errorText = False
            
            #print(originalLine)
            
            # change tabs to spaces
            line = line.replace("\t"," ")
            
            # "EQU" replacement
            for item in equ:
                line = line.replace(item, equ[item])
            
            # {var} replacement
            for o,c in varOpenClose:
                if o in line and c in line:
                    for item in symbols:
                        #line = line.replace(o+item+c, symbols[item])
                        while o+item+c in line.lower():
                            line = line.replace(line[line.find('{'):line.find('}')+1], symbols[item])
                        
                    for item in specialSymbols:
                        if o+item+c in line:
                            s = getSpecial(item)
                            line = line.replace(o+item+c, s)
            
            # remove single line comments
            for sep in commentSep:
                line = line.strip().split(sep,1)[0].strip()
            
            # remove comment blocks
            for sep in commentBlockOpen:
                if sep in line:
                    line = line.strip().split(sep,1)[0].strip()
                    blockComment+=1
            for sep in commentBlockClose:
                if sep in line:
                    line = line.strip().split(sep,1)[1].strip()
                    blockComment-=1
                    if cfg.isFalse(cfg.getValue('main', 'nestedComments')):
                        blockComment = 0
            if blockComment>0:
                line = ''
            
            if ifLevel:
                if ifData[ifLevel].bool == False:
                    
                    if line.split(" ",1)[0].strip().lower() not in ifDirectives:
                        ifData.line = line
                        line = ''
            
            if macro:
                if line.split(" ",1)[0].strip().lower() not in ['endm','endmacro']:
                    macros[macro].lines.append(originalLine)
                    line = ''
            
            b=[]
            k = line.split(" ",1)[0].strip().lower()
            
            if k!='' and (k=="-"*len(k) or k=="+"*len(k)):
                if not [k,addr] in aLabels:
                    aLabels.append([k, addr])
                    
                    # update so rest of line can be processed
                    line = (line.split(" ",1)+[''])[1].strip()
                    k = line.split(" ",1)[0].strip().lower()
            
            # This is really complicated but we have to check to see
            # if this is a label without a suffix somehow.
            if k!='' and not (k.startswith('.') and k[1:] in directives) and not k.endswith(tuple(labelSuffix)) and ' equ ' not in line.lower() and '=' not in line and k not in list(directives)+list(macros)+list(opcodes):
                if debug: print('label without suffix: {}'.format(k))
                k=k+labelSuffix[0]
            if k.endswith(tuple(labelSuffix)):
                symbols[k[:-1].lower()] = str(addr)
                
                # remove all local labels
                if not k.startswith(tuple(localPrefix)):
                    symbols = {k:v for (k,v) in symbols.items() if not k.startswith(tuple(localPrefix))}
                
                # update so rest of line can be processed
                line = (line.split(" ",1)+[''])[1].strip()
                k = line.split(" ",1)[0].strip().lower()
            
            # prefix is optional for valid directives
            if k.startswith(".") and k[1:] in directives:
                k=k[1:]
            
            if k == 'ifdef':
                ifLevel+=1
                ifData[ifLevel] = Map()
                
                data = line.split(" ",1)[1].strip().replace('==','=').lower()
                if data in symbols:
                    ifData[ifLevel].bool = True
                    ifData[ifLevel].done = True
                else:
                    ifData[ifLevel].bool = False
            elif k == 'ifndef':
                ifLevel+=1
                ifData[ifLevel] = Map()
                
                data = line.split(" ",1)[1].strip().replace('==','=').lower()
                
                if data in symbols:
                    ifData[ifLevel].bool = False
                else:
                    ifData[ifLevel].bool = True
                    ifData[ifLevel].done = True
            elif k == 'elseif':
                if ifData[ifLevel].done:
                    ifData[ifLevel].bool=False
                else:
                    k = 'if'
            elif k == 'iffileexist' or k == 'iffile':
                ifLevel+=1
                ifData[ifLevel] = Map()
                
                data = line.split(" ",1)[1].strip()
                if findFile(data):
                    ifData[ifLevel].bool = True
                    ifData[ifLevel].done = True
                else:
                    ifData[ifLevel].bool = False
            if k == 'if':
                ifLevel+=1
                ifData[ifLevel] = Map()
                
                data = line.split(" ",1)[1].strip().replace('==','=')
                
                if '=' in data:
                    l,r = data.split('=')
                    if getValue(l) == getValue(r):
                        ifData[ifLevel].bool = True
                        ifData[ifLevel].done = True
                    else:
                        ifData[ifLevel].bool = False
                else:
                    if getValue(data):
                        ifData[ifLevel].bool = True
                        ifData[ifLevel].done = True
                    else:
                        ifData[ifLevel].bool = False
            if k == 'else':
                ifData[ifLevel].bool = not ifData[ifLevel].done
            elif k == 'endif':
                ifLevel-=1
            elif k == 'arch':
                arch = line.split(" ")[1].strip().lower()
                if debug:
                    print('  Architecture: {}'.format(arch))
            elif k == 'header':
                headerSize = 16
            elif k == 'banksize':
                bankSize = getValue(line.split(" ")[1].strip())
            elif k == 'bank':
                bank = getValue(line.split(" ")[1].strip())
#                if debug:
#                    print('  Bank: {}'.format(bank))
            
            # hidden internally used directive used with include paths
            if k == "setincludefolder":
                currentFolder = (line.split(" ",1)+[''])[1].strip()
                hide = True
            
            elif k == "incbin" or k == "bin":
                filename = line.split(" ",1)[1].strip()
                filename = findFile(filename)
                
                try:
                    with open(filename, 'rb') as file:
                        b = list(file.read())
                except:
                    print("Could not open file.")
                lines = lines[:i]+['']+['setincludefolder '+currentFolder]+lines[i+1:]
            elif k == "include" or k=="incsrc":
                filename = line.split(" ",1)[1].strip()
                filename = findFile(filename)
                
                try:
                    with open(filename, 'r') as file:
                        newLines = file.read().splitlines()
                except:
                    print("Could not open file.")
                folder = os.path.split(filename)[0]
                
                newLines = ['setincludefolder '+folder]+newLines+['setincludefolder '+currentFolder]
                currentFolder = folder
                
                lines = lines[:i]+['']+newLines+lines[i+1:]
            elif k == 'includeall':
                folder = line.split(" ",1)[1].strip()
                files = [x for x in os.listdir(folder) if os.path.splitext(x.lower())[1] in ['.asm']]
                files = [x for x in files if not x.startswith('_')]
                lines = lines[:i]+['']+['include {}/{}'.format(folder, x) for x in files]+lines[i+1:]
            
            elif k == 'print' and passNum==2:
                v = line.split(" ",1)[1].strip()
                print(v)
            elif k == 'warning' and passNum==2:
                v = line.split(" ",1)[1].strip()
                print('warning: ' + v)
            elif k == 'error' and passNum==2:
                v = line.split(" ",1)[1].strip()
                print('Error: ' + v)
                exit()
            
            elif k == 'macro':
                v = line.split(" ")[1].strip()
                macro = v.lower()
                macros[macro]=Map()
                macros[macro].params = (line.split(" ", 2)+[''])[2].replace(',',' ').split()
                macros[macro].lines = []
                noOutput = True
            elif k == 'endm' or k == 'endmacro':
                macro = False
                noOutput = False
            
            if k in macros:
                params = line.split(" ",1)[1].replace(',',' ').split()
                
#                print(macros[k].params)
#                print(params)
                
                for item in mergeList(macros[k].params, params):
                    symbols[item[0].lower()] = item[1]
#                    print(item[0],'=',item[1])
                
#                for l in macros[k]['lines']:
#                    print(l)
                
                lines = lines[:i]+['']+macros[k].lines+lines[i+1:]
                
            if k == 'enum':
                oldAddr = addr
                addr = getValue(v)
                currentAddress = addr
                noOutput = True
            elif k == 'ende' or k == 'endenum':
                addr = oldAddr
                currentAddress = addr
                noOutput = False
            
            elif k == 'base':
                addr = getValue(line.split(' ',1)[1])
                if startAddress == False:
                    startAddress = addr
                currentAddress = addr
            
            elif k == 'org':
                if startAddress==False:
                    addr = getValue(line.split(' ',1)[1])
                    currentAddress = addr
                    startAddress = addr
                else:
                    k = 'pad'
            
            if k == "pad":
                data = line.split(' ',1)[1]
                
                fv = fillValue
                if ',' in data:
                    fv = getValue(data.split(',')[1])
                a = getValue(data.split(',')[0])
                
                b = b + ([fv] * (a-currentAddress))
            elif k == "align":
                data = line.split(' ',1)[1]
                
                fv = fillValue
                if ',' in data:
                    fv = getValue(data.split(',')[1])
                a = getValue(data.split(',')[0])
                
                b = b + ([fv] * ((a-currentAddress%a)%a))
                
            elif k == "hex":
                data = line.split(' ',1)[1]
                b = b + list(bytes.fromhex(''.join(['0'*(len(x)%2) + x for x in data.split()])))
                
            elif k == "db" or k=="byte" or k == 'byt':
                values = line.split(' ',1)[1].split(",")
                values = [x.strip() for x in values]
                
                for v in [getValue(x) for x in values]:
                    b = b + makeList(v)
                
            elif k == "dw" or k=="word" or k=='dbyt':
                values = line.split(' ',1)[1].split(",")
                values = [x.strip() for x in values]
                values = [getValue(x) for x in values]
                
                for value in values:
                    b = b + [value % 0x100, value>>8]
                
            elif k in opcodes:
                v = "0"
                if k in implied and k.strip() == line.strip().lower():
                    op = getOpWithMode(k, "Implied")
                elif k in accumulator and k.strip() == line.strip().lower():
                    op = getOpWithMode(k, "Accumulator")
                elif line.strip().lower() in [x+' a' for x in accumulator]:
                    op = getOpWithMode(k, "Accumulator")
                else:
                    op = False
                    ops = [x for x in asm if x.opcode==k]
                    
                    v = (line.split(" ",1)+[''])[1].strip()
                    
                    if k == "jmp" and v.startswith("("):
                        op = getOpWithMode(k, 'Indirect')
                    elif v.endswith('),y'):
                        op = getOpWithMode(k, '(Indirect), Y')
                    elif v.endswith(',x)'):
                        op = getOpWithMode(k, '(Indirect, X)')
                    elif v.endswith(',x'):
                        v = v.split(',x',1)[0]
                        if getLength(v)==1 and getOpWithMode(k, 'Zero Page, X'):
                            op = getOpWithMode(k, 'Zero Page, X')
                        elif getOpWithMode(k, 'Absolute, X'):
                            op = getOpWithMode(k, 'Absolute, X')
                    elif v.endswith(',y'):
                        v = v.split(',y',1)[0]
                        if getLength(v)==1 and getOpWithMode(k, 'Zero Page, Y'):
                            op = getOpWithMode(k, 'Zero Page, Y')
                        elif getOpWithMode(k, 'Absolute, Y'):
                            op = getOpWithMode(k, 'Absolute, Y')
                    elif v.startswith("#"):
                        v = v[1:]
                        op = getOpWithMode(k, 'Immediate')
                    else:
                        if getLength(v)==1 and getOpWithMode(k, 'Zero Page'):
                            op = getOpWithMode(k, "Zero Page")
                        elif getOpWithMode(k, "Absolute"):
                            op = getOpWithMode(k, "Absolute")
                        elif getOpWithMode(k, "Relative"):
                            op = getOpWithMode(k, "Relative")
                if op:
                    
                    if op.mode == 'Relative':
                        if addr>getValue(v):
                            v = str(0x100 - ((addr+op.length) - getValue(v)))
                        else:
                            v = str(getValue(v) - (addr+op.length))
                    b = [op.byte]
                    if op.length == 2:
                        b.append(getValue(v) % 0x100)
                    elif op.length == 3:
                        b.append(getValue(v) % 0x100)
                        b.append(math.floor(getValue(v)/0x100))
            
            if k == 'define':
                k = line.split(" ")[1].strip()
                v = line.split(" ",2)[-1].strip()
                if k == '$':
                    addr = getValue(v)
                    if startAddress == False:
                        startAddress = addr
                    currentAddress = addr
                else:
                    symbols[k.lower()] = v
                k=''

            
            if " equ " in line.lower():
                k = line[:line.lower().find(' equ ')]
                v = line[line.lower().find(' equ ')+len(' equ '):]
                equ[k] = v
            elif "=" in line:
                k = line.split("=",1)[0].strip()
                v = line.split("=",1)[1].strip()
                if k == '$':
                    addr = getValue(v)
                    if startAddress == False:
                        startAddress = addr
                    currentAddress = addr
                else:
                    symbols[k.lower()] = v
                k=''
            
            if len(b)>0:
                showAddress = True
                if noOutput==False and passNum == 2:
                    if bank == None:
                        if np:
                            out = np.append(out, np.array(b, dtype='B'))
                        else:
                            out = out + b
                    else:
                        fileOffset = addr % bankSize + bank*bankSize+headerSize
                        if fileOffset == len(out):
                            # We're in the right spot, just append
#                            print('yep')
#                            print(hex(fileOffset))
#                            print(hex(len(out)))
#                            print(hex(addr))

                            if np:
                                out = np.append(out, np.array(b, dtype='B'))
                            else:
                                out = out + b
                        elif fileOffset>len(out):
                            fv = fillValue
                            if np:
                                out = np.append(out, np.array(([fv] * (fileOffset-len(out))), dtype='B'))
                                out = np.append(out, np.array(b, dtype='B'))
                            else:
                                out = out + ([fv] * (fileOffset-len(out))) + b
                        elif fileOffset<len(out):
                            out = out[:fileOffset]+b+out[fileOffset+len(b):]
                addr = addr + len(b)
            
            if passNum == 2 and not hide:
                nBytes = cfg.getValue('main', 'list_nBytes')
                
                if startAddress:
                    outputText+="{:05X} ".format(currentAddress)
                else:
                    outputText+=' '*6
                
                if nBytes == 0:
                    outputText+="{}\n".format(originalLine)
                else:
                    listBytes = False
                    if noOutput:
                        listBytes = ' '*(3*nBytes+1)
                    else:
                        listBytes = ' '.join(['{:02X}'.format(x) for x in b[:nBytes]]).ljust(3*nBytes-1) + ('..' if len(b)>nBytes else '  ')
                    outputText+="{} {}\n".format(listBytes, originalLine)
                if errorText:
                    outputText+=errorText+"\n"
                    errorText = False
            if k==".org": showAddress = True

    with open(listFilename, 'w') as file:
        print(outputText, file=file)

    with open(outputFilename, "wb") as file:
        file.write(bytes(out))

    if debug:
        f = 'debug_symbols.txt'
        with open(f, "w") as file:
            for k,v in symbols.items():
                print(k,repr(v), file=file)

if __name__ == '__main__':
    if len(sys.argv) <2:
        print("Error: no file specified.")
        exit()

    filename = sys.argv[1]

    start = time.time()

    assemble(filename)

    end = time.time()-start
    if end>=3:
        print(time.strftime('Finished in %Hh %Mm %Ss.',time.gmtime(end)))
