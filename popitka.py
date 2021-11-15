import sqlite3
from random import shuffle

WHITE = 'WHITE'
BLACK = 'BLACK'


def smena(color):
    if color == WHITE:
        color = BLACK
    else:
        color = WHITE
    return color


def raund():
    return [['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp'],
            ['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp'],
            ['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp'],
            ['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp'],
            ['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp'],
            ['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp']]


class Board:
    def __init__(self):
        self.pole = raund()
        self.current = WHITE
        self.coloda = []  # колода игрока
        con = sqlite3.connect("Gvint.db")
        cur = con.cursor()
        self.result = cur.execute("""SELECT * FROM CART
            WHERE fraction like 'boys' """).fetchall()
        shuffle(self.result)
        # to do: раздача 13 карт с обязательной отдачей в 5карт
        podbor(self.coloda, Player, self.result)
        self.iicoloda = []  # колода компьютера
        self.result1 = cur.execute("""SELECT * FROM CART
            WHERE fraction like 'girls' """).fetchall()
        shuffle(self.result1)
        podbor(self.iicoloda, Intellect, self.result1)
        con.close()

    def ryadi(self, cart):
        if cart.type == 'Osadnoe':
            ryadi = [0, 5]
        elif cart.type == 'Archers':
            ryadi = [1, 4]
        elif cart.type == 'CloseFighter':
            ryadi = [2, 3]
        if (self.current == WHITE and cart.ability != 'Trap') \
                or (self.current == BLACK and cart.ability == 'Trap'):
            return ryadi[1]
        return ryadi[0]

    def hod(self):
        if self.current == WHITE:
            Player.move(self, self.coloda[0])
        else:
            Intellect.currentmove(self, self.iicoloda[0])


def podbor(coloda, Carta, result):
    res = []
    for i in range(len(result)):
        if i < 8:
            coloda.append(Carta(result[i][0], result[i][1],
                                result[i][2], result[i][4], result[i][5]))
            print(coloda[i].name)
        else:
            res.append(Carta(result[i][0], result[i][1],
                             result[i][2], result[i][4], result[i][5]))
            # print(res)
    # to do: замена карт при нажатии на карту
    print()
    result.clear()
    result.extend(res)  # для дальнейших действий с картами, которые не выпали игроку


class Player(Board):
    def __init__(self, name, cost, type, hero, ability):
        self.name = name
        self.hero = hero
        self.cost = cost
        self.type = type
        self.ability = ability

    def ability(self, cart):
        if cart.ability == 'Trap':
            self.coloda.extend(self.result[:2])
            self.result = self.result[2:]
        elif cart.ability == 'Summon':
            res = [i for i in self.coloda if i.ability == 'Prisivnic' \
                   and i.type == cart.type]
            rasnisa = len(self.coloda) - len(res) if \
                (len(self.coloda) - len(res) != len(self.coloda)) else 0
            self.coloda = [i for i in self.coloda if i.ability != 'Prisivnic' \
                           or i.type != cart.type]
            res1 = [i for i in self.result if i.ability == 'Prisivnic' \
                    and i.type == cart.type]
            self.result = [i for i in self.result if i.ability != 'Prisivnic' \
                           or i.type != cart.type]
            self.coloda.extend(res1)
            self.coloda.extend(res)
            for i in range(len(res1) + len(res)):
                deistvie = Player.move(self, self.coloda[-1], 1)
                if not deistvie:
                    if rasnisa > 0:
                        self.coloda.insert(0, self.coloda[-1])
                    else:
                        self.result.append(self.coloda[-1])
                    del self.coloda[-1]
                rasnisa -= 1

    def __repr__(self):
        return self.name

    def move(self, carta, prisivnic=0):
        ryad = self.ryadi(carta)
        if self.pole[ryad].count('emp') > 0:
            return Player.currentmove(self, ryad, carta, prisivnic)
        else:
            print(self.pole)
            a = input()
            return False
        # to do: return возвращает карту и ряд
        # to do: нажатие на карту, с показателем ряда, куда карта может переместиться

    def currentmove(self, ryad, carta, prisivnic):
        # print(self.pole[ryad].index('emp'))
        self.pole[ryad][self.pole[ryad].index('emp')] = carta
        del self.coloda[self.coloda.index(carta)]  # удаление выбранной карты из колоды
        if len(self.iicoloda) > 0 and prisivnic == 0:
            self.current = smena(self.current)
        Player.ability(self, carta)
        return True
        # to do: клик пользователя на карточку
        # to do: реализовать функции - способности с перемещением в ряд.
        # Способности карт учитываются


class Intellect(Board):
    def __init__(self, name, cost, type, hero, ability):  # to do: ИИ получает свою колоду карт
        self.name = name
        self.hero = hero
        self.cost = cost
        self.type = type
        self.ability = ability

    def ability(self, cart):
        # print(cart.name)
        if cart.ability == 'Trap':
            self.iicoloda.extend(self.result1[:2])
            self.result1 = self.result1[2:]
        elif cart.ability == 'Summon':
            res = [i for i in self.iicoloda if i.ability == 'Prisivnic' \
                   and i.type == cart.type]
            self.iicoloda = [i for i in self.iicoloda if i.ability != 'Prisivnic' \
                             or i.type != cart.type]
            rasnisa = len(self.iicoloda) - len(res) if \
                (len(self.iicoloda) - len(res) != len(self.iicoloda)) else 0
            res1 = [i for i in self.result1 if i.ability == 'Prisivnic' \
                    and i.type == cart.type]
            self.result1 = [i for i in self.result1 if i.ability != 'Prisivnic' \
                            or i.type != cart.type]
            self.iicoloda.extend(res1)
            self.iicoloda.extend(res)
            for i in range(len(res) + len(res1)):
                deistvie = Intellect.currentmove(self, self.iicoloda[-1], 1)
                if not deistvie:
                    if rasnisa > 0:
                        self.iicoloda.insert(0, self.iicoloda[-1])
                    else:
                        self.result1.append(self.iicoloda[-1])
                    del self.iicoloda[-1]
                rasnisa -= 1

    def __repr__(self):
        return self.name

    def currentmove(self, carta, prisivnic=0):
        ryad = self.ryadi(carta)
        # print(self.pole)
        self.pole[ryad][self.pole[ryad].index('emp')] = carta
        del self.iicoloda[self.iicoloda.index(carta)]
        if len(self.coloda) > 0 and prisivnic == 0:
            self.current = smena(self.current)
        Intellect.ability(self, carta)
        return True
        # to do: реализовать функции - способности с перемещением в ряд.
        # Способности карт учитываются


def main():
    desk = Board()
    winrade = 0
    winrade1 = 0
    while len(desk.coloda) > 0 or len(desk.iicoloda) > 0:
        # print(desk.coloda)
        # print(desk.iicoloda)
        desk.hod()
        first = 0
        second = 0
        print(desk.pole)
        for i in range(6):
            for ii in range(len(desk.pole[i])):
                if i < 3:
                    second += desk.pole[i][ii].cost if not isinstance(desk.pole[i][ii], str) else 0
                else:
                    first += desk.pole[i][ii].cost if not isinstance(desk.pole[i][ii], str) else 0
        # print(first, second)
        if len(desk.coloda) == 0 and len(desk.iicoloda) == 0:
            if first > second:
                winrade += 1
            else:
                winrade1 += 1
            # print(5555555555)
            # print(desk.pole)
            print(first, second)
            print(winrade, winrade1)
            desk = Board()
        # print(desk.pole)


main()
