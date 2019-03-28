from nltk.corpus import wordnet
import operator
import csv
from itertools import chain

"""
Alternatives of Wordnet:
PyWordNet
ConceptNet
Some dataset trained on educational words only
"""

# generate all unique synonyms
def generate_synonyms(word):

	synonyms = []
	for syn in wordnet.synsets(word):
		for l in syn.lemmas():
			if l.name() != word:
				synonyms.append(l.name())

	return list(set(synonyms))


def generate_antonyms(word):

	antonyms = []
	for syn in wordnet.synsets(word):
		for l in syn.lemmas():
			if l.antonyms():
				antonyms.append(l.antonyms()[0].name())
				# might run a loop on all antonyms intead of taking only one


# find synonymity score between 0 and 1 
def find_similarty_score(syn_name_1, syn_name_2):

	w1 = wordnet.synset(syn_name_1)
	w2 = wordnet.synset(syn_name_2)
	return w2.wup_similarity(w1)


# More hyponym of chemistry is electrochemistry & photochemistry
def generate_hyponyms(word):

	hyponyms = []
	for synset in wordnet.synsets(word):
		for sub_synset in wordnet.synset(synset.name()).hyponyms():
			hyponyms.append(sub_synset.name())
	return hyponyms

# hypernym of chemistry is natural science
def generate_hypernyms(word):

	hypernyms = []
	for synset in wordnet.synsets(word):
		for sub_synset in wordnet.synset(synset.name()).hypernyms():
			hypernyms.append(sub_synset.name())
	return hypernyms


unique_words = set()
frequency_count = {}
def main():

	# assuming word is a proper noun or a number or a spelling error if not found in wordnet

	data = open('test_data.txt')
	unfound = []
	words_count = 0
	all_rows = {}

	for line in data:
		
		words = line.split()
		for word in words:

			if wordnet.synsets(word):
				# taking first meaning of every word
				if word not in unique_words:
					
					unique_words.add(word)
					row = []
					words_count += 1
					synonyms = generate_synonyms(word)
					
					for synonym in synonyms:
						row.append(synonym)
					all_rows[word] = row

			else:
				unfound.append(word)
				"""
				Comments: 
				Search why 'and', '&', 'of', '-' are coming in the list
				Resolve for misstyped words like "thermodynamics
				Year numbers and range like 2018, 2016, 1927-56 are also coming
				"""

			# counts frequency of every word
			if word in unique_words:
				if word not in frequency_count:
					frequency_count[word] = 1
				else:
					frequency_count[word] += 1
	
	# print(all_rows)
	sorted_frequency_count = sorted(frequency_count.items(), key=operator.itemgetter(1))
	sorted_frequency_count.reverse()

	# write in general csvfile
	fields = ['Words', 'Synonyms']
	with open('synonyms_generated_general.csv', 'w') as csvfile:
		
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields)

		for i in range(0, len(sorted_frequency_count)):
			if len(all_rows[sorted_frequency_count[i][0]]) == 0:
				continue
			
			row = []
			row.append(sorted_frequency_count[i][0])
			for word in all_rows[sorted_frequency_count[i][0]]:
				row.append(word)

			csvwriter.writerow(row)

		# 
		# for root_word in all_rows:
		# 	row = []
		# 	row.append(root_word)
		# 	for word in all_rows[root_word]:
		# 		row.append(word)

		# 	csvwriter.writerow(row)	




	# for i in range(0, 30):
	# 	print(sorted_frequency_count[i][0])
	# 	for word in all_rows[sorted_frequency_count[i][0]]:
	# 		if word in unique_words:
	# 			print(word, end = ', ')
	# 	print('\n')


main()
print(generate_hyponyms('chemistry'))







