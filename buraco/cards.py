import emoji
import random
import curses
from curses import wrapper
spade, heart, club, diamond = emoji.emojize(":spade_suit:"), emoji.emojize(":heart_suit:"), emoji.emojize(":club_suit:"), emoji.emojize(":diamond_suit:")



class Node:
  def __init__(self, value, link_node=None):
    self.value = value
    self.link_node = link_node
    
  def set_link_node(self, link_node):
    self.link_node = link_node
    
  def get_link_node(self):
    return self.link_node
  
  def get_value(self):
    return self.value


class Card:
    ordem = "A234567891JQKA"

    def __init__(self, suit, rank, coringa = False):
        self.suit = suit
        self.rank = str(rank)
        self.place = self.ordem.find(rank)
        self.coringa = coringa
        self.chosen = False
        self.played = False
        self.mesa = False
        if rank == "1":
            self.rank += "0"
            self.esqueleto = f"""
                -------
               |{self.rank}    {self.suit}|
               |       |
               |       |
               |{self.suit}    {self.rank}|
                -------"""
        elif rank == "JOKER":
            self.esqueleto = f"""
                -------
               |{self.rank} {self.suit}|
               |       |
               |       |
               |{self.suit} {self.rank}|
                -------"""
        else:
            self.esqueleto = f"""
                -------
               |{self.rank}     {self.suit}|
               |       |
               |       |
               |{self.suit}     {self.rank}|
                -------"""
        if rank == "2":
            self.points = 10
        elif rank == "A":
            self.points = 15
        elif rank.isalpha():
            self.points = 10
        elif int(rank) < 8:
            self.points = 5
        elif rank == "JOKER":
            self.points = 20
        else:
            self.points = 10 
    def __repr__(self):
        return self.esqueleto
class Mão:
    ordem = "A234567891JQKA"
    
    
    def __init__(self, quant, points = 0, cards: list=None):
        self.quant = quant
        self.points = points
        self.cartas = cards if not cards is None else []
        self.suit = cards[0].suit
    
    
    def __add__(self, same):
        if type(same) is Mão:
            temp = None
            if self.suit != same.suit:
                return ValueError
            if same.cartas[0].place < self.cartas[-1].place:
                temp = same.cartas + self.cartas
            else:
                temp = self.cartas + same.cartas
            return temp
        

    def check_if_valid(self):
        last = self.cartas[0]
        for i in self.cartas:
            current = i
            if current.suit != last.suit and (not current.coringa or not last.coringa):
                return False
            else:
                last = current
                continue



    def check_limpa(self):
        point = ""
        for i in self.cartas:
            point += i.rank
        print(point)
        if self.ordem.find(point) >= 0:
            return True
        else:
            return False
class Jogo:
    rules = {
        "trinca" : False,
        "coringao" : False
    }
    def __init__(self, *args):
        self.players = []
        for arg in args:
            self.players.append(arg)
        if self.rules.coringao:
            self.baralho = Baralho(True,2)
        else:
            self.baralho = Baralho(False,2)
        self.baralho.distribuir(args)
        self.baralho.give_morto()
        self.mesa = Jogador(self.baralho.pop(0))
    

        


