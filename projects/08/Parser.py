import os
import sys
import inspect
from Common import VMCommandType

class Parser:
    def __init__(self, file):
        if not os.path.isfile(file):
            print("%s is not a file"%file)
            exit -1
        self.fd = open(file, 'r')

        self.__cmd_type_dict = {
            'add':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'sub':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'neg':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'eq':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'gt':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'lt':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'and':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'or':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'not':{'type':VMCommandType.C_ARITHMETIC, 'argc': 0},
            'push':{'type':VMCommandType.C_PUSH, 'argc': 2},
            'pop':{'type':VMCommandType.C_POP, 'argc': 2},
            'label':{'type':VMCommandType.C_LABEL, 'argc': 1},
            'goto':{'type':VMCommandType.C_GOTO, 'argc': 1},
            'if-goto':{'type':VMCommandType.C_IF, 'argc': 1},
            'return':{'type':VMCommandType.C_RETURN, 'argc': 0},
            'call':{'type':VMCommandType.C_CALL, 'argc': 2},
            'function':{'type':VMCommandType.C_FUNCTION, 'argc': 2},
        }
    
    def __del__(self):
        self.fd.close()

    def hasMoreCommands(self):
        while True:
            self.nextcmdline = self.fd.readline()
            # 结尾
            if self.nextcmdline == '':
                return False
            # 去掉前后空格
            self.nextcmdline = self.nextcmdline.strip()
            # 注释
            if self.nextcmdline.find('//') != -1:
                self.nextcmdline = self.nextcmdline.split('//', 1)[0]
            # 空行
            if self.nextcmdline == '':
                continue
            
            #print(self.nextcmdline)
            break

        return True
        

    def advance(self):
        self.__cmd = None
        self.__cmdtype = None
        self.__arg1 = None
        self.__arg2 = None

        cmdline = self.nextcmdline
        cmdlist = cmdline.split(' ', 2)

        cmd = cmdlist[0]
        argc = len(cmdlist) - 1

        if cmd not in self.__cmd_type_dict:
            sys.exit("err cmd:%s"%cmd)
        
        args = self.__cmd_type_dict.get(cmd)
        need_argc = args.get('argc')
        if argc < need_argc:
            sys.exit("%s need %d args, but %d"%(cmd, need_argc, argc))

        self.__cmd = cmd
        self.__cmdtype = args.get('type')
        if argc > 0:
            self.__arg1 = cmdlist[1]
        if argc > 1:
            self.__arg2 = cmdlist[2]

        #print('advance cmd=%s cmdtype=%s arg1=%s arg2=%s'%(self.__cmd, self.__cmdtype, self.__arg1, self.__arg2))

    def commandType(self):
        return self.__cmdtype

    def arg1(self):
        if self.__cmdtype == VMCommandType.C_ARITHMETIC:
            return self.__cmd
        if self.__cmdtype == VMCommandType.C_RETURN:
            print("cmd type is C_RETURN, shouldn't call function:%s"%inspect.stack()[1][3])
        return self.__arg1

    def arg2(self):
        if self.__cmdtype in [VMCommandType.C_PUSH, VMCommandType.C_POP, VMCommandType.C_FUNCTION, VMCommandType.C_CALL]:
            return self.__arg2
        
        return None
        