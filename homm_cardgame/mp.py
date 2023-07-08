# from gamedata_mp import *
# from game.models import *
from game.classes import *
from initialize import *
from gui.gui import *
import os
import django
import pygame
import pickle
import socket
import threading
import time
from pygame.locals import *

# card size: width 87 height 115. Pin it here since it will be standard for all cards
# myvenv\Scripts\activate

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homm_cardgame.settings')
# django.setup()

# my ip at home is '192.168.1.133' at DI its '192.168.201.216', from phone its 192.168.152.27
# IP-address of my linode server '170.187.187.119'
address = '192.168.1.133'
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((address, port))

Player1 = Player(player_color)
Player2 = Player(opponent_color)
factions = [castle, inferno, tower, necropolis]
turn_num = 0
game_state = 0
cards_changed = 0


def start_game():

    # Creating starting deck depending of chosen faction
    create_units_deck(Player1.deck, Player1.faction)
    # Dealing 3 starting cards
    for i in range(3):
        Player1.deal_card()
    synchronize_players(Player1, Player2)

    msg = 'Start game'
    pickled = pickle.dumps(msg)
    try:
        client_socket.sendall(pickled)
    except:
        print('No data was sent from client to server')
    print('Game state, Player active, Enemy active: ',
          game_state, Player1.active, Player2.active)

# Server-calling functions
def synchronize_players(p1, p2):
    global game_state
    pdata_1 = {
        'health': p1.health,
        'gold': p1.gold,
        'board': p1.board,
        'discard': p1.discard,
        'mana': p1.mana,
        'hand': p1.hand
    }
    pdata_2 = {
        'health': p2.health,
        'gold': p2.gold,
        'board': p2.board,
        'discard': p2.discard,
        'mana': p2.mana,
        'hand': p2.hand
    }
    pdata = [pdata_1, pdata_2, game_state]
    pd_pickled = pickle.dumps(pdata)
    try:
        client_socket.sendall(pd_pickled)
    except:
        print('No data was sent from client to server!')


def receive_data(client_socket):
    global turn_num, game_state
    while True:
        serialized_data = client_socket.recv(16384)
        try:
            data = pickle.loads(serialized_data)
        except Exception as e:
            print(e)
            time.sleep(2)
            data = pickle.loads(serialized_data)

        if isinstance(data, dict):
            if 'health' in data:
                Player1.health = data['health'][0]
                Player1.gold = data['gold'][0]
                Player1.mana = data['mana'][0]
                Player2.health = data['health'][1]
                Player2.gold = data['gold'][1]
                Player2.mana = data['mana'][1]
                Player1.active = data['active']
                turn_num = data['turn']
                game_state = data['state']
                Player1.board = data['boards'][0]
                Player2.board = data['boards'][1]
                Player1.discard = data['discards'][0]
                Player2.discard = data['discards'][1]
                Player1.hand = data['hands'][0]
                Player2.hand = data['hands'][1]


threading.Thread(target=receive_data, args=(client_socket,)).start()


pygame.init()

CLOCK = pygame.time.Clock()
FPS = 30

clicked = False
initialized = False

bg = pygame.image.load('game/images/background.jpg')
font = pygame.font.SysFont('Arial', 20)

# (1600-900), pygame.SCALED default
screen = pygame.display.set_mode((1600, 900), pygame.SCALED)
pygame.display.set_caption('Heroes of Might and Magic card game')

menurunning = True
gamerunning = False

# GUI drawing functions


def button_round(msg, x, y, radius, colour, status, action=None, image=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + radius > mouse[0] > x - radius and y + radius > mouse[1] > y - radius:
        if status == 'active' and Player1.active == True:
            if click[0] == 1 and action != None:  # and clicked == False:
                action()
    if image != None:
        screen.blit(
            pygame.image.load(image), (x, y)
        )
    else:
        pygame.draw.circle(screen, colour, (x, y), radius)

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    if image != None:
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x+45), (y+120))
    else:
        textSurf, textRect = text_objects_sm(msg, smallText)
        textRect.center = ((x), (y))
    screen.blit(textSurf, textRect)


