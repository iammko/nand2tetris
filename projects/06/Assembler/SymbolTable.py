

class SymbolTable:
    def __init__(self):
        # 预定义符号
        self.table = {
            "SP" :      0,
            "LCL":      1,
            "ARG":      2,
            "THIS":     3,
            "THAT":     4,
            "R0":       0,
            "R1":       1,
            "R2":       2,
            "R3":       3,
            "R4":       4,
            "R5":       5,
            "R6":       6,
            "R7":       7,
            "R8":       8,
            "R9":       9,
            "R10":      10,
            "R11":      11,
            "R12":      12,
            "R13":      13,
            "R14":      14,
            "R15":      15,
            "SCREEN":   16384, #0x4000
            "KBD":      24576, #0x6000
        }

    def addEntry(self, symbol, address):
        #print("add symbol [ %s : %d ]"%(symbol, address))
        self.table[symbol] = address
        
    def contains(self, symbol):
        return symbol in self.table

    def GetAddress(self, symbol):
        return self.table[symbol]
