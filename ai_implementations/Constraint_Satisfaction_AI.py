from WordleAI import WordleAI
from Helper_Functions import *

class Simple_CSP(WordleAI):


    def __init__(self, words):
        super().__init__(words)
        
        self.IG = IG_Calc(self.words)
        
        self.word_IG_dict = Calc_Word_IG(self.words,self.IG)
        
    
    def guess(self, guess_history):
    
        if len(guess_history) == 0:
            
            res_word = list(self.word_IG_dict.keys())
            res_word.sort(reverse=True)
            return self.word_IG_dict[res_word[0]]
            
        else:
            
            options = remaining_options(self.words, guess_history)
            self.word_IG_dict = Calc_Word_IG(options,self.IG)
            res_word = list(self.word_IG_dict.keys())
            res_word.sort(reverse=True)
            return self.word_IG_dict[res_word[0]]
            
        
    def get_author(self):
        return "Abhas"
        