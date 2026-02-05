import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
# ui_test.py에서 Ui MainWindow를 import한다.
from demo1 import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)

        # button clicked 이벤트 핸들러로 button_clicked 함수와 연결한다.
        self.ui.pb_confirm.clicked.connect(self.button_clicked)

    def button_clicked(self):
    	# input 위젯의 텍스트를 output 위젯에 셋한다.
        inputText = self.ui.line_windows1.text()
        self.ui.line_windows2.setText('{0}'.format(inputText))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
