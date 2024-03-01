from sklearn.model_selection import train_test_split
import csv

def reading_captions(file_path, set_files, dic):
    images_with_captions = []
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        for line in tsv_file:
            file_name = line[0].strip()
            if file_name not in set_files:
                continue            
            caption = line[1].strip()
            link = line[3].strip()
            images_with_captions.append((dic[file_name], caption, link))
    return images_with_captions

def write_to_tsv(data, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow(['Image File Name', 'Caption', 'Link'])
        tsv_writer.writerows(data)

data = []
dic = {}
file_path = 'filtering/mse_clip_scores.tsv'
with open(file_path, newline='', encoding='utf-8') as file:
    tsv_file = csv.reader(file, delimiter='\t')
    next(tsv_file)
    for row in tsv_file:
        data.append(row[0].split('.')[0])
        dic[row[0].split('.')[0]] = row[0]

# Split the data into training, evaluation, and test sets
train_data, test_and_eval_data = train_test_split(data, test_size=0.2, random_state=42)
evaluation_data, test_data = train_test_split(test_and_eval_data, test_size=0.5, random_state=42)

train_images_with_captions = reading_captions('MSE.tsv', set(train_data), dic)
eval_images_with_captions = reading_captions('MSE.tsv', set(evaluation_data), dic)
test_images_with_captions = reading_captions('MSE.tsv', set(test_data), dic)

write_to_tsv(train_images_with_captions, 'individual_tsvs/mse_training_set.tsv')
write_to_tsv(eval_images_with_captions, 'individual_tsvs/mse_evaluation_set.tsv')
write_to_tsv(test_images_with_captions, 'individual_tsvs/mse_testing_set.tsv')