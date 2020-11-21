from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import os
from random import randint
import sys, getopt
from client import Client
import time

WINDOW_WIDTH  = 950
WINDOW_HEIGHT = 720
WINDOW_NAME = "MIPTopoly"

HELPMSG='main.py --contract-address=<addr> --user-address=<uaddr> --user-name=<name>'
CONTRACT_ADDRESS = ""
USER_ADDRESS = ""
USER_NAME = ""

TOP=20
LEFT=740
WIDTH=190
DELIM=10


class Player(QGraphicsPixmapItem):
    def __init__(self, name, money=200, position=0, movesInPrison=0, isActionRequired=False):
        super().__init__()

        self.name = name
        self.money = money
        self.position = position

        self.load_images();

    def get_images(self):
        return self.players_images

    def DrawPlayer1(self):
        self.setPixmap(self.players_images[0])

        if(self.position == 0):
            self.setPos(QPointF(650, 650))

        if(self.position == 1):
            self.setPos(QPointF(475, 650))

        if(self.position == 2):
            self.setPos(QPointF(300, 650))

        if(self.position == 3):
            self.setPos(QPointF(125, 650))

        if(self.position == 4):
            self.setPos(QPointF(125, 475))

        if(self.position == 5):
            self.setPos(QPointF(125, 300))

        if(self.position == 6):
            self.setPos(QPointF(125, 125))

        if(self.position == 7):
            self.setPos(QPointF(300, 125))

        if(self.position == 8):
            self.setPos(QPointF(475, 125))

        if(self.position == 9):
            self.setPos(QPointF(650, 125))

        if(self.position == 10):
            self.setPos(QPointF(650, 300))

        if(self.position == 11):
            self.setPos(QPointF(650, 475))

    def DrawPlayer2(self):
        self.setPixmap(self.players_images[1])

        if(self.position == 0):
            self.setPos(QPointF(650, 590))

        if(self.position == 1):
            self.setPos(QPointF(475, 590))

        if(self.position == 2):
            self.setPos(QPointF(300, 590))

        if(self.position == 3):
            self.setPos(QPointF(125, 590))

        if(self.position == 4):
            self.setPos(QPointF(125, 415))

        if(self.position == 5):
            self.setPos(QPointF(125, 240))

        if(self.position == 6):
            self.setPos(QPointF(125, 65))

        if(self.position == 7):
            self.setPos(QPointF(300, 65))

        if(self.position == 8):
            self.setPos(QPointF(475, 65))

        if(self.position == 9):
            self.setPos(QPointF(650, 65))

        if(self.position == 10):
            self.setPos(QPointF(650, 240))

        if(self.position == 11):
            self.setPos(QPointF(650, 415))

    def load_images(self):
        self.players_images = []

        for i in range(2):
            n = QPixmap(QPixmap(os.path.join('pictures','players/player%s.png' % (i + 1))))
            self.players_images.append(n)

