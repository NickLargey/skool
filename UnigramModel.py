import pprint
import collections
from collections import Counter
import pandas as pd
import math
import os
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')

pp = pprint.PrettyPrinter()
stop_words = set(stopwords.words('english'))

punctuation_except_apostrophe = string.punctuation.replace("'", "")
pattern = f"[{re.escape(punctuation_except_apostrophe)}]"

def read_files_in_directory(directory_path):
    dic_term_frequency = collections.Counter()

    for file in os.listdir(directory_path):
        with open(directory_path + file, 'r') as rfile:
            for line in rfile:
                current_line = line.strip()
                current_line = current_line.lower()
                current_line = re.sub(pattern, '', current_line)
                tokens = word_tokenize(current_line)
                
                filtered_sentence = [w for w in tokens if not w in stop_words]
                dic_term_frequency.update(filtered_sentence)
                # for token in filtered_sentence:
                #     if token in dic_term_frequency:
                #         dic_term_frequency[token] += 1
                #     else:
                #         dic_term_frequency[token] = 1
    return dic_term_frequency


def freq_to_prob(dic_term_frequency):
    total_tokens = dic_term_frequency.total() + len(dic_term_frequency)
    dic_term_prob = {word: count / total_tokens for word, count in dic_term_frequency.items()}
    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0
    s_text = word_tokenize(input_text)
    filtered_sentence = [w.lower() for w in s_text if not w.lower() in stop_words]
    for word in filtered_sentence:
        if word in dic_term_prob:
            prob += math.log(dic_term_prob[word])
        else:
            prob += math.log(1/len(dic_term_prob))      
    return math.exp(prob)


def main():
    freq_dict = {}
    prob = {}
    for root, dirs, files in os.walk('./TM_CA1_Lyrics/'):
        for dir in dirs:
            freq_dict[dir] = read_files_in_directory(root + dir + '/')
            prob[dir] = freq_to_prob(freq_dict[dir]) 


    df = pd.read_csv("./test.tsv", sep='\t')

    for i in range(len(df)):
        prob_dict = {}
        for genre in prob:
            p = calculate_probability(prob[genre], df["Text"].iloc[i])
            prob_dict[genre] = p 

        # Find the genre with the maximum probability
        max_genre = max(prob_dict, key=prob_dict.get)
        max_value = prob_dict[max_genre]

        # Print the maximum value and its corresponding true value from the DataFrame
        print(f'Song # {i + 1}')    
        print(f"Max Probability Genre: {max_genre} with probability {max_value}")
        print(f"True Genre: {df['Genre'].iloc[i]}")
        sorted_dict = collections.OrderedDict(
            sorted(prob_dict.items()))
        pp.pprint(sorted_dict)
        print('\n')     


if __name__ == '__main__':
    main()
