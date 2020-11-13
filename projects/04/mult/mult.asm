// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// bzero 
@2
M=0


(LOOP)
// quit condition
@1
D=M
@END
D;JLE   // if R1 <= 0, goto END

// func
@0
D=M     // D=R0
@2
M=M+D   // R2=R2+R0, R2最终等于R1个R0相加
@1
M=M-1   // R1=R1-1

// continue
@LOOP
0;JMP

(END)
@END
0;JMP