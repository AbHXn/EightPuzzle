import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

import EPuzzleAi

goal = ['1','2','3','4','5','6','7','8','_']

class Puzzle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8 Puzzle")
        self.setFixedSize(300, 360)

        self.board = goal.copy()
        self.layout = QVBoxLayout()
        self.grid = QGridLayout()

        self.label = QLabel("8 Puzzle Game")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 14, QFont.Bold))

        self.buttons = []

        for i in range(9):
            btn = QPushButton("")
            btn.setFont(QFont("Arial", 18, QFont.Bold))
            btn.setFixedSize(80, 80)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 2px solid #555;
                }
                QPushButton:hover {
                    background-color: #dcdcdc;
                }
            """)

            btn.clicked.connect(lambda _, i=i: self.move(i))
            self.grid.addWidget(btn, i//3, i%3)
            self.buttons.append(btn)

        self.solve_btn = QPushButton("Solve")
        self.solve_btn.setFixedHeight(40)
        self.solve_btn.clicked.connect(self.solve)

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.solve_btn)

        self.setLayout(self.layout)
        self.update_ui()

    def to_2d(self):
        return [self.board[i*3:(i+1)*3] for i in range(3)]

    def to_1d(self, board2d):
        return [cell for row in board2d for cell in row]

    def get_neighbors(self, index):
        moves = []
        row, col = divmod(index, 3)

        if row > 0: moves.append(index - 3)
        if row < 2: moves.append(index + 3)
        if col > 0: moves.append(index - 1)
        if col < 2: moves.append(index + 1)

        return moves

    def move(self, index):
        empty = self.board.index('_')
        if index in self.get_neighbors(empty):
            self.board[empty], self.board[index] = self.board[index], self.board[empty]
            self.update_ui()

    def update_ui(self):
        for i in range(9):
            val = self.board[i]

            if val == '_':
                self.buttons[i].setText("")
                self.buttons[i].setStyleSheet("""
                    background-color: white;
                    border: 2px dashed #aaa;
                """)
            else:
                self.buttons[i].setText(val)
                self.buttons[i].setStyleSheet("""
                    background-color: #f0f0f0;
                    border: 2px solid #555;
                """)

    def solve(self):
        board2d = self.to_2d()
        ai = EPuzzleAi.EIGHT_PUZZLE(board=board2d)
        path = ai.play()

        if not path: return

        self.steps = [self.to_1d(state) for state in path[::-1]]
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(400)

    def animate(self):
        if self.step_index >= len(self.steps):
            self.timer.stop()
            return
        self.board = self.steps[self.step_index]
        self.update_ui()
        self.step_index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Puzzle()
    window.show()
    sys.exit(app.exec_())
