from PyQt5 import QtGui, QtCore, QtWidgets
import random

class Pacmen:

    def __init__(self, width, height):
        self.body = [13, 7]

        self.lifes = 3
        self.score = 0

        self.direction = 'left'
        self.color = QtGui.QImage('image/body.png')

        self.died = False
        self.width = width
        self.height = height

    def is_dead(self):
        self.died = True

class Ghosts:

    def __init__(self, width, height):
        self.bodies = [[13, 17], [14, 17], [15, 17], [16, 17]]

        self.color = QtGui.QImage('image/ghost.png')

        self.last_pos = [[12, 17], [15, 17], [14, 17], [15, 17]]
        self.width = width
        self.height = height


class Food:

    def __init__(self, width, height):
        self.bag = []

        self.color = QtGui.QImage('image/black_point.png')

        self.width = width
        self.height = height


class Board(QtWidgets.QFrame):
    SPEED = 150

    HEIGHTINBLOCKS = 33
    WIDTHINBLOCKS = 28

    def __init__(self, parent):
        super(Board, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        self.timer = QtCore.QBasicTimer()
        self.restart = False
        self.win = False
        self.win_path = False

        self.pacmen = Pacmen(Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS)
        self.ghosts = Ghosts(Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS)

        self.food = Food(Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS)
        self.map = []
        self.get_map()
        self.add_food()

    def get_map(self):
        mp = open('image/map.txt', 'r')
        i, j = 0, 0
        while not(i == 27 and j == 31):
            i, j = map(int, mp.readline().split())
            self.map.append([i, j])
        mp.close()

    def add_food(self):
        for i in range(self.WIDTHINBLOCKS):
            for j in range(self.HEIGHTINBLOCKS - 1):
                if ((i < self.ghosts.bodies[0][0] - 5 or i > self.ghosts.bodies[0][0] + 6) or
                    (j < self.ghosts.bodies[0][1] - 3 or j > self.ghosts.bodies[0][0] + 9)) and \
                        not([i, j] in self.map):
                    self.food.bag.append([i, j])

    def block_width(self):
        return self.frameGeometry().width() / Board.WIDTHINBLOCKS

    def block_height(self):
        return self.frameGeometry().height() / Board.HEIGHTINBLOCKS

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:

        painter = QtGui.QPainter(self)

        rect = self.contentsRect()
        gorect = QtCore.QRect(0, 0, self.width(), self.height())
        color_brick = QtGui.QImage('image/brick.png')
        color_heart = QtGui.QImage('image/heart.png')
        game_over = QtGui.QImage('image/game_over.png')
        game_win = QtGui.QImage('image/tian.png')
        mega_pacmen = QtGui.QImage('image/pacman.png')

        boardtop = rect.bottom() - self.frameGeometry().height()

        if self.win:
            painter.drawImage(gorect, game_win)
            painter.drawText(self.block_width() * 0, self.block_height() * 16, self.block_width() * 5,
                             self.block_height() * 2, 0, "Your WIN!, wait the second version, now you score: "
                             + str(self.pacmen.score))
        elif self.restart:
            painter.drawImage(gorect, game_over)
            painter.drawText(self.block_width() * 0, self.block_height() * 2, self.block_width() * 5,
                             self.block_height() * 2, 0, "Your score: " + str(self.pacmen.score))
            painter.drawText(self.block_width() * 0, self.block_height() * 3, self.block_width() * 5,
                             self.block_height() * 2, 0, "For restart please сlick!"+
                                                         " in the next attempt, you will definitely win :]")
        else:
            if (self.win_path):
                self.pacmen.color = mega_pacmen
            self.drawrect(painter, rect.left() + self.pacmen.body[0] * self.block_width(),
                          boardtop + self.pacmen.body[1] * self.block_height(), self.pacmen.color)

            for brick in self.map:
                self.drawrect(painter, rect.left() + brick[0] * self.block_width(),
                              boardtop + brick[1] * self.block_height(), color_brick)

            for fruit in self.food.bag:
                self.drawrect(painter, rect.left() + fruit[0] * self.block_width(),
                              boardtop + fruit[1] * self.block_height(), self.food.color)

            for ghost in self.ghosts.bodies:
                self.drawrect(painter, rect.left() + ghost[0] * self.block_width(),
                              boardtop + ghost[1] * self.block_height(), self.ghosts.color)

            for i in range(self.pacmen.lifes):
                self.drawrect(painter, rect.left() + (25 + i) * self.block_width(),
                              boardtop + 32 * self.block_height(), color_heart)

            painter.drawText(self.block_width() * 0, self.block_height() * 32,
                             self.block_width() * 5, self.block_height() * 2, 0, "Score: " + str(self.pacmen.score))

            if self.win_path:
                painter.drawText(self.block_width() * 10, self.block_height() * 32,
                                 self.block_width() * 5, self.block_height() * 2, 0, "You can eat ghoast")


    def drawrect(self, painter, x, y, color):
        rect = QtCore.QRect(x, y, self.block_width() - 2, self.block_height() - 2)
        painter.drawImage(rect, color)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.restart:
            self.Restart_Event()
            return

    def timerEvent(self, a0: QtCore.QTimerEvent) -> None:

        if a0.timerId() == self.timer.timerId():
            if not( self.pacmen.died) and not( self.win):
                self.pacmen_move()
                self.ghosts_move()
                self.collision()
            else:
                self.restart = True
            self.update()

    def collision(self):
        for fruit in self.food.bag:
            if fruit == self.pacmen.body:
                self.food.bag.remove(fruit)
                self.pacmen.score += 10
                if len(self.food.bag) == 0:
                    self.win_path = True
                break
        for ghost_i in range(len(self.ghosts.bodies)):
            if self.ghosts.bodies[ghost_i] == self.pacmen.body:
                if self.win_path:
                    self.ghosts.bodies.remove(self.ghosts.bodies[ghost_i])
                    self.ghosts.last_pos.remove(self.ghosts.last_pos[ghost_i])
                    if len(self.ghosts.bodies) == 0:
                        self.win = True
                    break
                else:
                    self.pacmen.lifes -= 1
                if self.pacmen.lifes == 0:
                    self.pacmen.is_dead()

    def pacmen_move(self):

        if self.pacmen.direction == 'left' and not([self.pacmen.body[0] - 1, self.pacmen.body[1]] in self.map):
            self.pacmen.body = [self.pacmen.body[0] - 1, self.pacmen.body[1]]

            if self.pacmen.body[0] == -1:
                self.pacmen.body[0] = self.pacmen.width - 1

        if self.pacmen.direction == 'right' and not([self.pacmen.body[0] + 1, self.pacmen.body[1]] in self.map):
            self.pacmen.body = [self.pacmen.body[0] + 1, self.pacmen.body[1]]

            if self.pacmen.body[0] == self.pacmen.width:
                self.pacmen.body[0] = 0

        if self.pacmen.direction == 'up' and not([self.pacmen.body[0], self.pacmen.body[1] - 1] in self.map):
            self.pacmen.body = [self.pacmen.body[0], self.pacmen.body[1] - 1]

        if self.pacmen.direction == 'down' and not([self.pacmen.body[0], self.pacmen.body[1] + 1] in self.map):
            self.pacmen.body = [self.pacmen.body[0], self.pacmen.body[1] + 1]

    def ghosts_move(self):
        for i in range(len(self.ghosts.bodies)):
            var_moves = [[self.ghosts.bodies[i][0] - 1, self.ghosts.bodies[i][1]],
                         [self.ghosts.bodies[i][0] + 1, self.ghosts.bodies[i][1]],
                         [self.ghosts.bodies[i][0], self.ghosts.bodies[i][1] - 1],
                         [self.ghosts.bodies[i][0], self.ghosts.bodies[i][1] + 1]]
            var_del = []
            for var in var_moves:
                if var in self.map:
                    var_del.append(var)
            if self.ghosts.last_pos[i] in var_moves:
                var_del.append(self.ghosts.last_pos[i])

            for var in var_del:
                var_moves.remove(var)
            if len(var_moves) != 0:
                rand = random.randint(0, len(var_moves) - 1)
                self.ghosts.last_pos[i] = self.ghosts.bodies[i]
                self.ghosts.bodies[i] = var_moves[rand]
                if self.ghosts.bodies[i][0] == self.ghosts.width:
                    self.ghosts.bodies[i][0] = 0
                    self.ghosts.last_pos[i] = [-1, self.ghosts.bodies[i][1]]
                if self.ghosts.bodies[i][0] == -1:
                    self.ghosts.bodies[i][0] = self.ghosts.width - 1
                    self.ghosts.last_pos[i] = [self.ghosts.width, self.ghosts.bodies[i][1]]

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:

        key = a0.key()

        if key == QtCore.Qt.Key.Key_Left:
            if not([self.pacmen.body[0] - 1, self.pacmen.body[1]] in self.map):
                self.pacmen.direction = 'left'

        if key == QtCore.Qt.Key.Key_Right:
            if not([self.pacmen.body[0] + 1, self.pacmen.body[1]] in self.map):
                self.pacmen.direction = 'right'

        if key == QtCore.Qt.Key.Key_Up:
            if not([self.pacmen.body[0], self.pacmen.body[1] - 1] in self.map):
                self.pacmen.direction = 'up'

        if key == QtCore.Qt.Key.Key_Down:
            if not([self.pacmen.body[0], self.pacmen.body[1] + 1] in self.map):
                self.pacmen.direction = 'down'

    def Restart_Event(self):
        self.timer.stop()
        self.ghosts = Ghosts(Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS)
        self.food = Food(Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS)
        self.add_food()
        self.pacmen = Pacmen(Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS)
        self.restart = False
        self.win_path = False
        self.win = False
        self.start()

    def start(self):
        self.timer.start(Board.SPEED, self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.setGeometry(100, 100, 600, 400)
        self.board.start()

        self.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())