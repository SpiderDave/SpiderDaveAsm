"""
ToDo:
    lots.
"""


import math, os, sys
from include import Cfg

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


directives = [
    'if', 'elseif', 'else', 'endif', 'ifdef', 'ifndef', 'equ', 'org', 'base', 'pad',
    'include', 'incsrc', 'incbin', 'bin', 'hex', 'word', 'dw', 'dcw', 'dc.w', 'byte',
    'db', 'dcb', 'dc.b', 'dsw', 'ds.w', 'dsb', 'ds.b', 'align', 'macro', 'rept',
    'endm', 'endr', 'enum', 'ende', 'ignorenl', 'endinl', 'fillvalue', 'dl', 'dh',
    'error', 'inesprg', 'ineschr', 'inesmir', 'inesmap', 'nes2chrram', 'nes2prgram',
    'nes2sub', 'nes2tv', 'nes2vs', 'nes2bram', 'nes2chrbram', 'unstable', 'hunstable'
]

directives = directives + [
    'byt', 'includeall', 'warning'
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

def assemble(filename, outputFilename = 'output.bin', listFilename = 'output.txt',):
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
            return [x[1] for x in aLabels if x[0]==label and x[1]<addr][-1], 2
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
                return -1, 1
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
                return -1, 1
            l = 1 if v <=256 else 2
            return v,l
        if '*' in v:
            v = v.split('*')
            v = getValue(v[0]) * getValue(v[1])
            l = 1 if v <=256 else 2
            return v,l
        if '/' in v:
            v = v.split('/')
            v = getValue(v[0]) / getValue(v[1])
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
        if v.startswith("$"):
            l = 1 if len(v)-1<=2 else 2
            v = int(v[1:],16)
        elif v.startswith("%"):
            l = 1
            v = int(v[1:],2)
        elif isNumber(v):
            l = 1 if int(v,10) <=256 else 2
            v = int(v,10)
        elif v.lower() in symbols:
            v, l = getValueAndLength(symbols[v.lower()])
        else:
            v = -1
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


    try:
        file = open(filename, "r")
    except:
        print("Error: could not open file.")
        exit()


    # Doing it this way removes the line endings
    lines = file.read().splitlines()
    originalLines = lines

    symbols = Map()
    aLabels = []
    blockComment = 0
    
    for passNum in (1,2):
        lines = originalLines
        addr = 0
        currentAddress = addr
        mode = ""
        showAddress = False
        out = []
        outputText = ''
        
        for i in range(10000000):
            if i>len(lines)-1:
                break
            line = lines[i]
            
            if passNum == 2: print(line)
            
            currentAddress = addr
            originalLine = line
            
            for sep in commentSep:
                line = line.strip().split(sep,1)[0].strip()
            
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
            
            b=[]
            k = line.split(" ",1)[0].strip().lower()
            if k.endswith(":"):
                symbols[k[:-1]] = str(addr)
                line = line.split(":",1)[1].strip()
                k = line.split(" ",1)[0].strip()
            
            if k!='' and (k=="-"*len(k) or k=="+"*len(k)):
                if not [k,addr] in aLabels:
                    aLabels.append([k, addr])
            
            # prefix is optional for valid directives
            if k.startswith(".") and k[1:] in directives:
                k=k[1:]
            
            if k == "incbin" or k == "bin":
                filename = line.split(" ",1)[1].strip()
                with open(filename, 'rb') as file:
                    b = list(file.read())
                    out = out + b
            if k == "include" or k=="incsrc":
                filename = line.split(" ",1)[1].strip()
                with open(filename, 'r') as file:
                    newLines = file.read().splitlines()
                lines = lines[:i]+['']+newLines+lines[i+1:]
            if k == "includeall":
                folder = line.split(" ",1)[1].strip()
                files = [x for x in os.listdir(folder) if os.path.splitext(x.lower())[1] in ['.asm']]
                files = [x for x in files if not x.startswith('_')]
                lines = lines[:i]+['']+['include {}/{}'.format(folder, x) for x in files]+lines[i+1:]
            
            if k == "print" and passNum==2:
                v = line.split(" ",1)[1].strip()
                print(v)
            if k == "warning" and passNum==2:
                v = line.split(" ",1)[1].strip()
                print("warning: " + v)
            if k == "error" and passNum==2:
                v = line.split(" ",1)[1].strip()
                print("Error: " + v)
                exit()
            
            if k == "org":
                addr = getValue(line.split(" ",1)[1])
                currentAddress = addr
            
            if k == "pad":
                data = line.split(' ',1)[1]
                
                fv = fillValue
                if ',' in data:
                    fv = getValue(data.split(',')[1])
                a = getValue(data.split(',')[0])
                
                b = b + ([fv] * (a-currentAddress))
                out = out + b
                addr = addr + len(b)
            if k == "align":
                data = line.split(' ',1)[1]
                
                fv = fillValue
                if ',' in data:
                    fv = getValue(data.split(',')[1])
                a = getValue(data.split(',')[0])
                
                b = b + ([fv] * ((a-currentAddress%a)%a))
                out = out + b
                addr = addr + len(b)
            if k == "hex":
                data = line.split(' ',1)[1]
                b = b + list(bytes.fromhex(''.join(['0'*(len(x)%2) + x for x in data.split()])))
                out = out + b
                addr = addr + len(b)
            if k == "db" or k=="byte" or k == 'byt':
                values = line.split(' ',1)[1].split(",")
                values = [x.strip() for x in values]
                #b = b + [getValue(x) for x in values]
                
                for v in [getValue(x) for x in values]:
                    b = b + makeList(v)
                
                out = out + b
                addr = addr + len(b)
            if k == "dw" or k=="word" or k=='dbyt':
                values = line.split(' ',1)[1].split(",")
                values = [x.strip() for x in values]
                values = [getValue(x) for x in values]
                
                for value in values:
                    b = b + [value % 0x100, value>>8]
                out = out + b
                addr = addr + len(b)
            
            if k.lower() in opcodes:
                v = "0"
                if k in implied and k.strip() == line.strip():
                    op = getOpWithMode(k, "Implied")
                elif k in accumulator and k.strip() == line.strip():
                    op = getOpWithMode(k, "Accumulator")
                else:
                    op = False
                    ops = [x for x in asm if x.opcode==k]
                    
                    v = line.split(" ",1)[1].strip()
                    
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
                    addr = addr + op.length
                    
                    if op.mode == 'Relative':
                        if addr>getValue(v):
                            v = str(0x100 - (addr - getValue(v)))
                        else:
                            v = str(getValue(v) - addr)
                    b = [op.byte]
                    if op.length == 2:
                        b.append(getValue(v) % 0x100)
                    elif op.length == 3:
                        b.append(getValue(v) % 0x100)
                        b.append(math.floor(getValue(v)/0x100))
                    out = out + b
            if "=" in line:
                v = line.split("=",1)[1].strip()
                symbols[k] = v
            
            
            if len(b)>0:
                showAddress = True
            
            if passNum == 2:
                nBytes = cfg.getValue('main', 'list_nBytes')
                
                if showAddress:
                    outputText+="{:05X} ".format(currentAddress)
                else:
                    outputText+=' '*6
                
                if nBytes == 0:
                    outputText+="{}\n".format(originalLine)
                else:
                    listBytes = ' '.join(['{:02X}'.format(x) for x in b[:nBytes]]).ljust(3*nBytes-1) + ('..' if len(b)>nBytes else '  ')
                    outputText+="{} {}\n".format(listBytes, originalLine)
                
            if k==".org": showAddress = True

    with open(listFilename, 'w') as file:
        print(outputText, file=file)

    with open(outputFilename, "wb") as file:
        file.write(bytes(out))


# create our config parser
cfg = Cfg("config.ini")

# read config file if it exists
cfg.load()

# number of bytes to show when generating list
cfg.setDefault('main', 'list_nBytes', 8)
cfg.setDefault('main', 'comment', ';,//')
cfg.setDefault('main', 'commentBlockOpen', '/*')
cfg.setDefault('main', 'commentBlockClose', '*/')
cfg.setDefault('main', 'nestedComments', True)
cfg.setDefault('main', 'fillValue', '$ff')

if len(sys.argv) <2:
    print("Error: no file specified.")
    exit()

filename = sys.argv[1]

assemble(filename)

cfg.save()