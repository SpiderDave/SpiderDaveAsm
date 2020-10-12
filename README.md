# SpiderDaveAsm
ASM 6502 Assembler made in Python


== Command line ==

Usage:
    py sdasm.py <asm file>
    
Currently, creates output.txt and output.bin.


== Features ==
* Supports all (official) 6502 opcodes

== Syntax ==

Comments:
    Comments start with a semicolon, and can also be used at the end of a line.
    
    --example--
    ; This is a comment
    -----------
    
Labels:
    Labels must end in a colon.  Code can be placed on the same line as labels.
    
    --example--
    Start:
    -----------

Numbers:
    Hexadecimal numbers start with "$".  Binary numbers start with "%".
    
    --example--
    lda #$00        ; The "#" indicates an "immediate" value.
    ora #%00001100
    sta $4002
    -----------
    
Operators:
    Supported operators: + - > <
    +   addition
    -   subtraction
    <   prefix to give lower byte of word
    >   prefix to give upper byte of word
    
== Directives ==

=
    Used to define a symbol.
    
    --example--
    foobar = $42
    -----------
    
org
    Set the address.
    
    --example--
    .org $8000  ; start assembling at $8000
    -----------

db
    Output bytes.  Multiple items are separated by commas.
    
    --example--
    .db $00, $01, $ff
    -----------

dw
    Output words.  Multiple items are separated by commas.
    
    --example--
    .dw $8012, $8340
    -----------


