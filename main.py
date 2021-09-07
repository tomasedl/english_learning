
import sys
import random
from PyQt5 import uic, QtWidgets,QtCore
from functools import partial

from storage import load_data
import logging

from dataclasses import dataclass

@dataclass
class Word():
    original: str
    translation: str

class App(QtWidgets.QDialog):
    

    def __init__(self):
        super(App, self).__init__() 
        uic.loadUi('app_layout.ui', self)
        self.show()

        self.load_data()
        self.current = None
        self.possition = None
        self.score = 0


        self.start_rewrite_the_word.clicked.connect(self.set_rewrite_the_word, QtCore.Qt.UniqueConnection)

        self.check_rewrite_word.clicked.connect(self.check_rewrite_the_word, QtCore.Qt.UniqueConnection)
        self.next_button_rewrite_word.clicked.connect(self.set_rewrite_the_word, QtCore.Qt.UniqueConnection)

        self.start_choose_the_word.clicked.connect(self.button_start_choose_the_word, QtCore.Qt.UniqueConnection)

        self.option1.clicked.connect(partial(self.check_choose_the_word, self.option1), QtCore.Qt.UniqueConnection)
        self.option2.clicked.connect(partial(self.check_choose_the_word, self.option2), QtCore.Qt.UniqueConnection)
        self.option3.clicked.connect(partial(self.check_choose_the_word, self.option3), QtCore.Qt.UniqueConnection)

    def set_logger(self):
        pass
        
    def load_data(self):
        self.vocabulary_bank = load_data()
        log.info("load vocabularies")

    ### shared\

    def get_random_world(self):
        choice = random.choice(list(self.vocabulary_bank.items())) 
        return Word(choice[0], choice[1])

    ### first tab -- choose the right word
    def button_start_choose_the_word(self):
        self.set_choose_the_word()

   

    def generate_items(self):
        vocabulary = self.get_random_world()
        alternative1 = self.get_random_world()
        alternative2 = self.get_random_world()

        return vocabulary, alternative1, alternative2

    def set_choose_the_word(self):
        vocab, a1, a2 = self.generate_items()
        self.current = vocab
        self.to_translate.setText(self.if_more_option_return_one(vocab.original))
        log.info(self.current)

        list_of_vocab = [vocab, a1, a2]

        for op in (self.option3, self.option2, self.option1):
            text = self.fill_buttons_randomly(list_of_vocab)
            #log.info(text, self.current.translation)
            op.setText(text)
            if self.current.translation.find(text) != -1:
                self.possition = op


    def fill_buttons_randomly(self, vocabulary_list):
        text = vocabulary_list.pop(random.randint(0, len(vocabulary_list) - 1)).translation
        return self.if_more_option_return_one(text)

    def check_choose_the_word(self, option):
        print(option == self.possition)
        if option == self.possition:
            self.set_choose_the_word()
            self.score += 1
            self.score_counter.setText(str(self.score))
        else:
            log.info("Try again")


    def if_more_option_return_one(self, input):
        input = input.split(".")
        return input[random.randint(0, len(input) - 1)]


    ### second tab -- rewrite the word

    def set_rewrite_the_word(self):
        vocabulary = self.get_random_world()
        self.to_rewrite.setText(vocabulary.translation)
        self.show_result.setText("")
        self.solution.setPlainText("")
        self.current = vocabulary

    def check_rewrite_the_word(self):
        log.info("aaaa")
        # TODO try to refactor with input [arametr]
        input = self.solution.toPlainText()
        if self.current.original.lower() == input.lower():
            self.score += 1
            self.score_rewrite_word.setText(str(self.score))
        


        
        
        


        










def set_logger(level):
    log = logging.getLogger()
    log.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


if __name__ == '__main__':
    log = set_logger(logging.INFO)


    word = Word("ahoj", "karle")
    print(word.translation)
    
  

    app = QtWidgets.QApplication(sys.argv)
    window = App()
    app.exec_()


    




#TODO 
#gui app that will showing words and will wait on answer - choose wich is correct, write it in english/czech and count errors and score and allow also time framed training
# read from custom file
# logging
# precommit
# make executable
# readme file
# show me my mistake
# reset score counter
# fix corner cases of empty textbox
# fix checking of more option in rewrite word