import nltk
import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class WordTokenizer:

    def __init__(self, content):
        # Tokenize the input texts.

        #Declare global tokens list to store all current document tokens, number of tokens and current token number
        global tokens, length, token_num
        token_num = -1
        #generate all base tokens by splitting with space
        tokens = content.split()
        #remove punctuational tokens
        tokens = [token for token in tokens if token.isalpha()]
        length = len(tokens)
        return

    def nextWord(self):
        # Return the next word in the document.
        # Return null, if it is the end of the document.
        global token_num, tokens, length
        #increment the current token number
        token_num+=1
        #check if all tokens not returned already i.e. current document is not over
        if token_num == length:
        	return None
        #fetch current token from tokens list.
        word = tokens[token_num]
        return word