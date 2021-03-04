from SignedAssembler import SignedAssembler as Assembler


assembler = Assembler()

assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\max\Max.asm')
assembler.Work()
assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\max\MaxL.asm')
assembler.Work()

assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\pong\Pong.asm')
assembler.Work()
assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\pong\PongL.asm')
assembler.Work()

assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\rect\Rect.asm')
assembler.Work()

assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\rect\RectL.asm')
assembler.Work()

assembler.SetFile(r'D:\Learn\Nand2Tetris\nand2tetris\projects\06\add\Add.asm')
assembler.Work()