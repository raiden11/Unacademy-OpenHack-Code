
import phonetics
import nltk
import jellyfish
import csv
import codecs, string

'''
Othe packages tried:
phonetics: Error, Phonetics not found
Fuzzy: No Output,
Rosetta Code: separate code for every metric
'''

weightage = {
    'soundex': 0.2,
    'metaphone': 0.4,
    'nysiis': 0.3,
    'match_rating_codex': 0.1
} 


def detect_language(character):
    
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return 'hindi'


def phonetic_similarity(word1, word2):

    encoding_1 = {}
    encoding_2 = {}
    algorithm_similarity_score = {}
    cumulative_score = 0
    
    encoding_1['metaphone'] = jellyfish.metaphone(word1)
    encoding_1['nysiis'] = jellyfish.nysiis(word1)
    encoding_1['soundex'] = jellyfish.soundex(word1)
    encoding_1['match_rating_codex'] = jellyfish.match_rating_codex(word1)

    encoding_2['metaphone'] = jellyfish.metaphone(word2)
    encoding_2['nysiis'] = jellyfish.nysiis(word2)
    encoding_2['soundex'] = jellyfish.soundex(word2)
    encoding_2['match_rating_codex'] = jellyfish.match_rating_codex(word2)

    for algorithm in encoding_1.keys():
        algorithm_similarity_score[algorithm] = jellyfish.levenshtein_distance(encoding_1[algorithm], encoding_2[algorithm]) * weightage[algorithm]
        cumulative_score += algorithm_similarity_score[algorithm]
        
    return cumulative_score     


def manual_testing():

    array1 = ['rome', 'rooman', 'noman', 'roma', 'ruman', 'ayush', 'rom', 'roman']
    array = ['kerela', 'sani', 'suni', 'sini', 'sini', 'gini', 'pop', 'dtu', 'meta', 'roman', 'honest', 'khan', 'maths', 'oligopoly', 'pension']
    array2 = ['tion', 'sion', 'tin']

    for word in array:
        print(word, phonetic_similarity(word, 'kerala'))



def match_educators_names():

    first_names = []
    last_names = []
    rows = []
    
    """
    A total of 91157 rows are there in the dataset
    Unique first names: 4806
    Unique last names: 3915
    """

    filename = "edu_names.csv"
    
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            rows.append(row)
    
    i = 0
    for row in range(1, len(rows)):

        i+=1
        if ord(rows[row][0][0]) <= 1000:
            first_names.append(rows[row][0])
        if len(rows[row][1]) > 0 and ord(rows[row][1][0]) <= 1000:
            last_names.append(rows[row][1])

    
    first_names = list(set(first_names))    
    last_names = list(set(last_names))


    # Good results for shefali, anoop, puja, ayussh, piyush, khusboo, gouri
    fields = ['First Name', 'Similar First Names']
    with open('phonetically_similar_first_names.csv', 'w') as csvfile:
        
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        for name in first_names:
            
            row = []
            row.append(name)
            for dname in first_names:
                if dname != name and phonetic_similarity(dname, name) <= 0.3:  # modifiable
                    row.append(dname)

            if len(row) > 1:
                csvwriter.writerow(row)


    # good results on rathore, agarwal, choudhary, chauhan, parashar, bhadauria, krishan, datta 
    fields = ['Last Name', 'Similar Last Names']
    with open('phonetically_similar_last_names.csv', 'w') as csvfile:
        
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        for name in last_names:
            
            row = []
            row.append(name)
            for dname in last_names:
                if dname != name and phonetic_similarity(dname, name) <= 0.3:  # modifiable
                    row.append(dname)

            if len(row) > 1:
                csvwriter.writerow(row)


match_educator_names()









