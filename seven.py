from enum import Enum
import random
# start: 1:20
# end  : 1:46


class Suit(Enum):
    SPADE = 0
    HEART = 1
    DIAMOND = 2
    CLUB = 3

    def __str__(self):
        marks = ['♠', '♥', '♦', '♣']
        return marks[self.value]


class Card:

    def __init__(self, num, suit):
        self.num = num
        self.suit = Suit(suit)

    def __repr__(self):
        nums = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        return "{} {}".format(self.suit, nums[self.num - 1])

    def __str__(self):
        nums = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        return "{} {}".format(self.suit, nums[self.num - 1])

    def __eq__(self, other):
        return self.num == other.num and self.suit.value == other.suit.value

    def __ne__(self, other):
        return self.num != other.num or self.suit.value != other.suit.value


class Table:

    def __init__(self):
        self.table = [[None for i in range(13)] for j in range(4)]
        self.deck = []

        for row in range(len(self.table)):
            self.table[row][4] = str(Card(5, row))
            for col in range(len(self.table[0])):
                if col != 5:
                    c = Card(col, row)
                    self.deck.append(c)

        random.shuffle(self.deck)
        self.hands = [self.deck[:23], self.deck[24:]]

    def print_table(self):
        for row in self.table:
            print(row)

    def get(self, id):
        return self.hands[id]

    def set(self, card):
        self.table[card.suit.value][card.num - 1] = str(card)

    def can_discard(self, card):
        return self.table[card.suit.value][card.num] is not None \
            or self.table[card.suit.value][card.num - 2] is not None


class Player:

    def __init__(self, hands, table):
        self.hands = hands
        self.table = table

    def discard(self, card):
        if card in self.hands:
            self.hands.remove(card)
            return card
        else:
            print("{} is not in your hands.".format(card))
            return False

    def choices(self):
        choices = []
        for card in self.hands:
            if self.table.can_discard(card):
                choices.append(card)
        return choices


class Bot(Player):

    def discard(self):
        c = random.choice(self.choices())
        self.hands.remove(c)
        print('Bot discard: {}'.format(c))
        return c


if __name__ == '__main__':
    t = Table()
    hands1 = t.get(0)
    player1 = Player(hands1, t)
    hands2 = t.get(1)
    bot = Bot(hands2, t)

    t.print_table()
    while True:
        print('your hands:\n{}'.format(player1.hands))
        print('Your choices:\n{}'.format(player1.choices()))
        while True:
            hand = input().split(" ")
            mark = 0
            if hand[0] == '♠':
                mark = 0
            elif hand[0] == '♥':
                mark = 1
            elif hand[0] == '♦':
                mark = 2
            elif hand[0] == '♣':
                mark = 3
            else:
                mark = int(hand[0])

            c = Card(int(hand[1]), mark)
            if player1.discard(c) and t.can_discard(c):
                t.set(c)
                c = bot.discard()
                t.set(c)
                t.print_table()
                break
