// 1 Class1.vm
(Class1.set)
@ARG
A=M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@Class1.0
M=D
@1
D=A
@ARG
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@Class1.1
M=D
@0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@R14
M=D
@R14
D=M
@5
A=D-A
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D
@SP
M=M+1
@R14
D=M
A=D-1
D=M
@THAT
M=D
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
@R15
D=M
A=D
0;JMP
(Class1.get)
@Class1.0
D=M
@SP
M=M+1
A=M-1
M=D
@Class1.1
D=M
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
@LCL
D=M
@R14
M=D
@R14
D=M
@5
A=D-A
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D
@SP
M=M+1
@R14
D=M
A=D-1
D=M
@THAT
M=D
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
@R15
D=M
A=D
0;JMP
// 1 Class2.vm
(Class2.set)
@ARG
A=M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@Class2.0
M=D
@1
D=A
@ARG
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@Class2.1
M=D
@0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@R14
M=D
@R14
D=M
@5
A=D-A
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D
@SP
M=M+1
@R14
D=M
A=D-1
D=M
@THAT
M=D
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
@R15
D=M
A=D
0;JMP
(Class2.get)
@Class2.0
D=M
@SP
M=M+1
A=M-1
M=D
@Class2.1
D=M
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
@LCL
D=M
@R14
M=D
@R14
D=M
@5
A=D-A
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D
@SP
M=M+1
@R14
D=M
A=D-1
D=M
@THAT
M=D
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
@R15
D=M
A=D
0;JMP
// 1 Sys.vm
(Sys.init)
@6
D=A
@SP
M=M+1
A=M-1
M=D
@8
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.init$ret_Class1.set_arg_2_idx_0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=A
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=A
@LCL
M=D
@Class1.set
0;JMP
(Sys.init$ret_Class1.set_arg_2_idx_0)
@0 
D=A
@R5
D=A+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@23
D=A
@SP
M=M+1
A=M-1
M=D
@15
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.init$ret_Class2.set_arg_2_idx_0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=A
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=A
@LCL
M=D
@Class2.set
0;JMP
(Sys.init$ret_Class2.set_arg_2_idx_0)
@0 
D=A
@R5
D=A+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@Sys.init$ret_Class1.get_arg_0_idx_0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=A
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=A
@LCL
M=D
@Class1.get
0;JMP
(Sys.init$ret_Class1.get_arg_0_idx_0)
@Sys.init$ret_Class2.get_arg_0_idx_0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=A
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=A
@LCL
M=D
@Class2.get
0;JMP
(Sys.init$ret_Class2.get_arg_0_idx_0)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
