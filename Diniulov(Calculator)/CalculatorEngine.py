operators = [
    '(', ')', '+', '-', '*',
    '/', '%', ';', '!', '^'
]

funcs = ['sqrt', 'sqr', 'inv', 'fact']

def fact(n):
    if (n <= 1):
        return 1
    return n * fact(n-1)

def strToNum(num: str):
    if (num):
        if ('.' in num):
            return float(num)
        else:
            return int(num)
    else:
        return None

class Token:
    def __init__(self, kind: str, value=0, function=''):
        self.kind = kind
        self.value = value
        self.func = function

class TokenStream:
    def __init__(self,stream):
        self.buffer = ''
        self.full = False
        self.setStream(stream)

    def setStream(self, stream: str):
        self.stream = stream

    def get(self):
        if (self.full):
            self.full = False
            return self.buffer
        if (not self.stream):
            return Token('')
        sym = self.stream[0]
        if (sym in operators):
            self.stream = self.stream[1:]
            return Token(sym)
        if (sym.isdigit() or sym == '.'):
            num = ''
            last = 0
            while (last < len(self.stream) and (self.stream[last].isdigit() or self.stream[last] == '.')):
                    num += self.stream[last]
                    last += 1
            self.stream = self.stream[last:]
            return Token('number', value=strToNum(num))
        if (sym.isalpha()):
            last = 0
            s = ''
            while (last < len(self.stream) and self.stream[last].isalpha()):
                s += self.stream[last]
                last += 1
            if s in funcs:
                self.stream = self.stream[last:]
                return Token('function', function=s)

    def putBack(self, t):
        self.buffer = t
        self.full = True

class CalculatorLogic:
    def __init__(self):
        self.ts = None

    def calculate(self, stream):
        self.ts = TokenStream(stream)
        t = self.expression()
        if (t != None):
            return str(round(t,6))
        else:
            return t

    def expression(self):
        left = self.term()
        while True:
            t = self.ts.get()
            if (t.kind == '+'):
                left += self.term()
            elif (t.kind == '-'):
                left -= self.term()
            else:
                self.ts.putBack(t)
                return left

    def term(self):
        left = self.third()
        while True:
            t = self.ts.get()
            if (t.kind == '*'):
                left *= self.third()
            elif (t.kind == '/'):
                left /= self.third()
            elif (t.kind == '%'):
                left %= self.third()
            else:
                self.ts.putBack(t)
                return left

    def third(self):
        left = self.second()
        while True:
            t = self.ts.get()
            if (t.kind == '^'):
                if (left < 0):
                    return
                left = pow(left, self.second())
            else:
                self.ts.putBack(t)
                return left

    def second(self):
        left = self.primary()
        t = self.ts.get()
        while True:
            if (t.kind == '!'):
                t = self.ts.get()
                left = fact(left)
            else:
                self.ts.putBack(t)
                return left

    def primary(self):
        t = self.ts.get()
        if (t.kind == '('):
            d = self.expression()
            t = self.ts.get()
            if (t.kind != ')'): return
            return d
        elif (t.kind == '-'):
            return -self.primary()
        elif (t.kind == '+'):
            return self.primary()
        elif (t.kind == 'number'):
            return t.value
        elif (t.kind == 'function'):
            func = t.func
            t = self.ts.get()
            if (t.kind != '('): return
            d = self.expression()
            t = self.ts.get()
            if (t.kind != ')'): return
            if (func == 'fact'):
                d = int(d)
                return fact(d)
            elif (func == 'sqrt'):
                return d**0.5
            elif (func == 'sqr'):
                return d**2
            elif (func == 'inv'):
                return -d