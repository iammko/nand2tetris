// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@status         // init status
M=0
D=0
@i              // init start screen address idx
M=0

(SETLOOP)
@KBD
D=M
@SETLOOP2   
D;JEQ
D=-1        // confirm status

(SETLOOP2)
@TEMP       // save new status
M=D
@status
D=D-M
@SETIDX     // no change, keep set next address
D;JEQ
@TEMP
D=M
@status     // new status start by cur idx
M=D

(SETADDRESS)
@i
D=M
@SCREEN
D=D+A
@address
M=D
@status
D=M
@address
A=M             // set A to SCREEN[idx]
M=D             // SCREEN[idx]=status
@SETLOOP
0;JMP

(SETNOKEYIDX)
@i
D=M             //no key, if i <= 0 then stop
@SETLOOP
D;JLE
@i
M=M-1           // set point to SCREEN[idx-1]
@SETADDRESS
0;JMP

(SETIDX)
@TEMP
D=M
@SETNOKEYIDX
D;JEQ           //nokey
@i              // has key, if i >= 8192 then keep
D=M
@8192
D=D-A
@SETLOOP
D;JGE
@i
M=M+1           // set point to SCREEN[idx+1]
@SETADDRESS
0;JMP



