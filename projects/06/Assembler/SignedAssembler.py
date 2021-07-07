import os
import Parser
import Code

#   语法规约
    ##  常数和符号：
        ### 常数必须是非负的，十进制
        ### 用户定义的符号可以由字母、数字、下划线(_)、点(.)、美元符号($)和冒号(:)组成，不能以数字开头
    ##  注释，//
    ##  空格，空格字符和空行被忽略
    ##  大小写习惯
        ### 汇编助记符必须大写。标签大写，变量小写，区分大小写

#   指令
    ##  A-指令
        ### 0 指令开头
        ### vvv vvvv vvvv vvvv 值
    ##  C-指令
        ### 1 指令开头
        ### 11 无作用
        ### a cccc cc comp域
        ### ddd dest域
        ### jjj jump域

#   符号
    ##  预定义符号
        ### 预先定义的符号，有对应的内存地址和值
    ##  标签符号
        ### 指代下一条命令所在的指令内存中的地址，保存在指定的内存地址当中，大写
    ##  变量符号
        ### 指代内存地址，映射在内存地址当中


class SignedAssembler:
    def __init__(self):
        self.file_list = []

    def AddFile(self, file):
        self.file_list.append(file)

    def Work(self):
        while(len(self.file_list) > 0):
            self.__SetFile(self.file_list.pop())
            self.__CompileFile()

    def __SetFile(self, file):
        self.file = file
        self.out_file = os.path.dirname(file) + os.path.sep + os.path.basename(file).split('.')[0] + r'.hack'

    def __CompileFile(self):
        parser = Parser.Parser(self.file)
        code = Code.Code()

        # 创建符号表
        import SymbolTable
        symbolTable = SymbolTable.SymbolTable()
        symbol_address = 16
        address_counter = 0
        while(parser.hasMoreCommands()):
            symbol = parser.symbol()

            # 伪命令行不计入指令地址
            if(parser.commandType() == Parser.CommandType.L_COMMAND):
                symbolTable.addEntry(symbol, address_counter)
                continue
            
            #print("current command address is %d"%address_counter)
            if(parser.commandType() == Parser.CommandType.A_COMMAND):
                if(symbolTable.contains(symbol) == False and symbol.isnumeric() == False):
                    # 加入符号表
                    symbolTable.addEntry(symbol, symbol_address)
                    symbol_address += 1
            # 指令地址+1
            address_counter += 1
        # 重置输入文件
        parser.Reset()

        with open(self.out_file, 'w') as out_f:
            newline = False
            while(parser.hasMoreCommands()):
                # 伪命令，在创建符号表的时候有用，在这可以直接跳过  # 有符号版本
                if(parser.commandType() == Parser.CommandType.L_COMMAND):
                    continue
                
                # 是否需要新的一行
                if(newline):
                    out_f.write("\n")
                if(newline == False):
                    newline = True

                # 获取新指令
                cmd = parser.advance()

                # A-指令
                if(parser.commandType() == Parser.CommandType.A_COMMAND):
                    acommand = parser.symbol()

                    # 符号替换
                    if(str.isnumeric(acommand) == False):
                        acommand = symbolTable.GetAddress(acommand)

                    binnumber = bin(int(acommand)).split("0b")[-1]
                    zero_count = 15 - len(binnumber)
                    zero_str = ""
                    while(zero_count > 0):
                        zero_str = zero_str + "0"
                        zero_count = zero_count - 1
                    bin_code = str.format("0{0}{1}", zero_str,binnumber)

                # C-指令
                if(parser.commandType() == Parser.CommandType.C_COMMAND):
                    c_dest = parser.dest()
                    c_comp = parser.comp()
                    c_jump = parser.jump()

                    bin_code = str.format("111{0}{1}{2}", code.comp(c_comp), code.dest(c_dest), code.jump(c_jump))

                # 输出二进制编码
                out_f.write(bin_code)