# Only for changing starting cards in the beginning
def button_change(msg, x, y, width, height, colour, index):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        colour = maroon
        if click[0] == 1 and action != None and clicked == False:
            change_starting_card(index)

    pygame.draw.rect(screen, colour, (x, y, width, height))
    smallText = pygame.font.Font("freesansbold.ttf", 18)
    textSurf, textRect = text_objects_sm(msg, smallText)
    textRect.center = ((x+(width/2)), (y+(height/2)))
    screen.blit(textSurf, textRect)


def cardtoplay(x, y, width, height, index):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if index < len(Player1.hand):
        screen.blit(pygame.image.load(
            Player1.hand[index].image), (x, y))
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if Player1.active == True and game_state < 2 and click[0] == 1 and Player1.gold >= Player1.hand[index].cost and cards_changed >= 3:
            pygame.time.delay(500)
            Player1.choose_card(Player1.hand[index], index)
            synchronize_players(Player1, Player2)


def factionslot(x, y, width, height, index):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    screen.blit(pygame.image.load(
        factions[index].image), (x, y))
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1:
            pygame.time.delay(500)
            Player1.faction = factions[index]


def cardslot(x, y, width, height, colour, index):
    global active_card
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1 and Player1.active_card != None:

            if Player1.active_card.name in devourer:  # Devil devours the strongest unit in enemy discard
                Player2.discard.sort(
                    key=lambda x: x.health_base, reverse=True)
                prey = Player2.discard.pop(0)
                random.shuffle(Player2.discard)
                Player1.active_card.attack += prey.attack
                Player1.active_card.health += prey.health_base

            Player1.board['front'][index] = Player1.active_card

            if Player1.active_card.name in card_drawing:
                Player1.deal_card()
                synchronize_players(Player1, Player2)

            if Player1.active_card.name in healer:
                Player1.active_card.bless(Player1)
                synchronize_players(Player1, Player2)

            if Player1.active_card.name in resurrect:  # angel resurrects the strongest unit in owner discard
                pygame.time.delay(200)
                Player1.active_card.resurrect(Player1)
            elif Player1.active_card.name in demonologist:  # Pit fiend transforms all allied imps into demons
                Player1.active_card.upgrade_demon(Player1.board)
                Player1.active_card = None
            else:
                Player1.active_card = None
            synchronize_players(Player1, Player2)
    if Player1.board['front'][index] != None:
        screen.blit(pygame.image.load(
            Player1.board['front'][index].image), (x, y))
    else:
        pygame.draw.rect(screen, colour, (x, y, width, height))


def cardslot_rear(x, y, width, height, colour, index):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1 and Player1.active_card != None:
            pygame.time.delay(500)
            if Player1.active_card.name in devourer:  # Devil devours the strongest unit in enemy discard
                Player2.discard.sort(
                    key=lambda x: x['health_base'], reverse=True)
                prey = Player2.discard.pop(0)
                random.shuffle(Player2.discard)
                Player1.active_card.attack += math.ceil(prey.attack/2)
                Player1.active_card.health += math.ceil(prey.health_base/2)

            Player1.board['rear'][index] = Player1.active_card

            if Player1.active_card.name in card_drawing:
                Player1.deal_card()
                synchronize_players(Player1, Player2)

            if Player1.active_card.name in healer:
                Player1.active_card.bless(Player1)
                synchronize_players(Player1, Player2)

            if Player1.active_card.name in resurrect:  # angel resurrects the strongest unit in owner discard
                pygame.time.delay(200)
                Player1.active_card.resurrect(Player1)
            elif Player1.active_card.name in demonologist:  # Pit fiend transforms allied imps into demons
                Player1.active_card.upgrade_demon(Player1.board)
                Player1.active_card = None
            else:
                Player1.active_card = None
            synchronize_players(Player1, Player2)
    if Player1.board['rear'][index] != None:
        screen.blit(pygame.image.load(
            Player1.board['rear'][index].image), (x, y))
    else:
        pygame.draw.rect(screen, colour, (x, y, width, height))


