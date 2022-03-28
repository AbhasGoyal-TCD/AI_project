from WordleAI import WordleAI
from Helper_Functions import *

class Greedy_min_max(WordleAI):

    def __init__(self, words):
        super().__init__(words)
        self.IG = IG_Calc(self.words)        
        self.word_IG_dict = Calc_Word_IG(self.words,self.IG)
        
    def guess(self, guess_history): 
        next_p_words = self.words
        remaining_words = self.words
    
        if len(guess_history) == 0:
            res_word = list(self.word_IG_dict.keys())
            res_word.sort(reverse=True)
            list_w= [self.word_IG_dict[res_word[0]]]
            
        else:
            #fetched the last gussed word
            length = len(guess_history)
            self.last_word = (guess_history[length-1])[0]
            #check based on responce given if the last word can be obtained
            responce =[]
            for entry in guess_history:
                min_wc = 100000
                chosen_word = ""
                self.smrt = {}
                w1 = entry[0]
                rmat = {}
                responce =[]
                for i in range(5):
                    if entry[1][i] == LetterInformation.CORRECT:
                        responce.append(2)
                    elif entry[1][i] == LetterInformation.PRESENT:
                        responce.append(1)
                    else:
                        responce.append(0)
                for w2 in next_p_words:
                    w2 = w2.strip()
                    msum = calc_response_vector(w1,w2)
                    if tuple(msum) not in rmat:
                        rmat[tuple(msum)] = [w2]
                    else:
                        rmat[tuple(msum)].append(w2)
                if tuple(responce) in rmat:
                    next_p_words = rmat[tuple(responce)]
                else:
                    next_p_words = self.words
                
            #fetch the possible next words metrix
            if len(next_p_words) == 1:
                return next_p_words[0]
            list_w = remaining_options(self.words, guess_history)
        
        min_wc = 100000
        chosen_word = ""
        srmat = {}
        for w1 in list_w:
            w1 = w1.strip()
            rmat = {}
            for w2 in next_p_words:
                w2 = w2.strip()
                msum = calc_response_vector(w1,w2)
                if tuple(msum) not in rmat:
                    rmat[tuple(msum)] = [w2]
                else:
                    rmat[tuple(msum)].append(w2)
            M = max([len(val) for val in rmat.values()])
            if M < min_wc:
                min_wc = M
                chosen_word = w1
        return chosen_word
        
    def get_author(self):
        return "Anuradha"
        