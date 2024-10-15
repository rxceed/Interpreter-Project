#Class token
class token:
    def __init__(self, type, val):
        self.type = type
        self.val = val

class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size
        self.top = -1
    def append(self, value):
        self.stack.append(value)
        self.top += 1
    def pop(self):
        self.stack.pop()
        self.top -= 1
    def GetTop(self):
        return self.stack[self.top]
    def GetSize(self):
        return self.top

#Class interptreter
class interpreter:
    def __init__(self, arg):
        self.arg = arg
        self.tokens = Stack(256)
        #self.pos = 0
        #self.TokenPos = 0
    
    #Function parsing string ke token
    def parse(self, c):
        if ord(c) >= 48 and ord(c) <= 57:
            for i in range(48, 58):
                if chr(i) == c:
                    t = token("INT", int(i-48))
        elif ord(c) >=97 and ord(c) <= 122:
            for i in range(97, 123):
                if chr(i) == c:
                    t = token("STR", chr(i)) 
        elif ord(c) == 43:
            t = token("OP", "+")
        elif ord(c) == 32:
            t = token("WHITESPACE", None)
        return t
    
    #Function driver
    def interpret(self):
        #Pengaturan dan pengurutan token ke dalam list tokens
        for c in self.arg:
            PrevToken = self.tokens.GetTop()
            self.tokens.append(self.parse(c))
            if self.tokens.GetTop().type == PrevToken.type:
                if self.tokens.GetTop().type == "INT":
                    self.tokens[self.tokens.GetSize()-1].val = self.tokens[self.tokens.GetSize()-1].val*10 + self.tokens.GetTop().val
                    self.tokens.pop()
                elif self.tokens.GetTop().type == "STR":
                    self.tokens[self.tokens.GetSize()-1].val = self.tokens[self.tokens.GetSize()-1].val + self.tokens.GetTop().val
                    self.tokens.pop()
            else:
                if self.tokens[self.tokens.GetSize()-1].type == "STR" and self.tokens.GetTop().type == "INT":
                    self.tokens.GetTop().val = chr(self.tokens.GetTop().val+48)
                    self.tokens[self.tokens.GetSize()-1].val = self.tokens[self.tokens.GetSize()-1].val + self.tokens.GetTop().val
                    self.tokens.pop()
            if self.tokens.GetTop().type == "WHITESPACE" and self.tokens[self.tokens.GetSize()-1].type != "STR":
                self.tokens.pop()
        self.tokens.append(token("EOF", None))
            
        #Penerjemahan token ke function logic
        while self.tokens.GetTop().type != "EOF":
            if self.tokens[self.TokenPos].type == "OP":
                if self.tokens[self.TokenPos].val == "+":
                    result = self.add(self.TokenPos)
                    self.tokens.insert(self.TokenPos, result)
                    self.tokens.pop(self.TokenPos+1)
                    self.tokens.pop(self.TokenPos+1)
                    self.tokens.pop(self.TokenPos-1)
                    self.TokenPos -= 2
                    print(result.val)
            elif self.tokens[self.TokenPos].type == "STR":
                if self.tokens[self.TokenPos].val == "tampilkan":
                    print(self.tokens[self.TokenPos+2].val)
            self.TokenPos += 1

        '''''
        for i in self.tokens:
            print(i.val)
        '''''
    #Function logic
    def add(self, pos):
        self.result = token("INT",self.tokens[pos-1].val + self.tokens[pos+1].val)
        return self.result


a = input()

test = interpreter(a)

test.interpret()

