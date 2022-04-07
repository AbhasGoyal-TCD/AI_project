import random
import numpy as np
import ast
import json

from WordleAI import WordleAI
from Helper_Functions import *
from WordleJudge import WordleJudge

class RL_Agent(WordleAI):

    def __init__(self, words, alpha=0.1,gamma=0.5,epsilon=0.3, mode = 'Competing'):
        super().__init__(words)
        self.IG = IG_Calc(self.words)
        #self.word_IG_dict = Calc_Word_IG(self.words,self.IG)
        self.cur_state = '00000'
        self.mode = mode
        self.qlearner = QLearner(self.words,alpha,gamma,epsilon, mode)
        self.prev_action = -1
        self.prev_state = '00000'
        self.epsilon_decay = 0
        self.judge = WordleJudge()
        
    def guess(self, guess_history):
        
        
        if len(guess_history) == 0:
            self.cur_state = '00000'
            self.prev_action = -1
            self.prev_state = '00000'
            if self.mode != 'Competing':
                self.epsilon_decay += 1
                if self.epsilon_decay % 50 == 0:
                    self.qlearner.epsilon = self.qlearner.epsilon/2
            
        rem_words = remaining_options(self.words.copy(), guess_history)
        undiscovered_words = undisc_rem_options(self.words.copy(),guess_history)
        legal_actions = self.get_legal_actions(rem_words, undiscovered_words)
        
        if len(guess_history) != 0:
            self.prev_state = self.cur_state
            
            #self.qlearner.update_qtable(self.prev_state, self.prev_action, self.cur_state, guess_history[-1])
            self.cur_state = self.form_state(self.cur_state, guess_history[-1])
            
            
        action = self.qlearner.get_action(self.cur_state, legal_actions)
        self.prev_action = action

        if action == 0:
            word_list = rem_words
        elif action == 1:
            word_list = undiscovered_words 
        else:
            word = random.choice(self.words)
            return word
        
        self.IG = IG_Calc(word_list)
        word_IG_dict = Calc_Word_IG(word_list,self.IG)
        res_word = list(word_IG_dict.keys())
        res_word.sort(reverse=True)
        
        return word_IG_dict[res_word[0]]
    
    #Combine feedbacks to obtain current state
    def form_state(self, cur_state, guess_history):
        state = ''
        
        for i in range(5):
            if guess_history[1][i] == LetterInformation.CORRECT:
                state += '2'
            elif guess_history[1][i] == LetterInformation.PRESENT and cur_state[i] != '2':
                state += '1'
            else:
                state += cur_state[i]
        
        return state
        
    #Get legal action of list selection depending on word availability in each list
    def get_legal_actions(self, CSP_list, Undis_list):
        actions = []
        
        if Undis_list:
            actions.append(2)
            actions.append(3)
        
        if CSP_list:
            actions.append(0)
            actions.append(1)
            
        if not bool(CSP_list) and not bool(Undis_list):
            actions.append(5)

        return actions
    
    
    def get_author(self):
        return "Abhas & Vyshnavi & Kaaviya"
        
        
class QLearner():

    def __init__(self,words,alpha, gamma, epsilon, mode):
        self.qwords = words
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon = epsilon
        self.action = ''
        self.action_count = 3
        self.qtable = {}
        
        if mode == 'Competing':
            with open('ai_implementations/RL_Training/RL_weights_a=' +str(alpha)+'_g='+str(gamma)+'_e='+ str(epsilon)+'.txt') as f:
                data = f.read()
            self.qtable = json.loads(data)
            self.epsilon = 2
            
        self.reward = 0.0
    
    def update_qtable(self,state,action,new_state, guess_history):
    
        if new_state in self.qtable.keys():
            a_prime = np.argmax(self.qtable[new_state])
        else:
            self.qtable[new_state]=[0,0,0]
            a_prime = random.randint(0,self.action_count-1)
        
        self.reward = self.get_reward(action,state, new_state,guess_history)
        if state == '22222':
            self.reward += 200       
        self.qtable[state][action]=(1-self.alpha)*self.qtable[state][action]+self.alpha*(self.reward+self.gamma*self.qtable[new_state][a_prime])
        

    def get_action(self,state, actions):
        #options = []
        #new_state = '0'+ str(len(guess_history))
        max_val = 0
        if state in self.qtable.keys():
            for ele in actions:
                if max_val <= self.qtable[state][ele]:
                    max_val = self.qtable[state][ele]
                    new_action = ele
        else:
            self.qtable[state]=[0,0,0]
            new_action = random.choice(actions)
        
        if self.epsilon > random.random():

            return random.choice(actions)
        else:
            return new_action      
        


    def get_reward(self,action,state,next_state, guess_history):
        r = 0
        entry = guess_history[1]
        if action == 1:
            for i in range(5):
                if entry[i] == LetterInformation.CORRECT:
                        r = r+20
                elif entry[i] == LetterInformation.PRESENT:
                        r = r+15
                else:
                        r = r+10
        else:
            for i in range(5):
                if state[i] != next_state[i]:
                    if next_state[i] == '2':
                        r += 20
                    else:
                        r+=15
        
        return r







