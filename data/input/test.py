import textract
import os

entries = os.listdir('files/')
for entry in entries:
	print(entry)

pdf = textract.process("files/1.pdf")
# ppt = textract.process("1.pptx")
# doc = textract.process("IS_2140_A1_2020.docx")

print(type(pdf))
pdf = pdf.decode("utf-8").split()
remove_list = ['\xc97']
pdf = [i for i in pdf if i != '\x97']


import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in pdf]
# print(stripped[:100])
# To take input from the user
# my_str = input("Enter a string: ")

# remove punctuation from the string
# print(pdf.split())


