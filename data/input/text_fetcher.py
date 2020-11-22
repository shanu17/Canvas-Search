import textract
import os
import string
entries = os.listdir('files/')

text_to_file = ""
for entry in entries:
	try:
		print(entry)
		doc = textract.process('files/'+entry)
		# print(doc)
		doc = doc.decode("utf-8").split()
		# print(doc)
		remove_list = ['\x97']
		pdf = [i for i in doc if i != '\x97']

		table = str.maketrans('', '', string.punctuation)
		stripped = [w.translate(table) for w in doc]
		print(stripped)
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass
	
	
# To take input from the user
# my_str = input("Enter a string: ")

# remove punctuation from the string
# print(pdf.split())


