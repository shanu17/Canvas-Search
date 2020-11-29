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
import os
import string
import json

miu = 2000
doc_to_title_dict = {}
user = sys.argv[1]
Query_string = " ".join(sys.argv[2:])

processed_file = Path.ResultHM1+'result_'+user+'.txt'
names_file = Path.FilesDictDir+'dict_'+user+'.txt'
dict_file =  Path.IndexDir+"dictionary_"+user
postings_file = Path.IndexDir+"postings_"+user

dr = open(names_file, "r", encoding='cp437')
while True:
    l = dr.readline()
    if not l:
        break
    l2 = l.split(":")
    doc_to_title_dict[int(l2[0])] = l2[1]
    pass

index = MyIndexReader.MyIndexReader(user)
search = QueryRetreivalModel.QueryRetrievalModel(index, user)
#preprocessing and indexing ends


extractor = ExtractQuery.ExtractQuery(Query_string)
#query execution starts
query= extractor.getQuries()

results = search.retrieveQuery(query, 4, miu, doc_to_title_dict, user)
rank = 1

final_json = []
if len(results)==0:
	print("[]")
else:
	for result in results: 
		item = {}
		item['query'] = query.getTopicId()
		item['docno'] = result.getDocNo()
		item['docname'] = result.getDocName().split("\n")[0]
		item['rank'] = rank
		item['score'] = result.getScore()
		rank+=1
		final_json.append(item)
	jsonData=json.dumps(final_json)
	print(jsonData)