import Classes.Path as Path
import math
# Efficiency and memory cost should be paid with extra attention.
global type_here, postings_file, dictionary_file, fd
class MyIndexReader:

    def __init__(self, user):
        global type_here, postings_file, dictionary_file, fd
        # type_here = type
        pre = ""
        pre = Path.IndexDir
        postings_file = pre+"postings_"+user
        dictionary_file = pre+"dictionary_"+user
        fd=open(dictionary_file, 'r')

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        #same get docid function as used in indexwriter
        return int(docNo)

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        return str(docId)
        #code to convert docid to docno string for trecweb and text types
        
    def getDocLength(self,docId, user):

        #get the path and name of file to be read
        # filename = Path.ResultHM1
        #open the file for reading
        filee = open(Path.ResultHM1+"result_"+user+'.txt', 'r')
        content=0
        num_collections=0
        while True:
            d = filee.readline()
            d = d.split("\n")[0]
            if not d:
                break
            if docId == d:
                c = filee.readline()
                c = c.split("\n")[0]
                # print(c)
                return len(c.split())

        return 0

    # Return DF.
    def DocFreq(self, token):
        word_number = 0
        not_found = True
        global type_here, postings_file, dictionary_file
        fd=open(dictionary_file, 'r')
        while(not_found):
            line = fd.readline()
            if not line:
                return 0
            spl = line.split(":")
            if spl[0]==token:
                break
            word_number+=1
        fd.close()
        fp = open(postings_file, 'r')
        fp_count = 0
        line2 = ""
        while(True):
            line2 = fp.readline()
            if not line2:
                return 0
            if fp_count==word_number:
                break
            fp_count+=1
        fp.close()
        return len((line2.split('|')[1]).split(';'))
        

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        global type_here, postings_file, dictionary_file
        fd=open(dictionary_file, 'r')
        not_found = True
        while(not_found):
            line = fd.readline()
            if not line:
                break
            spl = line.split(":")
            if spl[0]==token:
                fd.close()
                return int(spl[1])
        return 0

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        word_number = 0
        not_found = True
        global type_here, postings_file, dictionary_file
        fd=open(dictionary_file, 'r')
        while(not_found):
            line = fd.readline()
            if not line:
                return {}
            spl = ((line.split("\n"))[0]).split(":")
            # print(spl)
            if spl[0]==token:
                break
            word_number+=1
        fd.close()
        fp = open(postings_file, 'r')
        fp_count = 0
        line2 = ""
        while(True):
            line2 = fp.readline()
            if not line2:
                return {}
            if fp_count==word_number:
                break
            fp_count+=1
        fp.close()
        return_dict = {}
        filtered = line2.split('\n')[0]
        frequency_list = (filtered.split('|')[1]).split(';')
        for item in frequency_list:
            split_again = item.split(':')
            doc = split_again[0]
            fre = split_again[1]
            return_dict[doc] = fre
        return return_dict
