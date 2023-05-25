from PyQt5 import QtWidgets, QtGui
from CalculatorUI import Ui_MainWindow
from CalculatorModel import CalculatorModel

class Calculator(QtWidgets.QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.calculatorModel = CalculatorModel()

        self.ui.lineEditInput.setReadOnly(True)
        self.ui.lineEditInput.setText('0')
        self.ui.lableCurrentExpr.setText(self.calculatorModel.getLable())

        self.ui.pushButton0.clicked.connect(lambda: self.inputNums('0'))
        self.ui.pushButton1.clicked.connect(lambda: self.inputNums('1'))
        self.ui.pushButton2.clicked.connect(lambda: self.inputNums('2'))
        self.ui.pushButton3.clicked.connect(lambda: self.inputNums('3'))
        self.ui.pushButton4.clicked.connect(lambda: self.inputNums('4'))
        self.ui.pushButton5.clicked.connect(lambda: self.inputNums('5'))
        self.ui.pushButton6.clicked.connect(lambda: self.inputNums('6'))
        self.ui.pushButton7.clicked.connect(lambda: self.inputNums('7'))
        self.ui.pushButton8.clicked.connect(lambda: self.inputNums('8'))
        self.ui.pushButton9.clicked.connect(lambda: self.inputNums('9'))
        self.ui.pushButtonDot.clicked.connect(lambda: self.inputNums('.'))

        self.ui.pushButtonPlus.clicked.connect(lambda: self.inputOps('+'))
        self.ui.pushButtonMinus.clicked.connect(lambda: self.inputOps('-'))
        self.ui.pushButtonMult.clicked.connect(lambda: self.inputOps('*'))
        self.ui.pushButtonDiv.clicked.connect(lambda: self.inputOps('/'))
        self.ui.pushButtonMod.clicked.connect(lambda: self.inputOps('%'))

        self.ui.pushButtonBracketL.clicked.connect(lambda: self.inputOps('('))
        self.ui.pushButtonBracketR.clicked.connect(lambda: self.inputOps(')'))

        self.ui.pushButtonFactorial.clicked.connect(lambda: self.inputFunc('fact'))
        self.ui.pushButtonSqrt.clicked.connect(lambda: self.inputFunc('sqrt'))
        self.ui.pushButtonSqr.clicked.connect(lambda: self.inputFunc('sqr'))
        self.ui.pushButtonPLusMinus.clicked.connect(lambda: self.inputFunc('inv'))
        self.ui.pushButtonX_1.clicked.connect(lambda: self.inputFunc('1/'))

        self.ui.pushButtonC.clicked.connect(self.clearAll)
        self.ui.pushButtonCe.clicked.connect(self.clearLine)

        self.ui.pushButtonDel.clicked.connect(self.delete)
        self.ui.pushButtonEqual.clicked.connect(self.compute)

    def update(self):
        self.ui.lineEditInput.setText(self.calculatorModel.getLineEdit())
        self.ui.lableCurrentExpr.setText(self.calculatorModel.getLable())

    def delete(self):
        self.calculatorModel.delete()
        self.update()

    def compute(self):
        self.calculatorModel.compute()
        self.update()

    def inputNums(self, key):
        self.calculatorModel.inputDigits(key)
        self.update()

    def inputOps(self, key):
        self.calculatorModel.tryAddOp(key)
        self.update()

    def inputFunc(self, func):
        self.calculatorModel.tryAddFunc(func)
        self.update()

    def clearAll(self):
        self.calculatorModel.clearAll()
        self.update()

    def clearLine(self):
        self.calculatorModel.clearLine()
        self.update()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Calculator()
    MainWindow.show()
    sys.exit(app.exec_())