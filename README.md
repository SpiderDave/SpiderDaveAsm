# SpiderDaveAsm
ASM 6502 Assembler made in Python


## Command line ##

Usage:
    py sdasm.py <asm file>
    
Currently, creates output.txt and output.bin.


## Features ##
* Supports all (official) 6502 opcodes
* Anonymous labels

## Syntax ##

Opcodes:
    Standard 6502 ocodes are supported.  Opcodes are case-insensitive.

Comments:
    Comments start with a semicolon, and can also be used at the end of a line.
    
```
    ; This is a comment
```
    
Labels:
    Labels must end in a colon.  Code can be placed on the same line as labels.
    Anonymous labels are 1 or more "-" or "+" characters.  These labels will only
    search backwards for "-" and forwards for "+".
    
```
    Start:
    - lda PPUSTATUS     ; wait one frame
    bpl -
    
    - lda PPUSTATUS     ; wait another frame
    bpl -
```

Numbers:
    Hexadecimal numbers start with "$".  Binary numbers start with "%".
    
```
    lda #$00        ; The "#" indicates an "immediate" value.
    ora #%00001100
    sta $4002
```
    
Operators:
    Supported operators: + - > <
    +   addition
    -   subtraction
    <   prefix to give lower byte of word
    >   prefix to give upper byte of word
    
## Directives ##
    Most directives may optionally be prefixed with a ".".

=
    Used to define a symbol.  Symbol names are case-insensitive.
    
```
    foobar = $42
```
    
org
    Set the address.
    
```
    .org $8000  ; start assembling at $8000
```

db / byte / byt
    Output bytes.  Multiple items are separated by commas.
    
```
    .db $00, $01, $ff
```

dw / word
    Output words.  Multiple items are separated by commas.
    
```
    .dw $8012, $8340
```

include / incsrc
    
    Assemble another source file as if it were part of the source.
    
```
    include foobar.asm
```

incbin / bin
    
    Add a file to the assembly as raw data.
    
```
    include chr00.chr
```
    
    