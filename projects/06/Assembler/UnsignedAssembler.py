import os
import Parser
import Code

file = r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\max\MaxL.asm'
file_dir = os.path.dirname(file)
file_name = os.path.basename(file)
file_name = file_name.split('.')[0]

out_suffix = r'.hack'
out_file_name = file_name + out_suffix
out_file = file_dir + os.path.sep + out_file_name

parser = Parser.Parser(file)
code = Code.Code()

with open(out_file, 'w') as out_f:
    newline = False
    while(parser.hasMoreCommands()):
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
