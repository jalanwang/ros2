import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QFile
# ui_test.py에서 Ui MainWindow를 import한다.
from table_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)
        self.set_TableData()
        self.ui.tbl_student.itemClicked.connect(self.tbl_student_itemClicked)

    def set_TableData(self):
        table = self.ui.tbl_student
        table.setRowCount(4)
        table.setColumnCount(3)


        data = [
            ["이세빈","20170001","글로벌미디어학부"],
            ["김민수","20170002","전자정보공학부"],
            ["홍길동,","20180003","소프트웨어학부"],
            ["이석준","2019000","컴퓨터 학부"]
        ]

        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QTableWidgetItem(data[row][col])
                table.setItem(row,col,item)

    def tbl_student_itemClicked(self, item):
         print("Clicked cell value:", item.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
