import inspect
import os
import random
import importlib
import time
import json

import pytablewriter
import numpy as np
from pytablewriter.style import Style

from WordList import *
from WordleAI import *
from ai_implementations.RL_Agent import RL_Agent

class Competition:

    def __init__(self, competitor_directory, alpha, gamma, epsilon, wordlist_filename="data/official/combined_wordlist.txt", hard_mode=False):
        self.competitor_directory = competitor_directory
        self.wordlist = WordList(wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitors = RL_Agent(self.wordlist.get_list_copy(), alpha, gamma, epsilon, 'Training')
        self.hard_mode = hard_mode
        
    def load_RL(self):
        competitors = []
        for file in os.listdir(self.competitor_directory):
            if file.endswith(".py"):
                module = importlib.import_module(self.competitor_directory + "." + file[:-3])
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, WordleAI) and not inspect.isabstract(obj):
                        competitors.append(obj(self.wordlist.get_list_copy()))
        return competitors

        
    def guess_is_legal(self, guess, guess_history):
        return len(guess) == 5 and guess.lower() == guess and guess in self.words and (
                not self.hard_mode or is_hard_mode(guess, guess_history))

    def play(self, competitor, word):
        guesses = []
        success = False
        guess_history = []

        for i in range(6):  # Up to 100 guesses
            guess = competitor.guess(guess_history)
            if not self.guess_is_legal(guess, guess_history):
                print("Competitor ", competitor.__class__.__name__, " is a dirty cheater!")
                print("hard_mode: ", self.hard_mode, "guess: ", guess, "guess_history", guess_history)
                print("Competition aborted.")
                quit()

            guess_result = []
            for c in range(5):
                if guess[c] not in word:
                    guess_result.append(LetterInformation.NOT_PRESENT)
                elif word[c] == guess[c]:
                    guess_result.append(LetterInformation.CORRECT)
                else:
                    guess_result.append(LetterInformation.PRESENT)
            guess_history.append((guess, guess_result))
            guesses.append(guess)

            if guess == word:
                success = True
                competitor.qlearner.update_qtable(competitor.prev_state, competitor.prev_action, '22222', guess_history[-1])
                #competitor.guess(guess_history)
                break
            else:
                competitor.qlearner.update_qtable(competitor.prev_state, competitor.prev_action, competitor.form_state(competitor.cur_state,guess_history[-1]), guess_history[-1])
                
        return success, guesses
        
    def fight(self, rounds, print_details=False, solution_wordlist_filename='data/official/combined_wordlist.txt',
              shuffle=False):
        
        fight_words = WordList(solution_wordlist_filename).get_list_copy()
        for r in range(rounds):
            #for competitor in self.competitors:
            word = random.choice(fight_words) if shuffle else fight_words[r]
            print("Round: ",word)
            success, round_guesses = self.play(self.competitors, word)
            print("Round: ", r, success)

                
def main():
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(suppress=True)
    
    alpha = 0.3
    gamma = 0.1
    epsilon = 0.9

    competition = Competition("ai_implementations/RL_Training", alpha, gamma, epsilon, wordlist_filename="data/official/combined_wordlist.txt", hard_mode=False )
    competition.fight(rounds=1000, solution_wordlist_filename="data/official/shuffled_real_wordles.txt", print_details=False, shuffle = True)
    
    #print(competition.competitors.qlearner.qtable)
    
    with open('ai_implementations/RL_Training/RL_weights_a=' + str(alpha)+'_g='+str(gamma)+'_e='+str(epsilon)+ '.txt','w') as convert_file: 
      convert_file.write(json.dumps(competition.competitors.qlearner.qtable))

if __name__ == "__main__":
    main()
