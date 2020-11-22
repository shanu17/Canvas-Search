import Classes.Query as Query
import Classes.Path as Path
global queries, query_ids
import re
from nltk.stem import PorterStemmer
import string

class ExtractQuery:

    def __init__(self, query):
        # 1. you should extract the 4 queries from the Path.TopicDir
        global queries, query_ids
        queries = []
        query_ids = []

        #preparing stopwords list
        stopword_list = []

        #opening the stopword file
        stopword_file = open(Path.StopwordDir,'r', encoding='cp437')

        #reading all stopwords into a variable
        temp = stopword_file.readlines()
        #storing all the stopwords into a list
        stopword_list = [x.strip() for x in temp]

        # Initialising porter stemmer
        ps = PorterStemmer()

        
        #generate all base tokens by splitting with space
        tokens = query.split()
        #remove punctuational tokens
        table = str.maketrans('', '', string.punctuation)
        tokens = [w.translate(table) for w in tokens]
        filtered_tokens = []
        #loop through the tokens of current query
        for t in tokens:
            #root for tokens which are not stopwords after converting them to lowercase
            # print(t)
            t = t.lower()
            if t not in stopword_list:
            	#stemming the token
            	stemmed_t = ps.stem(t)
            	filtered_tokens.append(stemmed_t)

        filtered_query = " ".join(filtered_tokens)


        queries = filtered_query

        # 3. you can simply pick up title only for query.
        return

    # Return extracted queries with class Query in a list.
    def getQuries(self):
        global queries, query_ids
        return_list = []
        Q = Query.Query()
        Q.setQueryContent(queries)
        Q.setTopicId("1")
        return Q

