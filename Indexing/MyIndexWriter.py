import Classes.Path as Path
import re
# Efficiency and memory cost should be paid with extra attention.
global type_global
global dictionary, postings, documents_count
dictionary = {}
postings = {}
documents_count=0
from array import array
class MyIndexWriter:

    def __init__(self):
        global type_global
        #declare global variable for document type for use in other functions and set value
        type_global = type
        return

    def IndexToFile(self, user):
        '''write the inverted index to the file'''
        global dictionary, postings, documents_count
        #steps to create the output index file name in the relevant data folders
        pre = ""
        pre = Path.IndexDir
        postings_filename = pre+"postings_"+user
        dictionary_filename = pre+"dictionary_"+user
        f=open(postings_filename, 'w',encoding="utf-8")
        
        #steps to iterate over the postings list, generate a string format to write it to file.
        for term in postings:
            postinglist=[]
            for p in postings[term]:
                docID=p[0]
                frequency=p[1]
                postinglist.append(':'.join([str(docID) ,str(frequency)]))
            f.write(''.join((term,'|',';'.join(postinglist)))+'\n')
            
        f.close()
        #steps to write the dictionary list to file
        f2 = open(dictionary_filename,'w',encoding="utf-8")
        for term in dictionary:
            f2.write(str(term)+':'+str(dictionary[term])+'\n')
        f2.close()


    def get_docid(self,docno):
        return int(docno)
    # This method build index for each document.
	# NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo, content):

        global dictionary, postings, documents_count

        docid = self.get_docid(docNo)
        temp_postings = {}

        terms=content.split()
        #create postings list
        for position, term in enumerate(terms):
            try:
                temp_postings[term][1]+=1
            except:
                temp_postings[term]=[docid, 1]
        #create dictionary list
        for position, term in enumerate(terms):
            try:
                dictionary[term]+=1
            except:
                dictionary[term]=1
        #merge the new postings list with pervious global postings list
        for terms in temp_postings:
            try:
                postings[terms].append(temp_postings[terms])
            except:
                postings[terms] = [temp_postings[terms]]

        documents_count+=1
        return



    # Close the index writer, and you should output all the buffered content (if any).
    def close(self, user):
        global dictionary, postings
        self.IndexToFile(user)
        dictionary = {}
        postings = {}
        return
