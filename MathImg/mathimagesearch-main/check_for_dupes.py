from PIL import Image
import csv
import os
from tqdm import tqdm

def are_images_equal(image_path1, image_path2):
    # Open images using Pillow
    image1 = Image.open(image_path1).convert('RGB')
    image2 = Image.open(image_path2).convert('RGB')

    # Compare images
    return image1 == image2

# Function to read TSV file and return data as a list of dictionaries
def read_tsv(file_path):
    with open(file_path, newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        return list(reader)

# Replace 'clean_wiki_dataset.tsv' with the actual file path
file_path = 'clean_wiki_dataset.tsv'
data = read_tsv(file_path)

# Folder containing images
image_folder = 'wikipedia_images'

captions = {}

with open('clean_wiki_dataset_no_dupes.tsv', 'w') as file:
    for dic in tqdm(data, desc='Images'):
        save = True
        caption = dic['Caption']
        if caption in captions:
            image_path_set = captions[caption]
            curr_image_path = os.path.join(image_folder, dic["Image File Name"])
            for image_path in image_path_set:
                image_path = os.path.join(image_folder, image_path)
                if are_images_equal(curr_image_path, image_path):
                    save = False
        else:
            captions[caption] = set()
        captions[caption].add(dic["Image File Name"])
        if save:
            file.write(f"{dic['Image File Name']}\t{dic['Caption']}\t{dic['Link']}\n")