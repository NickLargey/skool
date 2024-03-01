import csv

from PIL import Image
import os


def size_filtering(directory, filtered_captions):
    # This method writes the name of file with appropriate width and height to the file and removes other formats than
    # png, jpg and gif
    with open("wiki_timath_filenames.tsv", "w", newline='') as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n', quotechar='"')
        for file in os.listdir(directory):
            if file not in filtered_captions:
                continue
            with Image.open(directory+file) as img:
                width, height = img.size
                if width < 50 or height < 50:
                    continue
                temp_name = file.lower()
                if temp_name.endswith(".png") or temp_name.endswith(".jpg") or temp_name.endswith(".gif"):
                    writer.writerow([file])


def caption_filtering(tsv_file_path):
    # this method returns the list of images with captions more than 3 words
    lst_files = []
    with open(tsv_file_path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        next(tsv_file)
        for line in tsv_file:
            # line[2] for mathse, line[1] for wiki
            # caption = line[2]
            caption = line[1]
            image_file = line[0]
            if len(caption.split(" "))<=3:
                continue
            lst_files.append(image_file)
    return lst_files


# directory = "/mnt/netstore1_home/behrooz.mansouri/math_wiki_images/images/"
# tsv_file_path = "/mnt/netstore1_home/behrooz.mansouri/math_wiki_images/wiki_image_caption_link_dataset.tsv"
directory = "../wikipedia_images/"
tsv_file_path = "../clean_wiki_dataset_no_dupes.tsv"
filtered_lst_captions = caption_filtering(tsv_file_path)
size_filtering(directory, filtered_lst_captions)