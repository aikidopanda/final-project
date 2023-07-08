import socket
from _thread import *
import threading
import pickle
import math
import time
import random
stopped = False
active_players = []

#my ip at home is '192.168.1.133' at DI its '192.168.201.216' from phone its '192.168.152.27'
# IP-address of my linode server '170.187.187.119'
#sudo apt-get install screen and then screen server.py - to run server infinitely
server = '0.0.0.0'
port = 5555

socket_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_handle.bind((server, port))
except socket.error as e:
    str(e)

try:    
    socket_handle.listen(2)
    print('Waiting for a connection, Server started')
except Exception as e:
    str(e)

current_player = 0
player_active = 1
game_state = 0 #current game state. 0 - attacker is playing, 1 - defender is playing, 2 - before attack, 3 - cards hit each other

lock = threading.Lock()

boards = [
    {
        'front': [None, None, None, None],
        'rear': [None, None, None, None]
    },
    {
        'front': [None, None, None, None],
        'rear': [None, None, None, None]
    },
]
health = [40, 40]
gold = [0, 0]
discards = [[],[]]
hands = [[],[]]
mana = [0,0]
turn_num = 0
turn_income = 2 + math.floor(turn_num/3)

def reset_to_default():
    global boards, health, gold, discards, hands, mana, turn_num, game_state
    boards = [
    {
        'front': [None, None, None, None],
        'rear': [None, None, None, None]
    },
    {
        'front': [None, None, None, None],
        'rear': [None, None, None, None]
    },
    ]
    health = [40, 40]
    gold = [0, 0]
    discards = [[],[]]
    hands = [[],[]]
    mana = [0,0]
    turn_num = 0
    game_state = 0
    # for conn in active_players:
    #     conn.close()
    # # subprocess.call([sys.executable] + sys.argv)


def send_data(data, conn):
    pickled = pickle.dumps(data)
    # conn.sendall(pickled)
    try:
        conn.sendall(pickled)
    except Exception as e:
        print(e)


def new_turn():
    global turn_num, turn_income, player_active, game_state
    if player_active == 1:
        player_active = 2
    else:
        player_active = 1
    turn_num = turn_num + 1
    turn_income = 2 + math.floor(turn_num/3)
    gold[0] += turn_income
    if gold[0] > turn_income * 2:
        gold[0] = turn_income * 2
    gold[1] += turn_income
    if gold[1] > turn_income * 2:
        gold[1] = turn_income * 2


def update_data(conn, player):
    global turn_num, turn_income, player_active, game_state, active_players

    while True:

        if player == 1:
            if (player_active == 1 and game_state%2==0) or (player_active == 2 and game_state == 1):
                active = True
            else:
                active = False

            player_data_server = {
                'health': health,
                'gold': gold,
                'mana': mana,
                'turn': turn_num,
                'boards': boards,
                'hands': hands,
                'discards': discards,
                'active': active,
                'state': game_state,
            }
        else:
            if (player_active == 2 and game_state%2==0) or (player_active == 1 and game_state == 1):
                active = True
            else:
                active = False

            health_reverse, gold_reverse, boards_reverse, discards_reverse, mana_reverse = health[::-1], gold[::-1], boards[::-1], discards[::-1], mana[::-1]
            hands_reverse = hands[::-1]

            player_data_server = {
                'health': health_reverse,
                'gold': gold_reverse,
                'mana': mana_reverse,
                'turn': turn_num,
                'boards': boards_reverse,
                'hands': hands_reverse,
                'discards': discards_reverse,
                'active': active,
                'state': game_state,
            }
        if conn in active_players:
            send_data(player_data_server, conn)
            time.sleep(2)


def threaded_client(connection, player):

    global stopped, health, gold, turn_num, player_active, current_player, game_state

    while True:
    # while stopped == False:
        serialized_data = connection.recv(16384)
        try:        
            data = pickle.loads(serialized_data)
        except Exception as e:
            print(e)
            time.sleep(2)
            data = pickle.loads(serialized_data)
        if not data or data == 'Stop':
            # stopped = True
            print("Received message from the client:", data)
            break
        elif data == 'Start game':
            print(player)
            if player == 2:
                coinflip = random.randint(1, 2)  # randomly determine the first turn when both players are connected
                if coinflip == 1:
                    player_active = 1
                else:
                    player_active = 2
                new_turn()
                print(f'Game state, active player, gold, health when player {player} connected: ', game_state, player_active, gold, health)
        else:
            if isinstance(data, list):
                if 'health' in data[0]:  # checking what kind of data we are getting from client
                    game_state = data[2]
                    if player == 1:
                        health[0] = data[0]['health']
                        health[1] = data[1]['health']
                        gold[0] = data[0]['gold']
                        gold[1] = data[1]['gold']
                        boards[0] = data[0]['board']
                        boards[1] = data[1]['board']
                        discards[0] = data[0]['discard']
                        discards[1] = data[1]['discard']
                        hands[0] = data[0]['hand']
                        hands[1] = data[1]['hand']
                        mana[0] = data[0]['mana']
                        mana[1] = data[1]['mana']
                        
                    else:
                        health[1] = data[0]['health']
                        health[0] = data[1]['health']
                        gold[1] = data[0]['gold']
                        gold[0] = data[1]['gold']
                        boards[1] = data[0]['board']
                        boards[0] = data[1]['board']
                        discards[1] = data[0]['discard']
                        discards[0] = data[1]['discard']
                        hands[1] = data[0]['hand']
                        hands[0] = data[1]['hand']
                        mana[1] = data[0]['mana']
                        mana[0] = data[1]['mana']
                    if game_state >= 3:
                        game_state = 0
                        new_turn()
                    # print('Health, gold, mana after adjustment: ', health, gold, mana)
                    # print(f'Boards after player {player} turn', boards)

    print(f'Player {player} has disconnected')
    current_player -= 1
    active_players.remove(connection)
    connection.close()
    if current_player == 0:
        reset_to_default()
        print('default player parameters have been reset')


def accept_connections():
    global current_player

    while True: #current_player < 2:
        connection, address = socket_handle.accept()
        current_player += 1
        print(f'Player {current_player} has connected')
        active_players.append(connection)
        threading.Thread(target=threaded_client, args=(
            connection, current_player)).start()

        updating_thread = threading.Thread(
            target=update_data, args=(connection, current_player))
        updating_thread.start()


accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
