from Parser import Parser
from CodeWriter import CodeWriter
from Common import VMCommandType
import os
import sys

if len(os.sys.argv) < 2:
    sys.exit("use %s file|path"%os.sys.argv[0])

def __getDirFileR(dir, path_dict):
    path_dict={
        'name':dir,
        'file':[],
        'dir':{}
    }
    l = os.listdir(dir)
    for f in l:
        cur = os.path.join(dir, f)
        if os.path.isfile(cur):
            if cur.split('.')[-1] != 'vm':
                continue
            path_dict['file'].append(cur)
            continue
        if os.path.isdir(cur):
            path_dict['dir'][cur] = {}                      
            __getDirFileR(cur, path_dict[cur])

def __parseFile(codeWriter, out_file, parse_file):
    parser = Parser(parse_file)
    codeWriter.setFileName(out_file, parse_file)

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == VMCommandType.C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())

        if parser.commandType() in [VMCommandType.C_PUSH, VMCommandType.C_POP]:
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())

        if parser.commandType() == VMCommandType.C_LABEL:
            codeWriter.writeLabel(parser.arg1())

        if parser.commandType() == VMCommandType.C_GOTO:
            codeWriter.writeGoto(parser.arg1())

        if parser.commandType() == VMCommandType.C_IF:
            codeWriter.writeIf(parser.arg1())

        if parser.commandType() == VMCommandType.C_FUNCTION:
            codeWriter.writeFunction(parser.arg1(), parser.arg2())

        if parser.commandType() == VMCommandType.C_RETURN:
            codeWriter.writeReturn()

        if parser.commandType() == VMCommandType.C_CALL:
            codeWriter.writeCall(parser.arg1(), parser.arg2())

def __parseDir(codeWriter, parse_dir):
    out_file = parse_dir + os.path.sep + os.path.basename(parse_dir) + '.asm'

    l = os.listdir(parse_dir)
    for f in l:
        cur = os.path.join(parse_dir, f)
        if os.path.isfile(cur):
            if cur.split('.')[-1] != 'vm':
                continue
            __parseFile(codeWriter, out_file, cur)
        if os.path.isdir(cur):
            __parseDir(codeWriter, cur)

def translate(file_arg):
    codeWriter = CodeWriter()
    #path_dict = {'file':[]} 

    # 文件
    if os.path.isfile(file_arg):
        ___out_file = file_arg.rsplit('.', 1)[0] + '.asm'
        __parseFile(codeWriter, ___out_file, file_arg)  

    # 目录
    if os.path.isdir(file_arg):
        #__getDirFileR(file_arg, path_dict)  
        __parseDir(codeWriter, file_arg)

    codeWriter.Close()
    
    
file_arg = os.sys.argv[1] 
translate(file_arg)