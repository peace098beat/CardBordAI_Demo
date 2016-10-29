#!coding:utf-8

import sys
import qdarkstyle
from PySide.QtCore import QMetaObject
from PySide.QtCore import QTimer, Slot
from PySide.QtGui import QApplication, QWidget

# from applogger import logger
from Operator import Operator
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QLineEdit
from PySide.QtGui import QPushButton
from PySide.QtGui import QTextEdit
from PySide.QtGui import QVBoxLayout

TALK_DELAY = 1000


class CardBordAIApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CardBord AI Demo ver0.10")
        self.operator = Operator()

        self.setupUi()

        self.operator.speach.connect(self.speak_ai)

        self.init()

    def setupUi(self):
        self.mainlayout = QVBoxLayout(self)

        self.title = QLabel("CardBord Operator", self)
        self.mainlayout.addWidget(self.title)

        self.user_txtarea = QTextEdit(self)
        self.ai_txtarea = QTextEdit(self)

        self.users_edit_title = QLabel("質問に答えてください")
        self.users_edit = QLineEdit("", self)

        self.txtarea_layout = QHBoxLayout()

        self.txtarea_layout.addWidget(self.user_txtarea)
        self.txtarea_layout.addWidget(self.ai_txtarea)

        self.mainlayout.addLayout(self.txtarea_layout)
        self.mainlayout.addWidget(self.users_edit_title)
        self.mainlayout.addWidget(self.users_edit)

        self.send_btn = QPushButton("send", self)
        self.send_btn.setObjectName("send_btn")
        self.mainlayout.addWidget(self.send_btn)

        QMetaObject.connectSlotsByName(self)

    def init(self):
        # Talkエリアの初期化
        self.user_txtarea.clear()
        self.ai_txtarea.clear()
        # オペレータ初期化、初期ワード取得
        self.operator.init()

    @Slot()
    def on_send_btn_clicked(self):
        # UI処理
        user_word = self.users_edit.text()
        if user_word == "":
            return None
        self.users_edit.clear()
        self.user_txtarea.append(user_word)

        # サーバー(エンジン)へユーザワードを送信
        self.operator.send(user_word)

    @Slot()
    def speak_ai(self, word):
        # AIのトークを表示
        # ディレイを使ってテンポを整える
        def wrapper():
            self.ai_txtarea.append(word)

        QTimer.singleShot(TALK_DELAY, wrapper)


if __name__ == '__main__':

    import traceback

    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet())
        dialog = CardBordAIApp()
        dialog.show()
        sys.exit(app.exec_())
    except:
        # logger.error(traceback.format_exc())
        print(traceback.format_exc())