def cardslot_opponent(x, y, width, height, colour, index):
    if Player2.board['front'][index] != None:
        screen.blit(pygame.image.load(
            Player2.board['front'][index].image), (x, y))
    else:
        pygame.draw.rect(screen, colour, (x, y, width, height))


def cardslot_opponent_rear(x, y, width, height, colour, index):
    if Player2.board['rear'][index] != None:
        screen.blit(pygame.image.load(
            Player2.board['rear'][index].image), (x, y))
    else:
        pygame.draw.rect(screen, colour, (x, y, width, height))


# Gameplay functions
def start():
    global menurunning, gamerunning
    menurunning = False
    gamerunning = True
    start_game()


def menuexit():
    global menurunning, gamerunning
    gamerunning = False
    # menurunning = True  # doesn't work as intended yet, should work on it when I have time


def exit_game():
    global menurunning
    global gamerunning
    msg = 'Stop'
    serialized = pickle.dumps(msg)
    client_socket.send(serialized)
    menurunning = False
    gamerunning = False


def processing():
    global turn_num, clicked, game_state
    Player1.active = False
    pygame.time.delay(1000)
    game_state += 1
    if game_state >= 2:
        if len(Player1.deck) > 0:
            Player1.deal_card()
    if game_state < 3:
        synchronize_players(Player1, Player2)
    else:
        for line in ['rear', 'front']:
            attacking(Player1.board[line])
        for v in Player1.board.values():
            for i in range(len(v)):
                if v[i] != None:
                    v[i].endofturn(Player1.board, Player1, Player2)
        for v in Player2.board.values():
            for i in range(len(v)):
                if v[i] != None:
                    v[i].endofturn(Player2.board, Player2, Player1)
        synchronize_players(Player1, Player2)
        game_state = 0

    clicked = False


def attacking(line):

    enemyfront = Player2.board['front']
    enemyrear = Player2.board['rear']
    enemy = Player2

    for i in range(len(line)):
        if line[i] != None:
            if line[i].name in devourer:
                line[i].devil_attack(Player2)
            if enemyfront[i] != None:
                # flying units can attack the backrank and will choose the target with less hp or if the backranker is ranged
                if line[i].flying == True and enemyrear[i] != None and (enemyrear[i].health <= enemyfront[i].health or enemyrear[i].ranged == True):
                    if enemyrear[i] in fireshield and line[i].health <= 2:
                        Player1.discard.append(line[i])
                        line[i] = None
                    else:
                        line[i].fight_melee(enemyrear[i])
                        # death_check(enemyrear[i], Player2)
                        if enemyrear[i].health <= 0:
                            if enemyrear[i].name in stoneform and enemyrear[i].transformed == False:
                                enemyrear[i].stoneform()
                            else:
                                Player2.discard.append(enemyrear[i])
                                enemyrear[i] = None
                # usual melee attack
                elif line[i].ranged == False:
                    if enemyfront[i].name in fireshield and line[i].health <= 2:
                        enemyfront[i].fireshield(line[i], Player1)
                    else:
                        line[i].fight_melee(enemyfront[i])
                # shooting and get no counter-attack cause we are ranged
                else:
                    line[i].fight_range(enemyfront[i])
                    if line[i].name in fireball:
                        line[i].fireball(i, enemyfront, Player2, enemyrear)
                        if enemyrear[i] != None:
                            enemyrear[i].health -= 1
                            death_check(enemyrear, i, Player2)

                # dead units go to the owner's discard unless there are some card or game effects
                if enemyfront[i].health <= 0:
                    if enemyfront[i].name in stoneform and enemyfront[i].transformed == False:
                        enemyfront[i].stoneform()
                    else:
                        if line[i].name in zombie:  # zombie apocalypse
                            line[i].zombie_spawn(Player1)
                        if line[i].name in predator and line[i].health > 0:  # hellhound
                            line[i].consume(enemyfront[i])
                        if line[i].name in life_drain and line[i].health > 0:  # Vampire
                            line[i].health += math.floor(line[i].attack/2)
                            if line[i].health > line[i].health_base:
                                line[i].health = line[i].health_base
                        if line[i].name in charge and line[i].health > 0:  # champion
                            if enemyrear[i] != None:
                                line[i].charge(enemyrear[i], Player2)
                                if enemyrear[i].health <= 0:
                                    if enemyrear[i].name in stoneform and enemyrear[i].transformed == False:
                                        enemyrear[i].stoneform()
                                    else:
                                        Player2.discard.append(enemyrear[i])
                                        enemyrear[i] = None
                        Player2.discard.append(enemyfront[i])
                        # If card is killed, clear its slot
                        enemyfront[i] = None

            # If enemy frontline is empty, attack the back rank
            elif enemyrear[i] != None:
                if line[i].ranged == False:
                    if enemyrear[i].name in fireshield and line[i].health <= 2:
                        enemyrear[i].fireshield(line[i], Player1)
                    else:
                        line[i].fight_melee(enemyrear[i])
                else:
                    line[i].fight_range(enemyrear[i])
                    if line[i].name in fireball:
                        line[i].fireball(i, enemyrear, Player2)
                if enemyrear[i].health <= 0:
                    if enemyrear[i].name in stoneform and enemyrear[i].transformed == False:
                        enemyrear[i].stoneform()
                    else:
                        if line[i].name in zombie:
                            line[i].zombie_spawn(Player1)
                        if line[i].name in predator and line[i].health > 0:
                            line[i].consume(enemyrear[i])
                        if line[i].name in life_drain and line[i].health > 0:  # Vampire
                            line[i].health += math.floor(line[i].attack/2)
                            if line[i].health > line[i].health_base:
                                line[i].health = line[i].health_base
                        if line[i].name in charge and line[i].health > 0:
                            line[i].charge(enemy)
                        Player2.discard.append(enemyrear[i])
                        enemyrear[i] = None
            else:
                if line[i].name in pillager and enemy.gold > 0:
                    enemy.gold -= 1
                line[i].fight_melee(enemy)

            # death_check(line, i, Player1)
            if line[i] and line[i].health <= 0:
                if line[i].name in stoneform and line[i].transformed == False:
                    line[i].stoneform()
                else:
                    Player1.discard.append(line[i])
                    line[i] = None


