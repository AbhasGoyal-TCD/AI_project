import random
import numpy as np

from WordleAI import WordleAI
from Helper_Functions import *

class RL_Agent(WordleAI):

    def __init__(self, words, alpha=0.9,gamma=0.9):
        super().__init__(words)
        self.IG = IG_Calc(self.words)
        self.word_IG_dict = Calc_Word_IG(self.words,self.IG)
        self.qlearner = QLearner(self.words,alpha,gamma)
        
    def guess(self, guess_history):
        if len(guess_history) == 0:
            res_word = list(self.word_IG_dict.keys())
            res_word.sort(reverse=True)
            return self.word_IG_dict[res_word[0]]
        else:
            options = self.qlearner.get_action(guess_history)
            print(options)
            self.word_IG_dict = Calc_Word_IG(options,self.IG)
            res_word = list(self.word_IG_dict.keys())
            res_word.sort(reverse=True)
            return self.word_IG_dict[res_word[0]]
   
    def get_author(self):
        return "Vyshnavi & Kaaviya"
        
        
class QLearner():

    def __init__(self,words,alpha, gamma):
        self.qwords = words
        self.alpha=alpha
        self.gamma=gamma
        self.state = '00'
        self.action = 0
        self.action_count = 2
        self.qtable = {'00':np.zeros(self.action_count)}
        self.reward = 0.0
    
    def update_qtable(self,s,a,new_state,reward):
        if new_state in self.qtable.keys():
            new_action = np.argmax(self.qtable[new_state])
        else:
            self.qtable[new_state]=np.zeros(self.action_count)
            new_action = random.randint(0,self.action_count-1)
        self.qtable[s][a]=(1-self.alpha)*self.qtable[s][a]+self.alpha*(reward+self.gamma*self.qtable[new_state][a_prime])
        return new_action

    def get_action(self,guess_history):
        options = []
        new_state = '0'+ str(len(guess_history))
        new_action = self.update_qtable(self.state,self.action,new_state,self.reward)
        self.reward = self.get_reward(guess_history)
        self.state = new_state
        if new_action == 0 :
                options_undisc = undisc_rem_options(self.qwords,guess_history)
                if len(options_undisc) == 0:
                    rem_options = remaining_options(self.qwords,guess_history)
                    self.action = 1
                    return rem_options
                self.action = new_action
                print('action',new_action)
                return options_undisc
        elif new_action == 1:
                rem_options = remaining_options(self.qwords,guess_history)
                if len(rem_options) == 0:
                    options_undisc = undisc_rem_options(self.qwords,guess_history)
                    self.action = 0
                    return options_undisc
                self.action = new_action
                print('action',new_action)
                return rem_options
        


    def get_reward(self,guess_history):
        r = 0
        entry = guess_history[::-1][0]
        for i in range(5):
            if entry[1][i] == LetterInformation.CORRECT:
                    r = r+20
            elif entry[1][i] == LetterInformation.PRESENT:
                    r = r+15
            else:
                    r = r-1
        return r







