from PyQt5.QtWidgets import *
import operator
from Graphics import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        for n in range(0, 10):
            getattr(self, 'pushButton_n%s' % n).pressed.connect(lambda v = n: self.input_number(v))

        self.pushButton_add.pressed.connect(lambda: self.operation(operator.add))
        self.pushButton_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.pushButton_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.pushButton_div.pressed.connect(lambda: self.operation(operator.truediv))
        self.pushButton_sqrt.pressed.connect(self.operation_sqrt)
        self.pushButton_eq.pressed.connect(self.equals)
        self.actionReset.triggered.connect(self.reset)
        self.pushButton_ac.pressed.connect(self.reset)
        self.actionExit.triggered.connect(self.close)
        self.pushButton_plus_minus.pressed.connect(self.plus_minus)
        self.pushButton_percent.pressed.connect(self.percent)
        self.pushButton_del.pressed.connect(self.delete_element)
        self.memory = 0;
        self.reset()
        self.show()

    def delete_element(self):
        self.stack[-1] = self.stack[-1]//10;
        self.display()

    def display(self):
        self.lcdNumber.display(self.stack[-1])

    def reset(self):
        self.state = 0
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def plus_minus(self):
        self.stack[-1] = -1*self.stack[-1];
        self.display()

    def percent(self):
        self.stack[-1] = self.stack[-1] * 0.01;
        self.display()
        

    def input_number(self, v):
        if self.state == 0:
            self.state = 1
            self.stack[-1] = v
        elif len(str(self.stack[-1]))<9:
            self.stack[-1] = self.stack[-1] * 10 + v
        else:
            self.display()
            return
        self.display()

    def operation(self, op):
        if self.current_op:
            self.equals()

        self.stack.append(0)
        self.state = 1
        self.current_op = op

    def operation_sqrt(self):
        self.state = 1
        if self.stack[-1]>0:
            self.stack[-1] = (self.stack[-1])**0.5;
            self.display()
        else:
            self.state = 0
            self.stack = [0]
            self.last_operation = None
            self.current_op = None
            self.lcdNumber.display("Error");
            
        

    def equals(self):
        if self.state == 0 and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Error')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = 0
                self.stack[-1] = round(self.stack[-1],2);
                if len(str(self.stack[-1]))<10:
                    self.display()
                else:
                    self.state = 0
                    self.stack = [0]
                    self.last_operation = None
                    self.current_op = None
                    self.lcdNumber.display("Error");

if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Calculator")

    window = MainWindow()
    app.exec_()

