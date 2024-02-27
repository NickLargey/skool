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
  for file in os.listdir(directory_path):
    with open(directory_path + file, 'r') as rfile:
      for line in rfile:
        current_line = line.strip()
        current_line = current_line.lower()
        current_line = re.sub(punct_pattern, '', current_line)
        tokens = word_tokenize(current_line)          
        filtered_sentence = [w for w in tokens if not w in stop_words]

        for token in filtered_sentence:
          if token in dic_term_frequency:
            dic_term_frequency[token] += 1
          else:
            dic_term_frequency[token] = 1

        for t in range(len(filtered_sentence) - 1):
          b_index = (filtered_sentence[t], filtered_sentence[t+1])
          if b_index in dic_pairs_frequency:
            dic_pairs_frequency[b_index] += 1
          else:  
            dic_pairs_frequency[b_index] = 1


  return dic_term_frequency, dic_pairs_frequency


def freq_to_prob(dic_term_frequency, dic_pairs_frequency):
  total_tokens = sum(dic_term_frequency.values()) + len(dic_term_frequency)
  dic_term_prob = {word: count / total_tokens for word, count in dic_term_frequency.items()}
  
  total_pairs = sum(dic_pairs_frequency.values()) + len(dic_pairs_frequency)
  dic_pairs_prob = {pair: count / total_pairs for pair, count in dic_pairs_frequency.items()}
  
  return dic_term_prob, dic_pairs_prob



def calculate_probability(dic_term_prob, input_text):
    prob = 0.0
    s_text = word_tokenize(input_text)
    text = re.sub('\s', ' ', input_text)
    text = re.sub(split_casing, r'\1 \2', text)
    text = text.strip()
    text = text.lower()
    s_text = re.sub(f'[{punct_pattern}]', '', text)
    s_text = word_tokenize(s_text)

    filtered_sentence = [w.lower() for w in s_text if not w.lower() in stop_words]
    filtered_sentence = [(filtered_sentence[i], filtered_sentence[i+1]) for i in range(len(filtered_sentence) - 1)]

    for word in filtered_sentence:
        if word in dic_term_prob.keys():
            prob += math.log(dic_term_prob[word])
        else:
            prob += 1/math.log(len(dic_term_prob))  
    return prob

def run_model(p_dict, df, genres):
    res_df = pd.DataFrame(columns=["Predicted"])
    for i in range(len(df)):
        prob_dict = {}
        for genre in p_dict:
            p = calculate_probability(p_dict[genre], df["Text"].iloc[i])
            prob_dict[genre] = p 

        max_genre = max(prob_dict, key=prob_dict.get) # Find the genre with the maximum probability
        max_value = prob_dict[max_genre]

        pred = pd.DataFrame({"Predicted": [max_genre]})
        res_df = pd.concat([res_df, pred], ignore_index=True)

        # Print the maximum value and its corresponding true value from the DataFrame
        print(f'Song # {i + 1}')    
        print(f"Max Probability Genre: {max_genre} with probability {max_value}")
        print(f"True Genre: {df['Genre'].iloc[i]}")
        
        sorted_dict = collections.OrderedDict(
            sorted(prob_dict.items()))
        pp.pprint(sorted_dict)
        print('\n') 

    best_res_df = pd.concat(
            [df, res_df], axis=1)
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


def main():
    freq_dict_uni  = {}
    freq_dict_bi = {}
    uni_prob = {}
    bi_prob = {}
    genres = []
    for root, dirs, files in os.walk('./TM_CA1_Lyrics/'):
        for dir in dirs:
            genres.append(str(dir))
            freq_dict_uni[dir], freq_dict_bi[dir] = read_files_in_directory(root + dir + '/')
            uni_prob[dir], bi_prob[dir] = freq_to_prob(freq_dict_uni[dir], freq_dict_bi[dir])

    df = pd.read_csv("./test.tsv", sep='\t')

    run_model(bi_prob, df, genres) 
    


if __name__ == '__main__':
    main()