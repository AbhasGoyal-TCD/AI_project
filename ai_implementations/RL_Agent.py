import random

from WordleAI import WordleAI
from Helper_Functions import *

class RL_Agent(WordleAI):

    def __init__(self, words, alpha, gamma):
        super().__init__(words)
        
        self.IG = IG_Calc(self.words)
        
        self.word_IG_dict = Calc_Word_IG(self.words,self.IG)
        self.qlearning = QLearner(alpha, gamma)
        
    def guess(self, guess_history):
		return random.choice(self.words)
	
	def get_author(self):
        return "Abhas"
        
        
class QLearner():

    def __init__(self, alpha, gamma):
        
        self.alpha=alpha
        self.gamma=gamma 
        self.qtable = {'Undiscovered':np.zeros(15),'Constrained_List':np.zeros(15)}