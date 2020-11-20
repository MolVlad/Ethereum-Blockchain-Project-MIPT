from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import os
from random import randint

WINDOW_WIDTH  = 950
WINDOW_HEIGHT = 720
WINDOW_NAME = "MIPTopoly"

TOP=20
LEFT=740
WIDTH=190
DELIM=10

#Is neccery to connect elements in scene for event handling.
class Communicate(QObject):

    closeApp = pyqtSignal()
    rollDice = pyqtSignal()

class Player(QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.name = "somename"
        self.addr = None
        self.money = 200
        self.position = 0
        self.movesInPrison = 0
        self.IsActionRequired = False

        self.load_images();

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.addr

    def get_money(self):
        return self.money

    def get_position(self):
        return self.position

    def get_movesInPrison(self):
        return self.movesInPrison

    def get_IsActionRequired(self):
        return self.IsActionRequired

    def set_money(self, ammount):
        self.money = ammount

    def set_position(self, new_position):
        self.position = new_position

    def set_movesInPrison(self, moves):
        self.movesInPrison = moves

    def set_IsActionRequired(self, action):
        self.IsActionRequired = action

    def DrawPlayer1(self, pos_num):
        self.setPixmap(self.players_images[0])

        if(pos_num == 0):
            self.setPos(QPointF(650, 650))

        if(pos_num == 1):
            self.setPos(QPointF(475, 650))

        if(pos_num == 2):
            self.setPos(QPointF(300, 650))

        if(pos_num == 3):
            self.setPos(QPointF(125, 650))

        if(pos_num == 4):
            self.setPos(QPointF(125, 475))

        if(pos_num == 5):
            self.setPos(QPointF(125, 300))

        if(pos_num == 6):
            self.setPos(QPointF(125, 125))

        if(pos_num == 7):
            self.setPos(QPointF(300, 125))

        if(pos_num == 8):
            self.setPos(QPointF(475, 125))

        if(pos_num == 9):
            self.setPos(QPointF(650, 125))

        if(pos_num == 10):
            self.setPos(QPointF(650, 300))

        if(pos_num == 11):
            self.setPos(QPointF(650, 475))



    def load_images(self):
        self.players_images = []

        for i in range(2):
            n = QPixmap(QPixmap(os.path.join('../res','players/player%s.png' % (i + 1))))
            self.players_images.append(n)

class Dice(QGraphicsPixmapItem):

    def __init__(self, *args, **kwargs):
        super(Dice, self).__init__(*args, **kwargs)

        self.signals = Communicate()

        self.load_images()

    def load_images(self):
        self.numbers_images = []

        for i in range(7):
            n = QPixmap(QPixmap(os.path.join('../res','dices/%s.png' % (i))))
            self.numbers_images.append(n)

    def DrawDice(self, number):
        SIZE=36
        self.setPixmap(self.numbers_images[number])
        self.setPos(QPointF(LEFT+WIDTH/2-SIZE/2, 600))

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        view = QGraphicsView()
        self.scene = QGraphicsScene()
        view.setScene(self.scene)

        self.scene.setSceneRect(QRectF(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        #Filling the background
        felt = QBrush(QPixmap(os.path.join('../res','background-pattern.png')))
        self.scene.setBackgroundBrush(felt)

        #Painting the field
        field = QGraphicsPixmapItem()
        field.setPixmap(QPixmap(os.path.join('../res','field.png')))
        field.setPos(QPointF(10, 5))
        self.scene.addItem(field)

        #Working with dice
        self.dice = Dice()
        self.scene.addItem(self.dice)
        self.dice.DrawDice(0)

        #Player init
        self.player_1 = Player()
        self.player_2 = Player()

        self.scene.addItem(self.player_1)
        self.player_1.DrawPlayer1(0)
        #Players
        player1_sample_text = "Player1"+", color = "+"red"+"\n"+"$200"
        self.player1_banner = QLabel(player1_sample_text)
        self.player1_banner.move(LEFT, TOP)
        self.player1_banner.resize(WIDTH, 40)
        self.player1_banner.setWordWrap(1)
        self.player1_banner.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.player1_banner)

        player2_sample_text = "Player2"+", color = "+"blue"+"\n"+"$200"
        self.player2_banner = QLabel(player2_sample_text)
        self.player2_banner.move(LEFT, TOP + 40 + DELIM)
        self.player2_banner.resize(WIDTH, 40)
        self.player2_banner.setWordWrap(1)
        self.player2_banner.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.player2_banner)
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

        #Connecting button with newMove
        self.button_newMove.clicked.connect(self.newMove)

        self.setCentralWidget(view)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle(WINDOW_NAME)

        self.show()

    def quit(self):
        self.close()

    def newMove(self):
        #TODO Handle changes from etherium contract
        #TODO Check order of moves
        self.dice.DrawDice(randint(0, 6))
        print(self.player_1.get_position())
        self.player_1.set_position((self.player_1.get_position() + 1) % 12)
        self.player_1.DrawPlayer1(self.player_1.get_position())

    def initGame(self, player_1, player_2):
        #TODO Handle starting game event from contract
        #TODO Init vars of pl_1 and pl_2. pl_1 is our local player as default
        pass

    def showStartDialog(self):
        #TODO: Add 2 buttons and 2 fields for name,
        pass

if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()
