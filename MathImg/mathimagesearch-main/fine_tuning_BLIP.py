from PIL import Image
from tqdm import tqdm
import numpy as np
import csv
import sys
from torch.utils.data import Dataset, DataLoader
from transformers import AutoProcessor, BlipForConditionalGeneration
import torch

class ImageCaptioningDataset(Dataset):
    def __init__(self, dataset, processor, image_folder):
        self.dataset = dataset
        self.processor = processor
        self.image_folder = image_folder

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        image = Image.open(self.image_folder + item['image']).convert('RGB')
        encoding = self.processor(images=image, text=item['text'][:512], padding="max_length", return_tensors="pt")
        # remove batch dimension
        encoding = {k:v.squeeze() for k,v in encoding.items()}
        return encoding

def read_tsvs(file_path):
    data = {}
    with open(file_path, newline='') as file:
        tsv_file = csv.reader(file, delimiter='\t', lineterminator='\n', quotechar='"')
        next(tsv_file)
        for i, line in enumerate(tsv_file):
            data[i] = {'image': line[0].strip(), 'text': line[1].strip()[:512]}
    return data

def evaluate_model(model, dataloader, device):
    total_loss = 0.0
    steps = 0

    model.eval()
    with torch.no_grad():
        for batch in tqdm(dataloader, total=len(dataloader), desc="Evaluating"):
            input_ids = batch.pop("input_ids").to(device)
            pixel_values = batch.pop("pixel_values").to(device)

            outputs = model(input_ids=input_ids, pixel_values=pixel_values, labels=input_ids)
            
            total_loss += outputs.loss.item()
            

            steps += 1

    return total_loss / steps

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

args = set(sys.argv[1:])
train = '--train' in args
test = '--test' in args
save = '--save' in args
load = '--load' in args

if load:
    model = BlipForConditionalGeneration.from_pretrained("finetuned_blip_model")

image_folder = 'wikipedia_images/'
batch_size = 8

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

model.train()
if train:
    num_epochs = 5
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    train_dataset = ImageCaptioningDataset(read_tsvs('tsvs/training_set.tsv'), processor, image_folder)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    eval_dataset = ImageCaptioningDataset(read_tsvs('tsvs/evaluation_set.tsv'), processor, image_folder)
    eval_dataloader = DataLoader(eval_dataset, batch_size=batch_size, shuffle=False)
    for epoch in range(num_epochs):
        pbar = tqdm(train_dataloader, total=len(train_dataloader))
        model.train()

        for batch in pbar:
            input_ids = batch.pop("input_ids").to(device)
            pixel_values = batch.pop("pixel_values").to(device)

            outputs = model(input_ids=input_ids,
                            pixel_values=pixel_values,
                            labels=input_ids)
            
            loss = outputs.loss
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            pbar.set_description(f"Epoch {epoch}/{num_epochs}, Loss: {loss.item():.4f}")

        eval_loss = evaluate_model(model, eval_dataloader, device)
        print(f'Evaluation Loss: {eval_loss}')

if test:
    test_dataset = ImageCaptioningDataset(read_tsvs('tsvs/testing_set.tsv'), processor, image_folder)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    test_loss = evaluate_model(model, test_dataloader, device)
    print(f'Testing Loss: {test_loss}')
    

model.train()

if save:
    # torch.save(model.state_dict(), "blip_model.pt")
    # model.load_state_dict(torch.load("blip_model.pt"))
    model.save_pretrained("finetuned_blip_model")

