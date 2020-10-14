# SpiderDaveAsm
ASM 6502 Assembler made in Python


## Command line ##

Usage:
    py sdasm.py <asm file>
    
Currently, creates output.txt and output.bin.


## Features ##
* Supports all (official) 6502 opcodes
* Anonymous labels

# Syntax #

Configuration:
    After running once, a config.ini will be generated.  Some syntax may be changed with configuration.

Opcodes:
    Standard 6502 ocodes are supported.  Opcodes are case-insensitive.

Comments:
    Comments start with a semicolon or "//", and can also be used at the end of a line.
    Block-level comments are enclosed in "/*" "*/" and may be nested.
    
```
    ; This is a comment
    // This is also a comment
    /*
        This is a block level comment
    */
```
    
## Labels ##
    Labels must end in a colon.  Code can be placed on the same line as labels.
    Anonymous labels are 1 or more "-" or "+" characters.  These labels will only
    search backwards for "-" and forwards for "+".  Labels starting with '@' are
    local labels.  They have limited scope, visible only between non-local labels.
    
    
```
    Start:
    - lda PPUSTATUS     ; wait one frame
    bpl -
    
    - lda PPUSTATUS     ; wait another frame
    bpl -
    
    label1:
    @tmp1:
    @tmp2:
    
    label2:
    @tmp1:
    @tmp2:
```

## Numbers ##
    Hexadecimal numbers start with "$".  Binary numbers start with "%".
    
```
    lda #$00        ; The "#" indicates an "immediate" value.
    ora #%00001100
    sta $4002
```

## Other Symbols ##
    
    A "$" by itself may be used to get or set the current address.
    
## Strings ##
    
    String values are partially supported.

```
    foo = "bar"             ; works
    .db foo, "ABC", $00     ; works
    lda "A"                 ; does not work
    .db "ABC"+1             ; works (adds 1 to each character)
    .db "A"+"A"             ; does not work
```

## Operators ##

NOTE: order of operations is wrong, and () is not supported yet.

| op | description                       |
|:--:|-----------------------------------|
|  * | multiplication                    |
|  / | division                          |
|  + | addition                          |
|  - | subtraction                       |
|  < | prefix to give lower byte of word |
|  > | prefix to give upper byte of word |    

## Directives ##
    Most directives may optionally be prefixed with a ".".

=
    Used to define a symbol.  Symbol names are case-insensitive.
    
```
    foobar = $42
```
    
org
    
    Set the starting address if it hasn't been assigned yet, otherwise
    org functions like pad.
    
```
    org $8000  ; start assembling at $8000
    .
    .
    .
    org $fffa, $80 ;equivalent to PAD $fffa, $80
```

base

        Set the program address.  This is useful for relocatable code,
        multiple code banks, etc.
    
```
    base $8000
```

pad
    
    Fill memory from the current address to a specified address.  A fill
    value may also be specified.
    
```
    pad $FFFA
    pad $FFFA, $ea
```

align
    
    Fill memory from the current address to specified byte boundary.  A fill
    value may also be specified.
    
```
    align 256
    align 256, $ea
```

fillvalue

    Change the default filler for pad, align, etc.
    
```
    fillvalue $ff
```

enum
ende

    Reassign PC and suppress assembly output.  Useful for defining
    variables in RAM.
    
```
    enum $200
    foo:    db 0
    foo2:   db 0
    enum
```

db / byte / byt
    
    Output bytes.  Multiple items are separated by commas.
    
```
    db $00, $01, $ff
```

dw / word
    
    Output words.  Multiple items are separated by commas.
    
```
    dw $8012, $8340
```

hex

    Compact way of laying out a table of hex values.  Only raw hex values
    are allowed, no expressions.  Spaces can be used to separate numbers.

```
    hex 456789ABCDEF  ;equivalent to db $45,$67,$89,$AB,$CD,$EF
    hex 0 1 23 4567   ;equivalent to db $00,$01,$23,$45,$67
```

include / incsrc
    
    Assemble another source file as if it were part of the source.
    
```
    include foobar.asm
```

includeall
    
    Include all .asm files in a folder.  Files starting with "_" will be ignored.
    
```
    include code/macros
```

incbin / bin
    
    Add a file to the assembly as raw data.
    
```
    include chr00.chr
```
    
print
    
    Print a message
    
```
    print Hello World!
```

warning
    
    Print a warning message.  The message will start with "Warning: ".
    
```
    warning missing data!
```

error
    
    Print an error message and stops the assembler.  The message will start with "Error: ".
    
```
    error file not found!
```
