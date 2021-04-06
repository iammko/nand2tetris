import os
from Common import VMCommandType, VMBoolType
#   RAM地址
#   0-15            16个虚拟寄存器                  
#   15-255          VM程序的所有VM函数的静态变量
#   256-2047        栈
#   2048-16383      堆（用于存放对象和数组
#   16384-24575     内存映像 I/O

#   内存访问
#   argument        函数参数                                    栈
#   local           函数局部变量                                栈
#   static          同一.vm文件的静态变量                       静态区
#   constant        常数伪段，范围0...32767                      常数
#   this，that      指向堆                                      堆，虚拟寄存器
#   pointer         指向this，that                              虚拟寄存器
#   temp            全局临时变量                                RAM[5-12]

class CodeWriter:
    def __init__(self):
        self.__table = {
            "SP" :      0,
            "LCL":      1,
            "ARG":      2,
            "THIS":     3,
            "THAT":     4,
            "R0":       0,
            "R1":       1,
            "R2":       2,
            "R3":       3,
            "R4":       4,
            "R5":       5,
            "R6":       6,
            "R7":       7,
            "R8":       8,
            "R9":       9,
            "R10":      10,
            "R11":      11,
            "R12":      12,
            "R13":      13,
            "R14":      14,
            "R15":      15,
        }
        
        self.__segment_dict = {
            'constant' : {'write_push_func' : self.__writeConstantPush},
            'local' : {'segment' :'LCL', 'write_push_func' : self.__writeBasePush, 'write_pop_func' : self.__writeBasePop},
            'argument' : {'segment' :'ARG', 'write_push_func' : self.__writeBasePush, 'write_pop_func' : self.__writeBasePop},
            'this' : {'segment' :'THIS', 'write_push_func' : self.__writeBasePush, 'write_pop_func' : self.__writeBasePop},
            'that' : {'segment' :'THAT', 'write_push_func' : self.__writeBasePush, 'write_pop_func' : self.__writeBasePop},
            'pointer' : {'segment' :'THIS', 'write_push_func' : self.__writePointerPush, 'write_pop_func' : self.__writePointerPop},
            'temp' : {'segment' :'R5', 'write_push_func' : self.__writePointerPush, 'write_pop_func' : self.__writePointerPop},
            'static' : {'write_push_func' : self.__writeStaticPush, 'write_pop_func' : self.__writeStaticPop},
        }
    
        # 汇编伪指令递增
        self.__logicidx = 0
        # 算数命令和逻辑命令 对应的 符号和输入方法
        self.__arithmetic = {    
            # '@'表示取地址
            'add' : { 'symbol' : '+', 'func' : self.__writeBinaryArithmetic},
            'sub' : { 'symbol' : '-', 'func' : self.__writeBinaryArithmetic},
            'neg' : { 'symbol' : '-', 'func' : self.__writeUnaryArithmetic},
            'and' : { 'symbol' : '&', 'func' : self.__writeBinaryArithmetic},
            'or'  : { 'symbol' : '|', 'func' : self.__writeBinaryArithmetic},
            'not' : { 'symbol' : '!', 'func' : self.__writeUnaryArithmetic},
            'eq' : { 'symbol' : 'JEQ', 'func' : self.__writeLogicArithmetic},
            'gt' : { 'symbol' : 'JGT', 'func' : self.__writeLogicArithmetic},
            'lt' : { 'symbol' : 'JLT', 'func' : self.__writeLogicArithmetic},
        }

        self.__curfilecount = 0
        self.fd = None

        # 当前声明函数名
        self.__curFunctionName = ''
        # call函数标签递增
        self.__callfuncidx = 0

        # 当前输出的文件
        self.__curoutfile = ''

    def setFileName(self, outfilename, parsefilename):
        if self.__curoutfile != outfilename:
            print("curfile:%s setfile:%s"%(self.__curoutfile, outfilename))
            self.__curoutfile = outfilename
            self.__curoutfilename = os.path.basename(self.__curoutfile)
            self.fd = open(outfilename, 'w')
            self.__curfilecount = 0
        self.__curfilecount += 1
        self.__curfilename = os.path.basename(parsefilename)
        self.__curfilenamenosuffix = self.__curfilename.split('.')[0]
        self.fd.write("// %d %s\n"%(self.__curfilecount, self.__curfilename))
        print(parsefilename)

    def writeArithmetic(self, Command):
        symbol = self.__arithmetic.get(Command).get('symbol')
        self.__arithmetic.get(Command).get('func')(symbol)
        
    # constant 将常数直接压入栈顶
    # local、argument、this、that，存放的是指定段的基地址base，操作时修改的是 *(base)+i 的值，类似修改指向对象*p的值
    # pointer、temp，修改指向的段，即base的值，类似改变指针p的值
    # static也是修改base值，但是地址通过汇编编译器分配
    def writePushPop(self, Command, segment, index):
        # 内存访问命令
        # Command segment index
        if Command == VMCommandType.C_PUSH:
            self.__segment_dict[segment].get('write_push_func')(segment=self.__segment_dict[segment].get('segment'), index=index)

        if Command == VMCommandType.C_POP:
            self.__segment_dict[segment].get('write_pop_func')(segment=self.__segment_dict[segment].get('segment'), index=index)

    def writeLabel(self, label):
        self.__writeStrList("(" + self.__makeLabelStr(label) + ")")

    def writeGoto(self, label):
        self.__writeStrList(
            [
                '@'+ self.__makeLabelStr(label),
                '0;JMP'
            ]
        )
    
    def writeIf(self, label):
        # 比较结果放入D寄存器
        self.__popStack()
        # !=0就跳转
        self.__writeStrList(
            [
                '@' + self.__makeLabelStr(label),
                'D;JNE'
            ]
        )

    # call f n, 调用之前需要用push命令,压入n个参数,作为函数f的传入参数
    def writeCall(self, functionName, numArgs):
        return_address = self.__makeLabelStr('ret_' + functionName + '_arg_' + numArgs + '_idx_' + str(self.__callfuncidx))
        # 保存返回地址
        self.__constantOrLabel2D(return_address)
        self.__pushStack()
        # 内存分布情况从上到下: 当前被调用函数的ARG区间 -> 调用函数的状态帧 -> 被调用函数的LCL区间
        # 保存LCL指针,即RAM[LCL]的值
        self.__ramAddress2D('LCL')
        self.__pushStack()
        # 保存ARG指针
        self.__ramAddress2D('ARG')
        self.__pushStack()
        # 保存THIS指针
        self.__ramAddress2D('THIS')
        self.__pushStack()
        # 保存THAT指针
        self.__ramAddress2D('THAT')
        self.__pushStack()
        # 重置ARG
        self.__writeStrList(
            [
                '@SP',
                'D=M',
                '@'+numArgs,
                'D=D-A',
                '@5',
                'D=D-A'
            ]
        )
        self.__registerD2Address('ARG')
        # 重置LCL
        self.__writeStrList(
            [
                '@SP',
                'D=M'
            ]
        )
        self.__registerD2Address('LCL')
        # goto f
        self.__writeStrList(
            [
                '@'+self.__makeFunctionNameStr(functionName),
                '0;JMP'
            ]
        )
        # 返回地址标签
        self.__writeStrList('(' + return_address + ')')

        self.__callfuncidx += 1

    def writeReturn(self):
        # 把LCL指向的地址放入R14,R14保存FRAME的值
        self.__ramAddress2D('LCL')
        self.__registerD2Address('R14')
        # 把返回地址放入R15, return_address的栈地址为*R14-5, *(*R14-5)为返回地址
        self.__ramAddress2D('R14') # D=*R14=FRAME
        self.__writeStrList([
            '@5', 
            'A=D-A',   # A=D-5=(*R14 - 5)=&return_address
            'D=M'    # D=return_address
        ])
        self.__registerD2Address('R15')
        # *ARG=pop(), 此时pop()是弹出被调用者的返回值,保存于调用者的栈顶(argument 0即调用者的栈顶)
        self.__popStack()
        self.__registerD2RAMAddress('ARG')
        # 恢复调用者的栈指针,SP = ARG + 1
        self.__ramAddress2D('ARG')
        self.__registerD2Address('SP')
        self.__writeStrList([
            '@SP',
            'M=M+1'
        ])
        
        # 恢复调用者的THAT
        self.__ramAddress2D('R14') # D=*R14=FRAME
        self.__writeStrList([
            'A=D-1',   # D-1=调用者THAT指针所在的地址
            'D=M'      # 取出地址D-1里的值,就是THAT指针的值
        ])
        self.__registerD2Address('THAT')
         # 恢复调用者的THIS
        self.__ramAddress2D('R14')
        self.__writeStrList([
            '@2', 
            'A=D-A',   
            'D=M'      
        ])
        self.__registerD2Address('THIS')
        # 恢复调用者的ARG
        self.__ramAddress2D('R14')
        self.__writeStrList([
            '@3', 
            'A=D-A',  
            'D=M'      
        ])
        self.__registerD2Address('ARG')
        # 恢复调用者的LCL
        self.__ramAddress2D('R14')
        self.__writeStrList([
            '@4', 
            'A=D-A',  
            'D=M'     
        ])
        self.__registerD2Address('LCL')

        # goto RET
        self.__ramAddress2D('R15')
        self.__writeStrList([
            'A=D',
            '0;JMP'
        ])
        

    def writeFunction(self, functionName, numLoacals):
        self.__curFunctionName = functionName
        self.__writeStrList("(" + self.__makeFunctionNameStr(functionName) + ")")
        loopNum = int(numLoacals)
        # 初始化local index
        # 此时LCL已经指向SP, 只需要往栈里添加loopNum个0, SP自然就向下移动loopNum个单位
        while loopNum > 0:
            # push constant 0
            self.writePushPop(VMCommandType.C_PUSH, 'constant', '0')
            loopNum -= 1
    
    # 引导代码
    def writeGuideCode(self):
        # SP 256
        self.__writeStrList([
            '@256',
            'D=A',
            '@SP',
            'M=D'
        ])
        # LCL 300
        self.__writeStrList([
            '@300',
            'D=A',
            '@LCL',
            'M=D'
        ])
        # ARG 400
        self.__writeStrList([
            '@400',
            'D=A',
            '@ARG',
            'M=D'
        ])
        # 起始调用Sys.init
        # 直接跳转
        # 这个方式得到的结果,和本书提供的工具Virtual Machine Emulator 加载*VME.tst输出的结果一致
        # | RAM[0] |RAM[261]|
        # | 257    |      0 |
        # 
        # self.__writeStrList([
        #     '@Sys.init',
        #     '0;JMP'
        # ])

        # 调用Call方法
        # | RAM[0] |RAM[261]|
        # | 262    |      3 |
        # 测试比较文件.cmp结果中,偏移了5位,正好是Call保存的调用者的数据,这里就直接调用call方法
        self.writeCall('Sys.init', '0')


    def __writeStrList(self, strList):
        if type(strList) is str:
            strList = [strList]

        for l in strList:
            self.fd.write(l+'\n')
            #print(l)

    def __makeFunctionNameStr(self, functionName):
        return functionName

    def __makeLabelStr(self, label):
        return self.__curFunctionName + "$" + label

    def __writeBasePush(self, segment, index):
        if index == '0':
            self.__writeStrList(
                [
                    '@'+segment,
                    'A=M',
                    'D=M'
                ]
            )
        else:
            self.__writeStrList(
                [
                '@'+index,
                'D=A',  # 保存index
                '@'+segment,
                'A=M+D',# 指向段的值+index=base+i放入A寄存器
                'D=M',  # 取base+i地址的值放入D寄存器
                ]
            )
        # D寄存器的值压入栈
        self.__pushStack()

    def __writeBasePop(self, segment, index):
        if index == '0':
            self.__popStack()
            self.__registerD2RAMAddress(segment)
            return
        
        # 将RAM[segment]+index放入R13
        self.__2Address('M', 'R13', segment, index)
        # 弹出栈顶元素，放入D寄存器
        self.__popStack()
        # 对地址RAM[segment]+index赋值
        self.__registerD2RAMAddress('R13')

    def __writePointerPush(self, segment, index):
        if index == '0':
            self.__ramAddress2D(segment)
        else:
            self.__writeStrList(
                [
                '@'+index,
                'D=A',  # 保存index
                '@'+segment,
                'A=A+D',# 指向段的地址+index=segment+i放入A寄存器
                'D=M',  # 取segment+i的值放入D寄存器
                ]
            )
        # D寄存器的值压入栈
        self.__pushStack()

    def __writePointerPop(self, segment, index):
        if index == '0':
            self.__popStack()
            self.__registerD2Address(segment)
            return

        self.__2Address('A', 'R13', segment, index)
        self.__popStack()
        self.__registerD2RAMAddress('R13')

    def __writeConstantPush(self, segment, index):
        self.__constantOrLabel2D(index)
        self.__pushStack()

    def __writeStaticPush(self, segment, index):
        self.__writeStrList(
            [
                str.format("@%s.%s"%(self.__curfilenamenosuffix, index)),
                'D=M'
            ]
        )
        self.__pushStack()

    def __writeStaticPop(self, segment, index):
        self.__popStack()
        self.__writeStrList(
            [
            str.format("@%s.%s"%(self.__curfilenamenosuffix, index)),
            'M=D'
            ]
        )

    # 逻辑命令
    def __writeLogicArithmetic(self, symbol):
        # 取出第一个元素y，放入D寄存器，SP--
        self.__popStack()
        # 取第二个元素x的地址，放入A寄存器
        self.__popStackAddress()
        # 相减x-y，做跳转
        logic_true = str.format("%s_TRUE_%d"%(self.__curfilenamenosuffix, self.__logicidx))
        logic_end = str.format("%s_END_%d"%(self.__curfilenamenosuffix, self.__logicidx))
        self.__writeStrList(
            [
                'D=M-D',
                '@'+logic_true,
                'D;'+symbol,
                'D=' + VMBoolType.FALSE.value,
                '@'+logic_end,
                '0;JMP',
                '('+logic_true+')',
                'D='+ VMBoolType.TRUE.value,
                '('+logic_end+')'
            ]
        )
        # 取栈顶元素值
        self.__popStackAddress()
        # 赋值
        self.__writeStrList('M=D')

        self.__logicidx += 1


    # 二元算术命令
    def __writeBinaryArithmetic(self, symbol):
        # 取出第一个元素，放入D寄存器，SP--
        self.__popStack()
        # 取出第二个元素的栈地址，放入A
        self.__popStackAddress()
        # 执行二元算术
        self.__writeStrList(str.format("M=M%sD"%symbol))

    # 一元算术命令
    def __writeUnaryArithmetic(self, symbol):
        # 取出第一个元素的栈地址
        self.__popStackAddress()
        # 执行一元算术
        self.__writeStrList(str.format("M=%sM"%symbol))
        

    # 将指定地址的值存入D寄存器
    def __ramAddress2D(self, address):
        self.__writeStrList(
            [
                '@' + address,
                'D=M'
            ]
        )

    # 指定地址a存放的地址b, 将地址b存放的值存入D寄存器
    def __ramRamAddress2D(self, address):
        self.__writeStrList(
            [
                '@' + address,
                'A=M',
                'D=M'
            ]
        )

    # 将常量或者标签地址存入D寄存器
    def __constantOrLabel2D(self, constantOrLabel):
        self.__writeStrList(
            [
                '@' + constantOrLabel,
                'D=A'
            ]
        )

    # 将地址segment+index或者@segment+index的值存入address
    def __2Address(self, AorM, address, segment, index):
         self.__writeStrList(
            [
                '@'+index,
                'D=A',
                '@'+segment,
                'D='+AorM+'+D',
                '@'+address,
                'M=D'
            ]    
        )

    # 将D寄存器的值输入RAM[address]
    def __registerD2RAMAddress(self, address):
        self.__writeStrList(
            [
                '@'+address,
                'A=M',
                'M=D'
            ]
        )

    # 将D寄存器的值输入address
    def __registerD2Address(self, address):
        self.__writeStrList(
            [
                '@'+address,
                'M=D'
            ]
        )

    # 弹出栈顶元素，放入D寄存器，SP--
    def __popStack(self):
        self.__writeStrList(
            [
                '@SP',
                'AM=M-1',
                'D=M'
            ]
        )

    # 将D寄存器的值压入栈顶，SP++
    def __pushStack(self):
        self.__writeStrList(
            [
                '@SP',
                'M=M+1',
                'A=M-1',
                'M=D'
            ]
        )

    # 取栈顶元素地址，放入A寄存器，SP不递减
    def __popStackAddress(self):
        self.__writeStrList(
            [
                '@SP',
                'A=M-1'
            ]
        )

    

    def Close(self):
        if self.fd != None:
            self.fd.close()
            self.fd = None
            self.__curFunctionName = ''