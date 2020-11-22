import Classes.Path as Path
from nltk.stem import PorterStemmer 
# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class WordNormalizer:

    def __init__(self):
    	#declare a global instance of Porter Stemmer
    	global ps
    	ps = PorterStemmer()
    	return

    def lowercase(self, word):
        return word.lower()

    def stem(self, word):
    	#return the stemmed word using porter stemmer
    	return ps.stem(word)
