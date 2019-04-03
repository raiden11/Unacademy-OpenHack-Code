import csv
import enchant
import re
from collections import Counter
from utils import cleanse


acronyms_list = set()
def detect_acronyms(document):

	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~+1234567890'''
	for letter in document:
		if letter in punctuations: 
			document = document.replace(letter, "")
	
	acronyms_found = 0
	words = document.split(' ')
	for word in words:
		if isAcronym(word):
			acronyms_list.add(word)
			acronyms_found += 1
	

def detect_from_file():

	#inefficient
	with open('abbreviation_data_set.csv') as csvfile:
		
		rows = []
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			rows.append(row)
			detect_acronyms(row[0])
		# english_words = enchant.Dict("en_US")
		# for word in acronyms_list:
		# 	if english_words.check(word):
		# 		print(word)
		

def find_expansion():

	file = open("abbreviations.txt", "r")

	abbreviations = []
	reduced_abbreviations = []
	all_initials = []

	# stripping newline and end dot
	for line in file:
		line = line.rstrip()
		if line[-1] == '.':
			line = line[:-1]
		abbreviations.append(line)

	# removing duplicate words without dot
	# could be made more efficient
	for acronym in abbreviations:
		flag = 0
		for dacronym in abbreviations:
			if "." in dacronym and not "." in acronym and dacronym.replace(".", "")  == acronym:
				flag = 1
		if flag == 0:
			reduced_abbreviations.append(acronym)


	# reduced_abbreviations = ['UPSC']
	# removing redundancy
	reduced_abbreviations = list(set(reduced_abbreviations))
	reduced_abbreviations.sort()


	# Tokenise into initials
	for word in reduced_abbreviations:
		initials = []
		i = 0
		while i < len(word):
			if word[i] == '.':
				i += 1
			
			if i + 1 < len(word) and word[i+1].islower():
				initials.append(str(word[i] + word[i+1]))
				i+=2
			
			else:
				initials.append(word[i])
				i += 1
		all_initials.append(initials)
	

	# remove punctuations
	with open('abbreviation_data_set.csv') as csvfile:
		
		descriptions = []
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			if len(row) > 1:
				descriptions.append(cleanse(row[1]))
	
	
	counter = 0
	# all_initials = [['I', 'I', 'T'], ['I', 'T'], ['H', 'I', 'I']]
	# descriptions = ["hey indian institute technology and i i t science"]
	fields = ['Abbreviation', 'Expansions']
	with open('extracted_acronyms.csv', 'w') as csvfile:

		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields)

		for initials in all_initials:
			
			row = []
			m = len(initials)
			matchings = []
			for description in descriptions:
				words = description.split(' ')
				n = len(words)
				for k in range(0, n - m + 1):
					i = 0
					j = k
					for j in range(k, k + m):
						if len(initials[i]) == 1:
							if words[j][0] == initials[i][0].lower():
								i += 1
							else:
								break
						else:
							if len(words[j]) > 1 and words[j][0] == initials[i][0].lower() and words[j][1] == initials[i][1]:
								i += 1
							else:
								break
						if i == m:
							matching = []
							x = 0
							while x < m:
								matching.append(words[k + x])
								x += 1
							
							matchings.append(matching)
							
			
			for matching in matchings:
				str1 = ' '.join(matching)
				row.append(str1)

			cnt = Counter(row)
			added = 0 
			row = []
			row.append(reduced_abbreviations[counter])
			for tup in cnt.most_common():
				row.append(tup[0])
				added += 1
				if added > 20:
					break

			csvwriter.writerow(row)
			counter += 1			
			print(counter)

find_expansion()






























