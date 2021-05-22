from os import system
import sys
from JackTokenizer import JackTokenizer
from Comm import Token, Keyword

def debug_log(text):
    print("[%s: line %s] --> %s"%(__file__, sys._getframe(1).f_lineno, text))

class CompilationEngine:
    def __init__(self, tokenizer, outFile):
        self.tokenizer = tokenizer
        self.outFileFd = open(outFile, 'w+')
        self.TabNum = 0

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
                return self.checkDecVarName()
            else:
                return False

        return True

    def checkDecVarName(self):
        #todo 检查声明的变量名是否合法
        return True

    def checkSubroutineCall(self):
        #todo 检查子程序名是否合法
        # 
        return True

    def compileClass(self):
        self.beforeCompileXXX('class')

        # 标识符 className
        if not self.tokenizer.hasMoreTokens():
            debug_log('class has no className')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log('class need className as follow, %s is err'%self.tokenizer.cur_token)
            exit(-1)
        lClassName = self.tokenizer.identifier()
        self.writexml(self.tokenizer.token2xml())

        # 符号 '{'
        if not self.tokenizer.hasMoreTokens():
            debug_log('class has no \'{\'')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.SYMBOL:
            debug_log('class %s miss symbol \'{\''%lClassName)
            exit(-1)
        self.writexml(self.tokenizer.token2xml())
        
        while True:
            if not self.tokenizer.hasMoreTokens():
                break
            
            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()

            if tokenType == Token.KEYWORD:
                if self.tokenizer.keyword() in ['static', 'field']:
                    self.compileClassVarDec()
                    continue

                if self.tokenizer.keyword() in ['constructor', 'function', 'method']:
                    self.compileSubroutine()
                    continue

            if tokenType == Token.SYMBOL and self.tokenizer.symbol() == '}':
                self.writexml(self.tokenizer.token2xml())
                break

            debug_log("class %s, err token:%s"%(lClassName, self.tokenizer.cur_token))
            exit(-1)

        self.afterCompileXXX('class')

    def compileClassVarDec(self):
        self.beforeCompileXXX('classVarDec')

        # keyword
        self.writexml(self.tokenizer.token2xml())

        # 类型
        classVarDecBits = 0x00
        
        while True:
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileClassVarDec err")
                exit(-1)

            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()

            # 类型
            if (classVarDecBits & 0x01) <= 0:
                if not self.checkValidType():
                    debug_log('unknow var type \'%s\''%self.tokenizer.keyword())
                    exit(-1)

                self.writexml(self.tokenizer.token2xml())
                classVarDecBits |= 0x01
                continue

            # 变量名
            if (classVarDecBits & 0x10) <= 0:
                if tokenType != Token.IDENTIFIER:
                    debug_log("compileClassVarDec var name must be a valid identifier")
                    exit(-1)
                self.writexml(self.tokenizer.token2xml())
                classVarDecBits |= 0x10
                continue

            # ,
            if tokenType == Token.SYMBOL and self.tokenizer.symbol() == ',':
                self.writexml(self.tokenizer.token2xml())
                # 重置变量位
                classVarDecBits &= 0x01
                continue

            # ;
            if tokenType == Token.SYMBOL and self.tokenizer.symbol() == ';':
                self.writexml(self.tokenizer.token2xml())
                break

            debug_log("compileClassVarDec err token \'%s\'"%self.tokenizer.cur_token)
            exit(-1)

        self.afterCompileXXX('classVarDec')

    def compileSubroutine(self):
        self.beforeCompileXXX('subroutineBody')
        
        # keyword
        self.writexml(self.tokenizer.token2xml())

        # 
        subroutineBits = 0b1
        bParam = False
        
        while True:
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileClassVarDec err")
                exit(-1)

            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()

            # 类型
            if (subroutineBits & 0b1) > 0:
                if not self.checkValidType():
                    if tokenType != Token.KEYWORD or self.tokenizer.keyword() != 'void':
                        debug_log("err: invalid type \'%s\' subroutineBits"%(self.tokenizer.cur_token))
                        exit(-1)
                self.writexml(self.tokenizer.token2xml())
                subroutineBits <<= 1
                continue

            # 子程序名
            if (subroutineBits & 0b10) > 0:
                if tokenType != Token.IDENTIFIER:
                    debug_log("err: invalid identifier \'%s\'"%self.tokenizer.cur_token)
                    exit(-1)
                #todo 检查标识符名字
                self.writexml(self.tokenizer.token2xml())
                subroutineBits <<= 1
                continue
            
            # '('
            if (subroutineBits & 0b100) > 0:
                if tokenType != Token.SYMBOL or self.tokenizer.symbol() != '(':
                    debug_log("err: miss symbol \'(\'")
                    exit(-1)
                self.writexml(self.tokenizer.token2xml())

                # paramlist
                self.compileParameterList()

                # ')'
                if tokenType != Token.SYMBOL or self.tokenizer.symbol() != ')':
                    debug_log("err: miss symbol \')\'")
                    exit(-1)
                self.writexml(self.tokenizer.token2xml())
                subroutineBits <<= 1
                continue

            # '{'
            if (subroutineBits & 0b1000) > 0:
                if tokenType != Token.SYMBOL or self.tokenizer.symbol() != '{':
                    debug_log("err: miss symbol \'{\'")
                    exit(-1)
                self.writexml(self.tokenizer.token2xml())
                subroutineBits <<= 1
                continue

            # subroutineBody
            if (subroutineBits & 0b10000) > 0:
                # varDec statements
                if tokenType == Token.KEYWORD:
                    if self.tokenizer.keyword() == 'var':
                        self.compileVarDec()
                        continue
                    if self.tokenizer.keyword() in ['let', 'if', 'while', 'do', 'return']:
                        self.compileStatements()
                        # }
                        self.writexml(self.tokenizer.token2xml())
                        break
                    debug_log("err: invalid keyword %s "%self.tokenizer.keyword())
                    exit(-1)

                
                # }
                if tokenType == Token.SYMBOL and self.tokenizer.symbol() == '}':
                    self.writexml(self.tokenizer.token2xml())
                    break

                print(self.tokenizer.cur_token)
                debug_log("err: miss \'}\' ")
                exit(-1)


            debug_log("err: compiler invalid bit ")
            exit(-1)

        self.afterCompileXXX('subroutineBody')
        pass

    def compileParameterList(self):
        # type or ')'
        paramlistBits = 0b1
        while True:
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileParameterList err")
                exit(-1)

            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()

            # type or ')'
            if (paramlistBits & 0b1) > 0:
                if tokenType == Token.KEYWORD:
                    if self.checkValidType():
                        self.writexml(self.tokenizer.token2xml())
                        subroutineBits <<= 1
                        continue
                    else:
                        debug_log("err: invalid type \'%s\'"%self.tokenizer.cur_token)
                        exit(-1)
                    
                if tokenType == Token.SYMBOL and self.tokenizer.symbol() == ')':
                    break
                
                debug_log("err: invalid token \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
                
                
            # varName
            if (subroutineBits & 0b10) > 0:
                if tokenType != Token.IDENTIFIER:
                    debug_log("err: unknown identifier \'%s\'"%self.tokenizer.cur_token)
                    exit(-1)
                # 检查变量名
                self.writexml(self.tokenizer.token2xml())
                subroutineBits <<= 1

            # ',' or ')'
            if (subroutineBits & 0b100) > 0:
                if tokenType == Token.SYMBOL:
                    if self.tokenizer.symbol() == ')':
                        break
                    if self.tokenizer.symbol() == ',':
                        self.writexml(self.tokenizer.token2xml())
                        subroutineBits <<= 1
                        continue

                    debug_log("err: invalid symbol \'%s\'"%self.tokenizer.cur_token)
                    exit(-1)

                debug_log("err: invalid token \'%s\'"%self.tokenizer.cur_token)
                exit(-1)

            # type
            if (subroutineBits & 0b1000) > 0:
                if not self.checkValidType():
                    debug_log("err: invalid type \'%s\'"%self.tokenizer.cur_token)
                    exit(-1)

                self.writexml(self.tokenizer.token2xml())
                subroutineBits >>= 2
                continue
        

    def compileVarDec(self):
        self.beforeCompileXXX('varDec')

        # 'var' 
        self.writexml(self.tokenizer.token2xml())

        varDecBits = 0b1
        while True:
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileVarDec err")
                exit(-1)

            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()
        
            # type 
            if (varDecBits & 0b1) > 0:
                if self.checkValidType():
                    self.writexml(self.tokenizer.token2xml())
                    varDecBits <<= 1
                    continue
                
                debug_log("compileVarDec err: invalid type \'%s\'"%self.tokenizer.cur_token)
                exit(-1)

            # varName(',' varName)* ';'
            if (varDecBits & 0b10) > 0:
                if tokenType == Token.IDENTIFIER:
                    if self.checkDecVarName():
                        self.writexml(self.tokenizer.token2xml())
                        varDecBits <<= 1
                        continue
                    
                    debug_log("compileVarDec err: repeat declare var name \'%s\'"%self.tokenizer.cur_token)
                    exit(-1)

                debug_log("compileVarDec err: invalid varname \'%s\'"%self.tokenizer.cur_token)
                exit(-1)

            # ',' or ';'
            if (varDecBits & 0b100) > 0:
                if tokenType == Token.SYMBOL:
                    if self.tokenizer.symbol() == ',':
                        self.writexml(self.tokenizer.token2xml())
                        varDecBits >>= 1
                        continue

                    if self.tokenizer.symbol() == ';':
                        self.writexml(self.tokenizer.token2xml())
                        break
                
                debug_log("compileVarDec err: miss \',\' or \';\', invalid token \'%s\'"%self.tokenizer.cur_token)
                exit(-1)

            debug_log("compileVarDec err: invalid token \'%s\'"%self.tokenizer.cur_token)
            exit(-1)
                    
        self.afterCompileXXX('varDec')
        pass

    def compileStatements(self):
        self.beforeCompileXXX('statements')

        bFirst = True
        while True:
            if not bFirst:
                if not self.tokenizer.hasMoreTokens():
                    debug_log("compileStatements err")
                    exit(-1)

                self.tokenizer.advance()
                tokenType = self.tokenizer.tokenType()

            if self.tokenizer.keyword() == 'let':
                self.compileLet()
            if self.tokenizer.keyword() == 'if':
                self.compileIf()
            if self.tokenizer.keyword() == 'while':
                self.compileWhile()
            if self.tokenizer.keyword() == 'do':
                self.compileDo()
            if self.tokenizer.keyword() == 'return':
                self.compileReturn()

            break

        self.afterCompileXXX('statements')

    def compileDo(self):
        self.beforeCompileXXX('doStatement')

        # 'do'
        self.writexml(self.tokenizer.token2xml())


        
        doBits = 0b1
        while True:
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileVarDec err")
                exit(-1)

            self.tokenizer.advance()
            tokenType = self.tokenizer.tokenType()

            # identifier
            if ( doBits & 0b1) > 0:
                if tokenType == Token.IDENTIFIER:
                    self.writexml(self.tokenizer.token2xml())
                    doBits <<= 1
                    continue

                debug_log("compileDo err: invalid identifier \'%s\'"%self.tokenizer.cur_token)
                exit(-1)

            # '.' or '('
            if (doBits & 0b10) > 0:
                if tokenType == Token.SYMBOL:
                    if self.tokenizer.symbol() == '.':
                        self.writexml(self.tokenizer.token2xml())
                        doBits <<= 1
                        continue
                    if self.tokenizer.symbol() == '(':
                        self.writexml(self.tokenizer.token2xml())
                        doBits <<= 3
                        continue

            # .identifer
            if ( doBits & 0b100) > 0:
                if tokenType == Token.IDENTIFIER:
                    self.writexml(self.tokenizer.token2xml())
                    doBits <<= 1
                    continue

            # '('
            if ( doBits & 0b1000) > 0:
                if tokenType == Token.SYMBOL and self.tokenizer.symbol() == '(':
                    self.writexml(self.tokenizer.token2xml())
                    self.compileExpressionList()

                    if tokenType == Token.SYMBOL and self.tokenizer.symbol() == ')':
                        self.writexml(self.tokenizer.token2xml())
                        break
                



        self.writexml(sys._getframe().f_code.co_name + '\n')
        self.afterCompileXXX('doStatement')
        pass

    def compileLet(self):
        self.beforeCompileXXX('letStatement')
        self.writexml(sys._getframe().f_code.co_name + '\n')
        self.afterCompileXXX('letStatement')
        pass

    def compileWhile(self):
        self.beforeCompileXXX('whileStatement')
        self.writexml(sys._getframe().f_code.co_name + '\n')
        self.afterCompileXXX('whileStatement')
        pass

    def compileReturn(self):
        self.beforeCompileXXX('returnStatement')
        self.writexml(sys._getframe().f_code.co_name + '\n')
        self.afterCompileXXX('returnStatement')
        pass

    def compileIf(self):
        self.beforeCompileXXX('ifStatement')
        self.writexml(sys._getframe().f_code.co_name + '\n')
        self.afterCompileXXX('ifStatement')
        pass

    def compileExpression(self):
        self.writexml(sys._getframe().f_code.co_name + '\n')
        pass

    def compileTerm(self):
        self.writexml(sys._getframe().f_code.co_name + '\n')
        pass

    def compileExpressionList(self):
        self.writexml(sys._getframe().f_code.co_name + '\n')
        pass

