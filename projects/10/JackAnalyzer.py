import os
import sys

from JackTokenizer import JackTokenizer

if len(sys.argv) < 2:
    sys.exit(" use python %s : file | path "%sys.argv[0])

source = sys.argv[1]

def __analyzeFile(file):

    tokenizer = JackTokenizer(file)

    tokenizer.hasMoreTokens()
    pass

def __analyzeDir(dir):
    pass


def __analyze(source_param):

    if os.path.isfile(source_param):
        __analyzeFile(source_param)
        return

    if os.path.isdir(source_param):
        __analyzeDir(source_param)
        return

__analyze(source)

