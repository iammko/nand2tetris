from Parser import Parser
from CodeWriter import CodeWriter
from Common import VMCommandType
import os
import sys

if len(os.sys.argv) < 2:
    sys.exit("use %s file|path"%os.sys.argv[0])

def __getDirFileR(dir):
    file_list = []
    l = os.listdir(dir)
    for f in l:
        cur_f = os.path.join(dir, f)
        if os.path.isfile(cur_f):
            if cur_f.split('.')[-1] != 'vm':
                continue
            file_list.append(cur_f)
            continue
        if os.path.isdir(cur_f):
            file_list.extend(__getDirFileR(cur_f))
    
    return file_list

file_arg = os.sys.argv[1]
file_list = []

# 文件
if os.path.isfile(file_arg):
    file_list.append(file_arg)

# 目录
if os.path.isdir(file_arg):
    file_list = __getDirFileR(file_arg)

if file_list is None:
    sys.exit("No such file or directory:'%s'"%file_arg)

codeWriter = CodeWriter()
for f in file_list:
    parser = Parser(f)

    out_file = f.split('.', 1)[0] + '.asm'
    codeWriter.setFileName(out_file)

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == VMCommandType.C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())

        if parser.commandType() in [VMCommandType.C_PUSH, VMCommandType.C_POP]:
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())

    
codeWriter.Close()