import os
import sys

from JackTokenizer import JackTokenizer

if len(sys.argv) < 2:
    sys.exit(" use python %s : file | path "%sys.argv[0])

source = sys.argv[1]

def __analyzeFile(file):

    tokenizer = JackTokenizer(file)

    i = 10
    while True:
        if not tokenizer.hasMoreTokens():
            break
        tokenizer.advance()
        print(tokenizer.cur_token, tokenizer.tokenType())

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

