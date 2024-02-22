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
nltk.download('stopwords')
nltk.download('punkt')

pp = pprint.PrettyPrinter()
stop_words = set(stopwords.words('english'))

punctuation_except_apostrophe = string.punctuation.replace("'", "")
pattern = f"[{re.escape(punctuation_except_apostrophe)}]"

def read_files_in_directory(directory_path):
  dic_term_frequency = {}
  dic_pairs_frequency = {}
  for file in os.listdir(directory_path):
    with open(directory_path + file, 'r') as rfile:
      for line in rfile:
        current_line = line.strip()
        current_line = current_line.lower()
        current_line = re.sub(pattern, '', current_line)
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



def calculate_probability(dic_term_prob, input_text, mode='uni'):
    prob = 0.0
    if mode == 'uni':
      s_text = word_tokenize(input_text)
      filtered_sentence = [w.lower() for w in s_text if not w.lower() in stop_words]
    if mode == 'bi':
      s_text = word_tokenize(input_text)
      filtered_sentence = [w.lower() for w in s_text if not w.lower() in stop_words]
      filtered_sentence = [(filtered_sentence[i], filtered_sentence[i+1]) for i in range(len(filtered_sentence) - 1)]
    else:
      raise ValueError('Invalid mode')
    
    for word in filtered_sentence:
        if word in dic_term_prob.keys():
            prob += math.exp(math.log10(dic_term_prob[word]))
            print(f'Found! Word: {word} Genre:{dic_term_prob[word]} Prob: {prob}')
        else:
            prob += -math.exp(math.log10(len(dic_term_prob)))
            print(f'Not Found :( Word: {word}  Prob: {prob}')      
    return prob

def run_model(p_dict, df, m):
   for i in range(len(df)):
        prob_dict = {}
        for genre in p_dict:
            p = calculate_probability(p_dict[genre], df["Text"].iloc[i], mode=m)
            prob_dict[genre] = p 
        
        max_genre = max(prob_dict, key=prob_dict.get) # Find the genre with the maximum probability
        max_value = prob_dict[max_genre]

        # Print the maximum value and its corresponding true value from the DataFrame
        print(f'Song # {i + 1}')    
        print(f"Max Probability Genre: {max_genre} with probability {max_value}")
        print(f"True Genre: {df['Genre'].iloc[i]}")
        
        sorted_dict = collections.OrderedDict(
            sorted(prob_dict.items()))
        pp.pprint(sorted_dict)
        print('\n') 

def main():
    freq_dict_uni  = {}
    freq_dict_bi = {}
    uni_prob = {}
    bi_prob = {}

    for root, dirs, files in os.walk('./TM_CA1_Lyrics/'):
        for dir in dirs:
            freq_dict_uni[dir], freq_dict_bi[dir] = read_files_in_directory(root + dir + '/')
            uni_prob[dir], bi_prob[dir] = freq_to_prob(freq_dict_uni[dir], freq_dict_bi[dir])

    df = pd.read_csv("./test.tsv", sep='\t')
   
    # run_model(uni_prob, df, mode='uni')
    run_model(bi_prob, df, 'bi') 
    

if __name__ == '__main__':
    main()