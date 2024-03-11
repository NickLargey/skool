from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
import math
import os
import nltk
import numpy as np
import re
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download("stopwords")

nltk.download('punkt')


def read_files_to_dictionaries(directory_path):
    """
    This method will iterate on all the files in the input sub-directories and for each song calculates the term
    frequencies
    @param directory_path: directory path where all the directories of different genre are located
    @return: dictionary with song name as the key and the value as a dictionary (A). (A) is a dictionary with key
    representing the token and value being the frequency in the document. The second return type will give you genre for
    each song.
    """
    dic_song_term_frequency = {}
    dic_song_genre = {}
    for genre in os.listdir(directory_path):
        path = directory_path + genre
        for file in os.listdir(path):
            temp_dic = {}
            with open(path + "/" + file, 'r') as rfile:
                for line in rfile:
                    current_line = line.strip()
                    ############################
                    # pre-process each line if you want to and save the results in current_line
                    # YOUR CODE
                    ############################
                    current_line = current_line.lower()
                    current_line = re.sub(r'[!.?,;:]', '', current_line)
                    token_list = word_tokenize(current_line)
                    token_list = [
                        word for word in token_list if word not in stopwords.words('english')]
                    # token_list = [word for word in word_tokenize(
                    #     current_line) if word not in stopwords.words('english')]
                    for token in token_list:
                        # Update frequency for existing term or add a new term with frequency 1
                        temp_dic[token] = temp_dic.get(token, 0) + 1
            song_name = file.split(".")[0]
            dic_song_term_frequency[song_name] = temp_dic
            dic_song_genre[song_name] = genre
    return dic_song_term_frequency, dic_song_genre


def get_TF_values(dic_song_term_frequency):
    """
    This method takes in token frequency per song as the input and returns TF per token/song
    @param dic_song_term_frequency: song name as key and dictionary A as value. In A, keys are the tokens with their
    frequencies as the values
    @return: Dictionary with song names as keys, and TF-Values as values. These values are also a dictionary of token as
    the keys and their TFs as values
    """
    dic_tf_per_song = {}

    for song, term_frequencies in dic_song_term_frequency.items():
        total_terms_in_song = sum(term_frequencies.values())
        tf_values = {term: freq / total_terms_in_song for term,
                     freq in term_frequencies.items()}
        dic_tf_per_song[song] = tf_values

    return dic_tf_per_song

# def get_TF_values(dic_song_term_frequency):
#     """
#     This method takes in token frequency per song as the input and returns TF per token/song
#     @param dic_song_term_frequency: song name as key and dictionary A as value. In A, keys are the tokens with their
#     frequencies as the values
#     @return: Dictionary with song names as keys, and TF-Values as values. These values are also a dictionary of token as
#     the keys and their TFs as values
#     """
#     dic_tf_per_song = {}
#     for song in dic_song_term_frequency.keys():
#         dic_words = {}
#         for word in dic_song_term_frequency[song].keys():
#             tf = math.log10(1 + dic_song_term_frequency[song][word])
#             dic_words[word] = tf
#         dic_tf_per_song[song] = dic_words
#     print(dic_tf_per_song)
#     return dic_tf_per_song


def get_IDF_values(dic_song_term_frequency):
    """
    This method calculates the IDF values for each token
    @param dic_song_term_frequency: song name as key and dictionary A as value. In A, keys are the tokens with their
    frequencies as the values
    @return: Dictionary with tokens as the keys and IDF values as values
    """

    dic_idf_values = {}
    num_songs = len(dic_song_term_frequency)
    term_in_songs_count = {}

    # Count the number of songs each term appears in
    for song, terms in dic_song_term_frequency.items():
        for term in terms:
            if term not in term_in_songs_count:
                term_in_songs_count[term] = 0
            term_in_songs_count[term] += 1

    # Calculate IDF for each term
    for term, count in term_in_songs_count.items():
        dic_idf_values[term] = math.log(num_songs / count)

    return dic_idf_values


# def get_IDF_values(dic_song_term_frequency):
#     """
#     This method calculates the IDF values for each token
#     @param dic_song_term_frequency: song name as key and dictionary A as value. In A, keys are the tokens with their
#     frequencies as the values
#     @return: Dictionary with tokens as the keys and IDF values as values
#     """
#     dic_idf_values = {}
#     num_songs = len(dic_song_term_frequency.keys())

#     for song in dic_song_term_frequency:
#         ############################
#         # Put your code here and then remove 'pass'
#         # YOUR CODE
#         ############################
#         pass

