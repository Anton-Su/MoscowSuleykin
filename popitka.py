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
        # to do: раздача 13 карт с обязательной отдачей в 5 карт
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
        elif cart.type == 'ALL':
            ryadi = [[0, 1, 2], [3, 4, 5]]
        if (self.current == WHITE and cart.ability != 'Trap') \
                or (self.current == BLACK and cart.ability == 'Trap'):
            return ryadi[1]
        return ryadi[0]

    def hod(self):
        if self.current == WHITE:
            Player.move(self, self.coloda[0])
        else:
            Intellect.move(self, self.iicoloda[0])

    def ability(self, cart, coloda, result, gamer, ryad=0, coloda2=None):
        if coloda2 is None:
            coloda2 = []
        if cart.ability == 'Trap':
            coloda.extend(result[:2])
            res = result[2:]
            result.clear()
            result.extend(res)
        elif cart.ability == 'Summon':
            res = [i for i in coloda if i.ability == 'Prisivnic' \
                   and i.teamcod == cart.teamcod]
            rasnisa = len(coloda) - len(res)
            colodaex = [i for i in coloda if i.ability != 'Prisivnic' \
                           or i.teamcod != cart.teamcod]
            res1 = [i for i in result if i.ability == 'Prisivnic' \
                    and i.teamcod == cart.teamcod]
            resultex = [i for i in result if i.ability != 'Prisivnic' \
                           or i.teamcod != cart.teamcod]
            coloda.clear()
            coloda.extend(colodaex)
            coloda.extend(res1)
            coloda.extend(res)
            result.clear()
            result.extend(resultex)
            for i in range(len(res1) + len(res)):
                deistvie = gamer.move(self, coloda[-1], 1)
                if not deistvie:
                    if rasnisa > 0:
                        coloda.insert(0, coloda[-1])
                    else:
                        result.append(coloda[-1])
                    del coloda[-1]
                rasnisa -= 1
        elif cart.ability == 'Shadow':
            print(ryad)
            b = int(input())
            print(self.pole[b])
            bb = int(input())
            if b in ryad and not isinstance(self.pole[b][bb], str):
                coloda.append(self.pole[b][bb])
                self.pole[b][bb] = 'emp'
                del coloda[coloda.index(cart)]
                if len(coloda2) > 0:
                    self.current = smena(self.current)


def podbor(coloda, Carta, result):
    res = []
    for i in range(len(result)):
        if i < 8:
            coloda.append(Carta(result[i][0], result[i][1],
                                result[i][2], result[i][4],
                                result[i][5], result[i][6]))
            print(coloda[i].name)
        else:
            res.append(Carta(result[i][0], result[i][1],
                             result[i][2], result[i][4],
                             result[i][5], result[i][6]))
            # print(res)
    # to do: замена карт при нажатии на карту
    print()
    result.clear()
    result.extend(res)  # для дальнейших действий с картами, которые не выпали игроку


class Player(Board):
    def __init__(self, name, cost, type, hero, ability, teamcod):
        self.name = name
        self.hero = hero
        self.cost = cost
        self.type = type
        self.ability = ability
        self.teamcod = teamcod

    def __repr__(self):
        return self.name

    def move(self, carta, prisivnic=0):
        ryad = self.ryadi(carta)
        if carta.ability == 'Shadow':
            self.ability(carta, self.coloda, self.result, Player, ryad, self.iicoloda)
        elif self.pole[ryad].count('emp') > 0:
            return Player.currentmove(self, ryad, carta, prisivnic)
        else:
            print('переполнение')
            print(self.pole)
            a = input()
            return False
        # to do: return возвращает карту и ряд
        # to do: нажатие на карту, с показателем ряда, куда карта может переместиться

    def currentmove(self, ryad, carta, prisivnic):
        del self.coloda[self.coloda.index(carta)]  # удаление выбранной карты из колоды
        self.pole[ryad][self.pole[ryad].index('emp')] = carta
        self.ability(carta, self.coloda, self.result, Player)
        if len(self.iicoloda) > 0 and prisivnic == 0:
            self.current = smena(self.current)
        return True
        # to do: клик пользователя на карточку
        # to do: реализовать функции - способности с перемещением в ряд.
        # Способности карт учитываются


class Intellect(Board):
    def __init__(self, name, cost, type, hero, ability, teamcod):  # to do: ИИ получает свою колоду карт
        self.name = name
        self.hero = hero
        self.cost = cost
        self.type = type
        self.ability = ability
        self.teamcod = teamcod

    def __repr__(self):
        return self.name

    def move(self, carta, prisivnic=0):
        ryad = self.ryadi(carta)
        if carta.ability == 'Shadow':
            self.ability(carta, self.iicoloda, self.result1, Intellect, ryad, self.coloda)
        elif self.pole[ryad].count('emp') > 0:
            del self.iicoloda[self.iicoloda.index(carta)]
            self.pole[ryad][self.pole[ryad].index('emp')] = carta
            self.ability(carta, self.iicoloda, self.result1, Intellect)
            if len(self.coloda) > 0 and prisivnic == 0:
                self.current = smena(self.current)
            return True
        else:
            print(self.pole)
            print('try again')
            a = input()
            return False
        # to do: реализовать функции - способности с перемещением в ряд.
        # Способности карт учитываются


def main():
    desk = Board()
    winrade = 0
    winrade1 = 0
    while len(desk.coloda) > 0 or len(desk.iicoloda) > 0:
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
        if len(desk.coloda) == 0 and len(desk.iicoloda) == 0:
            if first > second:
                winrade += 1
            else:
                winrade1 += 1
            print(first, second)
            print(winrade, winrade1)
            desk = Board()


main()
