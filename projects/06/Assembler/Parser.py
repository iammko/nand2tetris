from enum import Enum

class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

    C_DEST = 1
    C_JUMP = 2

class Parser:
    def __init__(self, filename):
        self.f = open(filename, 'r')

    def __del__(self):
        self.f.close()

    def Reset(self):
        self.f.seek(0)

    # 输入当中还有更多命令吗
    def hasMoreCommands(self):
        while True:
            self.cmd = self.f.readline()
            # 结尾
            if(self.cmd == ''):
                return False
            # 注释
            if(self.cmd.find('//') != -1):
                self.cmd = self.cmd.split('//', 1)[0]
            # 空行
            self.cmd = self.cmd.strip()
            if(self.cmd == ''):
                continue
            
            # 确认指令类型
            self.eCommandType = self.__commandType()
            # 确认C指令域类型
            self.eCType = self.__cType()
            break
        return True

    # 从输入中读取下一条命令，作为当前命令
    def advance(self):
        return self.cmd

    def __commandType(self):
        if(self.cmd[0] == '@'):
            return CommandType.A_COMMAND
        
        if(self.cmd[0] == '('):
            if(self.cmd[-1] != ')' or len(self.cmd) <= 2):
                print("L_COMMAND need end with ')' and not empty")
                exit -1
            return CommandType.L_COMMAND

        return CommandType.C_COMMAND
    
    def __cType(self):
        if(self.cmd.find('=') != -1):
            return CommandType.C_DEST
        if(self.cmd.find(';') != -1):
            return CommandType.C_JUMP
        return None

    # 返回当前命令类型
    # A_COMMAND A指令
    # C_COMMAND C指令
    # L_COMMAND 伪命令(Xxx)
    def commandType(self):
        return self.eCommandType
        

    # 返回形如@Xxx或(Xxx)的当前命令的符号或十进制值
    # 只有commandType()返回A_COMMAND或者L_COMMAND时调用
    def symbol(self):
        if(self.eCommandType == CommandType.A_COMMAND):
            return self.cmd[1:]
        if(self.eCommandType == CommandType.L_COMMAND):
            return self.cmd[1:-1]
        return None

    # 返回当前C-指令的dest助记符
    # 只有commandType()返回C_COMMAND时调用
    def dest(self):
        if(self.eCType != CommandType.C_DEST):
            return "null"
        return self.cmd.split('=', 1)[0]
        

    # 返回当前C-指令的comp助记符
    # 只有commandType()返回C_COMMAND时调用
    def comp(self):
        if(self.eCType == CommandType.C_DEST):
            return self.cmd.split('=', 1)[1]
        if(self.eCType == CommandType.C_JUMP):
            return self.cmd.split(';', 1)[0]
        return "null"

    # 返回当前C-指令的jump助记符
    # 只有commandType()返回C_COMMAND时调用
    def jump(self):
        if(self.eCType != CommandType.C_JUMP):
            return "null"
        return self.cmd.split(';', 1)[1]