class Baralho:
    naipes = [emoji.emojize(":spade_suit:"), emoji.emojize(":heart_suit:"), emoji.emojize(":club_suit:"), emoji.emojize(":diamond_suit:")]
    ranks = "A234567891JQK"
    
    def __init__(self, coringa = True,quant = 1):
        self.coringa = coringa
        self.cartas = []
        self.morto = {}
        for i in range(quant):
            for naipe in self.naipes:
                for rank in self.ranks:
                    if rank == "2":
                        self.cartas.append(Card(naipe,rank,True))
                    elif rank == "A":
                        self.cartas.append(Card(naipe,rank))
                    elif rank.isalpha():
                        self.cartas.append(Card(naipe,rank))
                    elif int(rank) < 8:
                        self.cartas.append(Card(naipe,rank))
                    else:
                        self.cartas.append(Card(naipe,rank))
            if self.coringa:
                self.cartas.append(Card("*","JOKER", True))
                self.cartas.append(Card("*","JOKER", True))
        


    
    def __len__(self):
        return len(self.cartas)

    def give(self):
        return self.cartas.pop(-1)

    def embaralhar(self):
        random.shuffle(self.cartas)
    def distribuir(self, *args):
        for jogador in args:
            cards = random.sample(self.cartas, k=11)
            for card in cards:
                #temp = card
                #leng = len(jogador)
                if card in self.cartas:
                    #temp = self.cartas.pop(self.cartas.index(card))
                    jogador.add_card(self.cartas.pop(self.cartas.index(card)))
                    #print(f'Given a {temp.rank}{temp.suit} to {jogador.nome} {leng}')
            
    def give_morto(self):
        for i in range(2):
            cards = random.sample(self.cartas, k=11)
            for card in cards:
                #temp = card
                #leng = len(jogador)
                if card in self.cartas:
                    #temp = self.cartas.pop(self.cartas.index(card))
                    self.cartas.pop(self.cartas.index(card))
                    #print(f'Given a {temp.rank}{temp.suit} to {jogador.nome} {leng}')
            self.morto[i] = cards
    def pop(self,item):
        return self.cartas.pop(self.cartas.index(item))


class Jogador:
    
    def __init__(self,nome, cards = None):
        self.cards = cards if cards is not None else {}
        self.nome = nome
        self.passed = False
        self.inhand = 0

    def __len__(self):
        count = 0
        for naipe in self.cards.values():
            for i in naipe:
                count += 1
        return count

    

    def turn(self):
        while not self.passed:
            pin = input(f"{self.nome}'s turn: Vai comprar daonde?")
            pin = pin.lower()
            if pin == "mesa":
                for card in mesa:
                    self.add_card(card)
            elif pin == "bolo":
                self.add_card(bolo.cartas.give(-1))

            else:
                pass

            self.passed = True if pin == "pass" else False
        self.passed = False
    


    def add_card(self, card):
        if type(card) is Card:
            if not card.suit in self.cards.keys():
                self.cards.setdefault(card.suit, [card])
                self.inhand += 1
                return
            else:
                self.cards[card.suit].append(card)
                self.inhand += 1
                return
    
    #Just checking if everything is going where it's supposed to
    def show(self):
        for i in self.cards.values():
            for x in i:
                print(f"{self.nome} has a {x.rank}{x.suit}")
    
    def get_cards(self):
        display = []
        for naipe in self.cards.values():
            for i in naipe:
                display += [i.esqueleto]
        return display
        
        
    
    def get_suits(self):
        for k in self.cards.keys():
            print(k)
        print(len(self.cards.keys()))
    
    def play_hand(self,cards):
        points = 0
        for i in cards:
            points += i.points
        mao = Mão(len(cards),points,cards)

def display_cards(cards):
    # Split each card into lines
    card_lines = [card.esqueleto.split('\n') for card in cards]
    for lists in card_lines:
        for line in lists:
            if lists.index(line) % 5 == 1:
                lists[lists.index(line)] =  " "+ line.strip() + " "
            else:
                lists[lists.index(line)] = line.strip()
    # Print cards side by side
    for line in zip(*card_lines):
        print("  ".join(line))


trinca = Mão(3,cards=[Card(spade,"2")])


jogador1 = Jogador("Placeholder1")        


jogador2 = Jogador("Placeholder2")

jogador3 = Jogador("Placeholder3")

jogador4 = Jogador("placeholder4")

bolo = Baralho( quant=2)
print(len(bolo.cartas))
mesa = Jogador("Mesa")
bolo.distribuir(jogador1,jogador2,jogador3,jogador4)
bolo.give_morto()

cards = jogador1.get_cards()
display_cards(jogador1.get_cards())
