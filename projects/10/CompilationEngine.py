from os import system
import sys
from JackTokenizer import JackTokenizer
from Comm import Token, Keyword

def debug_log(text, stack = 1):
    #SymbolTable.symbolTable.printTable()
    print("[%s: line %s] --> %s"%(__file__, sys._getframe(stack).f_lineno, text))

class CompilationEngine:
    def __init__(self, tokenizer, outFile):
        self.tokenizer = tokenizer
        self.outFileFd = open(outFile, 'w+')
        self.TabNum = 0
        self.funcStack = []

    def writexml(self, text):
        self.outFileFd.write(self.TabNum * '\t')
        self.outFileFd.write(text)

    def beforeCompileXXX(self, text):
        self.writexml('<' + text + '>\n')
        self.TabNum += 1

    def afterCompileXXX(self, text):
        self.TabNum -= 1
        self.writexml('</' + text + '>\n')

    def checkValidType(self):
        tokenType = self.tokenizer.tokenType()
        if tokenType == Token.KEYWORD:
            if self.tokenizer.keyword() in ['int', 'char', 'boolean']:
                pass
            else:
                return False
        else:
            if tokenType == Token.IDENTIFIER:
                return True
            else:
                return False

        return True
    
    def checkCompileSymbol(self, symbol):
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss symbol \'%s\'"%symbol, 2)
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.SYMBOL or self.tokenizer.symbol() != symbol:
            debug_log("err: miss symbol \'%s\' before \'%s\'"%(symbol, self.tokenizer.symbol()), 2)
            exit(-1)
        self.writexml(self.tokenizer.tokenStr())

    def compileClass(self):
        self.beforeCompileXXX('class')

        if not self.tokenizer.hasMoreTokens():
            debug_log("err: empty file")
            exit
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.KEYWORD:
            debug_log("err: must start with class %s tokentype:%s"%(self.tokenizer.cur_token, self.tokenizer.tokenType()))
            exit
        if self.tokenizer.keyword() != 'class':
            debug_log("err: must start with class %s keyword:%s"%(self.tokenizer.cur_token, self.tokenizer.keyword()))
            exit
        self.writexml(self.tokenizer.tokenStr())

        # 标识符 className
        if not self.tokenizer.hasMoreTokens():
            debug_log('class has no className')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log('class need className as follow, %s is err'%self.tokenizer.cur_token)
            exit(-1)
        lClassName = self.tokenizer.identifier()
        self.writexml(self.tokenizer.tokenStr())
        self.className = lClassName

        # 符号 '{'
        if not self.tokenizer.hasMoreTokens():
            debug_log('class has no \'{\'')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.SYMBOL:
            debug_log('class %s miss symbol \'{\''%lClassName)
            exit(-1)
        self.writexml(self.tokenizer.tokenStr())
        
        while True:
            if not self.tokenizer.hasMoreTokens():
                break

            if self.tokenizer.next_token in ['static', 'field']:
                self.compileClassVarDec()
                continue

            if self.tokenizer.next_token in ['constructor', 'function', 'method']:
                self.compileSubroutine()
                continue

            if self.tokenizer.next_token == '}':
                self.tokenizer.advance()
                self.writexml(self.tokenizer.tokenStr())
                break

            debug_log("class %s, err token:%s"%(lClassName, self.tokenizer.cur_token))
            exit(-1)

        self.afterCompileXXX('class')

    def compileClassVarDec(self):
        self.beforeCompileXXX('classVarDec')

        # keyword
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        # 类型
        if not self.tokenizer.hasMoreTokens():
            debug_log("compileClassVarDec err: miss var type")
            exit(-1)
        self.tokenizer.advance()
        if not self.checkValidType():
            debug_log('unknow var type \'%s\''%self.tokenizer.keyword())
            exit(-1)
        self.writexml(self.tokenizer.tokenStr())

        while True:
            # 变量名
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileClassVarDec err: miss var name")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("compileClassVarDec err: miss 'identifier' before \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
            self.writexml(self.tokenizer.tokenStr())

            if not self.tokenizer.hasMoreTokens():
                break

            # ,
            if self.tokenizer.next_token == ',':
                self.tokenizer.advance()
                self.writexml(self.tokenizer.tokenStr())
                continue

            break

        # ;
        self.checkCompileSymbol(';')

        self.afterCompileXXX('classVarDec')

    def compileSubroutine(self):
        self.beforeCompileXXX('subroutineDec')
        
        # keyword
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        # 类型 or void
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss subroutine type")
            exit(-1)
        self.tokenizer.advance()
        if not self.checkValidType():
            if self.tokenizer.tokenType() != Token.KEYWORD or self.tokenizer.keyword() != 'void':
                debug_log("err: invalid type \'%s\' "%(self.tokenizer.cur_token))
                exit(-1)
        self.writexml(self.tokenizer.tokenStr())

        # 子程序名
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss identifier")
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log("err: invalid identifier \'%s\'"%self.tokenizer.cur_token)
            exit(-1)
        self.writexml(self.tokenizer.tokenStr())
        self.funcStack.insert(0, self.tokenizer.identifier())

        # '('
        self.checkCompileSymbol('(')
        # paramlist
        self.compileParameterList()
        # ')'
        self.checkCompileSymbol(')')
        
        # subroutineBody
        self.beforeCompileXXX('subroutineBody')
        # '{'
        self.checkCompileSymbol('{')
        while True:
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss symbol \'}\'")
                exit(-1)
            # varDec 
            if self.tokenizer.next_token == 'var':
                self.compileVarDec()
                continue
            # statements
            if self.tokenizer.next_token in ['let', 'if', 'while', 'do', 'return']:
                self.compileStatements()
                continue

            break
        # '}'
        self.checkCompileSymbol('}')
        self.afterCompileXXX('subroutineBody')
        
        self.funcStack.pop()

        self.afterCompileXXX('subroutineDec')

    def compileParameterList(self): 
        self.beforeCompileXXX('parameterList')
        while True:
            # type
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss param type")
                exit(-1)
            if self.tokenizer.nextTokenType() != Token.KEYWORD and self.tokenizer.nextTokenType() != Token.IDENTIFIER:
                break
            self.tokenizer.advance()
            if not self.checkValidType():
                debug_log('unknow var type \'%s\''%self.tokenizer.cur_token)
                exit(-1)
            self.writexml(self.tokenizer.tokenStr())

            # varName
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss param varName")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("err: unknown identifier \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
            self.writexml(self.tokenizer.tokenStr())

            # ','
            if not self.tokenizer.hasMoreTokens():
                break
            if self.tokenizer.next_token != ',':
                break
            self.tokenizer.advance()
            self.writexml(self.tokenizer.tokenStr())

        self.afterCompileXXX('parameterList')
        

    def compileVarDec(self):
        self.beforeCompileXXX('varDec')

        # 'var' 
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        # type
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss var type")
            exit(-1)
        self.tokenizer.advance()
        if not self.checkValidType():
            debug_log('unknow var type \'%s\''%self.tokenizer.cur_token)
            exit(-1)
        self.writexml(self.tokenizer.tokenStr())
        varType = self.tokenizer.cur_token

        while True:
            # varName(',' varName)*
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss varName")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("err: invalid identifier \'%s\'"%self.tokenizer.tokenStr())
                exit(-1)
            self.writexml(self.tokenizer.tokenStr())

            # ','
            if not self.tokenizer.hasMoreTokens() :
                break
            if self.tokenizer.next_token != ',':
                break

            self.tokenizer.advance()
            self.writexml(self.tokenizer.tokenStr())
                    
        # ';'
        self.checkCompileSymbol(';')

        self.afterCompileXXX('varDec')

    def compileStatements(self):
        self.beforeCompileXXX('statements')

        while True:
            if not self.tokenizer.hasMoreTokens():
                break

            if self.tokenizer.next_token == 'let':
                self.compileLet()
            elif self.tokenizer.next_token == 'if':
                self.compileIf()
            elif self.tokenizer.next_token == 'while':
                self.compileWhile()
            elif self.tokenizer.next_token == 'do':
                self.compileDo()
            elif self.tokenizer.next_token == 'return':
                self.compileReturn()
            else:
                break

        self.afterCompileXXX('statements')

    def compileDo(self):
        self.beforeCompileXXX('doStatement')

        # 'do'
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        # subroutimeName | (className|varName).subroutineName
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss subroutimeName | (className|varName)")
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log("compileDo err: invalid identifier \'%s\'"%self.tokenizer.cur_token)
            exit(-1)            
        self.writexml(self.tokenizer.tokenStr())

        # 
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss \'(\'")
            exit(-1)

        if self.tokenizer.next_token == '.':
            self.tokenizer.advance()
            self.writexml(self.tokenizer.tokenStr())
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss subroutimeName after \'.\'")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("err: invalid subroutimeName \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
            self.writexml(self.tokenizer.tokenStr())

        # '('
        self.checkCompileSymbol('(')
        # expressionlist
        self.expressionListEndToken = ')'
        self.compileExpressionList()
        # ')'
        self.checkCompileSymbol(')')
        # ';'
        self.checkCompileSymbol(';')
                
        self.afterCompileXXX('doStatement')

    def compileLet(self):
        self.beforeCompileXXX('letStatement')

        # let
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())
        
        # varName
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss varName")
            exit(-1)
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        # ('[' expression ']')?
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss varName")
            exit(-1)
        if self.tokenizer.next_token == '[':
            self.tokenizer.advance()
            self.writexml(self.tokenizer.tokenStr())
            
            # expression
            self.compileExpression()

            # ']'
            self.checkCompileSymbol(']')
            
        # '='      
        self.checkCompileSymbol('=')      
        # expression
        self.compileExpression()
        # ';'
        self.checkCompileSymbol(';')

        self.afterCompileXXX('letStatement')

    def compileWhile(self):
        self.beforeCompileXXX('whileStatement')

        # while
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        # '('
        self.checkCompileSymbol('(')
        # expresssion
        self.compileExpression()
        # ')'
        self.checkCompileSymbol(')')
        # '{'
        self.checkCompileSymbol('{')
        # statements
        self.compileStatements()
        # '}'
        self.checkCompileSymbol('}')

        self.afterCompileXXX('whileStatement')

    def compileReturn(self):
        self.beforeCompileXXX('returnStatement')

        # return
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())

        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss \';\'")
            exit(-1)
        if self.tokenizer.next_token != ';':
            self.compileExpression()

        # ';'
        self.checkCompileSymbol(';')
        
        self.afterCompileXXX('returnStatement')

    def compileIf(self):
        self.beforeCompileXXX('ifStatement')
        
        # if
        self.tokenizer.advance()
        self.writexml(self.tokenizer.tokenStr())
        
        # '('
        self.checkCompileSymbol('(')
        # expression
        self.compileExpression()
        # ')'
        self.checkCompileSymbol(')')
        # '{'
        self.checkCompileSymbol('{')
        # statements
        self.compileStatements()
        # '}'
        self.checkCompileSymbol('}')

        # 'else' {}
        if self.tokenizer.hasMoreTokens() :
            if self.tokenizer.next_token == 'else':
                self.tokenizer.advance()
                self.writexml(self.tokenizer.tokenStr())
                # '{'
                self.checkCompileSymbol('{')
                # statements
                self.compileStatements()
                # '}'
                self.checkCompileSymbol('}')

        self.afterCompileXXX('ifStatement')

    def compileExpression(self):
        self.beforeCompileXXX('expression')

        while True:
            self.compileTerm()
            
            if not self.tokenizer.hasMoreTokens() :
                break

            if self.tokenizer.next_token in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                self.tokenizer.advance()
                self.writexml(self.tokenizer.tokenStr())
                continue
            break
        
        self.afterCompileXXX('expression')
        pass

    def compileTerm(self):
        self.beforeCompileXXX('term')

        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: invalid term")
            exit(-1)

        while True:
            tokenType = self.tokenizer.nextTokenType()
            if tokenType == Token.INT_CONST or tokenType == Token.STRING_CONST:
                self.tokenizer.advance()
                self.writexml(self.tokenizer.tokenStr())
                break
            if tokenType == Token.KEYWORD:
                self.tokenizer.advance()
                if self.tokenizer.keyword() not in ['true', 'false', 'null', 'this']:
                    debug_log("err: term can't use keyword \'%s\'"%self.tokenizer.keyword())
                    exit(-1)
                self.writexml(self.tokenizer.tokenStr())
                break
            if tokenType == Token.SYMBOL:
                if self.tokenizer.next_token in ['-', '~']:
                    self.tokenizer.advance()
                    self.writexml(self.tokenizer.tokenStr())
                    self.compileTerm()
                    break
                if self.tokenizer.next_token == '(':
                    self.tokenizer.advance()
                    self.writexml(self.tokenizer.tokenStr())
                    self.compileExpression()
                    self.checkCompileSymbol(')')
                    break
            
            if tokenType == Token.IDENTIFIER:
                self.tokenizer.advance()
                self.writexml(self.tokenizer.tokenStr())
                if not self.tokenizer.hasMoreTokens():
                    break

                if self.tokenizer.next_token == '[':
                    self.tokenizer.advance()
                    self.writexml(self.tokenizer.tokenStr())
                    self.compileExpression()
                    self.checkCompileSymbol(']')
                    break

                if self.tokenizer.next_token == '(':
                    self.tokenizer.advance()
                    self.writexml(self.tokenizer.tokenStr())
                    self.expressionListEndToken = ')'
                    self.compileExpressionList()
                    self.checkCompileSymbol(')')
                    break

                if self.tokenizer.next_token == '.':
                    self.tokenizer.advance()
                    self.writexml(self.tokenizer.tokenStr())
                    if not self.tokenizer.hasMoreTokens():
                        debug_log("err: expected 'identifier' after '.'")
                        exit(-1)
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() != Token.IDENTIFIER:
                        debug_log("err: expected 'identifier' before \'%s\''"%self.tokenizer.cur_token)
                        exit(-1)
                    self.writexml(self.tokenizer.tokenStr())
                    self.checkCompileSymbol('(')
                    self.expressionListEndToken = ')'
                    self.compileExpressionList()
                    self.checkCompileSymbol(')')

            break
        
        self.afterCompileXXX('term')

    def compileExpressionList(self):
        self.beforeCompileXXX('expressionList')
        
        if self.tokenizer.hasMoreTokens():
            if self.expressionListEndToken == None or self.tokenizer.next_token != self.expressionListEndToken:
                while True:
                    self.compileExpression()

                    if not self.tokenizer.hasMoreTokens() :
                        break
                    if self.tokenizer.next_token == ',':
                        self.tokenizer.advance()
                        self.writexml(self.tokenizer.tokenStr())
                        continue
                    break

        self.expressionListEndToken = None

        self.afterCompileXXX('expressionList')

