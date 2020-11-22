import PreProcessData.Collection_reader as Collection_reader
import PreProcessData.StopWordRemover as StopWordRemover
import PreProcessData.WordNormalizer as WordNormalizer
import PreProcessData.WordTokenizer as WordTokenizer
import Indexing.PreProcessedCorpusReader as PreprocessedCorpusReader
import Indexing.MyIndexWriter as MyIndexWriter
import Indexing.MyIndexReader as MyIndexReader
import datetime
import Classes.Path as Path
import Classes.Query as Query
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery
import sys
import textract
import os
import string

import fitz
# # option parser added by Om
# from optparse import OptionParser

# # initialise parser
# parser = OptionParser(usage="usage: %prog [options] arguments",
#                       version="%prog 0.8")

# # add the relevant required options to parser, option descriptions given in help of each option
# parser.add_option("-m", "--miu", action="store_const", const = 'miu', default=2000, dest='query', help="To set the value to the parameter µ")

#default niu value if no argument given.
miu = 2000 
# parse the arguments given form the command line
# (options, args) = parser.parse_args()

# if options.query =='miu':
#     miu = args[0]
#     print("Running miu: "+args[0])
doc_to_title_dict={}

def WriteIndex(user):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus =PreprocessedCorpusReader.PreprocessedCorpusReader(user)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter()
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1])
        count+=1
        if count%30000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close(user)
    return


def PreProcess(path, user):
    # Open the collection by type.
    
    entries = os.listdir(path)

    # Initialize essential objects.
    stopwordRemover = StopWordRemover.StopWordRemover()
    normalizer = WordNormalizer.WordNormalizer()
    wr = open(Path.ResultHM1+'result_'+user+'.txt', "w", encoding="utf8")
    dr = open(Path.FilesDictDir+'dict_'+user+'.txt', "w", encoding="utf8")
    doc = []
    
    #Process the corpus, document by document, iteratively.
    count = 0
    for entry in entries:
        try:
            file = fitz.open(path+entry)
            doc = ""
            for page in file:
                text = page.getText("text")
                doc = doc + text
            # doc = textract.process(path+entry)
            if doc == None:
                break
            doc = doc.split()
            # print(doc)
            # print(doc)
            remove_list = ['\x97']
            pdf = [i for i in doc if i != '\x97']

            table = str.maketrans('', '', string.punctuation)
            content = [w.translate(table) for w in pdf]
            doc_title = entry
            
            doc_to_title_dict[count]=doc_title
            # Output the doctitle.
            wr.write(str(count)+"\n")
            dr.write(str(count)+":"+doc_title+"\n")


            # Output the preprocessed content.
            for word in content:
                word = normalizer.lowercase(word)
                if stopwordRemover.isStopword(word) == False:
                    wr.write(normalizer.stem(word) + " ")
            wr.write("\n")
            count += 1
            print("finish " + str(count) + " docs")
            pass
        except Exception as e:
            print("document " + str(count) + " has error") 
            print(e) 
    wr.close()
    return

def run_search():
    #fetching the arguments from command line
    user = sys.argv[1]
    file_folder_path = './'+user+'/'
    processed_file = Path.ResultHM1+'result_'+user+'.txt'
    names_file = Path.FilesDictDir+'dict_'+user+'.txt'
    dict_file =  Path.IndexDir+"dictionary_"+user
    postings_file = Path.IndexDir+"postings_"+user

    if os.path.isfile(processed_file) and os.path.isfile(names_file):
        print("data already there preprocess")
        pass
    else:
        PreProcess(file_folder_path, user)
        pass
    #preprocessing and indexing starts
    if os.path.isfile(dict_file) and os.path.isfile(postings_file):
        print("data already there index")
        pass
    else:
        WriteIndex(user)
        pass
    
    return 

run_search()