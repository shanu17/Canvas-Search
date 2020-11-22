import Classes.Path as Path

class PreprocessedCorpusReader:

    def __init__(self, user):
    	#declare a global file pointer
    	global file
    	#get the path and name of file to be read
    	filename = Path.ResultHM1+'result_'+user+'.txt'
    	#open the file for reading
    	file = open(filename, 'r', encoding='cp437')
    	return
    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
    	global file
    	#read a line of the file every time next Document function is called, return None id EOF.
    	docNo = file.readline()
    	if not docNo:
    		file.close()
    		return None
    	content = file.readline()
    	if not content:
    		file.close()
    		return None

    	return [docNo, content]