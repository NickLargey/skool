import pprint
import pandas as pd
import collections
import math
import os
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')


def read_files_in_directory(directory_path):
    # key: tokens value: their frequency in all songs belonging to a genre
    dic_term_frequency = {}

    for file in os.listdir(directory_path):
        with open(directory_path + file, 'r') as rfile:
            for line in rfile:
                current_line = line.strip()
                # pre-process each line if you want to and save the results in current_line
                # YOUR CODE

                tokens = word_tokenize(current_line)
                # process the tokens and update your dictionary
                for token in tokens:
                    if token in dic_term_frequency:
                        dic_term_frequency[token] += 1
                    else:
                        dic_term_frequency[token] = 1
                # dic_term_frequency.append(token)

    return dic_term_frequency


def freq_to_prob(dic_term_frequency):
    dic_term_prob = {}
    total_tokens = len(dic_term_frequency)
    for token in dic_term_frequency:
        dic_term_prob[token] = dic_term_frequency[token] / total_tokens

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0
    s_text = input_text.split()
    for word in s_text:
        if word in dic_term_prob:
            prob = math.log(dic_term_prob[word] + 1) + prob
    return prob


def main():
    pp = pprint.PrettyPrinter()
    prob_dict = {}
    for root, dirs, files in os.walk('./TM_CA1_Lyrics/'):
        for dir in dirs:
            freq_list = freq_to_prob(read_files_in_directory(root + dir + '/'))
            p = calculate_probability(
                freq_list, "If you want my future, forget my past If you wanna get with me, better make it fast Now don't go wasting my precious time")
            prob_dict[dir] = p
    sorted_dict = collections.OrderedDict(
        sorted(prob_dict.items()))
    pp.pprint(sorted_dict)


if __name__ == '__main__':
    main()
