
import phonetics
import nltk
import jellyfish

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
    
array = ['rome', 'rooman', 'noman', 'roma', 'ruman', 'ayush', 'rom', 'roman']

for word in array:
    print(word, phonetic_similarity(word, 'roman'))
    


# def levenshtein(seq1, seq2):  
#     size_x = len(seq1) + 1
#     size_y = len(seq2) + 1

#     matrix = []
#     for i in range(0, size_x):
#         row = []
#         for j in range(0, size_y):
#             row.append(0)
#         matrix.append(row)
#     print(matrix)

#     for x in range(0, size_x):
#         matrix [x][0] = x
#     for y in range(0, size_y):
#         matrix [0][y] = y

#     for x in range(1, size_x):
#         for y in range(1, size_y):
#             if seq1[x-1] == seq2[y-1]:
#                 matrix [x][y] = min(
#                     matrix[x-1][y] + 1,
#                     matrix[x-1][y-1],
#                     matrix[x][y-1] + 1
#                 )
#             else:
#                 matrix [x][y] = min(
#                     matrix[x-1][y] + 1,
#                     matrix[x-1][y-1] + 1,
#                     matrix[x][y-1] + 1
#                 )
#     print(matrix)
#     return (matrix[size_x - 1][size_y - 1])





# -- initialize phonetics object

# word1 = Phonetics("Knuth")  
# word2 = Phonetics("Kant")  
# print ("Comparing %s with %s" % (word1.getText(), word2.getText()))

# # -- phonetic code
# codeList1 = word1.phoneticCode()  
# codeList2 = word2.phoneticCode()

# # -- weight
# weight = {  
#     "soundex": 0.2,
#     "caverphone": 0.2,
#     "metaphone": 0.5,
#     "nysiis": 0.1
# }

# # -- algorithms
# algorithms = ["soundex", "caverphone", "metaphone", "nysiis"]

# # -- total
# total = 0.0  
# for entry in algorithms:  
#     code1 = codeList1[entry]
#     code2 = codeList2[entry]
#     lev = levenshtein (code1, code2)
#     currentWeight = weight[entry]
#     print ("comparing %s with %s for %s (%0.2f: weight %0.2f)" % (code1, code2, entry, lev, currentWeight))
#     subtotal = lev * currentWeight
#     total += subtotal

# print ("total: %0.2f" % total)  




