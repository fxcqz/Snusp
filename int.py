#!/usr/bin/env Python
class Snusp():
    def __init__(self):
        self.ptrx = 0
        self.ptry = 0
        self.ptrd = 1
        self.prg = []
        self.cells = []
        self.currcell = 0
        self.running = 1
        self.debug = 0
        self.callstack = []

    def ldprg(self, fname):
        with open(fname, 'r') as f:
            self.prg = f.read().split('\n')
        self.cells.append(0) # init first mem cell

    def err(self, msg):
        if self.debug:
            print msg
        exit()

    def nextptr(self):
        if self.ptrd == 0:
            self.ptry -= 1
        if self.ptrd == 1:
            self.ptrx += 1
        if self.ptrd == 2:
            self.ptry += 1
        if self.ptrd == 3:
            self.ptrx -= 1
        # exit conditions
        if self.ptrx < 0:
            self.running = 0
            self.err("Notice: Pointer out of bounds. Ln: "+str(self.ptry)+", Col: "+str(self.ptrx))
        if self.ptry < 0:
            self.running = 0
            self.err("Notice: Pointer out of bounds. Ln: "+str(self.ptry)+", Col: "+str(self.ptrx))
        if self.ptrx >= len(self.prg[self.ptry]):
            self.running = 0
            self.err("Notice: Pointer out of bounds. Ln: "+str(self.ptry)+", Col: "+str(self.ptrx))
        if self.ptry >= len(self.prg):
            self.running = 0
            self.err("Notice: Pointer out of bounds. Ln: "+str(self.ptry)+", Col: "+str(self.ptrx))

    def readop(self):
        if self.ptry < len(self.prg) and self.ptrx <= self.ptrx:
            return si.prg[self.ptry][self.ptrx]
        return "Out of bounds error!"

    def op_add(self):
        self.cells[self.currcell] += 1

    def op_decr(self):
        self.cells[self.currcell] -= 1

    def op_movr(self):
        self.currcell += 1
        if len(self.cells) <= self.currcell:
            self.cells.append(0)

    def op_movl(self):
        if self.currcell > 0:
            self.currcell -= 1

    def op_rdin(self):
        uin = raw_input("PROG IN: ")
        self.cells[self.currcell] = ord(uin[:1])

    def op_write(self):
        print chr(self.cells[self.currcell])

    def op_lurd(self):
        if self.ptrd == 0:
            self.ptrd = 3
        elif self.ptrd == 1:
            self.ptrd = 2
        elif self.ptrd == 2:
            self.ptrd = 1
        elif self.ptrd == 3:
            self.ptrd = 0

    def op_ruld(self):
        if self.ptrd == 0:
            self.ptrd = 1
        elif self.ptrd == 1:
            self.ptrd = 0
        elif self.ptrd == 2:
            self.ptrd = 3
        elif self.ptrd == 3:
            self.ptrd = 2

    def op_skp(self):
        self.nextptr()

    def op_skpz(self):
        if self.cells[self.currcell] == 0:
            self.op_skp()

    def op_end(self):
        if self.cs_empty():
            exit()
        else:
            self.ptrx = self.callstack[-1][0]
            self.ptry = self.callstack[-1][1]
            self.ptrd = self.callstack[-1][2]
            self.cs_rm_ptr()
            self.nextptr()

    def dlr_search(self):
        for y in range(len(self.prg)):
            for x in range(len(self.prg[y])):
                if self.prg[y][x] == "$":
                    self.ptrx = x
                    self.ptry = y

    # stack functions
    def cs_add_ptr(self):
        lstmp = [self.ptrx, self.ptry, self.ptrd]
        self.callstack.append(lstmp)

    def cs_rm_ptr(self):
        del self.callstack[-1]

    def cs_empty(self):
        if not self.callstack:
            return True
        return False

    # interpreter functions
    def parse(self):
        self.dlr_search()
        while True:
            op = self.readop()
            if op == "+":
                self.op_add()
            if op == "-":
                self.op_decr()
            if op == ">":
                self.op_movr()
            if op == "<":
                self.op_movl()
            if op == ",":
                self.op_rdin()
            if op == ".":
                self.op_write()
            if op == "\\":
                self.op_lurd()
            if op == "/":
                self.op_ruld()
            if op == "!":
                self.op_skp()
            if op == "?":
                self.op_skpz()
            if op == "#":
                self.op_end()
            if op == "@":
                self.cs_add_ptr()
            self.nextptr()
            if self.running == 0:
                break

if __name__ == "__main__":
    si = Snusp()
    si.ldprg("test.sp")
    si.parse()
