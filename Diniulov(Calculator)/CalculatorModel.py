from CalculatorEngine import CalculatorLogic
from CalculatorEngine import operators
from CalculatorEngine import funcs

class CalculatorModel:
    def __init__(self):
        self.calc = CalculatorLogic()
        self.curState = []
        self.computed = ''
        self.line = ''
        self.lable = ''
        self.enteredDigits = ''
        self.bracketCount = [0, 0]

    def inputDigits(self, digit: str):
        if (self.computed):
            self.computed = ''

        if (self.enteredDigits == '0'):
            self.enteredDigits = digit
            self.update()
            return

        if (digit == '.'):
            if ('.' in self.enteredDigits):
                return

        self.enteredDigits += digit
        self.update()

    def delete(self):
        self.enteredDigits = self.enteredDigits[:-1]
        self.update()

    def tryAddOp(self, op: str):
        if (self.computed):
            if (not self.enteredDigits):
                self.curState = [self.computed]
                self.computed = ''

        if (op == '(' or op == ')'):
            self.tryAddBracket(op)
            return

        if (self.enteredDigits):
            self.curState.append(self.enteredDigits)
            self.enteredDigits = ''

        if (self.curState and self.curState[-1] in operators):
            if (self.curState[-1] != '(' and self.curState[-1] != ')'):
                self.curState[-1] = op
            else:
                self.curState.append(op)
        elif (self.curState and self.curState not in operators):
            self.curState.append(op)

        self.update()

    def tryAddBracket(self, br: str):
        if (br == ')'):
            if (self.bracketCount[1] >= self.bracketCount[0]):
                return

        if (br == '('):
            self.bracketCount[0] += 1
        elif (br == ')'):
            self.bracketCount[1] += 1

        if (self.enteredDigits):
            self.curState.append(self.enteredDigits)
            self.enteredDigits = ''

        if (self.curState and br == '('):
            last = self.curState[-1]
            if (last == ')'):
                self.curState.append('*')
            elif (last in operators):
                pass
            else:
                self.curState.append('*')

        self.curState.append(br)
        self.update()

    def tryAddFunc(self, func):
        if (self.computed):
            if (not self.enteredDigits):
                self.curState = [self.computed]
                self.computed = ''

        if (self.enteredDigits):
            self.curState.append(self.enteredDigits)
            self.enteredDigits = ''

        if (self.curState and self.curState[-1] in operators):
            if (self.curState[-1] != '(' and self.curState[-1] != ')'):
                self.curState = self.curState[:-1]
                self.computeLable()

        if (self.curState):
            if (self.curState[0] == '(' and self.curState[-1] == ')'):
                self.curState = self.compute()
                self.curState = [self.computed]
                self.computed = ''

            i = len(self.curState) - 1
            while (self.curState[i] in operators or self.curState[i] in funcs):
                i -= 1

            num = self.curState[i]
            t = self.curState[i + 1:]
            self.curState = self.curState[:i]
            self.curState += [func, '('] + [num] + [')'] + t
            i += 2
            if (not self.check()):
                return

            ind = i
            while (ind > 0 and self.curState[ind - 2] in funcs):
                ind -= 2

            computedLine = ''.join(self.curState[ind: i + (i - ind)//2 + 1])
            self.line = self.calc.calculate(computedLine)
            self.computeLable()

    def compute(self):
        if (self.enteredDigits):
            self.curState.append(self.enteredDigits)
            self.enteredDigits = ''

        if (not self.check()):
            return

        self.computed = self.calc.calculate(self.getStr())
        self.line = self.computed
        self.computeLable()
        self.curState = []
        self.bracketCount = [0, 0]

    def computeLable(self):
        if (self.curState and self.curState[-1] in operators):
            self.lable = ''.join(self.curState)
        elif (self.curState):
            self.lable = ''.join(self.curState)
        elif (not self.curState):
            self.lable = ''

    def check(self) -> bool:
        if (self.bracketCount[0] > self.bracketCount[1]):
            self.curState.append(')')
            self.bracketCount[1] += 1
            return self.check()

        size = len(self.curState)
        i = 0
        while (i < size):
            if (self.curState[i] in operators):
                if (self.curState[i] != ')'):
                    if (i + 1 < len(self.curState) and self.curState[i + 1] in operators):
                        if (self.curState[i + 1] != '('):
                            self.curState.insert(i + 1, '0')
                            size = len(self.curState)
                    if (i + 1 == len(self.curState)):
                        self.curState.append('0')
                        size = len(self.curState)
            i += 1

        for i in range(len(self.curState)):
            if ('/' in self.curState[i] or self.curState[i] == '%'):
                if (i + 1 < len(self.curState) and self.curState[i + 1] == '('):
                    ind = None
                    count = 0
                    for j in range(i, len(self.curState)):
                        if (self.curState[j] == '('):
                            count += 1
                        if (self.curState[j] == ')'):
                            count -= 1
                            if (count == 0):
                                ind = j
                                break
                    if (ind):
                        temp = self.curState
                        self.curState = temp[i + 1: ind + 1]
                        if (self.check()):
                            v = self.calc.calculate(self.getStr())
                            self.curState = temp
                            if (v == '0'):
                                self.putErrorToLineEdit('div by zero')
                                return False
                        self.curState = temp

                elif (i + 1 < len(self.curState) and self.curState[i + 1] == '0'):
                    self.putErrorToLineEdit('div by zero')
                    return False

            if (self.curState[i] == 'sqrt'):
                ind = None
                count = 0
                for j in range(i, len(self.curState)):
                    if (self.curState[j] == '('):
                        count += 1

                    if (self.curState[j] == ')'):
                        count -= 1
                        if (count == 0):
                            ind = j
                            break

                if (ind):
                    temp = self.curState
                    self.curState = temp[i + 1: ind + 1]
                    if (self.check()):
                        v = self.calc.calculate(self.getStr())
                        self.curState = temp
                        if (v < '0'):
                            self.putErrorToLineEdit('below zero')
                            return False
                    self.curState = temp

            if (self.curState[i] == ')'):
                if (i + 1 < len(self.curState) and self.curState[i+1][-1].isdigit()):
                    self.curState.insert(i + 1, '+')
        return True

    def putErrorToLineEdit(self, error: str):
        self.curState = []
        self.computed = ''
        self.enteredDigits = ''
        self.line = error
        self.computeLable()


    def getStr(self) -> str:
        return ''.join(self.curState)

    def update(self):
        self.line = self.enteredDigits
        self.computeLable()

    def getLineEdit(self) -> str:
        return self.line

    def getLable(self) -> str:
        return self.lable

    def clearAll(self):
        self.curState = []
        self.computed = ''
        self.enteredDigits = ''
        self.computeLable()
        self.line = ''

    def clearLine(self):
        self.line = ''
        self.enteredDigits = ''
