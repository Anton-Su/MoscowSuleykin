import sys  # Импортирует sys
from PyQt5 import uic, QtGui  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLabel, QWidget, QTableView
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import QSize, QTimer
from random import choice
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import pyglet
import sqlite3

animation = ["гифка3.gif", "гифка2.gif", "гифка.gif"]
vsriv = ["1.mp3", "2.mp3", "3.mp3"]
diction = {1: 'A',  # словарь, который перевод название первой клетки в букву
           2: 'B',
           3: 'C',
           4: 'D',
           5: 'E',
           6: 'F',
           7: 'G',
           8: 'H'}
WHITE = 'WHITE'  # константа, чтобы не ошибиться
BLACK = 'BLACK'
con = sqlite3.connect('Сheckers.db')
cur = con.cursor()
result = cur.execute('''delete from main''')
con.commit()


def opponent(color):  # функция, которая меняет цвет ходящей стороны
    if color == WHITE:
        color = BLACK
    else:
        color = WHITE
    return color


def opponent1(color):  # функция, которая в зависимости от играющей стороны доставляет картинку шашки
    if color == WHITE:
        coord = 'белая.png'
    else:
        coord = 'red.png'
    return coord


def opponent2(color):  # функция, которая в зависимости от играющей стороны доставляет картинку дамки
    if color == WHITE:
        coord = 'белая дамка.png'
    else:
        coord = 'red damka.png'
    return coord


def opponent3(time):
    if time > 180:
        cvet = int((300 - time) * 2.125)
        cvet1 = 255 - (int((300 - time) * 0.63))
        return cvet, cvet1, 0
    else:
        cvet = 179 - (int((180 - time) * 0.994))
        return 255, cvet, 0


class Board:  # класс доска
    def __init__(self):
        self.color = WHITE
        self.field = []
        for i in range(8):  # двойной список, который мы забиваем None, чтобы в последствии забить его экземплярами
            # наших классов
            self.field.append([None] * 8)
        self.field[0] = [Сheckers(WHITE), None, Сheckers(WHITE),
                         None, Сheckers(WHITE), None,
                         Сheckers(WHITE), None]
        self.field[1] = [
            None, Сheckers(WHITE), None, Сheckers(WHITE),
            None, Сheckers(WHITE), None, Сheckers(WHITE)]
        self.field[2] = [Сheckers(WHITE), None, Сheckers(WHITE),
                         None, Сheckers(WHITE), None,
                         Сheckers(WHITE), None]
        self.field[5] = [
            None, Сheckers(BLACK), None, Сheckers(BLACK),
            None, Сheckers(BLACK), None, Сheckers(BLACK)]
        self.field[6] = [Сheckers(BLACK), None, Сheckers(BLACK),
                         None, Сheckers(BLACK), None,
                         Сheckers(BLACK), None]
        self.field[7] = [None, Сheckers(BLACK), None,
                         Сheckers(BLACK), None, Сheckers(BLACK),
                         None, Сheckers(BLACK)]

    def current(self):
        return self.color

    def move_piece(self, row, col, button, count, count1, whitedamka, blackdamka):  # определение первого хода с
        # траекторией
        if str(self.field[row][col]) == self.color:
            self.cpisok = []
            vosmogno = True  # эта переменная будет разрешать / запрещать построение траектории
            if self.field[row][col].oposnavanie() == 'shacka':
                result, self.result2 = Сheckers.move(self, row, col, [(3, 3)], 2)
                if self.color == WHITE:
                    omega = 1
                else:
                    omega = -1
                if (whitedamka > 0 and self.color == WHITE) or (blackdamka > 0 and self.color == BLACK):
                    result2, self.result = Сrown.move(self, row, col, [(3, 3)], 2)
                    if result2 == 3:
                        vosmogno = False
                if result == 2 and vosmogno:
                    for i in self.result2:
                        if omega == i[0] - row and abs(i[1] - col) == 1:
                            self.cpisok.append(button[i[0]][i[1]])
                elif result == 3:
                    for i in range(len(self.result2)):
                        if i % 2 != 0 and abs(self.result2[i][0] - row) == abs(self.result2[i][1] - col) == 1 \
                                and abs(self.result2[i - 1][0] - row) == abs(self.result2[i - 1][1] - col) == 2:
                            self.cpisok.append(button[self.result2[i - 1][0]][self.result2[i - 1][1]])
            elif self.field[row][col].oposnavanie() == 'damka':
                result, self.result2 = Сrown.move(self, row, col, [(3, 3)], 2)
                if (count - whitedamka > 0 and self.color == WHITE) or (count1 - blackdamka > 0
                                                                        and self.color == BLACK):
                    result2, self.result = Сheckers.move(self, row, col, [(3, 3)], 2)
                    if result2 == 3:
                        vosmogno = False
                if result == 2 and vosmogno:
                    for i in self.result2:
                        if abs(i[0] - row) == abs(i[1] - col):
                            self.cpisok.append(button[i[0]][i[1]])
                elif result == 3:
                    for i in range(len(self.result2)):
                        if i % 2 != 0 and abs(self.result2[i][0] - row) == abs(self.result2[i][1] - col) \
                                and abs(self.result2[i - 1][0] - row) == abs(self.result2[i - 1][1] - col):
                            self.cpisok.append(button[self.result2[i][0]][self.result2[i][1]])
            for i in self.cpisok:
                i.setIcon(QIcon('зелёный.png'))
                i.setIconSize(QSize(56, 56))
            if len(self.cpisok) > 0:
                return str(self.field[row][col]) == self.color  # первый клик допустим только на свои фигуры

    def move(self, row, col, piece):  # второй клик
        for i in self.cpisok:
            i.setIcon(QIcon())  # стереть подсказки
        if self.field[piece[0][0]][piece[0][1]].oposnavanie() == 'shacka':  # если ходит шашка
            result = Сheckers.move(self, row, col, piece, 1)  # делаем проверку на то, что именно это шашка может ходить
            if result == 2:  # если шашка только может ходить, то надо проверить и на то, что дамка может только ходить
                # или её и вовсе не существует
                result1 = Сrown.move(self, row, col, piece, 1)
                if result1 == 3:  # если дамка рубит, то ход отменяется
                    return False
                else:
                    return Сheckers.move(self, row, col, piece)  # если всё хорошо, совершаем полноценный ход
            elif result == 3:  # если шашка рубит, то это удовлетворяет условиям
                return Сheckers.move(self, row, col, piece)
            else:
                return False
        elif self.field[piece[0][0]][piece[0][1]].oposnavanie() == 'damka':  # тоже самое, только наоборот
            result = Сrown.move(self, row, col, piece, 1)
            if result == 2:
                result1 = Сheckers.move(self, row, col, piece, 1)
                if result1 == 3:
                    return False
                else:
                    return Сrown.move(self, row, col, piece)
            elif result == 3:
                return Сrown.move(self, row, col, piece)
            else:
                return False

    def be_able_to(self, count, damka):  # проверим сторону на возможность играть дальше(застрявшая фигура)
        p = []
        if count - damka > 0:  # если есть обычные шашки
            p.append(Сheckers.move(self, 1, 2, [(3, 3)],
                                   3))  # просто рандомные аргументы, они при последнем аргументе == 3 не считаются
            # вообще
        if damka > 0:  # если есть дамка
            p.append(Сrown.move(self, 1, 2, [(3, 3)], 3))
        if 2 in p and len(p) == p.count(2):
            return 6  # код, значащмй поражение