#     for term in dic_idf_values:
#         ############################
#         # Put your code here and then remove 'pass'
#         # YOUR CODE
#         ############################
#         pass
#     return dic_idf_values


def song_to_vector(dic_tf_per_song, dic_idf):
    """
    This method will extract vector representation (based on TF-IDF) for each song
    @param dic_tf_per_song: TF dictionary with song name as key and dictionary of (token:TF) as value
    @param dic_idf: IDF dictionary with token as key and its IDF as value
    @return: dictionary of (song name, vector)
    """
    song_to_vec = {}

    # Ensure consistent order of terms
    sorted_terms = sorted(dic_idf.keys())

    for song, tf_values in dic_tf_per_song.items():
        # Initialize a list to store TF-IDF values for each term
        vec = []

        for term in sorted_terms:
            tf = tf_values.get(term, 0)
            idf = dic_idf.get(term, 0)
            tf_idf = tf * idf
            vec.append(tf_idf)

        song_to_vec[song] = np.array(vec)

    return song_to_vec


# def cosine_sim(numpy_vec1, numpy_vec2):
#     """
#     Using sklearn library, this method calculates the cosine similarity between two numpy vectors
#     @param numpy_vec1: vector 1
#     @param numpy_vec2: vector 2
#     @return: cosine similarity
#     """
#     return cosine_similarity(numpy_vec1, numpy_vec2)


def cosine_sim(numpy_vec1, numpy_vec2):
    """
    Using sklearn library, this method calculates the cosine similarity between two numpy vectors
    @param numpy_vec1: vector 1
    @param numpy_vec2: vector 2
    @return: cosine similarity
    """
    # Reshape the vectors to 2D arrays
    numpy_vec1_2d = numpy_vec1.reshape(1, -1)
    numpy_vec2_2d = numpy_vec2.reshape(1, -1)

    # Calculate cosine similarity and extract the single value from the result
    similarity_matrix = cosine_similarity(numpy_vec1_2d, numpy_vec2_2d)
    return similarity_matrix[0, 0]


def test_cosine(dic_song_vectors):
    print(cosine_sim(
        dic_song_vectors["Till I Collapse"].reshape(-1, 1), dic_song_vectors["Rap God"].reshape(-1, 1)))
    print(
        cosine_sim(dic_song_vectors["Till I Collapse"].reshape(-1, 1), dic_song_vectors["Billie Jean"].reshape(-1, 1)))


def test_tsne_plot(dic_song_vectors, dic_song_genre):
    lst_song_names = []
    lst_data = []
    colors = []
    tsne = TSNE(n_components=2)
    for song in list(dic_song_vectors.keys()):
        lst_song_names.append(song)
        lst_data.append(dic_song_vectors[song])
        color = get_color(dic_song_genre[song])
        colors.append(color)
    data = np.array(lst_data)
    vectors = tsne.fit_transform(data)
    ax = plt.axes()
    ax.set_facecolor("black")
    for i in range(len(vectors)):
        plt.scatter(vectors[i][0], vectors[i][1], color=colors[i])

    # Adding song names; this can make the plot messy; you can choose a fewer songs and uncomment this code
    for i, txt in enumerate(lst_song_names):
        if i % 10 == 0:
            plt.annotate(txt, (vectors[i][0], vectors[i][1]))
    plt.show()


def get_color(genre):
    """
    Assigns a color to each genre
    @param genre: song genre
    @return: genre's color
    """
    if genre == "Blues":
        color = 'blue'
    elif genre == "Country":
        color = 'red'
    elif genre == "Metal":
        color = 'gray'
    elif genre == "Pop":
        color = 'yellow'
    elif genre == "Rap":
        color = 'green'
    elif genre == "Rock":
        color = 'purple'
    return color


def main():
    # Path to the root Lyrics files
    path_to_root_dir = r"./Lyrics"
    for root, dirs, files in os.walk(path_to_root_dir):
        for dir in dirs:
            dic_song_dic_term_count, dic_song_genre = read_files_to_dictionaries(
                path_to_root_dir + "/")
    dic_song_dic_term_frequency = get_TF_values(dic_song_dic_term_count)
    dic_term_idfs = get_IDF_values(dic_song_dic_term_count)

    dic_song_vectors = song_to_vector(
        dic_song_dic_term_frequency, dic_term_idfs)
    test_cosine(dic_song_vectors)
    test_tsne_plot(dic_song_vectors, dic_song_genre)


if __name__ == '__main__':
    main()
