from Comm import VMSegment, VMCommand, SymbolTableKind

segmentStr = {
            SymbolTableKind.STATIC : 'static',
            SymbolTableKind.FIELD : 'this',
            SymbolTableKind.VAR : 'local',
            SymbolTableKind.ARG : 'argument',
            VMSegment.CONST : 'constant',
            VMSegment.ARG : 'argument',
            VMSegment.LOCAL : 'local',
            VMSegment.STATIC : 'static',
            VMSegment.THIS : 'this',
            VMSegment.THAT : 'that',
            VMSegment.POINTER : 'pointer',
            VMSegment.TEMP : 'temp',
        }

class VMWriter:
    def __init__(self, file) -> None:
        self.fileFd = open(file, 'w+')

    def writePush(self, segment, index):
        self.fileFd.write('push %s %d\n'%(segmentStr[segment], index))

    def writePop(self, segment, index):
        self.fileFd.write('pop %s %d\n'%(segmentStr[segment], index))

    def writeArithmetic(self, command):
        commWriter = {
            VMCommand.ADD : lambda : self.fileFd.write('add'),
            VMCommand.SUB : lambda : self.fileFd.write('sub'),
            VMCommand.NEG : lambda : self.fileFd.write('neg'),
            VMCommand.EQ  : lambda : self.fileFd.write('eq'),
            VMCommand.GT  : lambda : self.fileFd.write('gt'),
            VMCommand.LT  : lambda : self.fileFd.write('lt'),
            VMCommand.AND : lambda : self.fileFd.write('and'),
            VMCommand.OR  : lambda : self.fileFd.write('or'),
            VMCommand.NOT : lambda : self.fileFd.write('not'),
        }

        commWriter[command]()
        self.fileFd.write('\n')
        

    def writeLabel(self, label):
        self.fileFd.write('label %s\n'%label)

    def writeGoto(self, label):
        self.fileFd.write('goto %s\n'%label)

    def writeIf(self, label):
        self.fileFd.write('if-goto %s\n'%label)

    def writeCall(self, name, nArgs):
        self.fileFd.write('call %s %d\n'%(name, nArgs))

    def writeFunction(self, name, nArgs):
        self.fileFd.write('function %s %d\n'%(name, nArgs))

    def writeReturn(self):
        self.fileFd.write('return\n')

    def close(self):
        self.fileFd.close()