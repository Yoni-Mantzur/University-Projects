@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@LCL
D=M
@0
D=A+D
@R13
D=D+M
A=D-M
M=D-A
($LOOP_START)
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R14
M=D
@R14
D=M
@R15
@SP
M=M-1
A=M
D=M
@R13
M=D
@R14
D=M
@R13
M=M+D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@LCL
D=M
@0
D=A+D
@R13
D=D+M
A=D-M
M=D-A
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R14
M=D
@R14
D=M
@R15
@SP
M=M-1
A=M
D=M
@R13
M=D
@R14
D=M
@R13
M=M-D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@ARG
D=M
@0
D=A+D
@R13
D=D+M
A=D-M
M=D-A
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@$LOOP_START
D;JNE
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
