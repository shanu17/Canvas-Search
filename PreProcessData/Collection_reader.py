import re
import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class Collection_reader:

    def __init__(self):
        # 1. Open the file in Path.DataTextDir.
        #global file pointer of the text type input file with pointer repeatedly accessed in next function.
        global file, id_counter
        id_counter = 0
        file = open(Path.DataDir, 'r')
                     
    def nextDocument(self):

        # # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # # 2. When no document left, return null, and close the file.
        docNo = ""
        content = ""
        global file, id_counter
        global current_document
        #variable to store one document which will be returned during current function call.
        current_document = ""

        #variable to check the end of one document.
        end = re.compile(r'</START_TAG>')
        count = 0

        #loop over the whole text file which is broken when file ends
        while True:
            #read one line of the file
            line = file.readline()
            # print(line)

            #check whether this line is not the end of file
            if not line:
                file_not_finished=False
                file.close()
                return None
                break
            #add this line to the current document
            current_document+=line

            #if this line is </DOC> type then extract DOC Number and Content and return the data.
            if end.search(line):
                # print(c)
                

                startbody = current_document.find("<START_TAG>") + len("<START_TAG>")
                endbody = current_document.find("</START_TAG >")
                content = current_document[startbody:endbody]
               
                current_document=""
                count+=1
                id_counter +=1
                return [str(id_counter), content]
        
        return [docNo, content]