class MyWidget(QMainWindow, Board):
    def __init__(self):
        super().__init__()
        uic.loadUi('igra.ui', self)  # Загружаем дизайн
        self.setWindowTitle('Шашки. Version - 3.45')
        self.initUI()

    def initUI(self):  # присоединяю картинки к кнопкам и лейблам,
        # устанавливаю размеры, присоединяю к функциям
        self.pixmap = QPixmap('pole.jpg')
        self.label.setPixmap(self.pixmap)
        self.pushButton.setIcon(QIcon('белая.png'))
        self.pushButton.setIconSize(QSize(60, 60))
        self.pushButton_3.setIcon(QIcon('белая.png'))
        self.pushButton_3.setIconSize(QSize(60, 60))
        self.pushButton_5.setIcon(QIcon('белая.png'))
        self.pushButton_5.setIconSize(QSize(60, 60))
        self.pushButton_7.setIcon(QIcon('белая.png'))
        self.pushButton_7.setIconSize(QSize(60, 60))
        self.pushButton_10.setIcon(QIcon('белая.png'))
        self.pushButton_10.setIconSize(QSize(60, 60))
        self.pushButton_12.setIcon(QIcon('белая.png'))
        self.pushButton_12.setIconSize(QSize(60, 60))
        self.pushButton_14.setIcon(QIcon('белая.png'))
        self.pushButton_14.setIconSize(QSize(60, 60))
        self.pushButton_16.setIcon(QIcon('белая.png'))
        self.pushButton_16.setIconSize(QSize(60, 60))
        self.pushButton_10.setIcon(QIcon('белая.png'))
        self.pushButton_17.setIconSize(QSize(60, 60))
        self.pushButton_17.setIcon(QIcon('белая.png'))
        self.pushButton_19.setIconSize(QSize(60, 60))
        self.pushButton_19.setIcon(QIcon('белая.png'))
        self.pushButton_21.setIcon(QIcon('белая.png'))
        self.pushButton_21.setIconSize(QSize(60, 60))
        self.pushButton_23.setIcon(QIcon('белая.png'))
        self.pushButton_23.setIconSize(QSize(60, 60))
        self.pushButton_42.setIcon(QIcon('red.png'))
        self.pushButton_42.setIconSize(QSize(60, 60))
        self.pushButton_44.setIcon(QIcon('red.png'))
        self.pushButton_44.setIconSize(QSize(60, 60))
        self.pushButton_46.setIcon(QIcon('red.png'))
        self.pushButton_46.setIconSize(QSize(60, 60))
        self.pushButton_48.setIcon(QIcon('red.png'))
        self.pushButton_48.setIconSize(QSize(60, 60))
        self.pushButton_49.setIcon(QIcon('red.png'))
        self.pushButton_49.setIconSize(QSize(60, 60))
        self.pushButton_51.setIcon(QIcon('red.png'))
        self.pushButton_51.setIconSize(QSize(60, 60))
        self.pushButton_53.setIcon(QIcon('red.png'))
        self.pushButton_53.setIconSize(QSize(60, 60))
        self.pushButton_55.setIcon(QIcon('red.png'))
        self.pushButton_55.setIconSize(QSize(60, 60))
        self.pushButton_58.setIcon(QIcon('red.png'))
        self.pushButton_58.setIconSize(QSize(60, 60))
        self.pushButton_60.setIcon(QIcon('red.png'))
        self.pushButton_60.setIconSize(QSize(60, 60))
        self.pushButton_62.setIcon(QIcon('red.png'))
        self.pushButton_62.setIconSize(QSize(60, 60))
        self.pushButton_64.setIcon(QIcon('red.png'))
        self.pushButton_64.setIconSize(QSize(60, 60))
        self.pushButton_65.setIcon(QIcon('restart.png'))
        self.pushButton_65.setIconSize(QSize(230, 230))
        self.pushButton_66.setIcon(QIcon('ничья.jpg'))
        self.pushButton_66.setIconSize(QSize(230, 230))
        self.pushButton_67.setIcon(QIcon('сдаться.jpg'))
        self.pushButton_67.setIconSize(QSize(230, 230))
        self.pushButton.clicked.connect(self.hello)
        self.pushButton_2.clicked.connect(self.hello)
        self.pushButton_3.clicked.connect(self.hello)
        self.pushButton_4.clicked.connect(self.hello)
        self.pushButton_5.clicked.connect(self.hello)
        self.pushButton_6.clicked.connect(self.hello)
        self.pushButton_7.clicked.connect(self.hello)
        self.pushButton_8.clicked.connect(self.hello)
        self.pushButton_9.clicked.connect(self.hello)
        self.pushButton_10.clicked.connect(self.hello)
        self.pushButton_11.clicked.connect(self.hello)
        self.pushButton_12.clicked.connect(self.hello)
        self.pushButton_13.clicked.connect(self.hello)
        self.pushButton_14.clicked.connect(self.hello)
        self.pushButton_15.clicked.connect(self.hello)
        self.pushButton_16.clicked.connect(self.hello)
        self.pushButton_17.clicked.connect(self.hello)
        self.pushButton_18.clicked.connect(self.hello)
        self.pushButton_19.clicked.connect(self.hello)
        self.pushButton_20.clicked.connect(self.hello)
        self.pushButton_21.clicked.connect(self.hello)
        self.pushButton_22.clicked.connect(self.hello)
        self.pushButton_23.clicked.connect(self.hello)
        self.pushButton_24.clicked.connect(self.hello)
        self.pushButton_25.clicked.connect(self.hello)
        self.pushButton_26.clicked.connect(self.hello)
        self.pushButton_27.clicked.connect(self.hello)
        self.pushButton_28.clicked.connect(self.hello)
        self.pushButton_29.clicked.connect(self.hello)
        self.pushButton_30.clicked.connect(self.hello)
        self.pushButton_31.clicked.connect(self.hello)
        self.pushButton_32.clicked.connect(self.hello)
        self.pushButton_33.clicked.connect(self.hello)
        self.pushButton_34.clicked.connect(self.hello)
        self.pushButton_35.clicked.connect(self.hello)
        self.pushButton_36.clicked.connect(self.hello)
        self.pushButton_37.clicked.connect(self.hello)
        self.pushButton_38.clicked.connect(self.hello)
        self.pushButton_39.clicked.connect(self.hello)
        self.pushButton_40.clicked.connect(self.hello)
        self.pushButton_41.clicked.connect(self.hello)
        self.pushButton_42.clicked.connect(self.hello)
        self.pushButton_43.clicked.connect(self.hello)
        self.pushButton_44.clicked.connect(self.hello)
        self.pushButton_45.clicked.connect(self.hello)
        self.pushButton_46.clicked.connect(self.hello)
        self.pushButton_47.clicked.connect(self.hello)
        self.pushButton_48.clicked.connect(self.hello)
        self.pushButton_49.clicked.connect(self.hello)
        self.pushButton_50.clicked.connect(self.hello)
        self.pushButton_51.clicked.connect(self.hello)
        self.pushButton_52.clicked.connect(self.hello)
        self.pushButton_53.clicked.connect(self.hello)
        self.pushButton_54.clicked.connect(self.hello)
        self.pushButton_55.clicked.connect(self.hello)
        self.pushButton_56.clicked.connect(self.hello)
        self.pushButton_57.clicked.connect(self.hello)
        self.pushButton_58.clicked.connect(self.hello)
        self.pushButton_59.clicked.connect(self.hello)
        self.pushButton_60.clicked.connect(self.hello)
        self.pushButton_61.clicked.connect(self.hello)
        self.pushButton_62.clicked.connect(self.hello)
        self.pushButton_63.clicked.connect(self.hello)
        self.pushButton_64.clicked.connect(self.hello)
        self.pushButton_65.clicked.connect(self.bye)
        self.pushButton_66.clicked.connect(self.draw)
        self.pushButton_67.clicked.connect(self.defeat)
        self.pushButton_68.clicked.connect(self.open_second_form)
        self.pushButton_69.clicked.connect(self.basadannic)
        self.piece = []
        self.buttonpiece1 = []
        self.white = 0  # проверка на ничью / поражение
        self.black = 0
        # список названий кнопок
        self.buttonname = [
            ['pushButton', 'pushButton_2', 'pushButton_3', 'pushButton_4', 'pushButton_5', 'pushButton_6',
             'pushButton_7', 'pushButton_8'],
            ['pushButton_9', 'pushButton_10', 'pushButton_11', 'pushButton_12', 'pushButton_13',
             'pushButton_14',
             'pushButton_15', 'pushButton_16'],
            ['pushButton_17', 'pushButton_18', 'pushButton_19', 'pushButton_20', 'pushButton_21',
             'pushButton_22',
             'pushButton_23', 'pushButton_24'],
            ['pushButton_25', 'pushButton_26', 'pushButton_27', 'pushButton_28', 'pushButton_29',
             'pushButton_30',
             'pushButton_31', 'pushButton_32'],
            ['pushButton_33', 'pushButton_34', 'pushButton_35', 'pushButton_36', 'pushButton_37',
             'pushButton_38',
             'pushButton_39', 'pushButton_40'],
            ['pushButton_41', 'pushButton_42', 'pushButton_43', 'pushButton_44', 'pushButton_45',
             'pushButton_46',
             'pushButton_47', 'pushButton_48'],
            ['pushButton_49', 'pushButton_50', 'pushButton_51', 'pushButton_52', 'pushButton_53',
             'pushButton_54',
             'pushButton_55', 'pushButton_56'],
            ['pushButton_57', 'pushButton_58', 'pushButton_59', 'pushButton_60', 'pushButton_61',
             'pushButton_62',
             'pushButton_63', 'pushButton_64']]
        # список кнопок
        self.buttonname1 = [
            [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.pushButton_5,
             self.pushButton_6,
             self.pushButton_7, self.pushButton_8],
            [self.pushButton_9, self.pushButton_10, self.pushButton_11, self.pushButton_12, self.pushButton_13,
             self.pushButton_14,
             self.pushButton_15, self.pushButton_16],
            [self.pushButton_17, self.pushButton_18, self.pushButton_19, self.pushButton_20, self.pushButton_21,
             self.pushButton_22,
             self.pushButton_23, self.pushButton_24],
            [self.pushButton_25, self.pushButton_26, self.pushButton_27, self.pushButton_28, self.pushButton_29,
             self.pushButton_30,
             self.pushButton_31, self.pushButton_32],
            [self.pushButton_33, self.pushButton_34, self.pushButton_35, self.pushButton_36, self.pushButton_37,
             self.pushButton_38,
             self.pushButton_39, self.pushButton_40],
            [self.pushButton_41, self.pushButton_42, self.pushButton_43, self.pushButton_44, self.pushButton_45,
             self.pushButton_46,
             self.pushButton_47, self.pushButton_48],
            [self.pushButton_49, self.pushButton_50, self.pushButton_51, self.pushButton_52, self.pushButton_53,
             self.pushButton_54,
             self.pushButton_55, self.pushButton_56],
            [self.pushButton_57, self.pushButton_58, self.pushButton_59, self.pushButton_60, self.pushButton_61,
             self.pushButton_62,
             self.pushButton_63, self.pushButton_64]]
        self.label_5.hide()  # прячу ничейный счётчик
        self.lineEdit.hide()
        self.count = 12  # количество фигур белых
        self.count1 = 12  # количество фигур чёрных
        self.listWidget_2.clear()  # очищаю виджет на случай перезапуска
        self.listWidget_2.addItem(f'White: {self.count}')  # устанавливаю счётчик
        self.listWidget_2.addItem(f'Dark: {self.count1}')
        self.whitedamka = 0  # количество дамок с каждой стороны
        self.blackdamka = 0
        self.mir = 0  # cчётчик проверки на ничью
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.timer11)
        self.timer01 = 300
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.timer22)
        self.timer02 = 300
        self.firstTurn = False  # на случай первого хода у белого(запуск таймера)
        self.peremerie = False

    def basadannic(self):
        self.third_form = ThirdForm()
        self.third_form.show()

    def draw(self):  # при нажатии на кнопку "ничья"
        if self.count1 > 0 and self.count > 0 and self.timer01 > 0 and self.timer02 > 0 and not self.peremerie:
            # делаю так, чтобы проигравший не мог предложить ничью
            name, ok = QInputDialog.getItem(self, 'Ничья?', '', ('да', 'нет'), 1, False)
            if name == 'да':
                self.timer2.stop()
                self.timer1.stop()
                self.listWidget.addItem(f'Запрос на ничью принят')
                cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                '{300 - int(self.timer02)}', 'ничья')''')
                self.peremerie = True
                con.commit()
            else:
                self.listWidget.addItem(f'Запрос на ничью отклонён')
                return 1

    def defeat(self):  # аналогично
        if self.count1 > 0 and self.count > 0 and self.timer01 > 0 and self.timer02 > 0 and not self.peremerie:
            name, ok = QInputDialog.getItem(self, 'Сдаётесь?', '', ('да', 'нет'), 1, False)
            if name == 'да':
                self.timer2.stop()
                self.timer1.stop()
                self.listWidget.addItem(f'Оппонент {self.color} сдался!')
                cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                            final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                            '{300 - int(self.timer02)}', '{self.color} сдался')''')
                con.commit()
                self.peremerie = True  # чтобы не было ошибок с повторным определением победителя
            else:
                self.listWidget.addItem(f'Оппонент {self.color} не сдался!')
                return 1

    def bye(self):  # перезапуск
        if self.count > 0 and self.count1 > 0 and self.timer01 > 0 \
                and self.timer02 > 0 and not self.peremerie:  # играть было ещё можно
            cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                    final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                    '{300 - int(self.timer02)}', 'игра прервана по техническим причинам')''')
        con.commit()
        self.hide()
        self.timer2.stop()
        self.timer1.stop()
        self.__init__()
        self.field[0] = [Сheckers(WHITE), None, Сheckers(WHITE),
                         None, Сheckers(WHITE), None,
                         Сheckers(WHITE), None]
        self.field[1] = [
            None, Сheckers(WHITE), None, Сheckers(WHITE),
            None, Сheckers(WHITE), None, Сheckers(WHITE)]
        self.field[2] = [Сheckers(WHITE), None, Сheckers(WHITE),
                         None, Сheckers(WHITE), None,
                         Сheckers(WHITE), None]
        self.field[5] = [
            None, Сheckers(BLACK), None, Сheckers(BLACK),
            None, Сheckers(BLACK), None, Сheckers(BLACK)]
        self.field[6] = [Сheckers(BLACK), None, Сheckers(BLACK),
                         None, Сheckers(BLACK), None,
                         Сheckers(BLACK), None]
        self.field[7] = [None, Сheckers(BLACK), None,
                         Сheckers(BLACK), None, Сheckers(BLACK),
                         None, Сheckers(BLACK)]
        self.show()
        self.listWidget.clear()

    def hello(self):
        if self.count1 > 0 and self.count > 0 and self.timer01 > 0 and self.timer02 > 0 and not self.peremerie:  # пока играть можно
            name = self.sender().objectName()  # определю номер кнопки, которую нажал пользовать
            for i in range(len(self.buttonname)):
                if name in self.buttonname[i]:
                    if len(self.piece) == 0:  # если кнопка является "первой"
                        result = Board.move_piece(self, i, self.buttonname[i].index(name), self.buttonname1,
                                                  self.count, self.count1, self.whitedamka, self.blackdamka)
                        # если кнопка соответвует цвету
                        if result:
                            music = pyglet.media.load('выбор.mp3')
                            music.play()
                            self.listWidget.addItem(f'Выбран квадрат '
                                                    f'{diction[self.buttonname[i].index(name) + 1]}{i + 1}'
                                                    f' - {self.color}')
                            self.piece.append((i, self.buttonname[i].index(name)))
                            self.buttonpiece1.append(self.sender())
                            if not self.firstTurn:
                                self.timer1.start(10)
                                self.firstTurn = True

                    else:
                        result = Board.move(self, i, self.buttonname[i].index(name), self.piece)
                        if result == 2:  # если можно ходить
                            music = pyglet.media.load('ходьба.mp3')
                            music.play()
                            self.listWidget.addItem(f'Перемещение на '
                                                    f'{diction[self.buttonname[i].index(name) + 1]}{i + 1}'
                                                    f' - {opponent(self.color)}')
                            self.buttonpiece1.append(self.sender())
                            if self.field[i][
                                self.buttonname[i].index(name)].oposnavanie() == 'shacka':  # если ходила обычная шашка
                                self.buttonpiece1[0].setIcon(QIcon(''))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                                self.buttonpiece1[1].setIcon(QIcon(opponent1(opponent(self.color))))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                            else:  # если ходила дамка
                                self.buttonpiece1[0].setIcon(QIcon(''))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                                self.buttonpiece1[1].setIcon(QIcon(opponent2(opponent(self.color))))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                        elif result:  # если "рубили"
                            self.pokas = True  # чтобы при отсчёте времени не зацикливался
                            x, y, count = result
                            x_ = self.buttonname1[x][y].x()  # узнать координаты точки взрыва
                            y_ = self.buttonname1[x][y].y()
                            self.label999 = QLabel(self)
                            self.label999.resize(60, 60)
                            self.label999.move(x_ + 1, y_ + 1)
                            self.label999.show()
                            self.movie = QMovie(choice(animation))  # рандом из 3 анимаций
                            self.label999.setMovie(self.movie)
                            self.movie.start()
                            self.movie.setSpeed(600)
                            self.timer = QTimer(self)
                            self.timer.timeout.connect(self.showTime)
                            self.timer.start(500)  # наша гифка идёт 0.5 секунд
                            music = pyglet.media.load(choice(vsriv))
                            music.play()
                            self.buttonpiece1.append(self.sender())
                            if self.field[i][
                                self.buttonname[i].index(name)].oposnavanie() == 'shacka':  # если ходила шашка
                                self.buttonpiece1[0].setIcon(QIcon(''))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                                self.buttonname1[x][y].setIcon(QIcon(''))
                                if len(count) == 0:  # если рубим "дважды" или т.п
                                    self.buttonpiece1[1].setIcon(QIcon(opponent1(opponent(self.current()))))
                                    self.listWidget.addItem(f'Съели на '
                                                            f'{diction[self.buttonname[i].index(name) + 1]}{i + 1}'
                                                            f' - {opponent(self.color)}')
                                else:
                                    self.buttonpiece1[1].setIcon(QIcon(opponent1(self.current())))
                                    self.listWidget.addItem(f'Съели на '
                                                            f'{diction[self.buttonname[i].index(name) + 1]}{i + 1}'
                                                            f' - {self.color}')
                            else:  # аналогично
                                self.buttonpiece1[0].setIcon(QIcon(''))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                                self.buttonpiece1[1].setIconSize(QSize(60, 60))
                                self.buttonname1[x][y].setIcon(QIcon(''))
                                self.buttonname1[x][y].setIconSize(QSize(60, 60))
                                if len(count) == 0:
                                    self.buttonpiece1[1].setIcon(QIcon(opponent2(opponent(self.current()))))
                                else:
                                    self.buttonpiece1[1].setIcon(QIcon(opponent2(self.current())))
                        else:
                            self.listWidget.addItem(f'Перемещение не удалось')
                        self.piece = []
                        self.buttonpiece1 = []
                        if self.color == WHITE:
                            self.timer2.stop()
                            self.timer1.start(10)
                        elif self.color == BLACK:
                            self.timer1.stop()
                            self.timer2.start(10)
                        self.count = 0  # обнуление
                        self.count1 = 0
                        for i in range(len(self.field)):
                            for ii in range(len(self.field[i])):
                                self.count += 1 if str(self.field[i][ii]) == WHITE else 0
                                self.count1 += 1 if str(self.field[i][ii]) == BLACK else 0
                        self.listWidget_2.clear()
                        self.listWidget_2.addItem(f'White: {self.count}')
                        self.listWidget_2.addItem(f'Dark: {self.count1}')
                        if self.color == BLACK and self.black == 0 \
                                and self.count - self.count1 >= 3:  # пк кинет вам предложение сдаться при условиях
                            self.listWidget.addItem(f'Компьютер предлагает чёрным сдаться')
                            self.black = self.defeat()  # чтобы пк не кидал предложения вечно
                        elif self.color == WHITE and self.white == 0 and self.count1 - self.count >= 3:  # аналогично
                            self.listWidget.addItem(f'Компьютер предлагает белым сдаться')
                            self.white = self.defeat()
                            # считаем количество дамок
                        self.whitedamka = sum([1 for i in range(len(self.field)) for ii in range(len(self.field[i])) if
                                               'WHITE' == str(self.field[i][ii]) and self.field[i][
                                                   ii].oposnavanie() == 'damka'])
                        self.blackdamka = sum([1 for i in range(len(self.field)) for ii in range(len(self.field[i])) if
                                               'BLACK' == str(self.field[i][ii]) and self.field[i][
                                                   ii].oposnavanie() == 'damka'])
                        if self.whitedamka == self.count and self.blackdamka == self.count1 and \
                                result is not False and result is not True:
                            if self.mir == 0:
                                self.listWidget.addItem(f'Компьютер предлагает cторонам помириться')
                                self.mir = self.draw()  # чтобы не кидал миры вечно
                                self.label_5.show()
                                self.lineEdit.show()
                            else:
                                # запускается отсчёт от 15(14)
                                if self.lineEdit.text() != '0':
                                    self.lineEdit.setText(str(int(self.lineEdit.text()) - 1))
                                    if self.lineEdit.text() == '0':
                                        cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                                                        final) VALUES({self.count}, {self.count1}, 
                                                        '{300 - int(self.timer01)}', 
                                                        '{300 - int(self.timer02)}', 'ничья')''')
                                        con.commit()
                                        self.peremerie = True
                                        self.listWidget.addItem(f'Ничья установлена')
                        d = 0
                        if self.color == WHITE and result is not False and result is not True:  # если ход состоялся
                            d = Board.be_able_to(self, self.count, self.whitedamka)
                            if d == 6:
                                d = 66
                        elif self.color == BLACK and result is not False and result is not True:
                            d = Board.be_able_to(self, self.count1, self.blackdamka)
                            if d == 6:
                                d = 666
                        if not(self.count1 > 0 and self.count > 0 and d != 666 and d != 66):
                            self.timer1.stop()
                            self.timer2.stop()
                            if self.count == 0 or d == 66:
                                cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                                            final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                                            '{300 - int(self.timer02)}', 'победа чёрных')''')
                                con.commit()
                                self.count = 0
                                self.listWidget.addItem(f'Победа чёрных')
                            elif self.count1 == 0 or d == 666:
                                cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                                            final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                                            '{300 - int(self.timer02)}', 'победа белых')''')
                                con.commit()
                                self.count1 = 0
                                self.listWidget.addItem(f'Победа белых')
                        else:
                            coord = opponent1(self.color)
                            if coord == 'белая.png':  # установим фон(белый или чёрный)
                                self.pixmap_2 = QPixmap('')
                                self.label_3.setPixmap(self.pixmap_2)
                            else:
                                self.pixmap_2 = QPixmap('чёрный фон.jpg')
                                self.label_3.setPixmap(self.pixmap_2)

    def showTime(self):  # остановка гифки с таймером
        if self.pokas:
            self.movie.stop()
            self.label999.hide()
            self.timer.stop()
            self.pokas = False

    def open_second_form(self):
        self.second_form = SecondForm()
        self.second_form.show()

    def timer11(self):
        if self.timer02 != 0 and self.timer01 - 0.01 > 0:
            self.timer01 -= 0.01
            sec = int(self.timer01) % 60
            if sec < 10:
                sec = '0' + str(sec)
            self.textEdit.setText(f'{int(self.timer01) // 60}:{sec}')
            v = opponent3(self.timer01)
            self.label_2.setStyleSheet(f'background: rgb{v}')
        else:
            self.timer01 = 0
            self.timer1.stop()
            cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                                                        final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                                                        '{300 - int(self.timer02)}', 'победа чёрных по времени')''')
            con.commit()
            self.listWidget.addItem(f'Победа чёрных по времени')
            self.textEdit.setText(f'0:00')

    def timer22(self):
        if self.timer02 - 0.01 > 0 and self.timer01 != 0:
            self.timer02 -= 0.01
            sec = int(self.timer02) % 60
            if sec < 10:
                sec = '0' + str(sec)
            self.textEdit_2.setText(f'{int(self.timer02) // 60}:{sec}')
            v = opponent3(self.timer02)
            self.label_6.setStyleSheet(f'background: rgb{v}')
        else:
            self.timer02 = 0
            self.timer2.stop()
            cur.execute(f'''INSERT INTO main(whitecount, blackcount, whitetime, blacktime, 
                                                                    final) VALUES({self.count}, {self.count1}, '{300 - int(self.timer01)}', 
                                                                    '{300 - int(self.timer02)}', 'победа белых по времени')''')
            con.commit()
            self.listWidget.addItem(f'Победа белых по времени')
            self.textEdit_2.setText(f'0:00')


class ThirdForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('База данных')
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('Сheckers.db')
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('main')
        model.select()
        view.setModel(model)
        view.resize(600, 600)


class SecondForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1500, 800)
        self.setWindowTitle('Правила игры')
        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap('туториал1.jpg'))
        self.lbl_pict.resize(200, 200)
        self.lbl_pict.move(800, 40)
        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap('туториал2.jpg'))
        self.lbl_pict.resize(200, 200)
        self.lbl_pict.move(1100, 40)
        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap('туториал3.jpg'))
        self.lbl_pict.resize(200, 200)
        self.lbl_pict.move(750, 260)
        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap('туториал4.jpg'))
        self.lbl_pict.resize(200, 200)
        self.lbl_pict.move(1050, 260)
        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap('туториал5.jpg'))
        self.lbl_pict.resize(300, 200)
        self.lbl_pict.move(700, 490)
        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap('туториал6.jpg'))
        self.lbl_pict.resize(300, 200)
        self.lbl_pict.move(1025, 490)
        self.lbl = QLabel('''
                                                                                                        Основные догмы этой игры: 
                                                                                                        
        
        1) Зелёные значки (кружки) - допустимая траектория 
        движения выбранной шашки.
        
        
        2) Игра позволяет шашкам есть вперёд и назад,
         игрок сам волен выбирать, сколько шашек съест за ход. 
        
        
        3) Игрок волен съесть любую шашку, которая удовлетворяет 
        стандартным условиям. Нет обязательного правила 
        "где больше потенциальных съедений, такой и твой ход".
        
        
        4) Дамкой здесь стать можно в случае перехода чёрной шашки
         на первую или белой шашки на восьмую клетки. 
        
        
        5) Если новая дамка стала таковой в результате съедения фигуры, то
        она продолжает свой ход, если есть, что она может съесть, как дамка.
        
        
        6) Ничья проста: если у противника и соперника есть только дамки,
         ставится отсчёт, длительностью в 15 ходов. 
         Не успели определить победителя - мир.
        
        
        7) Поражение наступает в следствии истечения времени 
        или лишении противника всех его фигур. 
        
        
        8) Зажатость фигур соперника учтена и считается поражением.''', self)

        self.lbl.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.lbl.adjustSize()


class Сrown(Board):  # класс дамка
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color

    def oposnavanie(self):
        return 'damka'

    def move(self, row, col, piece, proverka=0):
        count = []  # рубления
        count1 = []  # ходы без рублений
        row1, col1 = piece[0]
        for i in range(len(self.field)):  # алгоритм вычисления всех возможных кодов и рублений
            for ii in range(len(self.field[i])):
                if self.color == str(self.field[i][ii]) and self.field[i][ii].oposnavanie() == 'damka':
                    def tabi2(row2, col2, p, vremen):
                        if str(self.field[row2][col2]) == self.color:
                            p[0] = 5
                        if str(self.field[row2][col2]) == opponent(self.color):
                            if p[0] == 0:
                                p[0] = p[0] + 1
                                vremen.append(row2)
                                vremen.append(col2)
                            elif p[0] == 1:
                                p[0] = 5
                        if str(self.field[row2][col2]) == 'None' and p[0] != 5:
                            if p[0] == 0:
                                count1.append((row2, col2))
                            if len(vremen) == 2:
                                count.append((vremen[0], vremen[1]))
                                count.append((row2, col2))
                            p[0] = 0

                    def tabi(i=i, ii=ii):
                        j = 7 - i
                        j1 = i
                        p = [0]
                        vremen = []
                        for iii in range(1, j + 1):
                            if 8 > i + iii > -1 and 8 > ii + iii > -1:
                                tabi2(i + iii, ii + iii, p, vremen)
                        p = [0]
                        vremen = []
                        for iii in range(1, j + 1):
                            if 8 > i + iii > -1 and 8 > ii - iii > -1:
                                tabi2(i + iii, ii - iii, p, vremen)
                        p = [0]
                        vremen = []
                        for iii in range(1, j1 + 1):
                            if 8 > i - iii > -1 and 8 > ii + iii > -1:
                                tabi2(i - iii, ii + iii, p, vremen)
                        p = [0]
                        vremen = []
                        for iii in range(1, j1 + 1):
                            if 8 > i - iii > -1 and 8 > ii - iii > -1:
                                tabi2(i - iii, ii - iii, p, vremen)

                    tabi()
        if len(count) == 0 and len(count1) > 0 and proverka == 0 \
                and (row, col) in count1 \
                and abs(row - row1) == abs(col - col1):  # если всё по - настоящему и ходить можно только
            piice = self.field[row1][col1]
            self.field[row1][col1] = None
            self.field[row][col] = piice
            self.color = opponent(self.color)
            return 2
        elif len(count) > 0 and proverka == 0 and (row, col) in count and \
                count.index((row, col)) % 2 != 0:
            popitka = []
            for i in range(len(count)):
                if count[i] != (row, col):
                    if abs(count[i][0] - piece[0][0]) == abs(count[i][1] - piece[0][1]):
                        popitka.append(count[i - 1])
                        popitka.append(count[i])
            d = popitka.index((row, col))
            # всё по - настоящему, можно рубить
            x, y = popitka[d - 1]
            piice = self.field[row1][col1]
            self.field[x][y] = None
            self.field[row1][col1] = None
            self.field[row][col] = piice
            count = []
            tabi(row, col)
            if len(count) == 0:
                self.color = opponent(self.color)
            return x, y, count
        if len(count) == 0 and len(count1) == 0 and proverka == 3:
            return 2
        elif proverka == 3:
            return 3
        if proverka != 0 and len(count) > 0:
            if proverka == 1:
                return 3
            else:
                return 3, count
        if proverka != 0 and len(count) == 0:
            if proverka == 1:
                return 2
            else:
                return 2, count1
        else:
            return False


class Сheckers(Board):  # почти аналогично, класс шашка
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color

    def oposnavanie(self):
        return 'shacka'

    def move(self, row, col, piece, proverka=0):
        massiv = []
        count = []
        row1, col1 = piece[0]
        if self.color == WHITE:
            omega = row - row1
        else:
            omega = row1 - row
        for i in range(len(self.field)):
            for ii in range(len(self.field[i])):
                if self.color == str(self.field[i][ii]) and self.field[i][ii].oposnavanie() == 'shacka':
                    def tabi2(z, vremen):
                        if 7 >= z[0] >= 0 and 7 >= z[1] >= 0:
                            if 6 >= z[0] >= 1 and 6 >= z[1] >= 1 and str(self.field[z[0]][z[1]]) == opponent(
                                    self.color):
                                if vremen == 1 and str(self.field[z[0] + 1][z[1] + 1]) == 'None':
                                    count.append((z[0] + 1, z[1] + 1))
                                    count.append((z[0], z[1]))
                                if vremen == 2 and str(self.field[z[0] + 1][z[1] - 1]) == 'None':
                                    count.append((z[0] + 1, z[1] - 1))
                                    count.append((z[0], z[1]))
                                if vremen == 3 and str(self.field[z[0] - 1][z[1] + 1]) == 'None':
                                    count.append((z[0] - 1, z[1] + 1))
                                    count.append((z[0], z[1]))
                                if vremen == 4 and str(self.field[z[0] - 1][z[1] - 1]) == 'None':
                                    count.append((z[0] - 1, z[1] - 1))
                                    count.append((z[0], z[1]))
                            if self.color == WHITE and (vremen == 1 or vremen == 2) and \
                                    str(self.field[z[0]][z[1]]) == 'None':
                                massiv.append(z)
                            elif self.color == BLACK and (vremen == 3 or vremen == 4) and \
                                    str(self.field[z[0]][z[1]]) == 'None':
                                massiv.append(z)

                    def tabi(i=i, ii=ii):
                        tabi2((i + 1, ii + 1), 1)
                        tabi2((i + 1, ii - 1), 2)
                        tabi2((i - 1, ii + 1), 3)
                        tabi2((i - 1, ii - 1), 4)

                    tabi()
        if len(count) == 0 and len(massiv) > 0 and omega == abs(col1 - col) == 1 \
                and (row, col) in massiv and proverka == 0:
            piice = self.field[row1][col1]
            self.field[row1][col1] = None
            self.field[row][col] = piice
            if self.color == WHITE and row == 7:
                self.field[row][col] = Сrown(WHITE)
            elif self.color == BLACK and row == 0:
                self.field[row][col] = Сrown(BLACK)
            self.color = opponent(self.color)
            return 2
        elif len(count) > 0 and (row, col) in count and \
                proverka == 0 and abs(row - row1) == abs(col1 - col) == 2:
            popitka = []
            for i in range(len(count)):
                if count[i] != (row, col):
                    if abs(count[i][0] - piece[0][0]) == abs(count[i][1] - piece[0][1]) == 1:
                        popitka.append(count[i - 1])
                        popitka.append(count[i])
            x, y = popitka[popitka.index((row, col)) + 1]
            piice = self.field[row1][col1]
            self.field[x][y] = None
            self.field[row1][col1] = None
            self.field[row][col] = piice
            count = []
            if self.color == WHITE and row == 7:
                self.field[row][col] = Сrown(WHITE)
                result, result1 = Сrown.move(self, 1, 2, [(3, 3)], 2)
                if result == 3:
                    count = result1
                else:
                    self.color = opponent(self.color)
            elif self.color == BLACK and row == 0:
                self.field[row][col] = Сrown(BLACK)
                result, result1 = Сrown.move(self, 1, 2, [(3, 3)], 2)
                if result == 3:
                    count = result1
                else:
                    self.color = opponent(self.color)
            else:
                tabi(row, col)
                if len(count) == 0:
                    self.color = opponent(self.color)
            return x, y, count
        if len(count) == 0 and len(massiv) == 0 and proverka == 3:
            return 2
        elif proverka == 3:
            return 3
        if proverka != 0 and len(count) > 0:
            if proverka == 1:
                return 3
            else:
                return 3, count
        if proverka != 0 and len(count) == 0:
            if proverka == 1:
                return 2
            else:
                return 2, massiv
        else:
            return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


main()
