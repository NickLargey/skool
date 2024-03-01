import csv

from PIL import Image
import os


def size_filtering(directory, filtered_captions):
    # This method writes the name of file with appropriate width and height to the file and removes other formats than
    # png, jpg and gif
    cnt = 0
    with open("mse_timath_filenames.tsv", "w", newline='') as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n', quotechar='"')
        for file in os.listdir(directory):
            if file.split('.')[0] not in filtered_captions:
                continue
            try:
                with Image.open(directory+file) as img:
                    width, height = img.size
                    if width < 50 or height < 50:
                        continue
                    temp_name = file.lower()
                    if temp_name.endswith(".png") or temp_name.endswith(".jpg") or temp_name.endswith(".gif"):
                        writer.writerow([file])
            except Exception as e:
                cnt += 1
    print(cnt)


def caption_filtering(tsv_file_path):
    # this method returns the list of images with captions more than 3 words
    lst_files = []
    with open(tsv_file_path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            caption = line[1]
            image_file = line[0]
            if len(caption.split(" "))<=3:
                continue
            lst_files.append(image_file)
    return lst_files


directory = "../MSEImages/"
tsv_file_path = "../MSE.tsv"
filtered_lst_captions = caption_filtering(tsv_file_path)
size_filtering(directory, filtered_lst_captions)