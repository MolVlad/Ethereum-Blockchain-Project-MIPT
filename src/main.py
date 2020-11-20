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

class Player:
    def __init__(self, name, addr, money, position, movesInPrison, IsActionRequired):
        self._name = name
        self._addr = addr
        self._money = money
        self._position = position
        self._movesInPrison = movesInPrison
        self._IsActionRequired = IsActionRequired

    def get_name(self):
        return self._name

    def get_addr(self):
        return self._addr

    def get_money(self):
        return self._money

    def get_position(self):
        return self._position

    def get_movesInPrison(self):
        return self._movesInPrison

    def get_IsActionRequired(self):
        return self._IsActionRequired

    def set_money(self, ammount):
        _money = ammount

    def set_position(self, new_position):
        _position = new_position

    def set_movesInPrison(self, moves):
        _movesInPrison = moves

    def set_IsActionRequired(self, action):
        _IsActionRequired = action

class Dice(QGraphicsPixmapItem):

    def __init__(self, *args, **kwargs):
        super(Dice, self).__init__(*args, **kwargs)

        self.signals = Communicate()

        self.numbers_images = []
        self.load_images()

    def load_images(self):
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

        #Player init
        self.player_1 = Player("somename", None, 200, 0, 0, False)
        self.player_2 = Player("somename", None, 200, 0, 0, False)

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

        #Players
        player1_sample_text = "Player1"+", color = "+"red"+"\n"+"$200"
        self.player1 = QLabel(player1_sample_text)
        self.player1.move(LEFT, TOP)
        self.player1.resize(WIDTH, 40)
        self.player1.setWordWrap(1)
        self.player1.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.player1)

        player2_sample_text = "Player2"+", color = "+"blue"+"\n"+"$200"
        self.player2 = QLabel(player2_sample_text)
        self.player2.move(LEFT, TOP + 40 + DELIM)
        self.player2.resize(WIDTH, 40)
        self.player2.setWordWrap(1)
        self.player2.setAlignment(Qt.AlignCenter)
        self.scene.addWidget(self.player2)
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
