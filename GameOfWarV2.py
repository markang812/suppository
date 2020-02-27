import random

################################################################################
class War:
    def playGame(self):
        self.playingField = Game(['King Crimson', 'Gold Experience Requiem'])
        self.playingField.dealCards()
        self.playingField.play()



################################################################################

class Game:

    def __init__(self, players):
        self.players = [Player(name, Hand()) for name in players]
        self.deck = CardDeck()
        self.rounds = 0
    
    def printFormat(self,string, line):
        print('\n{}\n{}'.format(string, line * len(string)))

    def dealCards(self):
        self.deck.shuffle()
        self.deck.setupPlayerHand(self.players)
        for player in self.players:
            player.showHand()

    def playOnce(self, tied=None):
        if tied is None:
            self.roundCount()
        collection = Pile()
        for player in (self.players if tied is None else tied):
            player.placeCard(collection)
            if tied:
                player.placeBonus(collection, 3)
        winner = collection.winner
        if winner is not None:
            collection.reward(winner)
        else:
            winner = self.playOnce(collection.tied)
            collection.reward(winner)
        return winner

    def roundCount(self):
        self.rounds += 1
        self.printFormat('Starting round {}'.format(self.rounds), '=')

    def play(self):
        while not self.finished:
            self.playOnce()
        self.showWinner()

    def showWinner(self):
        for player in self.players:
            if player.hand.has_cards:
                print()
                print(player.name, 'wins!')
                break

    @property
    def finished(self):
        return sum(bool(player.hand.cards) for player in self.players) == 1

################################################################################

class Player:

    def __init__(self, name, hand):
        self.name, self.hand = name, hand

    def placeCard(self, collection):
        if self.hand.has_cards:
            collection.addCards(self.hand.take_top(), self)

    def placeBonus(self, collection, count):
        collection.addBonuses(self.hand.cards[:count])
        self.hand.cards = self.hand.cards[count:]

    def giveCards(self, cards):
        self.hand.add_all(cards)

    def showHand(self):
        print(str(self.name)+ ' has ' + str(self.hand))

################################################################################

class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        return ', '.join(map(str, self.cards))

    def addCards(self, card):
        self.cards.append(card)

    def take_top(self):
        return self.cards.pop(0)

    def add_all(self, cards):
        self.cards.extend(cards)

    @property
    def has_cards(self):
        return bool(self.cards)

################################################################################

class CardDeck:

    def __init__(self):
        self.cards = [Card(s, r) for s in Card.SUITE for r in Card.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def setupPlayerHand(self, players):
        hands = [player.hand for player in players]
        while len(self.cards) >= len(players):
            for hand in hands:
                hand.addCards(self.cards.pop())
        return hands

################################################################################

class Card:

    SUITE = 'H D S C'.split()
    RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

    def __init__(self, suite, rank):
        self.suite, self.rank = suite, rank

    def __str__(self):
        return '{}-{}'.format(self.rank, self.suite)

    @property
    def value(self):
        return self.RANKS.index(self.rank)

################################################################################

class Pile:

    def __init__(self):
        self.cards = []
        self.players = []
        self.bonus = []

    def addCards(self, card, player):
        self.cards.append(card)
        self.players.append(player)

    def addBonuses(self, cards):
        self.bonus.extend(cards)

    @property
    def winner(self):
        self.show_pile()
        values = [card.value for card in self.cards]
        self.best = max(values)
        if values.count(self.best) == 1:
            return self.players[values.index(self.best)]

    def show_pile(self):
        for player, card in zip(self.players, self.cards):
            print('{} laid down a {}.'.format(player.name, card))

    def reward(self, player):
        player.giveCards(self.cards)
        player.giveCards(self.bonus)

    @property
    def tied(self):
        for card, player in zip(self.cards, self.players):
            if card.value == self.best:
                yield player

################################################################################

if __name__ == '__main__':
    game = War()
    game.playGame()