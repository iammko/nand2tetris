class VMWriter:
    def __init__(self, file) -> None:
        self.fileFd = open(file, 'w+')

    def writePush(self, segment, index):
        # push segment index
        pass

    def writePop(self, segment, index):
        # pop segment index
        pass

    def writeArithmetic(self, comand):

        pass

    def writeLabel(self, label):
        # (label)
        pass

    def writeGoto(self, label):
        # goto label
        pass

    def writeIf(self, label):
        # if-goto label
        pass

    def writeCall(self, name, nArgs):
        # call name nArgs
        pass

    def writeFunction(self, name, nArgs):
        # function name nArgs
        pass

    def writeReturn(self):
        # return 
        pass

    def close(self):
        pass