def cancel_card():
    if Player1.active_card != None:
        Player1.gold += Player1.active_card.cost
        Player1.hand.append(Player1.active_card)
        Player1.active_card = None
        synchronize_players(Player1, Player2)


def change_starting_card(index):

    global cards_changed

    pygame.time.delay(500)
    cards_changed += 1

    card = Player1.hand.pop(index)
    Player1.deck.append(card)
    random.shuffle(Player1.deck)
    Player1.deal_card()
    synchronize_players(Player1, Player2)


def player_is_ready():
    global cards_changed
    cards_changed += 3


def death_check(line, index, player):
    if line[index].health <= 0:
        if line[index].name in stoneform and line[index].transformed == False:
            line[index].stoneform()
        else:
            player.discard.append(line[index])
            line[index] = None


while menurunning:
    screen.blit(bg, (0, 0))

    if initialized == False:
        initialized = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menurunning = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit_game()
                # menurunning = False

    largeText = pygame.font.Font('freesansbold.ttf', 95)
    # TextSurf, TextRect = text_objects("HoMM Card game", largeText)
    # TextRect.center = (800, 300)
    # screen.blit(TextSurf, TextRect)

    menuText = pygame.font.Font("freesansbold.ttf", 20)

    screen.blit(
        pygame.image.load('game/images/faction.png'), (1220, 10)
    )

    ChoiceSurf, ChoiceRect = text_objects_sm("Choose your faction", menuText)
    ChoiceRect.center = (1400, 50)
    screen.blit(ChoiceSurf, ChoiceRect)

    FactionSurf, FactionRect = text_objects_sm(f'{Player1.faction}', menuText)
    FactionRect.center = (1400, 100)
    screen.blit(FactionSurf, FactionRect)

    for i, faction in enumerate(factions):
        factionslot(1250, 200 + i * 150, 300, 140, i)

    button('Start game', 700, 500, 250, 100, red,
           'active', start, 'game/images/menubutton.png')
    button('Quit', 700, 650, 250, 100, red, 'active',
           exit_game, 'game/images/menubutton.png')

    pygame.display.flip()
    CLOCK.tick(FPS)


