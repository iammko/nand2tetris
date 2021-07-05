from os import system
import sys
from JackTokenizer import JackTokenizer
from Comm import Token, Keyword, VMSegment, VMCommand, SymbolTableKind
from SymbolTable import symbolTable, SymbolTable
from VMWriter import VMWriter

def debug_log(text, stack = 1):
    #SymbolTable.symbolTable.printTable()
    print("[%s: line %s] --> %s"%(__file__, sys._getframe(stack).f_lineno, text))

op_privilege = {
    '+':5, '-':5, 
    '*':6, '/':6, 
    '&':4, '|':4, 
    '<':3, '>':3, 
    '=':2
}

class CompilationEngine:
    def __init__(self, tokenizer, outFile):
        self.tokenizer = tokenizer
        #self.outFileFd = open(outFile, 'w+')
        self.vmWriter = VMWriter(outFile)
        self.outFile = outFile
        self.TabNum = 0
        self.funcStack = []
        self.symbolTable = None
        self.whileInc = 0
        self.ifInc = 0

    def __del__(self):
        self.vmWriter.close()

    def writexml(self, text):
        return
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

        # 标识符 className
        if not self.tokenizer.hasMoreTokens():
            debug_log('class has no className')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log('class need className as follow, %s is err'%self.tokenizer.cur_token)
            exit(-1)
        self.className = self.tokenizer.identifier()
        if symbolTable.get(self.className) != None:
            debug_log('err: repeat class \'%s\''%self.className)
            exit(-1)
        symbolTable[self.className] = SymbolTable()
        self.symbolTable = symbolTable[self.className]

        # 符号 '{'
        if not self.tokenizer.hasMoreTokens():
            debug_log('class has no \'{\'')
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.SYMBOL:
            debug_log('class %s miss symbol \'{\''%self.className)
            exit(-1)
        
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
                break

            debug_log("class %s, err token:%s"%(self.className, self.tokenizer.cur_token))
            exit(-1)

    def compileClassVarDec(self):
        # keyword
        self.tokenizer.advance()
        if self.tokenizer.keyword() == 'static':
            varKind = SymbolTableKind.STATIC
        else: # 'field'
            varKind = SymbolTableKind.FIELD

        # 类型
        if not self.tokenizer.hasMoreTokens():
            debug_log("compileClassVarDec err: miss var type")
            exit(-1)
        self.tokenizer.advance()
        if not self.checkValidType():
            debug_log('unknow var type \'%s\''%self.tokenizer.keyword())
            exit(-1)
        varType = self.tokenizer.cur_token

        while True:
            # 变量名
            if not self.tokenizer.hasMoreTokens():
                debug_log("compileClassVarDec err: miss var name")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("compileClassVarDec err: miss 'identifier' before \'%s\'"%self.tokenizer.cur_token)
                exit(-1)

            varName = self.tokenizer.identifier()
            if self.symbolTable.KindOf(varName) != SymbolTableKind.NONE:
                debug_log("compileClassVarDec err: repeat class var \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
            # 写入符号表
            self.symbolTable.Define(varName, varType, varKind)

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

    def compileSubroutine(self):
        self.symbolTable.startSubroutine()
        # keyword
        self.tokenizer.advance()
        subroutineKind = self.tokenizer.keyword()

        # 类型 or void
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss subroutine type")
            exit(-1)
        self.tokenizer.advance()
        if not self.checkValidType():
            if self.tokenizer.tokenType() != Token.KEYWORD or self.tokenizer.keyword() != 'void':
                debug_log("err: invalid type \'%s\' "%(self.tokenizer.cur_token))
                exit(-1)

        # 子程序名
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss identifier")
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log("err: invalid identifier \'%s\'"%self.tokenizer.cur_token)
            exit(-1)
        self.funcStack.insert(0, self.tokenizer.identifier())
        functionName =  self.className + '.' + self.tokenizer.cur_token

        # '('
        self.checkCompileSymbol('(')
        # paramlist
        self.compileParameterList()
        # ')'
        self.checkCompileSymbol(')')

        # subroutineBody
        # '{'
        self.checkCompileSymbol('{')
        # varDec 
        while True:
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss symbol \'}\'")
                exit(-1)
            if self.tokenizer.next_token != 'var':
                break

            self.compileVarDec()

        self.vmWriter.writeFunction(functionName, self.symbolTable.VarCount(SymbolTableKind.VAR))

        # 构造函数
        if subroutineKind == 'constructor':
            # 分配内存 
            self.vmWriter.writePush(VMSegment.CONST, self.symbolTable.VarCount(SymbolTableKind.FIELD))
            self.vmWriter.writeCall('Memory.alloc', 1)
            # 将指针分配给this
            self.vmWriter.writePop(VMSegment.POINTER, 0)

        # 
        if subroutineKind == 'method':
            # 将参数1(对象地址)，赋值给this, 通过pointer[0]
            self.vmWriter.writePush(VMSegment.ARG, 0)
            self.vmWriter.writePop(VMSegment.POINTER, 0)

        # statements
        while True:
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss symbol \'}\'")
                exit(-1)
            
            if self.tokenizer.next_token in ['let', 'if', 'while', 'do', 'return']:
                self.compileStatements()
                continue

            break

        # '}'
        self.checkCompileSymbol('}')
        self.funcStack.pop()

    def compileParameterList(self): 
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
            varType = self.tokenizer.cur_token

            # varName
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss param varName")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("err: unknown identifier \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
            varName = self.tokenizer.cur_token
            # 写入符号表
            self.symbolTable.Define(varName, varType, SymbolTableKind.ARG)

            # ','
            if not self.tokenizer.hasMoreTokens():
                break
            if self.tokenizer.next_token != ',':
                break
            self.tokenizer.advance()

    def compileVarDec(self):
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
            varName = self.tokenizer.cur_token
            # 写入符号表
            self.symbolTable.Define(varName, varType, SymbolTableKind.VAR)

            # ','
            if not self.tokenizer.hasMoreTokens() :
                break
            if self.tokenizer.next_token != ',':
                break

            self.tokenizer.advance()
            self.writexml(self.tokenizer.tokenStr())
                    
        # ';'
        self.checkCompileSymbol(';')

    def compileStatements(self):
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

    def compileDo(self):
        # 'do'
        self.tokenizer.advance()

        # subroutimeName | (className|varName).subroutineName
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss subroutimeName | (className|varName)")
            exit(-1)
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != Token.IDENTIFIER:
            debug_log("compileDo err: invalid identifier \'%s\'"%self.tokenizer.cur_token)
            exit(-1)            

        doFuncName = ''
        finalName = self.tokenizer.identifier()
        # 
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss \'(\'")
            exit(-1)

        paramNum = 0
        if self.tokenizer.next_token == '.':
            self.tokenizer.advance()
            if not self.tokenizer.hasMoreTokens() :
                debug_log("err: miss subroutimeName after \'.\'")
                exit(-1)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != Token.IDENTIFIER:
                debug_log("err: invalid subroutimeName \'%s\'"%self.tokenizer.cur_token)
                exit(-1)
            
            if self.symbolTable.getValByName(finalName) != None:
                # 需要对象的方法, this指针放在参数1, 根据对象名查找信息
                self.vmWriter.writePush(self.symbolTable.KindOf(finalName), self.symbolTable.IndexOf(finalName))
                paramNum = 1
                doFuncName = self.symbolTable.TypeOf(finalName) + '.' + self.tokenizer.identifier()
            else:
                doFuncName = finalName + '.' + self.tokenizer.identifier()
        else:
            # 直接调用方法, 将对象基地址传入(this指针的值, 通过pointer[0])
            self.vmWriter.writePush(VMSegment.POINTER, 0)
            paramNum = 1
            doFuncName = self.className +'.'+ finalName

        # '('
        self.checkCompileSymbol('(')
        # expressionlist 
        self.expressionListEndToken = ')'
        paramNum += self.compileExpressionList()
        # ')'
        self.checkCompileSymbol(')')
        # ';'
        self.checkCompileSymbol(';')

        self.vmWriter.writeCall(doFuncName, paramNum)
        self.vmWriter.writePop(VMSegment.TEMP, 0)


    def compileLet(self):
        # let
        self.tokenizer.advance()
        
        # varName
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss varName")
            exit(-1)
        self.tokenizer.advance()

        # 2种情况
        # 变量
        # 数组
        bIsArray = False
        varName = self.tokenizer.identifier()
        kind = self.symbolTable.KindOf(varName)
        index = self.symbolTable.IndexOf(varName)
        # ('[' expression ']')?
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss varName")
            exit(-1)
        if self.tokenizer.next_token == '[':
            # push数组首地址
            self.vmWriter.writePush(kind, index)
            self.tokenizer.advance()
            # expression
            self.compileExpression()
            # ']'
            self.checkCompileSymbol(']')
            # 数组首地址和偏移的和
            self.vmWriter.writeArithmetic(VMCommand.ADD)
            # 地址存入temp[1], temp[0]用于do方法弹出值
            self.vmWriter.writePop(VMSegment.TEMP, 1)
            bIsArray = True
            
        # '='      
        self.checkCompileSymbol('=')
        # expression
        self.compileExpression()
        # ';'
        self.checkCompileSymbol(';')
        if bIsArray:
            # 从temp[1]取出变量地址,放入that(pointer[1])
            self.vmWriter.writePush(VMSegment.TEMP, 1)
            self.vmWriter.writePop(VMSegment.POINTER, 1)
            # *that = expression, 数组成员赋值
            self.vmWriter.writePop(VMSegment.THAT, 0)
        else:
            # 变量赋值
            self.vmWriter.writePop(kind, index)
        
        

    def compileWhile(self):
        # while
        self.tokenizer.advance()
        whileLabel1 = '%s_%s_while_%d_%d'%(self.className, self.funcStack[0], self.tokenizer.lineNum, self.whileInc)
        self.vmWriter.writeLabel(whileLabel1)
        self.whileInc += 1
        whileLabel2 = '%s_%s_while_%d_%d'%(self.className, self.funcStack[0], self.tokenizer.lineNum, self.whileInc)
        self.whileInc += 1

        # '('
        self.checkCompileSymbol('(')
        # expresssion
        self.compileExpression()
        # ')'
        # 取个反, 错误的直接跳转到结束, 好处理一些
        self.vmWriter.writeArithmetic(VMCommand.NOT)
        self.vmWriter.writeIf(whileLabel2)

        self.checkCompileSymbol(')')
        # '{'
        self.checkCompileSymbol('{')
        # statements
        self.compileStatements()
        # '}'
        self.checkCompileSymbol('}')

        self.vmWriter.writeGoto(whileLabel1)
        self.vmWriter.writeLabel(whileLabel2)

    def compileReturn(self):
        # return
        self.tokenizer.advance()
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: miss \';\'")
            exit(-1)
        if self.tokenizer.next_token != ';':
            self.compileExpression()
        # ';'
        self.checkCompileSymbol(';')

        self.vmWriter.writeReturn()

    def compileIf(self):
        # if
        self.tokenizer.advance()
        ifLabel1 = '%s_%s_if_%d_%d'%(self.className, self.funcStack[0], self.tokenizer.lineNum, self.ifInc)
        self.ifInc += 1
        ifLabel2 = '%s_%s_if_%d_%d'%(self.className, self.funcStack[0], self.tokenizer.lineNum, self.ifInc)
        self.ifInc += 1

        # '('
        self.checkCompileSymbol('(')
        # expression
        self.compileExpression()
        # ')'
        self.vmWriter.writeArithmetic(VMCommand.NOT)
        self.vmWriter.writeIf(ifLabel1)

        self.checkCompileSymbol(')')
        # '{'
        self.checkCompileSymbol('{')
        # statements
        self.compileStatements()
        # '}'
        self.checkCompileSymbol('}')
        self.vmWriter.writeGoto(ifLabel2)

        self.vmWriter.writeLabel(ifLabel1)
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
        
        self.vmWriter.writeLabel(ifLabel2)

    def writeArithmetic(self, command):
        if command == '+':
            self.vmWriter.writeArithmetic(VMCommand.ADD)
        if command == '-':
            self.vmWriter.writeArithmetic(VMCommand.SUB)
        if command == '*':
            self.vmWriter.writeCall('Math.multiply', 2)
        if command == '/':
            self.vmWriter.writeCall('Math.divide', 2)
        if command == '&':
            self.vmWriter.writeArithmetic(VMCommand.AND)
        if command == '|':
            self.vmWriter.writeArithmetic(VMCommand.OR)
        if command == '<':
            self.vmWriter.writeArithmetic(VMCommand.LT)
        if command == '>':
            self.vmWriter.writeArithmetic(VMCommand.GT)
        if command == '=':
            self.vmWriter.writeArithmetic(VMCommand.EQ)

    def compileExpression(self):
        stack = []
        while True:
            self.compileTerm()
            
            if not self.tokenizer.hasMoreTokens() :
                break

            if self.tokenizer.next_token in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                self.tokenizer.advance()
                op = self.tokenizer.symbol()
                if len(stack) <= 0:
                    stack.insert(0, self.tokenizer.symbol())
                else:
                    while len(stack) > 0:
                        # 逆波兰式
                        # 当前符号优先级不大于栈顶符号优先级, 弹出栈顶符号, 直到优先级大于或者为空时插入
                        top_op = stack[0]
                        if op_privilege[op] >= op_privilege[top_op]:
                            break
                        stack.pop()
                        # 写入VM代码
                        self.writeArithmetic(top_op)
                    stack.insert(0, op)
                continue
            break

        while len(stack) > 0:
            self.writeArithmetic(stack[0])
            stack.pop()

    def compileTerm(self):
        if not self.tokenizer.hasMoreTokens() :
            debug_log("err: invalid term")
            exit(-1)

        while True:
            tokenType = self.tokenizer.nextTokenType()
            if tokenType == Token.INT_CONST:
                self.tokenizer.advance()
                self.vmWriter.writePush(VMSegment.CONST, self.tokenizer.intVal())
                break
            if tokenType == Token.STRING_CONST:
                self.tokenizer.advance()
                self.vmWriter.writePush(VMSegment.CONST, len(self.tokenizer.stringVal()))
                self.vmWriter.writeCall('String.new', 1)
                for c in self.tokenizer.stringVal():
                    self.vmWriter.writePush(VMSegment.CONST, ord(c))
                    self.vmWriter.writeCall('String.appendChar', 2)
                break
            if tokenType == Token.KEYWORD:
                self.tokenizer.advance()
                keyword = self.tokenizer.keyword()
                if keyword == 'true':
                    # true = -1 -> push constant 1; neg;
                    self.vmWriter.writePush(VMSegment.CONST, 1)
                    self.vmWriter.writeArithmetic(VMCommand.NEG)
                elif keyword == 'false':
                    # null = 0 -> push constant 0
                    self.vmWriter.writePush(VMSegment.CONST, 0)
                elif keyword == 'null':
                    # false = 0 -> push constant 0
                    self.vmWriter.writePush(VMSegment.CONST, 0)
                elif keyword == 'this':
                    # this -> push argument 0
                    self.vmWriter.writePush(VMSegment.POINTER, 0)
                else:
                    debug_log("err: term can't use keyword \'%s\'"%self.tokenizer.keyword())
                    exit(-1)
            if tokenType == Token.SYMBOL:
                next_token = self.tokenizer.next_token
                if next_token == '-':
                    self.tokenizer.advance()
                    self.compileTerm()
                    # neg
                    self.vmWriter.writeArithmetic(VMCommand.NEG)

                elif next_token == '~':
                    self.tokenizer.advance()
                    self.compileTerm()
                    # not
                    self.vmWriter.writeArithmetic(VMCommand.NOT)

                elif next_token == '(':
                    self.tokenizer.advance()
                    self.compileExpression()
                    self.checkCompileSymbol(')')
                    break
            
            if tokenType == Token.IDENTIFIER:
                self.tokenizer.advance()
                if not self.tokenizer.hasMoreTokens():
                    break

                curIdentifier = self.tokenizer.identifier()

                if self.tokenizer.next_token == '[':
                    # push数组基地址
                    self.vmWriter.writePush(self.symbolTable.KindOf(curIdentifier), self.symbolTable.IndexOf(curIdentifier))
                    self.tokenizer.advance()
                    self.compileExpression()
                    self.checkCompileSymbol(']')
                    # 数组偏移已经push
                    # add
                    self.vmWriter.writeArithmetic(VMCommand.ADD)
                    # 通过pointer将地址存入that指针
                    self.vmWriter.writePop(VMSegment.POINTER, 1)
                    # 取对应数组成员的值
                    self.vmWriter.writePush(VMSegment.THAT, 0)
                    break

                # subroutineName(expressionList)
                if self.tokenizer.next_token == '(':
                    self.tokenizer.advance()
                    self.expressionListEndToken = ')'
                    argNum = self.compileExpressionList()
                    self.checkCompileSymbol(')')
                    self.vmWriter.writeCall(curIdentifier, argNum)
                    break

                # (class|varName).subroutineName(expressionList)
                if self.tokenizer.next_token == '.':
                    self.tokenizer.advance()
                    if not self.tokenizer.hasMoreTokens():
                        debug_log("err: expected 'identifier' after '.'")
                        exit(-1)
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() != Token.IDENTIFIER:
                        debug_log("err: expected 'identifier' before \'%s\''"%self.tokenizer.cur_token)
                        exit(-1)
                    subroutineName = self.tokenizer.identifier()
                    self.checkCompileSymbol('(')
                    self.expressionListEndToken = ')'
                    argNum = self.compileExpressionList()
                    self.checkCompileSymbol(')')
                    if self.symbolTable.getValByName(curIdentifier) != None:
                        # varName, 将对象放入argument 0
                        self.vmWriter.writePush(self.symbolTable.KindOf(curIdentifier), self.symbolTable.IndexOf(curIdentifier))
                        argNum += 1
                    self.vmWriter.writeCall(curIdentifier+'.'+subroutineName, argNum)
                    break

                # 变量
                self.vmWriter.writePush(self.symbolTable.KindOf(curIdentifier), self.symbolTable.IndexOf(curIdentifier))
            break

    def compileExpressionList(self):
        num = 0
        if self.tokenizer.hasMoreTokens():
            if self.expressionListEndToken == None or self.tokenizer.next_token != self.expressionListEndToken:
                while True:
                    self.compileExpression()
                    num += 1

                    if not self.tokenizer.hasMoreTokens() :
                        break
                    if self.tokenizer.next_token == ',':
                        self.tokenizer.advance()
                        continue
                    break

        self.expressionListEndToken = None

        return num

