from Comm import SymbolTableKind

class SymbolTable:
    def __init__(self):
        self.tableList = []
        self.tableList.append({})
        self.tableList.append({})

        # 子程序符号表
        self.tableList[0]['counter'] = {SymbolTableKind.ARG:0, SymbolTableKind.VAR:0}
        self.tableList[0]['symbol'] = {}
        # 类符号表
        self.tableList[1]['counter'] = {SymbolTableKind.STATIC:0, SymbolTableKind.FIELD:0}
        self.tableList[1]['symbol'] = {}

        self.kindTableMap = {SymbolTableKind.STATIC:self.tableList[1], SymbolTableKind.FIELD:self.tableList[1], SymbolTableKind.ARG:self.tableList[0], SymbolTableKind.VAR:self.tableList[0]}

    def getTableByKind(self, kind):
        return self.kindTableMap[kind]

    def getValByName(self, name):
        for i in (0, len(self.tableList) - 1):
            val = self.tableList[i]['symbol'].get(name)
            if val != None:
                return val

        return None

    def startSubroutine(self):
        self.tableList[1].clear()

    def Define(self, name , type, kind):
        table = self.getTableByKind(kind)

        if table == None:
            print("err kind ", kind)
            exit(-1)

        table['symbol'][name] = {}
        table['symbol'][name]['type'] = type
        table['symbol'][name]['kind'] = kind
        table['symbol'][name]['index'] = table['counter'][kind]
        table['counter'][kind] += 1

    def VarCount(self, kind):
        table = self.getTableByKind(kind)

        return table['counter'][kind]

    def KindOf(self, name):
        val = self.getValByName(name)
        if val != None:
            return val['kind']

        return SymbolTableKind.NONE

    def TypeOf(self, name):
        val = self.getValByName(name)
        if val != None:
            return val['type']

        return None

    def IndexOf(self, name):
        val = self.getValByName(name)
        if val != None:
            return val['index']

        return None

symbolTable = {}