while gamerunning:
    screen.blit(bg, (0, 0))

    if Player1.active == True:
        if game_state == 0:
            action = 'attacking'
            instruction = 'Click the card or press its number on keyboard to play it'
        elif game_state == 1:
            action = 'defending'
            instruction = 'Click the card or press its number on keyboard to play it'
        else:
            action = 'attacking'
            instruction = 'Press the round button to attack the opponent'
    else:
        if game_state == 0 or game_state == 2:
            action = 'defending'
            instruction = 'Wait for your opponent turn'
        elif game_state == 1:
            action = 'attacking'
            instruction = 'Wait for your opponent turn'

    if Player1.health <= 0 and Player2.health <= 0:
        result = 'Tie!'
    elif Player1.health <= 0:
        result = 'Defeat!'
    elif Player2.health <= 0:
        result = 'Victory!'

    largeText = pygame.font.Font('freesansbold.ttf', 40)

    button("Active card",
           10, 10, 150, 40, player_color, 'passive')
    if Player1.active_card != None:
        cardborder(50.5, 49, 89, 117, black)
        screen.blit(pygame.image.load(
            Player1.active_card.image), (51.5, 50))
    button("Change",
           10, 165, 150, 40, player_color, 'active', cancel_card)

    if Player2.health <= 0:
        button(f"{result} Press Esc to quit",
               10, 825, 900, 80, player_color, 'passive')
    elif Player1.health <= 0:
        button(f"Defeat! Press Esc to quit",
               10, 825, 900, 80, player_color, 'passive')
    else:
        button(f"Its turn {turn_num}, phase {game_state}. You are {action}. {instruction}",
               10, 825, 1000, 80, player_color, 'passive')

    for j in range(2):
        if j == 0:
            for i in range(4):
                cardborder(872 + i * 100, 524 + j * 150,
                           89, 117, black)
                cardslot(873 + i * 100, 525 + j * 150,
                         87, 115, player_color, i)
                if Player1.board['front'][i]:
                    button(f"{Player1.board['front'][i].attack} | {Player1.board['front'][i].health}",
                           873 + i * 100, 640 + j * 150, 87, 20, player_color, 'passive')
        if j == 1:
            for i in range(4):
                cardborder(872 + i * 100, 524 + j * 150,
                           89, 117, black)
                cardslot_rear(873 + i * 100, 525 + j * 150,
                              87, 115, player_color, i)
                if Player1.board['rear'][i]:
                    button(f"{Player1.board['rear'][i].attack} | {Player1.board['rear'][i].health}",
                           873 + i * 100, 640 + j * 150, 87, 20, player_color, 'passive')

    for j in range(2):
        if j == 0:
            for i in range(4):
                cardborder(872 + i * 100, 24 + j * 150,
                           89, 117, black)
                cardslot_opponent_rear(
                    873 + i * 100, 25 + j * 150, 87, 115, opponent_color, i)
                if Player2.board['rear'][i]:
                    button(f"{Player2.board['rear'][i].attack} | {Player2.board['rear'][i].health}",
                           873 + i * 100, 140 + j * 150, 87, 20, opponent_color, 'passive')
        if j == 1:
            for i in range(4):
                cardborder(872 + i * 100, 24 + j * 150,
                           89, 117, black)
                cardslot_opponent(873 + i * 100, 25 + j * 150,
                                  87, 115, opponent_color, i)
                if Player2.board['front'][i]:
                    button(f"{Player2.board['front'][i].attack} | {Player2.board['front'][i].health}",
                           873 + i * 100, 140 + j * 150, 87, 20, opponent_color, 'passive')

    for i, card in enumerate(Player1.hand):
        cardborder(19 + i * 100, 689,
                   89, 137, black)
        cardtoplay(20 + i * 100, 710, 87, 115, i)
        button(f"{i + 1}",
               43 + i * 100, 640, 43, 20, player_color, 'passive')
        button(f"{card.attack} | {card.health}",
               20 + i * 100, 690, 87, 20, opponent_color, 'passive')
        button(f"Cost: {card.cost}",
               20 + i * 100, 660, 87, 20, maroon, 'passive')
        if cards_changed < 3:
            cardborder(19 + i * 100, 609, 89, 22, black)
            button_change("Change",
            20 + i * 100, 610, 87, 20, player_color, i)
            
    if cards_changed < 3:
        cardborder(19, 579, 89, 22, black)
        button("Ready",
                20, 580, 87, 20, player_color, 'active', player_is_ready)

    if game_state >= 2 and Player1.active == True:
        button_round(f'Attack (Space)', 1010, 350,
                     95, red, 'active', processing, 'game/images/endturn.png')
    elif Player1.active == True:
        button_round(f'End turn (Space)', 1010, 350,
                     95, red, 'active', processing, 'game/images/endturn.png')
    else:
        button_round(f'Wait for opponent', 1010, 350,
                     95, red, 'active', processing, 'game/images/endturn.png')

    smallText = pygame.font.Font("freesansbold.ttf", 26)
    miniText = pygame.font.Font("freesansbold.ttf", 18)
    income = 2 + math.floor(turn_num/3)

    screen.blit(
        pygame.image.load('game/images/hp.png'), (1330, 620)
    )

    TextSurf, TextRect = text_objects_sm(f'{Player1.health}', smallText)
    TextRect.center = (1375, 675)
    screen.blit(TextSurf, TextRect)

    screen.blit(
        pygame.image.load('game/images/hp.png'), (1330, 120)
    )
    TextSurf, TextRect = text_objects_sm(f'{Player2.health}', smallText)
    TextRect.center = (1375, 175)
    screen.blit(TextSurf, TextRect)

    cardborder(1324, 224, 202, 52, black)
    button(f'Max gold stored: {income * 2}', 1325,
           225, 200, 50, opponent_color, 'passive')

    screen.blit(
        pygame.image.load('game/images/gold.png'), (1400, 630)
    )

    TextSurf, TextRect = text_objects(f'{Player1.gold}+{income}', smallText)
    TextRect.center = (1475, 675)
    screen.blit(TextSurf, TextRect)

    cardborder(1324, 724, 202, 52, black)
    button(f'Max gold stored: {income * 2}', 1325,
           725, 200, 50, player_color, 'passive')

    screen.blit(
        pygame.image.load('game/images/gold.png'), (1400, 130)
    )
    TextSurf, TextRect = text_objects(f'{Player2.gold}+{income}', smallText)
    TextRect.center = (1475, 175)
    screen.blit(TextSurf, TextRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerunning = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit_game()

            if event.key == K_1 and Player1.hand[0] != None and Player1.gold >= Player1.hand[0].cost:
                Player1.gold -= Player1.hand[0].cost
                Player1.active_card = Player1.hand.pop(0)
            elif event.key == K_2 and Player1.hand[1] != None and Player1.gold >= Player1.hand[1].cost:
                Player1.gold -= Player1.hand[1].cost
                Player1.active_card = Player1.hand.pop(1)
            elif event.key == K_3 and Player1.hand[2] != None and Player1.gold >= Player1.hand[2].cost:
                Player1.gold -= Player1.hand[2].cost
                Player1.active_card = Player1.hand.pop(2)
            elif event.key == K_4 and Player1.hand[3] != None and Player1.gold >= Player1.hand[3].cost:
                Player1.gold -= Player1.hand[3].cost
                Player1.active_card = Player1.hand.pop(3)
            elif event.key == K_5 and Player1.hand[4] != None and Player1.gold >= Player1.hand[4].cost:
                Player1.gold -= Player1.hand[4].cost
                Player1.active_card = Player1.hand.pop(4)
            elif event.key == K_6 and Player1.hand[5] != None and Player1.gold >= Player1.hand[5].cost:
                Player1.gold -= Player1.hand[5].cost
                Player1.active_card = Player1.hand.pop(5)

            if event.key == K_SPACE:
                processing()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