class Dice(QGraphicsPixmapItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.load_images()

    def load_images(self):
        self.numbers_images = []

        for i in range(7):
            n = QPixmap(QPixmap(os.path.join('pictures','dices/%s.png' % (i))))
            self.numbers_images.append(n)

    def DrawDice(self, number):
        SIZE=36
        self.setPixmap(self.numbers_images[number])
        self.setPos(QPointF(LEFT+WIDTH/2-SIZE/2, 600))

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.client=Client(CONTRACT_ADDRESS, USER_NAME, USER_ADDRESS, verbose=False)
        #enroll = self.client.enrollGame()

        #while not self.client.isGameActive():
        #    print("Waiting another player")
        #    time.sleep(1)

        view = QGraphicsView()
        self.scene = QGraphicsScene()
        view.setScene(self.scene)

        self.scene.setSceneRect(QRectF(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        #Filling the background
        felt = QBrush(QPixmap(os.path.join('pictures','background-pattern.png')))
        self.scene.setBackgroundBrush(felt)

        #Painting the field
        field = QGraphicsPixmapItem()
        field.setPixmap(QPixmap(os.path.join('pictures','field.png')))
        field.setPos(QPointF(10, 5))
        self.scene.addItem(field)

        #Working with dice
        self.dice = Dice()
        self.scene.addItem(self.dice)
        self.dice.DrawDice(6)

        #players = self.client.getPlayers()

        #Player 1 init
        #name = list(players.keys())[0]
        #player = players[name]
        #self.player_1 = Player(name, money=player['money'], position=player['position'])
        self.player_1 = Player("somename")

        #Player 2 init
        #name = list(players.keys())[1]
        #player = players[name]
        #self.player_2 = Player(name, money=player['money'], position=player['position'])
        self.player_2 = Player("somename")

        self.scene.addItem(self.player_1)
        self.scene.addItem(self.player_2)

        self.player_1.DrawPlayer1()
        self.player_2.DrawPlayer2()

        #Players
        player1_sample_text = self.player_1.name + " " + str(self.player_1.money) + "$"
        self.player1_banner = QLabel(player1_sample_text)
        self.player1_banner.move(LEFT, TOP)
        self.player1_banner.resize(WIDTH, 40)
        self.player1_banner.setWordWrap(1)
        self.player1_banner.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.player1_banner)

        player2_sample_text = self.player_2.name + " " + str(self.player_2.money) + "$"
        self.player2_banner = QLabel(player2_sample_text)
        self.player2_banner.move(LEFT, TOP + 40 + DELIM)
        self.player2_banner.resize(WIDTH, 40)
        self.player2_banner.setWordWrap(1)
        self.player2_banner.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.player2_banner)

        self.player1_image = QGraphicsPixmapItem()
        self.player1_image.setPixmap(self.player_1.get_images()[0].scaled(QSize(20, 20)))
        self.player1_image.setPos(QPointF(900, 30))
        self.scene.addItem(self.player1_image)

        self.player2_image = QGraphicsPixmapItem()
        self.player2_image.setPixmap(self.player_2.get_images()[1].scaled(QSize(20, 20)))
        self.player2_image.setPos(QPointF(900, 80))
        self.scene.addItem(self.player2_image)

        #Game log
        log_sample_text = ("Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Toll station, pay 50$ to Phil\n"
                           "Vlados at position 1 : Finished his way (looooh, pi*or)\n")

        self.log = QPlainTextEdit(log_sample_text)
        self.log.move(LEFT, TOP + 90 + DELIM*2)
        self.log.resize(WIDTH, 350)
        self.log.setReadOnly(1)
        self.scene.addWidget(self.log)

        #Question
        question_sample_text = "Do you want to purchase avenue X?"
        self.question = QLabel(question_sample_text)
        self.question.move(LEFT, TOP + 440 + DELIM*3)
        self.question.resize(WIDTH, 40)
        self.question.setWordWrap(1)
        self.question.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.question)

        #Buttons for answers to the question
        self.button_no = QPushButton("NO")
        self.button_no.move(LEFT, TOP + 480 + DELIM*4)
        self.button_no.resize(int((WIDTH - DELIM)/2), 50)
        self.scene.addWidget(self.button_no)

        self.button_yes = QPushButton("YES")
        self.button_yes.move(int(LEFT + WIDTH/2 + DELIM/2), TOP + 480 + DELIM*4)
        self.button_yes.resize(int((WIDTH - DELIM)/2), 50)
        self.scene.addWidget(self.button_yes)

        #Button for new move
        self.button_newMove = QPushButton("ROLL THE DICE")
        self.button_newMove.move(LEFT, TOP + 550 + DELIM*5 + 30)
        self.button_newMove.resize(WIDTH, 50)
        proxy_button = self.scene.addWidget(self.button_newMove)

        #Connecting buttons with functions
        self.button_newMove.clicked.connect(self.newMove_handler)
        self.button_yes.clicked.connect(self.yes_handler)
        self.button_no.clicked.connect(self.no_handler)

        #Timer for handling events from contract
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_handler)
        self.timer.start()

        self.setCentralWidget(view)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle(WINDOW_NAME)

        self.show()

    def quit(self):
        self.close()

    def timer_handler(self):
        print("smth")

    def yes_handler(self):
        pass

    def no_handler(self):
        pass

    def newMove_handler(self):
        #TODO Handle changes from etherium contract
        #TODO Check order of moves
        self.dice.DrawDice(randint(0, 6))

        self.player_1.set_position((self.player_1.get_position() + 1) % 12)
        self.player_1.DrawPlayer1()

        self.player_2.set_position((self.player_2.get_position() + 1) % 12)
        self.player_2.DrawPlayer2()

    def initGame(self, player_1, player_2):
        #TODO Handle starting game event from contract
        #TODO Init vars of pl_1 and pl_2. pl_1 is our local player as default
        pass

from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == '__main__':

    suppress_qt_warnings()

    #Handle cmdline arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:u:n:",["contract_address=","user_address=","user_name="])
    except getopt.GetoptError:
       print(HELPMSG)
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print(HELPMSG)
          sys.exit()
       elif opt in ("-c", "--contract_address"):
          CONTRACT_ADDRESS = arg
       elif opt in ("-u", "--user_address"):
          USER_ADDRESS = arg
       elif opt in ("-n", "--user_name"):
          USER_NAME = arg
    print("contract_address="+CONTRACT_ADDRESS)
    print("user_address="+USER_ADDRESS)
    print("user_name="+USER_NAME)
    if (CONTRACT_ADDRESS == "" or USER_ADDRESS == "" or USER_NAME == ""):
        print(HELPMSG)
        sys.exit(1)

    app = QApplication([])
    window = MainWindow()
    app.exec_()
