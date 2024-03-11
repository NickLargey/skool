import os
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')


# might be useful?
from collections import Counter


def read_files_in_directory(directory_path):
    # key: tokens value: their frequency in all songs belonging to a genre
    dic_term_frequency = {}
    dic_pairs_frequency = {}
    for file in os.listdir(directory_path):
        with open(directory_path + file, 'r') as rfile:
            for line in rfile:
                current_line = line.strip()
                # pre-process each line if you want to and save the results in current_line
                # YOUR CODE

                tokens = word_tokenize(current_line)
                # process the tokens and update your dictionary
                # YOUR CODE

    return dic_term_frequency, dic_pairs_frequency


def freq_to_prob(dic_term_frequency, dic_pairs_frequency):
    dic_term_prob = {}
    # YOUR CODE
    # Convert the frequencies to probabilities

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0

    return prob


def main():
    return

