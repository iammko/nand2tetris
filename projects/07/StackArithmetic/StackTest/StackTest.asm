// 1 StackTest.asm
@17
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_0
D;JEQ
D=0
@StackTest_END_0
0;JMP
(StackTest_TRUE_0)
D=-1
(StackTest_END_0)
@SP
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@16
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_1
D;JEQ
D=0
@StackTest_END_1
0;JMP
(StackTest_TRUE_1)
D=-1
(StackTest_END_1)
@SP
A=M-1
M=D
@16
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_2
D;JEQ
D=0
@StackTest_END_2
0;JMP
(StackTest_TRUE_2)
D=-1
(StackTest_END_2)
@SP
A=M-1
M=D
@892
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_3
D;JLT
D=0
@StackTest_END_3
0;JMP
(StackTest_TRUE_3)
D=-1
(StackTest_END_3)
@SP
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@892
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_4
D;JLT
D=0
@StackTest_END_4
0;JMP
(StackTest_TRUE_4)
D=-1
(StackTest_END_4)
@SP
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_5
D;JLT
D=0
@StackTest_END_5
0;JMP
(StackTest_TRUE_5)
D=-1
(StackTest_END_5)
@SP
A=M-1
M=D
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_6
D;JGT
D=0
@StackTest_END_6
0;JMP
(StackTest_TRUE_6)
D=-1
(StackTest_END_6)
@SP
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_7
D;JGT
D=0
@StackTest_END_7
0;JMP
(StackTest_TRUE_7)
D=-1
(StackTest_END_7)
@SP
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@StackTest_TRUE_8
D;JGT
D=0
@StackTest_END_8
0;JMP
(StackTest_TRUE_8)
D=-1
(StackTest_END_8)
@SP
A=M-1
M=D
@57
D=A
@SP
M=M+1
A=M-1
M=D
@31
D=A
@SP
M=M+1
A=M-1
M=D
@53
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
M=M+D
@112
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
@SP
A=M-1
M=-M
@SP
AM=M-1
D=M
@SP
A=M-1
M=M&D
@82
D=A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
M=M|D
@SP
A=M-1
M=!M