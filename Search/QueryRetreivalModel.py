import Classes.Query as Query
import Classes.Document as Document
from heapq import heappush, heappop
import Classes.Path as Path

global collectionLength, num_collections
class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader, user):
        self.indexReader = ixReader
        # docsList = self.indexReader.searcher.doc_count()
        global collectionLength, num_collections
        collectionLength = 0 
        # for i in range(docsList):
        #     collectionLength += self.indexReader.getDocLength(i)

        global file_again
        #get the path and name of file to be read
        filename = Path.ResultHM1+"result_"+user+'.txt'
        #open the file for reading
        file_again = open(filename, 'r')
        content=0
        num_collections=0
        while True:
            d = file_again.readline()
            if not d:
                break
            d = d.split("\n")[0]
            
            if (content==1):
                collectionLength+= len(d.split())
                content=0
            else:
                num_collections+=1
                content=1



        return

    def rawScore(self, token, token_collection_freq ,token_count, document_length, collection_length, miu):
        m = int(miu)
        # print(document_length, token_count, collection_length, miu)
        score = ((document_length/(document_length+m))*(token_count/document_length)) + ((m/(document_length+m))*(token_collection_freq/collection_length));
        return score;


    def Union(self, lst1, lst2): 
        final_list = list(set().union(lst1, lst2)) 
        return final_list 
    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN, miu, names,user):

        global collectionLength
        query = query.getQueryContent()
        query_tokens = query.split()
        faulty_tokens = []


        relevant_document_ids = []
        postings_dictionary = {}
       
        # print("phase 1 done")
        tokens_not_found = 0
        #This is for handling query tokens which appear in no document and 
        #we will use this loop to also get the documents for which score will not be zero.
        # i.e. atleast one term of query appears atleast once somewhere in the document.
        for token in query_tokens:
            token_posting = self.indexReader.getPostingList(token)

            if len(token_posting) == 0:
                faulty_tokens.append(token)
                tokens_not_found +=1
                print(token, "not found in any document")


            else:
                current_ids = []
                for keys in token_posting:
                    current_ids.append(keys)
                relevant_document_ids = self.Union(relevant_document_ids,current_ids)    
                postings_dictionary[token] = token_posting

        if tokens_not_found == len(query_tokens):
            return []
        for f in faulty_tokens:
            query_tokens.remove(f)


        #This is for computing all token scores and store in the dictionary described below
        #dictionary to store score values of form {token1:{document_id:score, ...}, token2:{document_id:score],...}
        token_score_dictionary = {} 
        for t in query_tokens:
            token_score_dictionary[t] = {}
            for d in relevant_document_ids :
                token_score_dictionary[t][d] = 0.0
        # print("phase 2 done")

        count = 0
        for t in query_tokens:
            #collection frequency fetching
            token_collection_freq = self.indexReader.CollectionFreq(t)
            for d in relevant_document_ids:
                # print(d)
                #variables we need for score are seperated here
                # c(t,d)
                count_t_d = 0
                if d in postings_dictionary[t]:
                    count_t_d = int(postings_dictionary[t][d])
                #|D| calculation
                documentLength = self.indexReader.getDocLength(d, user)
                current_doc_score = self.rawScore(t , token_collection_freq, count_t_d, documentLength, collectionLength, miu)
                token_score_dictionary[t][d] =  current_doc_score
                current_doc_score = 0.0
                count+=1

        #we have the scores ready and for each query term

        # dictionary to store cummulative scores of each doc, together with that we find the best 20 scores
        final_scores = []
        #top 20 heap is declared beow
        heap = []

        for d in relevant_document_ids:
            document_query_score = 1.0
            for t in query_tokens:
                document_query_score = document_query_score*token_score_dictionary[t][d]

            final_scores.append((-document_query_score,d)) 

        # here we create a heapq object for priority queue and add all the elements.
        for item in final_scores:
            heappush(heap, item)

        return_list = []
        for i in range(topN):
            val = heappop(heap)
            result = Document.Document()
            result.setDocNo(self.indexReader.getDocNo(int(val[1])))
            result.setDocName(names[int(val[1])])
            result.setDocId(int(val[1]))
            result.setScore(-val[0])
            return_list.append(result)


        return return_list