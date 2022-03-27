import numpy as np
from WordleAI import LetterInformation

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
    
    
def IG_Calc(words):

    """
    Calculates the information obtained from each word by finding out the number of times a letter has appeared in the corpus at each position.
    Each word is assigned an Information gain number based on letters present
    """
    
    IG[26][5] = np.zeros((26,5))
    
    Total_characters = len(words)*5
    
    for word in words:
        for index,ele in enumerate(word):
            IG[ord(ele)][index] += 1
    
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
                sum_IG += IG[ord(ele)][index]
        
        word_IG_dict[sum_IG] = word
    
    return word_IG_dict