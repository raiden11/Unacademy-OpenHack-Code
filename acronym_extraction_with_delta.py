import csv
import enchant
import re
from collections import Counter
from utils import cleanse
from nltk import ngrams
from abbreviation_extraction_develop.abbreviations import schwartz_hearst


def most_frequent_abbreviations():

	with open("most_frequent_abbreviations.csv", "r") as csvfile:

		abbreviations = []
		readCSV = csv.reader(csvfile, delimiter = ',')
		for row in readCSV:
			abbreviations.append(row[0])
		
	abbreviations[2] = 'MCQ'
	abbreviations[12] = 'PYQ'
	
	return abbreviations


def match(a, b):

	if len(a) == 1:
		if b[0].lower() == a[0].lower():
			return True
	elif len(a) == 2:
		if len(b) >= 2 and b[0].lower() == a[0].lower and b[1].lower() == a[1].lower():
			return True
	return False


def preprocess_abbreviations(reduced_abbreviations):

	all_initials = []
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

		initials_1 = []
		for initial in initials:
			initials_1.append(initial.lower())
		
		all_initials.append(initials_1)

	return all_initials


def preprocess_descriptions():

	with open('abbreviation_data_set.csv') as csvfile:
		
		descriptions = []
		names = []
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			if len(row) > 1:
				descriptions.append(cleanse(row[1]))
			names.append(cleanse(row[0]))

	return descriptions, names


def find_proximal_expansion(all_initials, descriptions, names, threshold):

	index = 0
	# print(all_initials[2])
	abbrevation_expansions = {}
	for initials in all_initials:

		index += 1
		m = len(initials)
		abbreviation = ''.join(initials)
		abbrevation_expansions[abbreviation] = []
		matchings = []
		print(index, abbreviation)

		regex = '^' + '.* '.join(initials) + '.*$'
		r = re.compile(regex)
		matchings = []

		for delta in range(0, threshold + 1):
			if len(matchings) > 0:
				break
			
			for description in descriptions:
			
				n = m + delta
				grams = ngrams(description.split(), n)

				for gram in grams:
					flag = 0
					if abbreviation in gram:
						continue

					for word in gram:
						if word.startswith(abbreviation):
							flag = 1
							break
					if flag == 1:
						continue

					pattern = ' '.join(gram)
					if r.match(pattern):
						matchings.append(pattern)

			for name in names:
			
				n = m + delta
				grams = ngrams(name.split(), n)

				for gram in grams:
					flag = 0
					if abbreviation in gram:
						continue

					for word in gram:
						if word.startswith(abbreviation):
							flag = 1
							break
					if flag == 1:
						continue

					pattern = ' '.join(gram)
					if r.match(pattern):
						matchings.append(pattern)

		frequent_matchings = Counter(matchings)
		i = 0
		for matching in frequent_matchings.most_common():
			abbrevation_expansions[abbreviation].append(matching[0])
			i += 1
			if i == 5:
				break
		
		# print(idxx)	
	return abbrevation_expansions


def merge_results(threshold):
	
	frequent_abbreviations = most_frequent_abbreviations()
	all_initials = preprocess_abbreviations(frequent_abbreviations)
	descriptions, names = preprocess_descriptions()
	abbreviation_expansions = find_proximal_expansion(all_initials, descriptions, names, threshold)
	schwartz_hearst_abbreviation_expansions = schwartz_hearst.extract_abbreviation_definition_pairs('./abbreviation_data_set.csv')
	
	fields = ['Acronym', 'Expansions']	
	with open("final_merged_abbreviations.csv", "w") as csvfile:

		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields)				
		merged_abbreviations = {}

		for pairs in schwartz_hearst_abbreviation_expansions.keys():

			merged_abbreviations[pairs] = []
			merged_abbreviations[pairs].append(schwartz_hearst_abbreviation_expansions[pairs])

		for abbreviation in frequent_abbreviations:
			if abbreviation in merged_abbreviations:
			
				left = 3
				if abbreviation.lower() in abbreviation_expansions:
					for word in abbreviation_expansions[abbreviation.lower()]:
						if word.lower() == merged_abbreviations[abbreviation][0].lower():
							continue
						left -= 1
						merged_abbreviations[abbreviation].append(word)
						if left == 0:
							break

			else:
				left = 4
				merged_abbreviations[abbreviation] = []
				if abbreviation.lower() in abbreviation_expansions:
					for word in abbreviation_expansions[abbreviation.lower()]:
						left -= 1
						merged_abbreviations[abbreviation].append(word)
						if left == 0:
							break

		for key in merged_abbreviations.keys():
			row = []
			row.append(key)
			for word in merged_abbreviations[key]:
				row.append(word)
			csvwriter.writerow(row)

		# for abbreviation in frequent_abbreviations:
		# 	row = []
		# 	row.append(abbreviation)
		# 	abbreviation = abbreviation.lower()
		# 	left = 3
		# 	if abbreviation in schwartz_hearst_abbreviation_expansions:
		# 		row.append(schwartz_hearst_abbreviation_expansions[abbreviation])
		# 		left = 2
		# 		for word in abbreviation_expansions[abbreviation]:
		# 			if word != schwartz_hearst_abbreviation_expansions[abbreviation]:
		# 				row.append(word)
		# 				left -= 1
		# 			if left == 0:
		# 				break

		# 	else:
		# 		left = 3
		# 		for word in abbreviation_expansions[abbreviation]:
		# 			row.append(word)
		# 			left -= 1
		# 			if left == 0:
		# 				break
		# 	print(row)
		# 	csvwriter.writerow(row)


merge_results(1)
# Correct:
# HRM: Human Resource Management
# NTSE: 
# OOP:
# TOM:
# IELTS:
# HTML:
# RRB:
# PYQ:
# UPPSC:
# TNPSC:
# RPSC:
# JEE:
# MCQ:
# MCQs
# CGL:
# AFCAT: Only once
# KVS:
# DBMS:
# JPSC:
# HR: Highly Recommended, Human resource, Human Rights, Hindin Reasoning
# EE: Entrance exams
# MPTET:
# RC: Reading Comprehension, Revision Course
# GK: general Knowledge
# PHP: Progression harmonic Progression
# WBPSC:
# CLAT:
# KPSC:
# GPSC:
# DNA:
# SQL:
# PPSC:
# GRE:
# LIC: Learn Important Concepts
# MCQS:
# SNAP:
# STL:
# SOT:
# P&C:
# sin 
# tan
# cos
# EMI:
# JIPMER:
# A.P
# GP
# JAM
# G.D.
# ZP: Zila Parishad
# I/O: Input-Output
# op-amp: operational amplifier


# Failed at :
# CTET
# AFCAT
# 60 minutes
# IIT
# TET
# B-School
# stem: statement



























