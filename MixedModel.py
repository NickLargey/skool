import pprint
import collections
import math
import os
import re
import string
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')

pp = pprint.PrettyPrinter()
stop_words = set(stopwords.words('english'))
punct_pattern = re.escape(string.punctuation)
split_casing = r'([a-z])([A-Z])'


def read_files_in_directory(directory_path):
    dic_term_frequency = {}
    dic_pairs_frequency = {}
    val_df = pd.DataFrame(columns=["Text", "Genre"])
    f_count = math.floor(len(directory_path)*0.9)
    index = 0
    for file in os.listdir(directory_path):
        if index <= f_count:
            with open(directory_path + file, 'r') as rfile:
                for line in rfile:
                    current_line = line.strip()
                    current_line = current_line.lower()
                    current_line = re.sub(f'[{punct_pattern}]', '', current_line)
                    tokens = word_tokenize(current_line)
                    filtered_sentence = [
                        w for w in tokens if not w in stop_words]

                    for token in filtered_sentence:
                        if token in dic_term_frequency:
                            dic_term_frequency[token] += 1
                        else:
                            dic_term_frequency[token] = 1

                    for t in range(len(filtered_sentence) - 1):
                        b_index = (
                            filtered_sentence[t], filtered_sentence[t+1])
                        if b_index in dic_pairs_frequency:
                            dic_pairs_frequency[b_index] += 1
                        else:
                            dic_pairs_frequency[b_index] = 1
            index += 1
        else:
            with open(directory_path + file, 'r') as f:
                r_text = f.read()
                text = re.sub('\s', ' ', r_text)
                text = text.strip()
                text = text.lower()
                text = re.sub(f'[{punct_pattern}]', '', text)
                tokens = word_tokenize(text)
                filtered_sentence = [
                    w for w in tokens if not w in stop_words]
                dir = directory_path.split('/')[-2]
                new_row = pd.DataFrame({'Text': [text], 'Genre': [dir]})

                val_df = pd.concat([val_df, new_row], ignore_index=True)
                index += 1

    return dic_term_frequency, dic_pairs_frequency, val_df


def freq_to_prob(dic_term_frequency, dic_pairs_frequency):
    total_tokens = sum(dic_term_frequency.values()) + len(dic_term_frequency)
    dic_term_prob = {word: count / total_tokens for word,
                     count in dic_term_frequency.items()}

    total_pairs = sum(dic_pairs_frequency.values()) + len(dic_pairs_frequency)
    dic_pairs_prob = {pair: count / total_pairs for pair,
                      count in dic_pairs_frequency.items()}
    return dic_term_prob, dic_pairs_prob


def calculate_probability(dic_term_prob, input_text, mode):
    prob = 0.0
    text = re.sub('\s', ' ', input_text)
    text = re.sub(split_casing, r'\1 \2', text)
    text = text.strip()
    text = text.lower()
    s_text = re.sub(f'[{punct_pattern}]', '', text)
                
    if mode == 'uni':
        s_text = word_tokenize(s_text)
        filtered_sentence = [w.lower()
                             for w in s_text if not w.lower() in stop_words]
    elif mode == 'bi':
        s_text = word_tokenize(s_text)
        filtered_sentence = [w.lower()
                             for w in s_text if not w.lower() in stop_words]
        filtered_sentence = [(filtered_sentence[i], filtered_sentence[i+1])
                             for i in range(len(filtered_sentence) - 1)]
    else:
        raise ValueError('Invalid mode')

    for word in filtered_sentence:
        if word in dic_term_prob.keys():
            prob += math.log(dic_term_prob[word])
        else:
            prob += 1/math.log(len(dic_term_prob))
    return prob


