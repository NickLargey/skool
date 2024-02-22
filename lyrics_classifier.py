import os
import glob
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import pandas as pd


root_dir = './TM_CA1_Lyrics'  # replace with your directory path
data = []  # List to store file data

for subdir, dirs, files in os.walk(root_dir):
    for file in glob.glob(os.path.join(subdir, '*.txt')):
        with open(file, 'r') as f:
            content = f.read()
            data.append(
                {'Lyrics': content, 'Genre': str(subdir.split('\\')[-1])})

lyrics_data = pd.DataFrame(data, columns=["Lyrics", "Genre"])

lyrics_data = lyrics_data.dropna(subset=["Genre", "Lyrics"])
lyrics_data['Lyrics'] = lyrics_data['Lyrics'].str.replace(
    r'\s+', ' ', regex=True)
lyrics_data['Lyrics'] = lyrics_data['Lyrics'].str.replace(
    r'[.,!?;:]', '', regex=True)

# print(lyrics_data.head())

# Create n-grams
vectorizer = CountVectorizer(ngram_range=(2, 4))
X = vectorizer.fit_transform(lyrics_data['Lyrics'])
y = lyrics_data['Genre']

# # Split data into training and test sets
# X_train, X_val, y_train, y_val = train_test_split(
#     X, y, test_size=0.3, random_state=42)

# # Train the classifier
# clf = MultinomialNB()
# clf.fit(X_train, y_train)

# # Evaluate the model
# y_pred = clf.predict(X_val)
# print(classification_report(y_val, y_pred))
