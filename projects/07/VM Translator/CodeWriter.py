import os
from Common import VMCommandType
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

    def setFileName(self, filename):
        self.fd = open(filename, 'w')
        self.__curfilecount = 1
        self.__curfilename = os.path.basename(filename)
        self.__curfilenamenosuffix = self.__curfilename.split('.')[0]
        self.fd.write("// %d %s\n"%(self.__curfilecount, self.__curfilename))
        print(filename)

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

    def __writeStrList(self, strList):
        if type(strList) is str:
            strList = [strList]

        for l in strList:
            self.fd.write(l+'\n')
            #print(l)

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
            self.__writeStrList(
                [
                    str.format('@%s'%segment),
                    'D=M'
                ]
            )
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
        self.__writeStrList(
            [
            '@'+index,
            'D=A',
            ]
        )
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
        # 取出第一个元素，放入D寄存器，SP--
        self.__popStack()
        # 取第二个元素的地址，放入A寄存器
        self.__popStackAddress()
        # 相减，做跳转
        logic_true = str.format("%s_TRUE_%d"%(self.__curfilenamenosuffix, self.__logicidx))
        logic_end = str.format("%s_END_%d"%(self.__curfilenamenosuffix, self.__logicidx))
        self.__writeStrList(
            [
                'D=M-D',
                '@'+logic_true,
                'D;'+symbol,
                'D=0',
                '@'+logic_end,
                '0;JMP',
                '('+logic_true+')',
                'D=-1',
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