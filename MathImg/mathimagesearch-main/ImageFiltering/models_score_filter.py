import requests
import torch
from PIL import Image
import csv

from tqdm import tqdm


def read_filtered_images(file_path):
    # Reading the filtered images
    lst_files = []
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        for line in tsv_file:
            lst_files.append(line[0].strip())
    return lst_files


def reading_captions(file_path, lst_files):
    dic_file_images = {}
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        next(tsv_file)
        for line in tsv_file:
            file_name = line[0].strip()
            if file_name not in lst_files:
                continue
            caption = line[1]
            dic_file_images[file_name] = caption
    return dic_file_images


lst_files = read_filtered_images("wiki_timath_filenames.tsv")
# print(len(lst_files))
dic_file_caption = reading_captions("../clean_wiki_dataset_no_dupes.tsv", lst_files)
# print(len(dic_file_caption))

from sentence_transformers import SentenceTransformer, util
from PIL import Image

model = SentenceTransformer('clip-ViT-B-32')

with open("wiki_clip_scores.tsv", "w", newline='') as file:
    writer = csv.writer(file, delimiter='\t', lineterminator='\n', quotechar='"')
    writer.writerow(["Image File Name"])
    for file_name in tqdm(dic_file_caption):
        # print(file_name)
        caption = dic_file_caption[file_name]
        # image = Image.open("/mnt/netstore1_home/behrooz.mansouri/math_wiki_images/images/" + file_name)#.convert('RGB')
        img_emb = model.encode(Image.open("../wikipedia_images/" + file_name))

        limit = 77
        second_try = False
        while True:
            try:
                # print(caption)
                text_emb = model.encode([caption])
                break
            except:
                # caption = caption.split(".")[0]
                if second_try:
                    caption = " ".join(caption.split(" ")[:limit])
                    limit -= 1
                second_try = True

        # Compute cosine similarities
        cos_scores = util.cos_sim(img_emb, text_emb)
        # print()
        score = cos_scores[0][0].cpu().numpy()
        if score > 0.295:
            writer.writerow([file_name])




### Back up code but was not used
# #####################################################################
# import clip
#
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("ViT-B/32", device=device, jit=False)
# from sentence_transformers import SentenceTransformer, util
# with open("Clip_scores.tsv", "w", newline='') as file:
#     writer = csv.writer(file, delimiter='\t', lineterminator='\n', quotechar='"')
#     for file_name in tqdm(dic_file_caption):
#         # print(file_name)
#         caption = dic_file_caption[file_name]
#         image = Image.open("/mnt/netstore1_home/behrooz.mansouri/math_wiki_images/images/" + file_name)#.convert('RGB')
#         # text = caption
#         image = preprocess(image).unsqueeze(0).to(device)
#         limit = 77
#         second_try = False
#         while True:
#             try:
#                 text = clip.tokenize([caption]).to(device)
#                 break
#             except:
#                 # caption = caption.split(".")[0]
#                 if second_try:
#                     caption = " ".join(caption.split(" ")[:limit])
#                     limit -= 1
#                 second_try = True
#         # print(len(text))
#         with torch.no_grad():
#             image_features = model.encode_image(image)
#             print(len(image_features))
#             print(image_features.shape)
#             text_features = model.encode_text(text)
#             print(len(text_features))
#             print(text_features.shape)
#             print(util.cos_sim(image_features[0], text_features[0])[0])
#             # image_features /= image_features.norm(dim=-1, keepdim=True)
#             # text_features /= text_features.norm(dim=-1, keepdim=True)
#             similarity = (image_features @ text_features.T).softmax(dim=-1)
#             print(similarity)
#             logits_per_image, logits_per_text = model(image, text)
#             probs = logits_per_image.softmax(dim=1).cpu().numpy()
#             print(probs)
#             input("stop")
#             score = probs[0][0]
#             writer.writerow([file_name, str(score)])

