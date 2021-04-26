class JackTokenizer:
    def __init__(self, file):
        self.fd = open(file, 'w')
        self.cur_token = None
        self.next_token = None

        

    def hasMoreTokens(self):

        

        return True