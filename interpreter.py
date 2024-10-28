import sys

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
        if self.IsEmpty() is False:
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
        self.TokenHistory = Stack(256)
        self.OPCodeHistory = Stack(256)
        self.ValueStack = Stack(256)
        self.AbstractStack = Stack(256)
        #self.variable = Stack(256)
        self.variable = LinkedList()
    
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
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = str(self.tokens.GetElement(self.tokens.GetSize()-1).val) + self.tokens.GetTop().val
                        self.tokens.pop()
                    elif self.tokens.GetTop().type == "OPCODE":
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = str(self.tokens.GetElement(self.tokens.GetSize()-1).val) + self.tokens.GetTop().val
                        self.tokens.pop()
                    elif self.tokens.GetTop().type == "WHITESPACE" and (QuoteCheck.IsEmpty() is False):
                        self.tokens.GetTop().val = chr(32)
                        self.tokens.GetElement(self.tokens.GetSize()-1).val = self.tokens.GetElement(self.tokens.GetSize()-1).val + self.tokens.GetTop().val
                        self.tokens.pop()
            #if self.tokens.GetTop().type == "WHITESPACE" and self.tokens.GetElement(self.tokens.GetSize()-1).type != ("OPCODE" or "STR"):
            #    self.tokens.pop()
            
        #Penerjemahan token ke function logic
        while self.tokens.IsEmpty() is False:
            if self.tokens.GetTop().type == "INT" or self.tokens.GetTop().type == "STR":
                self.ValueStack.push(self.tokens.GetTop())
            elif self.tokens.GetTop().type == "OPCODE":
                if self.tokens.GetTop().val == "TAMPILKAN":
                    if self.TokenHistory.IsEmpty() is False:
                        self.ShowVariableValue(self.variable.search(self.TokenHistory.GetTop().val))
                        self.TokenHistory.pop()
                    else:
                        self.ShowLatestInStack()
                elif self.tokens.GetTop().val == "SIMPAN":
                    self.variable.AppendToHead(self.AbstractStack.GetTop().val, self.ValueStack.GetTop().val, self.ValueStack.GetTop().type)
                    self.AbstractStack.pop()
                    self.ValueStack.pop()
                elif self.tokens.GetTop().val == "BACA":
                    ReadValue = token("INPUT", input())
                    self.ReadInput(ReadValue)
                elif self.tokens.GetTop().val == "KONVERSI":
                    if self.OPCodeHistory.GetTop().val == "BIN":
                        if self.TokenHistory.IsEmpty() is False:
                            self.ConvertToBinary(token(self.variable.search(self.TokenHistory.GetTop().val).type, self.variable.search(self.TokenHistory.GetTop().val).value))
                            self.TokenHistory.pop()
                            self.OPCodeHistory.pop()
                        else:
                            self.ConvertToBinary(self.ValueStack.GetTop())
                            self.OPCodeHistory.pop()
                    elif self.OPCodeHistory.GetTop().val == "DEC":
                        if self.TokenHistory.IsEmpty() is False:
                            self.ConvertToDecimal(token(self.variable.search(self.TokenHistory.GetTop().val).type, self.variable.search(self.TokenHistory.GetTop().val).value))
                            self.TokenHistory.pop()
                            self.OPCodeHistory.pop()
                        else:
                            self.ConvertToDecimal(self.ValueStack.GetTop())
                            self.OPCodeHistory.pop()
                    elif self.OPCodeHistory.GetTop().val == "OCT":
                        if self.TokenHistory.IsEmpty() is False:
                            self.ConvertToOctal(token(self.variable.search(self.TokenHistory.GetTop().val).type, self.variable.search(self.TokenHistory.GetTop().val).value))
                            self.TokenHistory.pop()
                            self.OPCodeHistory.pop()
                        else:
                            self.ConvertToOctal(self.ValueStack.GetTop())
                            self.OPCodeHistory.pop()
                    elif self.OPCodeHistory.GetTop().val == "HEX":
                        if self.TokenHistory.IsEmpty() is False:
                            self.ConvertToHex(token(self.variable.search(self.TokenHistory.GetTop().val).type, self.variable.search(self.TokenHistory.GetTop().val).value))
                            self.TokenHistory.pop()
                            self.OPCodeHistory.pop()
                        else:
                            self.ConvertToHex(self.ValueStack.GetTop())
                            self.OPCodeHistory.pop()
                elif self.tokens.GetTop().val == "BIN" or self.tokens.GetTop().val == "DEC" or self.tokens.GetTop().val == "OCT" or self.tokens.GetTop().val == "HEX":
                    self.OPCodeHistory.push(self.tokens.GetTop())
                elif self.variable.size > 0 and self.tokens.GetTop().val == self.variable.search(self.tokens.GetTop().val).name:
                    self.TokenHistory.push(self.tokens.GetTop())
                else:
                    self.AbstractStack.push(self.tokens.GetTop())
                    
            self.tokens.pop()
    #Function logic
    def ShowLatestInStack(self):
        if self.ValueStack.IsEmpty() is False:
            print(self.ValueStack.GetTop().val)
    def ShowVariableValue(self, var):
        print(var.value)
    def ReadInput(self, input):
        self.ValueStack.pop()
        for c in input.val:
            if (ord(c) >= 48 and ord(c) <= 57) and (input.type == "INPUT" or input.type == "INT"): #Kenali angka
                input.type = "INT"
            else:
                input.type = "STR"
        self.ValueStack.push(input)
    def add(self, pos):
        self.result = token("INT",self.tokens[pos-1].val + self.tokens[pos+1].val)
        return self.result
    def ConvertToBinary(self, ValueToConvert):
        if ValueToConvert.type == "INT":
            self.ValueStack.push(token("BIN", bin(int(ValueToConvert.val))))
        elif ValueToConvert.type == "STR" or ValueToConvert.type == "OCT" or ValueToConvert.type == "HEX":
            if ValueToConvert.val[1] == "o" or ValueToConvert.val[1] == "O":
                self.ValueStack.push(token("BIN", bin(int(ValueToConvert.val, 8))))
            elif ValueToConvert.val[1] == "x" or ValueToConvert.val[1] == "X":
                self.ValueStack.push(token("BIN", bin(int(ValueToConvert.val, 16))))
    def ConvertToDecimal(self, ValueToConvert):
        if ValueToConvert.val[1] == "o" or ValueToConvert.val[1] == "O":
            self.ValueStack.push(token("INT", int(ValueToConvert.val, 8)))
        elif ValueToConvert.val[1] == "x" or ValueToConvert.val[1] == "X":
            self.ValueStack.push(token("INT", int(ValueToConvert.val, 16)))
        elif ValueToConvert.val[1] == "b" or ValueToConvert.val[1] == "B":
            self.ValueStack.push(token("INT", int(ValueToConvert.val, 2)))
    def ConvertToOctal(self, ValueToConvert):
        if ValueToConvert.type == "INT":
            self.ValueStack.push(token("OCT", oct(int(ValueToConvert.val))))
        elif ValueToConvert.type == "STR" or ValueToConvert.type == "BIN" or ValueToConvert.type == "HEX":
            if ValueToConvert.val[1] == "b" or ValueToConvert.val[1] == "B":
                self.ValueStack.push(token("OCT", oct(int(ValueToConvert.val, 2))))
            elif ValueToConvert.val[1] == "x" or ValueToConvert.val[1] == "X":
                self.ValueStack.push(token("OCT", oct(int(ValueToConvert.val, 16))))
    def ConvertToHex(self, ValueToConvert):
        if ValueToConvert.type == "INT":
            self.ValueStack.push(token("HEX", hex(int(ValueToConvert.val))))
        elif ValueToConvert.type == "STR" or ValueToConvert.type == "OCT" or ValueToConvert.type == "BIN":
            if ValueToConvert.val[1] == "o" or ValueToConvert.val[1] == "O":
                self.ValueStack.push(token("HEX", hex(int(ValueToConvert.val, 8))))
            elif ValueToConvert.val[1] == "b" or ValueToConvert.val[1] == "B":
                self.ValueStack.push(token("HEX", hex(int(ValueToConvert.val, 2))))

f = open(sys.argv[1], "r")
test = interpreter()
for x in f.readlines():
    test.read(x)
    test.interpret()