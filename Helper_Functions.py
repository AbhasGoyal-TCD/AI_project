import numpy as np
from WordleAI import LetterInformation
from functools import lru_cache
from WordleJudge import WordleJudge

#Constraint based filtering on returned guesses.
#Credits: OutcomeBasedAI.py To be referenced
def remaining_options(words, guess_history):
    """
    Filters a word list with all the known information.
    Returns the list of remaining options.
    """
    present = set()
    not_present = set()
    correct = set()
    present_letters = set()
    for entry in guess_history:
        
        for i in range(5):
            if entry[1][i] == LetterInformation.CORRECT:
                correct.add((entry[0][i], i))
                present_letters.add(entry[0][i])
            elif entry[1][i] == LetterInformation.PRESENT:
                present.add((entry[0][i], i))
                present_letters.add(entry[0][i])
            else:
                not_present.add(entry[0][i])

    for c in present_letters:
        words = [w for w in words if c in w]
    for c in not_present:
        words = [w for w in words if c not in w]
    for c in correct:
        words = [w for w in words if w[c[1]] == c[0]]
    for c in present:
        words = [w for w in words if w[c[1]] != c[0]]

    return words

def undisc_rem_options(words, guess_history):
    """
    Filters a word list with all the unknown information.
    Returns the list of remaining options.
    """
    letters = set()
    for entry in guess_history:
        for i in range(5):
            if entry[1][i] == LetterInformation.CORRECT:
                letters.add(entry[0][i])
            elif entry[1][i] == LetterInformation.PRESENT:
                letters.add(entry[0][i])
            else:
                letters.add(entry[0][i])
   
    for c in letters:
        words = [w for w in words if c not in w]

    return words
    
def IG_Calc(word):

    """
    Calculates the information obtained from each word by finding out the number of times a letter has appeared in the corpus at each position.
    Each word is assigned an Information gain number based on letters present
    """
    
    IG = np.zeros((26,5))
    
    Total_characters = len(word)*5
    
    for w in word:
        for index,ele in enumerate(w):
            IG[ord(ele)-97][index] += 1
    
    IG = np.divide(IG,Total_characters)
    
    return IG
    
def Calc_Word_IG(words, IG):

    """
    
    """
    word_IG_dict = {}
    occured_letter = ""
    for word in words:
    
        occured_letter = ""
        sum_IG = 0
        
        for index,ele in enumerate(word):
            if ele not in occured_letter:
                sum_IG += IG[ord(ele)-97][index]
        
        word_IG_dict[sum_IG] = word
    
    return word_IG_dict

@lru_cache(maxsize=None)
def calc_response_vector(w1,w2):
    tw2 = w2
    msum = [0 for i in range(5)]
    for c_ind in range(5):
        if w1[c_ind] == tw2[c_ind]:
            msum[c_ind] = 2
            tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
    for c_ind in range(5):
        if w1[c_ind] in tw2 and msum[c_ind] == 0:
            msum[c_ind] = 1
            ind_app = tw2.find(w1[c_ind])
            tw2 = tw2[:ind_app] + "*" + tw2[ind_app+1:]
    return msum

def Wordle_prob(words, judge):
    word_IG_dict = {}

    for word in words:
        word_IG_dict[judge.is_wordle_probability(word)] = word
        
    return word_IG_dict
    
    
@lru_cache(maxsize=None)
def calculate_response(word1,word2):
    r = [0,1,2,3,4]
    vector = []
    for i in r:
        if word1[i] == word2[i]:
            vector.append(2)
        else :
           vector.append(0) 
    for i in r:
        if word1[i] in word2 and vector[i] == 0:
            vector[i] = 1
    return vector