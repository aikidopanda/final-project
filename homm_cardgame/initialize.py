from game.classes import *
import random

castle = Faction(name='Castle', image='game/images/factions/Castle.webp')
inferno = Faction(name='Inferno', image='game/images/factions/Inferno.webp')
tower = Faction(name='Tower', image='game/images/factions/Tower.webp')
necropolis = Faction(name='Necropolis', image='game/images/factions/Necropolis.webp')

def create_units_deck(deck, faction=castle):
    if faction == castle:

        for i in range(7):
            pikeman = Card(
                name='Pikeman',
                health=4,
                health_base=4,
                attack=2,
                cost=2,
                ranged=False,
                flying=False,
                faction=castle,
                image = 'game/images/cards/Castle/Pikeman.webp'
            )
            deck.append(pikeman)

        for i in range(6):
            archer = Card(
                name='Archer',
                health=2,
                health_base=2,
                attack=3,
                cost=3,
                ranged=True,
                flying=False,
                faction=castle,
                image = 'game/images/cards/Castle/Archer.webp'
            )
            deck.append(archer)

        for i in range(5):
            griffin = Card(
                name='Royal Griffin',
                health=7,
                health_base=7,
                attack=4,
                cost=4,
                ranged=False,
                flying=True,
                faction=castle,
                image = 'game/images/cards/Castle/Royal Griffin.webp'
            )
            deck.append(griffin)

        for i in range(4):
            knight = Card(
                name='Knight',
                health=8,
                health_base=8,
                attack=5,
                cost=5,
                ranged=False,
                flying=False,
                faction=castle,
                image = 'game/images/cards/Castle/Knight.webp'
            )
            deck.append(knight)

        for i in range(3):
            monk = Card(
                name='Monk',
                health=6,
                health_base=6,
                attack=3,
                cost=6,
                ranged=True,
                flying=False,
                faction=castle,
                image = 'game/images/cards/Castle/Monk.webp'
            )
            deck.append(monk)

        for i in range(2):
            champion = Card(
                name='Champion',
                health=12,
                health_base=12,
                attack=7,
                cost=7,
                ranged=False,
                flying=False,
                faction=castle,
                image = 'game/images/cards/Castle/Champion.webp'
            )
            deck.append(champion)

        angel = Card(
            name='Angel',
            health=15,
            health_base=15,
            attack=10,
            cost=8,
            ranged=False,
            flying=True,
            faction=castle,
            image = 'game/images/cards/Castle/Angel.webp'
        )
        deck.append(angel)

    elif faction == inferno:

        for i in range(7):
            imp = Card(
                name='Imp',
                health=2,
                health_base=2,
                attack=2,
                cost=2,
                ranged=False,
                flying=False,
                faction=inferno,
                image = 'game/images/cards/Inferno/Imp.webp'
            )
            deck.append(imp)

        for i in range(6):
            gog = Card(
                name='Gog',
                health=2,
                health_base=2,
                attack=2,
                cost=3,
                ranged=True,
                flying=False,
                faction=inferno,
                image = 'game/images/cards/Inferno/Gog.webp'
            )
            deck.append(gog)

        for i in range(5):
            hellhound = Card(
                name='Hell Hound',
                health=5,
                health_base=5,
                attack=6,
                cost=4,
                ranged=False,
                flying=False,
                faction=inferno,
                image = 'game/images/cards/Inferno/HellHound.webp'
            )
            deck.append(hellhound)

        for i in range(4):
            demon = Card(
                name='Demon',
                health=6,
                health_base=6,
                attack=6,
                cost=5,
                ranged=False,
                flying=False,
                faction=inferno,
                image = 'game/images/cards/Inferno/Demon.webp'
            )
            deck.append(demon)

        for i in range(3):
            pit_fiend = Card(
                name='Pit Fiend',
                health=8,
                health_base=8,
                attack=7,
                cost=6,
                ranged=False,
                flying=False,
                faction=inferno,
                image = 'game/images/cards/Inferno/PitFiend.webp'
            )
            deck.append(pit_fiend)

        for i in range(2):
            efreet = Card(
                name='Efreet',
                health=9,
                health_base=9,
                attack=8,
                cost=7,
                ranged=False,
                flying=True,
                faction=inferno,
                image = 'game/images/cards/Inferno/Efreet.webp'
            )
            deck.append(efreet)

        devil = Card(
            name='Devil',
            health=13,
            health_base=13,
            attack=10,
            cost=8,
            ranged=False,
            flying=True,
            faction=inferno,
            image = 'game/images/cards/Inferno/Devil.webp'
        )
        deck.append(devil)
    
    elif faction == tower:
        for i in range(7):
            gremlin = Card(
                name='Gremlin',
                health=1,
                health_base=1,
                attack=2,
                cost=2,
                ranged=True,
                flying=False,
                faction=tower,
                image = 'game/images/cards/Tower/Gremlin.webp'
            )
            deck.append(gremlin)
        for i in range(6):
            gargoyle = Card(
                name='Stone Gargoyle',
                health=1,
                health_base=1,
                attack=3,
                cost=3,
                ranged=False,
                flying=True,
                faction=tower,
                image = 'game/images/cards/Tower/Stone_Gargoyle.webp'
            )
            deck.append(gargoyle)
        for i in range(5):
            golem = Card(
                name='Stone Golem',
                health=9,
                health_base=9,
                attack=5,
                cost=4,
                ranged=False,
                flying=False,
                faction=tower,
                image = 'game/images/cards/Tower/Golem.webp'
            )
            deck.append(golem)
        for i in range(4):
            mage = Card(
                name='Mage',
                health=4,
                health_base=4,
                attack=4,
                cost=5,
                ranged=True,
                flying=False,
                faction=tower,
                image = 'game/images/cards/Tower/Mage.webp'
            )
            deck.append(mage)
        for i in range(3):
            genie = Card(
                name='Genie',
                health=6,
                health_base=6,
                attack=4,
                cost=6,
                ranged=False,
                flying=True,
                faction=tower,
                image = 'game/images/cards/Tower/Genie.webp'
            )
            deck.append(genie)
        for i in range(2):
            naga = Card(
                name='Naga',
                health=13,
                health_base=13,
                attack=8,
                cost=7,
                ranged=False,
                flying=False,
                faction=tower,
                image = 'game/images/cards/Tower/Naga.webp'
            )
            deck.append(naga)
        giant = Card(
            name='Giant',
            health=12,
            health_base=12,
            attack=7,
            cost=8,
            ranged=True,
            flying=False,
            faction=tower,
            image = 'game/images/cards/Tower/Giant.webp'
        )
        deck.append(giant)

    elif faction == necropolis:
        for i in range(7):
            skeleton = Card(
                name='Skeleton',
                health=3,
                health_base=3,
                attack=2,
                cost=2,
                ranged=False,
                flying=False,
                faction=necropolis,
                image = 'game/images/cards/Necropolis/Skeleton.webp'
            )
            deck.append(skeleton)
        for i in range(6):
            walking_dead = Card(
                name='Walking Dead',
                health=5,
                health_base=5,
                attack=4,
                cost=3,
                ranged=False,
                flying=False,
                faction=necropolis,
                image = 'game/images/cards/Necropolis/Walking_Dead.webp'
            )
            deck.append(walking_dead)
        for i in range(5):
            wight = Card(
                name='Wight',
                health=5,
                health_base=5,
                attack=3,
                cost=4,
                ranged=False,
                flying=True,
                faction=necropolis,
                image = 'game/images/cards/Necropolis/Wight.webp'
            )
            deck.append(wight)
        for i in range(4):
            vampire = Card(
                name='Vampire',
                health=7,
                health_base=7,
                attack=6,
                cost=5,
                ranged=False,
                flying=False,
                faction=necropolis,
                image = 'game/images/cards/Necropolis/Vampire.webp'
            )
            deck.append(vampire)
        for i in range(3):
            lich = Card(
                name='Lich',
                health=6,
                health_base=6,
                attack=4,
                cost=6,
                ranged=True,
                flying=False,
                faction=necropolis,
                image = 'game/images/cards/Necropolis/Lich.webp'
            )
            deck.append(lich)
        for i in range(2):
            black_knight = Card(
                name='Black Knight',
                health=12,
                health_base=12,
                attack=7,
                cost=7,
                ranged=False,
                flying=False,
                faction=necropolis,
                image = 'game/images/cards/Necropolis/Black_Knight.webp'
            )
            deck.append(black_knight)
        bone_dragon = Card(
            name='Bone Dragon',
            health=18,
            health_base=18,
            attack=7,
            cost=8,
            ranged=False,
            flying=True,
            faction=necropolis,
            image = 'game/images/cards/Necropolis/Bone_Dragon.webp'
        )
        deck.append(bone_dragon)
        


    random.shuffle(deck)

def deal_card(deck, hand):
    if len(deck) > 0:
        card = deck.pop()
        hand.append(card)

