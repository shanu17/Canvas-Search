import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class StopWordRemover:

    def __init__(self):
        # Load and store the stop words from the fileinputstream with appropriate data structure.
        # NT: address of stopword.txt is Path.StopwordDir.

        #creating a list to store all stopword, decalred global for easy accessing from other functions
        global stopword_list
        stopword_list = []

        #opening the stopword file
        stopword_file = open(Path.StopwordDir,'r', encoding='cp437')

        #reading all stopwords into a variable
        temp = stopword_file.readlines()
        #storing all the stopwords into a list
        stopword_list = [x.strip() for x in temp]
        # print(stopword_list)
        return

    def isStopword(self, word):
        # Return true if the input word is a stopword, or false if not.
        global stopword_list
        #accesing the global stopword list and checking if the input word is present in it. 
        if word in stopword_list:
        	return True
        return False
