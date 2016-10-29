#! coding:utf-8


import numpy as np
import re
import time

from PySide.QtCore import QObject, Signal


class Operator(QObject):
    speach = Signal(str)

    def __init__(self):
        super().__init__()
        self.engin = SearchEngine()
        pass

    def init(self):
        self.speach.emit("お問い合わせ有難うございます。私、お問い合わせ係のシンヤAIです。")
        time.sleep(1)
        q_word = self.engin.getQuestion()
        self.speach.emit(q_word)

    def send(self, word):
        # オウム返し
        # self.speach.emit(word)

        if re.search(r"こんにちわ", word):
            self.speach.emit("こんにちわ。今日はよろしくお願いいたします。")
        else:
            self.engin.setAnswer(word)
            q_word = self.engin.getQuestion()
            self.speach.emit(q_word)

class SearchEngine(object):
    sizes = (20, 40, 60, 80, 100, 120, 140)
    sizes_fazzi = ("手のひら", "膝丈", "片腕", "太もも", "腰丈", "胸", "首")
    sizes_scale_sm = ("小さい", "低い", "短い","低い","低い","低い","低い")
    sizes_scale_bg = ("大きい", "高い", "長い","高い","高い","高い","高い")
    size_points = np.array([0, 0, 0, 0, 0, 0, 0])
    has_question = True

    def getQuestion(self):

        y = np.array(self.size_points)
        x = np.array(range(y.size))

        if np.sum(y) == 0:
            moment = 0
        else:
            moment = np.dot(y, x) / np.sum(y)
        self.search_index = int(np.round(moment))
        index = self.search_index

        # 終了判定
        maxv = np.max(self.size_points)
        max_count = np.sum(self.size_points == maxv)

        print(self.size_points, index, moment, max_count)


        if max_count == 1:
            # question終了
            self.has_question = False
            s= "お客様へ提案させて頂く段ボールのサイズは正方形{}cmタイプです。\n".format(self.sizes[index])
            s += "追って営業担当から直接ご連絡を差し上げますので今しばらくお待ちください。"

            return s

        pos = self.sizes_fazzi[index]
        scale_word = self.sizes_scale_sm[index]
        q_word = "梱包物の高さは{}よりも{}ですか?".format(pos, scale_word)


        return q_word

    def setAnswer(self, ans):
        a_word = ans

        if re.search(u"大", a_word):
            self.size_points[self.search_index:] += 1
        elif re.search(u"小", a_word):
            self.size_points[self.search_index:] -= 1
        elif re.search(u"高", a_word):
            self.size_points[self.search_index:] += 1
        elif re.search(u"低", a_word):
            self.size_points[self.search_index:] -= 1
        elif re.search(u"長", a_word):
            self.size_points[self.search_index:] += 1
        elif re.search(u"短", a_word):
            self.size_points[self.search_index:] -= 1
        elif re.search(u"同",a_word):
            self.size_points[self.search_index] += 2

        np.clip(self.size_points,0,100, self.size_points)



if __name__ == '__main__':
    import unittest


    class TestSearchEngine(unittest.TestCase):
        def setUp(self):
            self.search_engine = SearchEngine()

        def test_q(self):
            q_word = self.search_engine.getQuestion()
            a_word = "大きいです"
            self.search_engine.setAnswer(a_word)

            print("Q:{}".format(q_word))
            print("A:{}".format(a_word))
            print(self.search_engine.size_points)

            q_word = self.search_engine.getQuestion()
            a_word = "小さいです"
            self.search_engine.setAnswer(a_word)

            print("Q:{}".format(q_word))
            print("A:{}".format(a_word))
            print(self.search_engine.size_points)

            q_word = self.search_engine.getQuestion()
            a_word = "小さいです"
            self.search_engine.setAnswer(a_word)

            print("Q:{}".format(q_word))
            print("A:{}".format(a_word))
            print(self.search_engine.size_points)
    unittest.main()
