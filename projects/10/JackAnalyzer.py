import os
import sys

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

if len(sys.argv) < 2:
    sys.exit(" use python %s : file | path "%sys.argv[0])

source = sys.argv[1]

def __analyzeFile(file):

    tokenizer = JackTokenizer(file)

    # 字元转换器输出
    # outFile = os.path.dirname(file) + os.path.sep + os.path.basename(file).split('.')[0] + 'T.xml'
    # outFileFd = open(outFile, 'w+')
    # tokenizer.outputxml(outFileFd)

    # 语法分析器
    outFile = os.path.dirname(file) + os.path.sep + os.path.basename(file).split('.')[0] + '.xml'
    compilationEngine = CompilationEngine(tokenizer, outFile)
    compilationEngine.compileClass()

def __analyzeDir(dir):
    files = os.listdir(dir)
    for f in files:
        if f.split('.')[-1] != 'jack':
            continue
        __analyzeFile(os.path.join(dir, f))
    # for root, dirs, files in os.walk(dir):
    #     for f in files:
    #         if f.split('.')[-1] != 'jack':
    #             continue
    


def __analyze(source_param):

    if os.path.isfile(source_param):
        __analyzeFile(source_param)
        return

    if os.path.isdir(source_param):
        __analyzeDir(source_param)
        return

__analyze(source)

