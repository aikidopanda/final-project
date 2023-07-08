import math
import random
# Trait functions
longspear = ['Pikeman']
healer = ['Monk']
armor = ['Knight', 'Stone Golem']
charge = ['Champion']
resurrect = ['Angel']
pillager = ['Imp']
card_drawing = ['Imp']
fireball = ['Gog']
predator = ['Hell Hound']
demonologist = ['Pit Fiend']
fireshield = ['Efreet']
devourer = ['Devil']
repair = ['Gremlin']
stoneform = ['Stone Gargoyle']
mana = ['Mage']
gold_generate = ['Genie']
zombie = ['Walking Dead']
regeneration = ['Wight']
life_drain = ['Vampire']
necromancer = ['Lich']
cursing = ['Black Knight']
decay = ['Bone Dragon']
giants = ['Giant']


class Player:
    def __init__(self, color, name='Player'):
        self.health = 40
        self.gold = 2
        self.mana = 0
        self.blessings = 0
        self.shielded = False
        self.attack = 0
        self.deck, self.hand, self.discard = [], [], []
        self.board = {
            'front': [None, None, None, None],
            'rear': [None, None, None, None],
        }
        self.active_card = None
        self.color = color
        self.name = name
        self.faction = ''
        self.active = False

    def __str__(self):
        return f'player: {self.name}, health: {self.health}, gold: {self.gold}'

    def choose_card(self, card, index):
        self.gold -= card.cost
        self.active_card = self.hand.pop(index)

    def deal_card(self):
        if len(self.deck) > 0:
            card = self.deck.pop()
            self.hand.append(card)


class Faction:

    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class Card:

    def __init__(self, name, health, health_base, attack,
                 cost, ranged, flying, image, faction=None):
        self.name = name
        self.health = health
        self.health_base = health_base
        self.attack = attack
        self.attack_base = attack
        self.cost = cost
        self.ranged = ranged
        self.flying = flying
        self.image = image
        self.faction = faction
        self.transformed = False  # for now, used only with stone gargoyles
        # self.attacked_this_turn == False

    def __str__(self) -> str:
        return f'{self.name}, health: {self.health}, attack: {self.attack}, cost: {self.cost}'

    def __repr__(self):
        return f'{self.name}, health: {self.health}, attack: {self.attack}, cost: {self.cost}'

    def fight_range(self, other):
        other.health -= other.name in armor and (self.attack - 1) or self.attack

    def fight_melee(self, other):
        if hasattr(other, 'name') and other.name in longspear:
            other.attacked(self)
        if self.name in cursing and other.attack > 0:
            other.attack -= 1
        other.health -= other.name in armor and (self.attack - 1) or self.attack
        if hasattr(other, 'ranged') and other.ranged == True and other.name not in giants:
            self.health -= math.floor(other.attack/2)
        else:
            self.health -= (self.name in armor and other.attack > 0) and (other.attack - 1) or other.attack

    def attacked(self, other):
        other.health -= 1
        if other.health <= 0:
            other.attack = 0
            other = None

    def fireshield(self, other, player):
        other.health -= 2
        if other.health <= 0:
            other.attack = 0
            player.discard.append(other)
            other = None

    def endofturn(self, board, player=None, player2=None):
        if self.name in healer:
            if player.health < 40:
                player.health += 1
            for k, v in board.items():
                for i in range(len(v)):
                    if v[i] != None and v[i].health < v[i].health_base:
                        v[i].health += 1
        if self.name in repair:
            for k, v in board.items():
                for i, card in enumerate(v):
                    if card != None and card.name == 'Stone Golem':
                        card.health += 2
                        if card.health > card.health_base:
                            card.health = card.health_base
        if self.name in mana:
            player.mana += 1
            if player.mana > 3:
                jenie_bonus = Card(
                    name='Genie',
                    health=6,
                    health_base=6,
                    attack=4,
                    cost=3,
                    ranged=False,
                    flying=True,
                    image='game/images/cards/Tower/Genie.webp'
                )
                player.hand.append(jenie_bonus)
                player.mana = 0
        if self.name in gold_generate:
            player.gold += 1
            if player.gold >= 8:
                player.deal_card()
        if self.name in regeneration:
            self.health = self.health_base
        if self.name in necromancer:
            skeleton_bonus = Card(
                name='Skeleton',
                health=3,
                health_base=3,
                attack=2,
                cost=1,
                ranged=False,
                flying=False,
                image='game/images/cards/Necropolis/Skeleton.webp'
            )
            player.hand.append(skeleton_bonus)
        if self.name in decay:
            player2.health -= 1

    def bless(self, player):
        player.blessings += 1
        if player.blessings >= 2:
            angel_bonus = Card(
                name='Angel',
                health=15,
                health_base=15,
                attack=10,
                cost=8,
                ranged=False,
                flying=True,
                image = 'game/images/cards/Castle/Angel.webp'
            )
            player.deck.append(angel_bonus)
            random.shuffle(player.deck)
            player.blessings = 0

    def resurrect(self, player):
        player.discard.sort(key=lambda x: x.cost, reverse=True)
        player.discard[0].health = player.discard[0].health_base
        player.discard[0].attack = player.discard[0].attack_base
        player.discard[1].health = player.discard[1].health_base
        player.discard[1].attack = player.discard[1].attack_base
        player.discard[2].health = player.discard[1].health_base
        player.discard[2].attack = player.discard[1].attack_base
        if player.discard[0].cost == 8: #angels can't resurrect each other, it would be imbalanced
            player.hand.append(player.discard[2])
            player.active_card = player.discard.pop(1)
        else:
            player.hand.append(player.discard[1])
            player.active_card = player.discard.pop(0)
        random.shuffle(player.discard)

    def consume(self, other):
        if other != None:
            self.health += math.ceil(other.health_base/2)
            if self.health > self.health_base:
                self.health = self.health_base

    def charge(self, other, player=None):
        other.health -= math.ceil(self.attack/2)

    def upgrade_demon(self, board):
        for k, v in board.items():
            for i, card in enumerate(v):
                if card != None and card.name == 'Imp':
                    card.health = 6
                    card.health_base = 6
                    card.attack = 6
                    card.image = 'game/images/cards/Inferno/Demon.webp'

    def fireball(self, index, front, player, rear=None):
        if (index-1) >= 0 and front[index-1] != None:
            front[index-1].health -= 1
            if front[index-1].health <= 0:
                player.discard.append(front[index-1])
                front[index-1] = None
        if (index+1) < len(front) and front[index+1] != None:
            front[index+1].health -= 1
            if front[index+1].health <= 0:
                player.discard.append(front[index+1])
                front[index+1] = None
        if rear != None:
            if hasattr(rear, 'health'):
                print('Fireball!')
                rear[index].health -= 1
                if rear[index].health <= 0:
                    player.discard.append(rear[index])
                    rear[index] = None

    def devil_attack(self, player):
        player.health -= 2

    def stoneform(self):
        self.health = 4
        self.attack = 1
        self.transformed = True

    def zombie_spawn(self, player):
        zombie_bonus = Card(
            name='Walking Dead',
            health=5,
            health_base=5,
            attack=4,
            cost=3,
            ranged=False,
            flying=False,
            image='game/images/cards/Necropolis/Walking_Dead.webp'
        )
        player.hand.append(zombie_bonus)