def mixed_model(u_prob_dict, b_prob_dict, test_df, genres):
    greek_lambda = 1
    prob_dict = {}
    best_lambda = 0
    best_tp_cnt = 0
    best_res_df = pd.DataFrame()

    while greek_lambda >= 0:
        res_df = pd.DataFrame(
            columns=["Predicted", "True"])
        curr_tp_cnt = 0
        for i in range(len(test_df)):
            for genre in genres:
                unigram = calculate_probability(
                    u_prob_dict[genre], test_df["Text"].iloc[i], mode='uni')
                bigram = calculate_probability(
                    b_prob_dict[genre], test_df["Text"].iloc[i], mode='bi')

                p = greek_lambda * unigram + (1 - greek_lambda) * bigram
                prob_dict[genre] = p

            max_genre = max(prob_dict, key=prob_dict.get)
            true_genre = test_df['Genre'].iloc[i]

            if max_genre == true_genre:
                curr_tp_cnt += 1
            res_df = pd.concat([res_df, pd.DataFrame(
                {'Predicted': [max_genre], 'True': [true_genre]})], ignore_index=True)

        # print(f'Lambda: {greek_lambda:.3f}, Current True Positive Count: {curr_tp_cnt}, Best True Positive Count: {best_tp_cnt}')
        if curr_tp_cnt > best_tp_cnt:
            best_tp_cnt = curr_tp_cnt
            best_lambda = greek_lambda
            best_res_df = pd.concat(
                [test_df, pd.DataFrame(res_df['Predicted'])], axis=1)
        
        greek_lambda -= 0.01
    
    print(f'Best Lambda: {best_lambda} \n')
    print(best_res_df, '\n')
    confusion_matrix(best_res_df, genres)
    f1_scores, f1 = f1_score(best_res_df, genres)
    print(f'F1 Scores: {f1_scores}')
    print(f'Average F1 Score: {f1}')


def confusion_matrix(c_list, genres):
    c_matrix = pd.DataFrame(0, index=genres, columns=genres)

    for i in range(len(c_list)):
        c_matrix.loc[c_list['Genre'].iloc[i], c_list['Predicted'].iloc[i]] += 1

    print("Confusion Matrix: \n", c_matrix, '\n')

# Precision = instances correctly classified for a class/all instances both true and false called out by the model
# Recall = instances correctly classified for a class/all instances that truly belong to the class
def f1_score(df, genres):
    genres = genres
    f1_scores = {}
    macro_f1 = 0
    for genre in genres:
        # True positives: Predicted = genre and Actual = genre
        tp = len(df[(df['Predicted'] == genre) & (df['Genre'] == genre)])
        # False positives: Predicted = genre but Actual != genre
        fp = len(df[(df['Predicted'] == genre) & (df['Genre'] != genre)])
        # False negatives: Predicted != genre but Actual = genre
        fn = len(df[(df['Predicted'] != genre) & (df['Genre'] == genre)])
        # Precision and Recall
        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        # F1 Score
        f1 = 2 * (precision * recall) / (precision +
                                         recall) if (precision + recall) != 0 else 0

        f1_scores[genre] = f1
        macro_f1 += f1
    avg_f1 = macro_f1 / len(genres)    
    return f1_scores, avg_f1


def build_train_val_sets(root_path='./TM_CA1_Lyrics/'):
    freq_dict_uni = {}
    freq_dict_bi = {}
    uni_prob = {}
    bi_prob = {}

    genres = []

    validation_df = pd.DataFrame(columns=["Text", "Genre"])

    for root, dirs, files in os.walk(root_path):
        for dir in dirs:
            genres.append(str(dir))
            freq_dict_uni[dir], freq_dict_bi[dir], val_df = read_files_in_directory(
                root + dir + '/')
            validation_df = pd.concat(
                [validation_df, val_df], ignore_index=True)
            uni_prob[dir], bi_prob[dir] = freq_to_prob(
                freq_dict_uni[dir], freq_dict_bi[dir])

    return uni_prob, bi_prob, validation_df, genres


def main():
    uni_prob, bi_prob, validation_df, genres = build_train_val_sets(
        './TM_CA1_Lyrics/')
    df = pd.read_csv("./test.tsv", sep='\t')
    # replace validation_df with df to test
    mixed_model(uni_prob, bi_prob, validation_df, genres)


if __name__ == '__main__':
    main()
