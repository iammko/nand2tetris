from os import system
from JackTokenizer import JackTokenizer
from Comm import Token, Keyword

class CompilationEngine:
    def __init__(self, tokenizer, outFile):
        self.tokenizer = tokenizer
        self.outFileFd = open(outFile, 'w+')
        self.TabNum = -1

        if not self.tokenizer.hasMoreTokens():
            print("err: empty file")
            exit

        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.KEYWORD:
            print("err: must start with class %s tokentype:%s"%(self.tokenizer.cur_token, self.tokenizer.tokenType()))
            exit
    
        if self.tokenizer.keyword() != 'class':
            print("err: must start with class %s keyword:%s"%(self.tokenizer.cur_token, self.tokenizer.keyword()))
            exit

    def writexml(self, text):
        self.outFileFd.write(self.TabNum * '\t')
        self.outFileFd.write(text)

    def compileClass(self):
        self.TabNum += 1
        self.writexml('<class>\n')

        # 标识符 className
        if not self.tokenizer.hasMoreTokens():
            print('class has no className')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            print('class need className as follow, %s is err'%self.tokenizer.cur_token)
            exit(-1)
        lClassName = self.tokenizer.identifier()
        self.writexml(self.tokenizer.token2xml())

        # 符号 '{'
        if not self.tokenizer.hasMoreTokens():
            print('class has no \'{\'')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.SYMBOL:
            print('class %s miss symbol \'{\''%lClassName)
            exit(-1)
        self.writexml(self.tokenizer.token2xml())
        
        while True:
            if not self.tokenizer.hasMoreTokens():
                break
            
            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()
            if tokenType == Token.SYMBOL and self.tokenizer.symbol() == '}':
                self.writexml(self.tokenizer.token2xml())
                self.writexml('</class>\n')

            if tokenType == Token.KEYWORD:
                if self.tokenizer.keyword() in ['static', 'field']:
                    self.compileClassVarDec()
                    continue

                if self.tokenizer.keyword() in ['constructor', 'function', 'method']:
                    self.compileSubroutine()
                    continue

            print("class %s, err token:%s"%(lClassName, self.tokenizer.cur_token))
            exit(-1)

        self.TabNum -= 1


    def compileClassVarDec(self):
        self.TabNum += 1

        # keyword
        self.writexml(self.tokenizer.token2xml())
        
        # 类型
        if not self.tokenizer.hasMoreTokens():
            print("compileClassVarDec err")
            exit

        self.tokenizer.advance()
        tokenType = self.tokenizer.tokenType()
        if tokenType == Token.KEYWORD:
            if self.tokenizer.keyword() in ['int', 'char', 'boolean']:
                self.writexml(self.tokenizer.token2xml())

        if tokenType == Token.IDENTIFIER:
            self.writexml(self.tokenizer.token2xml())

        # 变量名, 变量名
        while True:
            if not self.tokenizer.hasMoreTokens():
                print("compileClassVarDec err")
                exit

        self.TabNum -= 1


        

    def compileSubroutine(self):
        self.TabNum += 1
        self.writexml(__name__ + '\n')
        self.TabNum -= 1
        pass

    def compileParameterList(self):
        self.writexml(__name__ + '\n')
        pass

    def compileVarDec(self):
        self.writexml(__name__ + '\n')
        pass

    def compileStatements(self):
        self.writexml(__name__ + '\n')
        pass

    def compileDo(self):
        self.writexml(__name__ + '\n')
        pass

    def compileLet(self):
        self.writexml(__name__ + '\n')
        pass

    def compileWhile(self):
        self.writexml(__name__ + '\n')
        pass

    def compileReturn(self):
        self.writexml(__name__ + '\n')
        pass

    def compileIf(self):
        self.writexml(__name__ + '\n')
        pass

    def compileExpression(self):
        self.writexml(__name__ + '\n')
        pass

    def compileTerm(self):
        self.writexml(__name__ + '\n')
        pass

    def compileExpressionList(self):
        self.writexml(__name__ + '\n')
        pass

