from WordleAI import WordleAI
from Helper_Functions import *

class Greedy_min_max(WordleAI):

    def __init__(self, words):
        super().__init__(words)
        self.IG = IG_Calc(self.words)        
        self.word_IG_dict = Calc_Word_IG(self.words,self.IG)
        
    def guess(self, guess_history): 
        next_p_words = self.words
    
        if len(guess_history) == 0:
            res_word = list(self.word_IG_dict.keys())
            res_word.sort(reverse=True)
            list_w= [self.word_IG_dict[res_word[0]]]
            return list_w[0]
        else:
            #fetched the last gussed word
            length = len(guess_history)
            self.last_word = (guess_history[length-1])[0]
            #check based on responce given if the last word can be obtained
            responce =[]
            for en in guess_history:
                word1 = en[0]
                matrix = {}
                responce =[]
                r = [0,1,2,3,4]
                for i in r:
                    if en[1][i] == LetterInformation.CORRECT:
                        responce.append(2)
                    elif en[1][i] == LetterInformation.PRESENT:
                        responce.append(1)
                    else:
                        responce.append(0)
                for word2 in next_p_words:
                    word2 = word2.strip()
                    vector = calculate_response(word1,word2)
                    if tuple(vector) not in matrix:
                        matrix[tuple(vector)] = [word2]
                    else:
                        matrix[tuple(vector)].append(word2)
                next_p_words = matrix[tuple(responce)]
                    
            #fetch the possible next words metrix
            if len(next_p_words) == 1:
                return next_p_words[0]
            list_w = remaining_options(self.words, guess_history)
        minimum_wc = 100000
        next_word = ""
        for word1 in list_w:
            word1 = word1.strip()
            matrix = {}
            for word2 in next_p_words:
                word2 = word2.strip()
                vector = calculate_response(word1,word2)
                if tuple(vector) not in matrix:
                    matrix[tuple(vector)] = [word2]
                else:
                    matrix[tuple(vector)].append(word2)
            Max = max([len(val) for val in matrix.values()])
            if Max < minimum_wc:
                minimum_wc = Max
                next_word = word1
        return next_word
        
    def get_author(self):
        return "Anuradha"
        