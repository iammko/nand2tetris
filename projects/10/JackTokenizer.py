import os
from Comm import Token, Keyword

class JackTokenizer:
    def __init__(self, file):
        self.fd = open(file, 'r')
        self.cur_token = ''
        self.next_token = ''
        self.cur_line = ''
        # 是否在注释块当中
        self.inCommentBlock = False
        
        self.keywordList = ['class', 'constructor', 'function', 'method', 'field', 'static', 
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 
            'let', 'do', 'if', 'else', 'while', 'return']
        self.symbolList = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    
    def parseNewLine(self):
        readFlag = True
        line = ''
        while True:
            if readFlag:
                line = self.fd.readline()
                if line == '':
                    return False

            line = line.strip()

            startCommentPos = 0

            # 注释块 /* */
            if self.inCommentBlock == False:
                startCommentPos = line.find('/*')
                if startCommentPos != -1:
                    self.inCommentBlock = True

            if self.inCommentBlock:
                endCommentPos = line.find('*/', startCommentPos)
                if endCommentPos == -1:
                    # 仍然在注释块中
                    continue
                
                # 删除注释部分
                #print(line)
                newLine = ""
                if startCommentPos > 0:
                    newLine = line[: startCommentPos] + ' '
                newLine = newLine + line[endCommentPos + 2 : ]
                line = newLine

                # 剩下语句重新解析
                self.inCommentBlock = False
                readFlag = False
                continue

            readFlag = True

            # 行注释
            commentIdx = line.find('//')

            # 行首注释 //
            if commentIdx == 0:
                continue

            # 行后注释 var int a; //
            # 前面奇数个双引号表示在双引号当中,考虑到双引号出现只能是字符串, 并且不允许出现在表达式当中
            if commentIdx != -1:
                while True:
                    #print("[%s] find '//' at %d"%(line, commentIdx))
                    doublequoteNum = line.count(r'"', 0, commentIdx)
                    if doublequoteNum != 1:
                        # '//' 不在双引号当中
                        line = line[0:commentIdx]
                        break
                    
                    #print("at %d, '//' is in \" \" "%commentIdx)
                    # '//' 在双引号当中, 查找下一个
                    commentIdx = line.find('//', commentIdx + 2)
                    if commentIdx == -1:
                        # 没有了
                        break
            
            if line == '':
                continue

            self.cur_line = line
            return True

    # 解析当前行的token, 解析出token返回true, 解析完了返回false
    def parseToken(self):
        if self.cur_line == '':
            return False
        
        # 解析一行的token
        bInDoubleQuote = False
        while self.cur_line != '':
            c = self.cur_line[0]

            # 是否将当前字符从当前行移除
            bRmvChar = True
            # 是否将当前字符加入token
            bAddToToken = True
            # 是否返回字元
            bReturnToken = False

            # 字符串
            if c == '"':
                if bInDoubleQuote == False:
                    bInDoubleQuote = True
                    # 有已解析的token
                    if self.next_token != '':
                        bRmvChar = False
                        bAddToToken = False
                        bReturnToken = True
                else:
                    # 第二个双引号
                    bReturnToken = True

            # 空格
            if not bInDoubleQuote and c.isspace():
                # 没有已解析的token, 继续解析
                bAddToToken = False
                if self.next_token != '':
                # 有已解析的token
                    bReturnToken = True
            
            # 字元符号
            if not bInDoubleQuote and c in self.symbolList:
                # 没有已解析的token, 当前符号作为解析的token
                if self.next_token == '':
                    bReturnToken = True
                else:
                # 有已解析的
                    bAddToToken = False
                    bRmvChar = False
                    bReturnToken = True

            if bRmvChar:
                if len(self.cur_line) == 1:
                    self.cur_line = ''
                else:
                    self.cur_line = self.cur_line[1:]

            if bAddToToken:
                self.next_token = self.next_token + c

            if bReturnToken:
                if self.next_token != '':
                    return True
    
        return False


    def hasMoreTokens(self):
        if self.next_token != '':
            return True

        # 检查是否还有内容
        if self.cur_line == '':
            if self.parseNewLine() == False:
                return False

        # 解析行
        if self.parseToken():
            #print(self.next_token)
            return True

        # 递归新行
        return self.hasMoreTokens()

    def advance(self):
        self.cur_token = self.next_token
        self.next_token = ''

    def tokenType(self):
        if self.cur_token in self.keywordList:
            return Token.KEYWORD

        if self.cur_token in self.symbolList:
            return Token.SYMBOL

        if self.cur_token.isidentifier():
            return Token.IDENTIFIER

        if self.cur_token.isnumeric():
            return Token.INT_CONST

        if len(self.cur_token) > 2 and self.cur_token[0] == '"' and self.cur_token[-1] == '"' :
            return Token.STRING_CONST

        print('err: illegal token > %s <'%self.cur_token)
        exit(-1)

    def keyword(self):
        return self.cur_token

    def symbol(self):
        return self.cur_token
 
    def identifier(self):
        return self.cur_token

    def intVal(self):
        return (int)(self.cur_token)

    def stringVal(self):
        return self.cur_token.replace('"','')

    def tokenStr(self):
        tokenType = self.tokenType()
        if tokenType == Token.KEYWORD:
            return '<keyword> ' + self.keyword()  + ' </keyword>'+ '\n'
        if tokenType == Token.SYMBOL:
            out_token = self.symbol()       
            if self.cur_token == '<':
                out_token = '&lt;'
            if self.cur_token == '>':
                out_token = '&gt;'
            if self.cur_token == '&':
                out_token = '&amp;'
            return '<symbol> ' + out_token + ' </symbol>' + '\n'
        if tokenType == Token.IDENTIFIER:
            return '<identifier> ' + self.identifier() + ' </identifier>'+ '\n'
        if tokenType == Token.INT_CONST:
            return '<integerConstant> ' + (str)(self.intVal()) + ' </integerConstant>'+ '\n'
        if tokenType == Token.STRING_CONST:
            return '<stringConstant> ' + self.stringVal() + ' </stringConstant>'+ '\n'

        print("err: tokenType %s is err type"%tokenType)
        exit(-1)
    
    def outputxml(self, outFile):
        outFile.write('<tokens>\n')
        while True:
            if not self.hasMoreTokens():
                break
            self.advance()
            outFile.write('\t'+self.token2xml())
        outFile.write('</tokens>\n')
            