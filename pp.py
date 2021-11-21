import sys
import csv
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QTableWidgetItem, QTableWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('Распознавание фотографии')
        self.label_ = QLabel('Cъедобно, вероятно, это фрукт', self)
        self.label_.move(125, 25)
        self.label_.resize(400, 100)
        self.label_.hide()
        self.btn = QPushButton('Загрузить фотографию', self)
        self.btn.resize(200, 200)
        self.btn.move(100, 100)
        self.btn1 = QPushButton('retry', self)
        self.btn1.resize(150, 50)
        self.btn1.move(0, 0)
        self.btn2 = QPushButton('ok', self)
        self.btn2.resize(100, 50)
        self.btn2.move(100, 300)
        self.btn2.setStyleSheet(f'background: rgb(0, 255, 0)')
        self.btn3 = QPushButton('not ok', self)
        self.btn3.resize(100, 50)
        self.btn3.move(200, 300)
        self.btn3.setStyleSheet(f'background: rgb(255, 0, 0)')
        self.btn3.hide()
        self.btn2.hide()
        self.btn4 = QPushButton('Редактировать шаблон', self)
        self.btn4.move(390, 100)
        self.btn4.resize(200, 50)
        self.label = QLabel(self)
        self.label.resize(200, 200)
        self.label.move(100, 100)
        self.label.hide()
        # Подпишем функцию-слот self.count() на сигнал clicked кнопки btn
        self.btn.clicked.connect(self.count)
        self.btn1.clicked.connect(self.count1)
        self.loadTable('excel.csv')
        self.btn4.clicked.connect(self.loadtable)

    def loadtable(self):
        self.tableWidget.show() if self.tableWidget.isHidden() else self.tableWidget.hide()

    def loadTable(self, name):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(340, 170)
        self.tableWidget.resize(350, 130)
        with open(name) as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.hide()

    def count(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if fname:
            self.pixmap = QPixmap(fname)
            self.label.setPixmap(self.pixmap)
            self.label.show()
            self.btn.hide()
            self.btn2.show()
            self.btn3.show()
            self.label_.show()

    def count1(self):
        self.hide()
        self.__init__()
        self.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

main()