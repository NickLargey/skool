import pandas as pd
import re

punc = set([':', '.', '—', '–', '-'])

def remove_patterns(text):
    pattern = re.compile(r'^(?:img.\s*\d.|figure-\d.\d.\d|figure-\d.\d\s-|figure\sI|figure\sII|figure\sIII|figure\sIV|figure\sV|figure\s(\d.)+|figure\s(\w+)\s\([a-z]\)—|figure-\d+\s\((\w+)\):|figure-\d+:|figure\s\((\w+)\)|figure\s(\w+)—|figure\s(\w+)–|figure\s(\w+)\s\([a-z]\)–|figure\s(\w+)[:.]|figure\s[a-zA-Z][:.]|figure\s\d+\s-|figure\s:|figure\s\d+|figure\.\s\d+:|figure\s\d+:|figure\.\s\d+|figure\d+.|figure\s\d+.|figure\s\d+|figure\.|figure:|figure\s–|fig\s\d+:|fig\s\d+.|fig\s\d+|fig-\d+:|fig,\s\d.|fig\.\s\d+:|fig\.\s\d+|fig\d+\.|fig\.|fig:)', flags=re.IGNORECASE)
    
    new_text = re.sub(pattern, '', text).strip()
    if new_text and new_text[0] in punc:
        new_text = new_text[1:]
    return new_text.strip()

file_path = 'wiki_dataset.tsv'
df = pd.read_csv(file_path, sep='\t')
for index, row in df.iterrows():
    cap = str(row['Caption'])
    cap = remove_patterns(cap.strip())
    if cap:
        df.loc[index, 'Caption'] = remove_patterns(cap.strip())

new_df = df[['Image File Name', 'Caption', 'Link', 'Title']].dropna()
new_file_path = 'clean_wiki_dataset.tsv'
new_df.to_csv(new_file_path, sep='\t', index=False)
