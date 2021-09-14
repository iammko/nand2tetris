import os
from Comm import Token, Keyword

class JackTokenizer:
    def __init__(self, file):
        self.fd = open(file, 'r')
        self.cur_token = ''
        self.next_token = ''
        self.cur_line = ''
        self.lineNum = 0
        # 是否在注释块当中
        self.inCommentBlock = False
        # 是否在双引号中
        self.inDoubleQuote = False
        
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

            curStr = ''
            newLine = ''
            for c in line:
                curStr += c
                # 在注释块当中
                if self.inCommentBlock:
                    if curStr == '*':
                        continue                    
                    if curStr == '*/':
                        self.inCommentBlock = False
                    curStr = ''
                    continue

                # 不在注释块中

                # 双引号
                if curStr == '"':
                    self.inDoubleQuote = not self.inDoubleQuote

                # 不在双引号中
                if not self.inDoubleQuote:
                    # 判断注释字符
                    if curStr == '/':
                        continue

                    # 判断是不是块注释
                    if curStr == '/*':
                        curStr = ''
                        self.inCommentBlock = True
                        continue

                    # 判断是不是行注释
                    if curStr == '//':
                        curStr = ''
                        break

                newLine += curStr
                curStr = ''
            
            if newLine == '':
                continue

            self.cur_line = newLine
            return True
        self.lineNum += 1

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

    def nextTokenType(self):
        if self.next_token in self.keywordList:
            return Token.KEYWORD

        if self.next_token in self.symbolList:
            return Token.SYMBOL

        if self.next_token.isidentifier():
            return Token.IDENTIFIER

        if self.next_token.isnumeric():
            return Token.INT_CONST

        if len(self.next_token) > 2 and self.next_token[0] == '"' and self.next_token[-1] == '"' :
            return Token.STRING_CONST

        print('err: illegal token > %s <'%self.next_token)
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
            