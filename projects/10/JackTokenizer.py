class JackTokenizer:
    def __init__(self, file):
        self.fd = open(file, 'r')
        self.cur_token = None
        self.next_token = None
        self.cur_line = ''
        # 是否在注释块当中
        self.inCommentBlock = False
        
        self.keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 
            'let', 'do', 'if', 'else', 'while', 'return']
        self.symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    

    def parseToken(self):

        pass

    def hasMoreTokens(self):
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
                print(line)
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

            print(line)
            break

        return True