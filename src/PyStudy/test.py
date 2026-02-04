import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
# ui_test_ui.py에서 Ui MainWindow를 import한다.
from ui_test_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)

        # button clicked 이벤트 핸들러로 button_clicked 함수와 연결한다.
        self.ui.PB2.setText("버튼 2입니다")
        self.ui.PB1.clicked.connect(self.button_clicked1)
        self.ui.PB2.clicked.connect(self.button_clicked2)
        self.ui.PASSWORD_INPUT.focusInEvent = self.on_password_focus_in
        self.ui.RDIO_HOT.clicked.connect(self.RDIO_HOT_clicked)
        self.ui.RDIO_COLD.clicked.connect(self.RDIO_COLD_clicked)
        self.ui.checkBox.clicked.connect(self.checkbox_clicked)
        self.ui.checkBox_2.toggled.connect(self.checkbox_2_toggled)
        self.ui.comboBox_1.addItems(["선택 1", "선택 2", "선택 3", "선택 4"])

        self.items=["option1", "option2", "option3", "option4"]
        self.ui.comboBox_2.addItems(self.items)

    def RDIO_HOT_clicked(self):
        self.ui.CHOICE.setText("HOT 선택")

    def RDIO_COLD_clicked(self):
        self.ui.CHOICE.setText("COLD 선택")

    def button_clicked1(self):
    	# input 위젯의 텍스트를 output 위젯에 셋한다.
        inputText = self.ui.ID_INPUT.text()
        self.ui.ID.setText('{0}'.format(inputText))

    def button_clicked2(self):
    	# input 위젯의 텍스트를 output 위젯에 셋한다.
        txtBtn = self.ui.PB2.text()
        self.ui.EMERGENCY_TEXT.setText(txtBtn)

    def on_password_focus_in(self, event):
        self.ui.PASSWORD_INPUT.setText('')
        # QLineEdit의 원본 focusInEvent 호출
        from PySide6.QtWidgets import QLineEdit
        QLineEdit.focusInEvent(self.ui.PASSWORD_INPUT, event)

    def checkbox_clicked(self, checked):
        if checked:
            self.ui.CHECK_TEXT.setText("체크박스 1 선택됨")
        else:
            self.ui.CHECK_TEXT.setText("체크박스 1 해제됨")

    def checkbox_2_toggled(self, checked):
        if checked:
            self.ui.CHECK_TEXT.setText("체크박스 2 선택됨")
        else:
            self.ui.CHECK_TEXT.setText("체크박스 2 해제됨")

    def changeEvent(self, event):
        return super().changeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
