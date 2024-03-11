from collections import Counter
import os
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')


def read_files_in_directory(directory_path):
    # key: tokens value: their frequency in all songs belonging to a genre
    dic_term_frequency = Counter()

    for file in os.listdir(directory_path):
        with open(os.path.join(directory_path, file), 'r') as rfile:
            for line in rfile:
                current_line = line.strip()
                # pre-process each line if you want to and save the results in current_line
                # Example preprocessing: lowercasing
                current_line = current_line.lower()

                tokens = word_tokenize(current_line)
                # process the tokens and update your dictionary
                dic_term_frequency.update(tokens)

    return dic_term_frequency


def freq_to_prob(dic_term_frequency):
    dic_term_prob = {}
    total_count = sum(dic_term_frequency.values())
    for token, freq in dic_term_frequency.items():
        dic_term_prob[token] = freq / total_count

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 1.0
    tokens = word_tokenize(input_text.lower())
    for token in tokens:
        # Assign a small probability for unknown words
        prob *= dic_term_prob.get(token, 0)

    return prob


def main():
    directory_path = 'path/to/your/directory'
    dic_term_frequency = read_files_in_directory(directory_path)
    dic_term_prob = freq_to_prob(dic_term_frequency)

    input_text = "example text"
    probability = calculate_probability(dic_term_prob, input_text)
    print(f"Probability of the text '{input_text}': {probability}")


if __name__ == "__main__":
    main()
