class Document:

    def __init__(self):
        return

    docid = ""
    docno = ""
    docname = ""
    score = 0.0

    def getDocId(self):
        return self.docid

    def getDocName(self):
        return self.docname

    def getDocNo(self):
        return self.docno

    def getScore(self):
        return self.score

    def setDocId(self, docid):
        self.docid = docid

    def setDocName(self, docname):
        self.docname = docname

    def setDocNo(self, no):
        self.docno = no

    def setScore(self, the_score):
        self.score = the_score
