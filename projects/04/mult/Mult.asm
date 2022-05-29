// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@p  
M=0
@1     
D=M
@i
M=D

(LOOP)
    @0
    D=M
    @p
    M=M+D
    @i
    M = M-1
    D=M
    @1
    @END1
    D;JEQ
    @LOOP  
    0;JMP

(END1)
    @p
    D=M
    @2
    M=D
(END2)
    @END2
    0;JMP


