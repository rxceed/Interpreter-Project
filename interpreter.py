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
    def push(self, value):
        self.stack.append(value)
        self.top += 1
    def pop(self):
        self.stack.pop()
        self.top -= 1
    def IsEmpty(self):
        if self.top < 0:
            return True
        else:
            return False
    def GetElement(self, index):
        return self.stack[index]
    def GetTop(self):
        return self.stack[self.top]
    def GetSize(self):
        return self.top

class LinkedList:
    class Node:
        def __init__(self, name, value, type, ref = None):
            self.value = value
            self.name = name
            self.type = type
            self.ref = ref

    def __init__(self):
        self.head = None
        self.size = 0
    def AppendToHead(self, name, value, type):
        node = self.Node(name, value, type)
        node.ref = self.head
        self.head = node
        self.size += 1
    def search(self, name):
        current = self.head
        for i in range(self.size):
            if name == current.name:
                return current
            current = current.ref
        return self.Node(0, 0, 0)

#Class interptreter
class interpreter:
    def __init__(self):
        self.tokens = Stack(256)
        self.ValueStack = Stack(256)
        self.AbstractStack = Stack(256)
        #self.variable = Stack(256)
        self.variable = LinkedList()
        #self.pos = 0
        #self.TokenPos = 0
    
    #Function parsing string ke token
    def read(self, arg):
        self.arg = arg
    def parse(self, c):
        if ord(c) >= 48 and ord(c) <= 57: #Kenali angka
            for i in range(48, 58):
                if chr(i) == c:
                    t = token("INT", int(i-48))
                    return t
        elif ord(c) >=97 and ord(c) <= 122: #Kenali a-z
            for i in range(97, 123):
                if chr(i) == c:
                    t = token("OPCODE", chr(i)) 
                    return t
        elif ord(c) >=65 and ord(c) <= 90: #Kenali A-Z
            for i in range(65, 91):
                if chr(i) == c:
                    t = token("OPCODE", chr(i)) 
                    return t
        elif ord(c) == 34:
            t = token("STR", chr(34))
            return t
        elif ord(c) == 43:
            t = token("OP", "+")
            return t
        elif ord(c) == 32:
            t = token("WHITESPACE", None)
            return t
        elif c == "\n":
            t = token("ENTER", None)
            return t
    
    #Function driver
    def interpret(self):
        #Pengaturan dan pengurutan token ke dalam list tokens
        QuoteCheck = Stack(4)
        PrevToken = token("NONE", 0)
        for c in self.arg:
            if self.tokens.IsEmpty() is False:
                PrevToken = self.tokens.GetTop()
            self.tokens.push(self.parse(c))

            if self.tokens.GetTop().val == chr(34):
                if QuoteCheck.IsEmpty():
                    QuoteCheck.push(chr(34))
                else:
                    QuoteCheck.pop()
                    self.tokens.pop()
                    self.tokens.push(token("WHITESPACE", None))
            
            if self.tokens.GetTop().type == PrevToken.type:
                if self.tokens.GetTop().type == "INT":
                    self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val*10 + self.tokens.GetTop().val
                    self.tokens.pop()
                elif self.tokens.GetTop().type == "OPCODE":
                    self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                    self.tokens.pop()
                elif self.tokens.GetTop().type == "STR":
                    if self.tokens.GetElement(self.tokens.GetSize()-1).val == chr(34):
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetTop().val
                        self.tokens.pop()
                    else:
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                        self.tokens.pop()
            else:
                if self.tokens.GetElement(self.tokens.GetSize()-1).type == "OPCODE" and self.tokens.GetTop().type == "INT":
                    self.tokens.GetTop().val = chr(self.tokens.GetTop().val+48)
                    self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                    self.tokens.pop()
                elif self.tokens.GetElement(self.tokens.GetSize()-1).type == "STR" and (self.tokens.GetTop().type == "INT" or self.tokens.GetTop().type == "OPCODE" or self.tokens.GetTop().type == "WHITESPACE"):
                    if self.tokens.GetElement(self.tokens.GetSize()-1).val == chr(34):
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetTop().val
                        self.tokens.pop()
                    elif self.tokens.GetTop().type == "INT":
                        self.tokens.GetTop().val = chr(self.tokens.GetTop().val+48)
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                        self.tokens.pop()
                    elif self.tokens.GetTop().type == "OPCODE":
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                        self.tokens.pop()
                    elif self.tokens.GetTop().type == "WHITESPACE":
                        self.tokens.GetTop().val = chr(32)
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                        self.tokens.pop()
            if self.tokens.GetTop().type == "WHITESPACE" and self.tokens.GetElement(self.tokens.GetSize()-1).type != ("OPCODE" or "STR"):
                self.tokens.pop()
        #self.tokens.push(token("EOF", None))
            
        #Penerjemahan token ke function logic
        while self.tokens.IsEmpty() is False:
            if self.tokens.GetElement(self.tokens.GetSize()-1).type == "OP":
                if self.tokens.GetElement(self.tokens.GetSize()-1).val == "+":
                    result = self.add(self.TokenPos)
                    '''''
                    self.tokens.insert(self.TokenPos, result)
                    self.tokens.pop(self.TokenPos+1)
                    self.tokens.pop(self.TokenPos+1)
                    self.tokens.pop(self.TokenPos-1)
                    print(result.val)
                    '''''
            elif self.tokens.GetTop().type == "INT" or self.tokens.GetTop().type == "STR":
                self.ValueStack.push(self.tokens.GetTop())
            elif self.tokens.GetTop().type == "OPCODE":
                if self.tokens.GetTop().val == "TAMPILKAN":
                    if self.ValueStack.IsEmpty() is False:
                        print(self.ValueStack.GetTop().val)
                        self.ValueStack.pop()
                    #print("lll")
                elif self.tokens.GetTop().val == "SIMPAN":
                    self.variable.AppendToHead(self.AbstractStack.GetTop().val, self.ValueStack.GetTop().val, self.ValueStack.GetTop().type)
                    self.AbstractStack.pop()
                    self.ValueStack.pop()
                elif self.variable.size > 0 and self.tokens.GetTop().val == self.variable.search(self.tokens.GetTop().val).name:
                    self.ValueStack.push(token(self.variable.search(self.tokens.GetTop().val).type, self.variable.search(self.tokens.GetTop().val).value))
                else:
                    self.AbstractStack.push(self.tokens.GetTop())
            self.tokens.pop()

        '''''
        for i in self.tokens:
            print(i.val)
        '''''
    #Function logic
    def add(self, pos):
        self.result = token("INT",self.tokens[pos-1].val + self.tokens[pos+1].val)
        return self.result


#a = input()

#test = interpreter(a)

#test.interpret()

f = open("file.ext", "r")
test = interpreter()
for x in f.readlines():
    test.read(x)
    test.interpret()

