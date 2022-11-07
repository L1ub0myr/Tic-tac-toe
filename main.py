import random

from main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from my_bot import Bot


def check(btn1, btn2, btn3):
    if btn1 == btn2 and btn2 == btn3:
        if btn1 in ("✖", "৹") or btn2 in ("✖", "৹") or btn3 in ("✖", "৹"):
            return True


def winner_light(buttons, color_=None):
    for button in buttons:
        color = "red" if button.text() == "✖" else "blue"
        if color_:
            button.setStyleSheet(f"color: red; background: {color_}; border: 3px solid red; border-radius: 15px;")
        else:
            button.setStyleSheet(
                f"color: {color}; background: #89ff6b; border: 3px solid {color}; border-radius: 15px;")


class App(QMainWindow):
    PLAY_FLAG = 0
    PLAYER_1 = 0
    PLAYER_2 = 0
    COUNTER = 0

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.complete = {self.ui.btn_1: "", self.ui.btn_2: "", self.ui.btn_3: "",
                         self.ui.btn_4: "", self.ui.btn_5: "", self.ui.btn_6: "",
                         self.ui.btn_7: "", self.ui.btn_8: "", self.ui.btn_9: ""}
        self.default_stylesheet = "QPushButton {\n	background: white;\n	border: 3px solid grey;\n	border-radius: " \
                                  "15px;\n}\nQPushButton:hover {\n	background: #e6e6e6;\n	border-radius: " \
                                  "15px;\n}\nQPushButton:pressed {\n	background: white;\n	border: 3px solid " \
                                  "grey;\n	border-radius: 15px;\n} "

    def connect_button(self, button):
        button.clicked.connect(lambda: self.draw(button))

    def init_ui(self):
        self.ui.start_game.clicked.connect(self.start)
        for i in [self.ui.btn_1, self.ui.btn_2, self.ui.btn_3,
                  self.ui.btn_4, self.ui.btn_5, self.ui.btn_6,
                  self.ui.btn_7, self.ui.btn_8, self.ui.btn_9]:
            self.connect_button(i)

    def start(self):
        self.ui.start_game.setEnabled(False)
        self.ui.start_game.setStyleSheet("")
        self.player_step()
        buttons = [self.ui.btn_1, self.ui.btn_2, self.ui.btn_3,
                   self.ui.btn_4, self.ui.btn_5, self.ui.btn_6,
                   self.ui.btn_7, self.ui.btn_8, self.ui.btn_9]
        for btn in buttons:
            btn.setEnabled(True)

    def draw(self, btn):
        try:
            if self.COUNTER % 2 == 0:
                text = "✖" if self.PLAY_FLAG % 2 == 0 else "৹"
            else:
                text = "৹" if self.PLAY_FLAG % 2 == 0 else "✖"
            font = QtGui.QFont()
            font.setFamily("Monaco")
            font.setPointSize(75)
            btn.setFont(font)
            color = "red" if text == "✖" else "blue"
            btn.setStyleSheet(f"color: {color}; background: white; border: 3px solid {color}; border-radius: 15px;")
            btn.setText(text)
            self.complete[btn] = text
            self.PLAY_FLAG += 1
            self.player_step()
            self.check_winner()
            if self.PLAY_FLAG == 9:
                self.stop_game()
            btn.setEnabled(False)
        except StopIteration:
            self.stop_game()

    def check_winner(self):
        if check(self.complete[self.ui.btn_1], self.complete[self.ui.btn_2], self.complete[self.ui.btn_3]):
            winner_light([self.ui.btn_1, self.ui.btn_2, self.ui.btn_3])
            self.stop_game(winner=self.ui.btn_1.text())
        if check(self.complete[self.ui.btn_4], self.complete[self.ui.btn_5], self.complete[self.ui.btn_6]):
            winner_light([self.ui.btn_4, self.ui.btn_5, self.ui.btn_6])
            self.stop_game(winner=self.ui.btn_4.text())
        if check(self.complete[self.ui.btn_7], self.complete[self.ui.btn_8], self.complete[self.ui.btn_9]):
            winner_light([self.ui.btn_7, self.ui.btn_8, self.ui.btn_9])
            self.stop_game(winner=self.ui.btn_7.text())
        if check(self.complete[self.ui.btn_1], self.complete[self.ui.btn_4], self.complete[self.ui.btn_7]):
            winner_light([self.ui.btn_1, self.ui.btn_4, self.ui.btn_7])
            self.stop_game(winner=self.ui.btn_1.text())
        if check(self.complete[self.ui.btn_2], self.complete[self.ui.btn_5], self.complete[self.ui.btn_8]):
            winner_light([self.ui.btn_2, self.ui.btn_5, self.ui.btn_8])
            self.stop_game(winner=self.ui.btn_2.text())
        if check(self.complete[self.ui.btn_3], self.complete[self.ui.btn_6], self.complete[self.ui.btn_9]):
            winner_light([self.ui.btn_3, self.ui.btn_6, self.ui.btn_9])
            self.stop_game(winner=self.ui.btn_3.text())
        if check(self.complete[self.ui.btn_1], self.complete[self.ui.btn_5], self.complete[self.ui.btn_9]):
            winner_light([self.ui.btn_1, self.ui.btn_5, self.ui.btn_9])
            self.stop_game(winner=self.ui.btn_1.text())
        if check(self.complete[self.ui.btn_3], self.complete[self.ui.btn_5], self.complete[self.ui.btn_7]):
            winner_light([self.ui.btn_3, self.ui.btn_5, self.ui.btn_7])
            self.stop_game(winner=self.ui.btn_3.text())

    def stop_game(self, winner=None):
        if winner:
            if winner == "✖":
                self.PLAYER_1 += 1
                self.ui.label_3.setText(f"{self.PLAYER_1}")
                self.show_messagebox(QMessageBox.Information, "Гра завершена", "Переможець:\nГравець ✖")
            elif winner == "৹":
                self.PLAYER_2 += 1
                self.ui.label_4.setText(f"{self.PLAYER_2}")
                self.show_messagebox(QMessageBox.Information, "Гра завершена", "Переможець:\nГравець ৹")
        else:
            winner_light([self.ui.btn_1, self.ui.btn_2, self.ui.btn_3,
                          self.ui.btn_4, self.ui.btn_5, self.ui.btn_6,
                          self.ui.btn_7, self.ui.btn_8, self.ui.btn_9], color_="grey")
            self.show_messagebox(QMessageBox.Information, "Гра завершена", "Нічия")
        self.complete = {self.ui.btn_1: "", self.ui.btn_2: "", self.ui.btn_3: "",
                         self.ui.btn_4: "", self.ui.btn_5: "", self.ui.btn_6: "",
                         self.ui.btn_7: "", self.ui.btn_8: "", self.ui.btn_9: ""}
        buttons = [self.ui.btn_1, self.ui.btn_2, self.ui.btn_3,
                   self.ui.btn_4, self.ui.btn_5, self.ui.btn_6,
                   self.ui.btn_7, self.ui.btn_8, self.ui.btn_9]
        for btn in buttons:
            btn.setText("")
            btn.setEnabled(False)
            btn.setStyleSheet(self.default_stylesheet)
        self.ui.start_game.setEnabled(True)
        self.PLAY_FLAG = 0
        self.COUNTER += 1
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.ui.start_game.setFont(font)
        self.ui.start_game.setText("START")
        self.ui.start_game.setStyleSheet("QPushButton {\n"
                                         "    background: #9bfc90;\n"
                                         "    border: 5px solid black;\n"
                                         "    border-radius: 10px;\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background: #72fc62;\n"
                                         "    border: 3px solid black;\n"
                                         "    border-radius: 5px;\n"
                                         "}r")

    def show_messagebox(self, type_msg, title, text):
        msg = QMessageBox()
        msg.setIcon(type_msg)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStyleSheet("background: none;")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def player_step(self):
        if self.COUNTER % 2 == 0:
            if self.PLAY_FLAG % 2 == 0:
                self.set_params_button("✖", "blue")
            else:
                self.set_params_button("৹", "red")
        else:
            if self.PLAY_FLAG % 2 == 0:
                self.set_params_button("৹", "blue")
            else:
                self.set_params_button("✖", "red")

    def set_params_button(self, text, color):
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(75)
        self.ui.start_game.setFont(font)
        self.ui.start_game.setText(text)
        self.ui.start_game.setStyleSheet(f"background: white; border: 5px solid {color}; "
                                         f"color: {color}; border-radius: 10px;")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
