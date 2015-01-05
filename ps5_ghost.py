import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()


def ghost(wordlist):
    word = ''
    turn = 0
    while word not in wordlist or len(word) < 4:
        if turn % 2 == 0:
            player = 1
        else:
            player = 2
        letter = input("Player %d say a letter:\n" % player)
        while letter not in string.ascii_letters:
            letter = input("Player %d say a letter:\n" % player)
        word += letter.lower()
        print(word)
        if not exists(wordlist, word):
            print("Player %d loses because no possible word exists" % player)
            return None
        turn += 1
    print("Player %d loses because %s is a word" % (player, word))
    return None


def exists(wordlist, wordfrag):
    for word in wordlist:
        if wordfrag == word[:len(wordfrag)]:
            return True
    return False
        