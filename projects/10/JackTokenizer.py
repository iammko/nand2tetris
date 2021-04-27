class JackTokenizer:
    def __init__(self, file):
        self.fd = open(file, 'w')
        self.cur_token = None
        self.next_token = None
        self.cur_line = ''
        # 是否在双引号字符串当中
        self.inString = False
        # 是否在注释块当中
        self.inBlock = False
        
        self.symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    

    def parseToken(self):

        pass

    def hasMoreTokens(self):




    
        

        return True