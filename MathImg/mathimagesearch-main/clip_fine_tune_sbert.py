"""
    Code from https://github.com/UKPLab/sentence-transformers/blob/master/examples/training/clip/train_clip.ipynb
"""
import csv
import os
import re
import string
import sys
import numpy as np
from tqdm import tqdm

from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import bs4
from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses, util, models
from torch.utils.data import DataLoader
from PIL import Image

def create_train_dataset(file_path, wiki_prefix, mse_prefix):
    dataset = []
    cnt1 = 0
    cnt2 = 0
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        next(tsv_file)
        for line in tsv_file:
            if '_' in line[0]:
                image_path = mse_prefix + line[0].strip()
                cnt1 += 1
            else:
                image_path = wiki_prefix + line[0].strip()
                cnt2 += 1
            caption = line[1].strip()
            dataset.append(InputExample(texts=[Image.open(image_path).convert('RGB'), caption[:77]], label=1))
    print(cnt1)
    print(cnt2)
    return dataset

def create_eval_dataset(file_path, wiki_prefix, mse_prefix):
    images = []
    captions = []
    scores = []
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        next(tsv_file)
        for line in tsv_file:
            if '_' in line[0]:
                image_path = mse_prefix + line[0].strip()
            else:
                image_path = wiki_prefix + line[0].strip()
            caption = line[1].strip()
            images.append(Image.open(image_path).convert('RGB'))
            captions.append(caption[:77])
            scores.append(1)
    return images, captions, scores

def create_test_dataset(file_path, wiki_prefix, mse_prefix):
    images = []
    captions = []
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        next(tsv_file)
        for line in tsv_file:
            if '_' in line[0]:
                image_path = mse_prefix + line[0].strip()
            else:
                image_path = wiki_prefix + line[0].strip()
            caption = line[1].strip()
            images.append(image_path)
            captions.append(caption[:77])
    return images, captions

def calculate_mrr_recall(data):
    mrr = 0.0
    recall = 0.0

    for i, (score, label, caption, image) in enumerate(data):
        if label:
            mrr = 1.0 / (i + 1)
            if i == 0:
                recall = 1.0
                print(image, caption)
            break

    return (mrr, recall)

def get_averages(data, prefix):
    all_mrr = [x[0] for x in data]
    all_recall = [x[1] for x in data]

    average_mrr = sum(all_mrr) / len(all_mrr)
    average_recall = sum(all_recall) / len(all_recall)
    
    print(f"{prefix} Testing MRR: {average_mrr}")
    print(f"{prefix} Testing Recall@1: {average_recall}")

args = sys.argv[1:]

if '--load' in args:
    model = SentenceTransformer('CLIP_FineTuned_SBERT/')
else:
    model = SentenceTransformer('clip-ViT-B-32')

wiki_prefix = 'wikipedia_images/'
mse_prefix = 'MSEImages/'

if '--train' in args:
    train_dataset = create_train_dataset('tsvs/training_set.tsv', wiki_prefix, mse_prefix)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=4)
    train_loss = losses.ContrastiveLoss(model=model)

    eval_images, eval_captions, eval_scores = create_eval_dataset('tsvs/evaluation_set.tsv', wiki_prefix, mse_prefix)
    evaluator = EmbeddingSimilarityEvaluator(sentences1=eval_images, sentences2=eval_captions, scores=eval_scores, name='train-eval')

    model.fit([(train_dataloader, train_loss)], epochs=1, evaluator=evaluator, show_progress_bar=True, save_best_model=True, output_path='CLIP_FineTuned_NEW')

if '--test' in args:
    test_images, test_captions = create_test_dataset('tsvs/testing_set.tsv', wiki_prefix, mse_prefix)
    both_mrr_and_recall = []
    image_caption_mrr_and_recall = []
    caption_image_mrr_and_recall = []

    image_paths = [str(image) for image in test_images]
    image_embeddings = {path: model.encode(path) for path in image_paths}
    caption_embeddings = {caption: model.encode([caption]) for caption in test_captions}

    cached_scores = {}

    total_iterations = len(test_captions)

    for i, caption in tqdm(enumerate(test_captions), total=total_iterations, desc=f'Calculating MRR and Recall@1'):
        correct = False
        ranked_list = []

        for j, image in enumerate(test_images):
            if i == j:
                correct = True

            caption_emb = caption_embeddings[caption]
            image_emb = image_embeddings[image]

            if (caption, image) in cached_scores:
                score = cached_scores[(caption, image)]
            else:
                score = util.cos_sim(caption_emb, image_emb)
                cached_scores[(caption, image)] = score

            ranked_list.append((score.item(), correct, caption, image))

            correct = False

        sorted_ranked_list = sorted(ranked_list, key=lambda x: x[0], reverse=True)
        mrr, recall = calculate_mrr_recall(sorted_ranked_list)
        caption_image_mrr_and_recall.append((mrr, recall))
        both_mrr_and_recall.append((mrr, recall))
    
    total_iterations = len(test_images)
    
    for i, image in tqdm(enumerate(test_images), total=total_iterations, desc=f'Calculating MRR and Recall@1'):
        correct = False
        ranked_list = []

        for j, caption in enumerate(test_captions):
            if i == j:
                correct = True

            caption_emb = caption_embeddings[caption]
            image_emb = image_embeddings[image]

            if (caption, image) in cached_scores:
                score = cached_scores[(caption, image)]
            else:
                score = util.cos_sim(caption_emb, image_emb)
                cached_scores[(caption, image)] = score

            ranked_list.append((score.item(), correct, caption, image))

            correct = False

        sorted_ranked_list = sorted(ranked_list, key=lambda x: x[0], reverse=True)
        mrr, recall = calculate_mrr_recall(sorted_ranked_list)
        image_caption_mrr_and_recall.append((mrr, recall))
        both_mrr_and_recall.append((mrr, recall))

    get_averages(caption_image_mrr_and_recall, 'Caption to Image')
    get_averages(image_caption_mrr_and_recall, 'Image to Caption')
    get_averages(both_mrr_and_recall, 'Combined')

# Finetuned
# Caption to Image Testing MRR: 0.00256302136723039
# Caption to Image Testing Recall@1: 0.00032102728731942215
# Image to Caption Testing MRR: 0.0026512268432280516
# Image to Caption Testing Recall@1: 0.00032102728731942215
# Combined Testing MRR: 0.0026071241052292183
# Combined Testing Recall@1: 0.00032102728731942215

# Original
# Caption to Image Testing MRR: 0.0028612847822108425
# Caption to Image Testing Recall@1: 0.0
# Image to Caption Testing MRR: 0.0028011011274615455
# Image to Caption Testing Recall@1: 0.00032102728731942215
# Combined Testing MRR: 0.0028311929548361903
# Combined Testing Recall@1: 0.00016051364365971107