import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
from PIL import Image

# Function to remove newlines from a string
def remove_newlines(s):
    return s.replace('\n', ' ').replace('\r', '')

def is_image_openable(image_path):
    try:
        with Image.open(image_path) as img:
            return True
    except Exception:
        return False

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

folder_path = 'WikiHTML'
output_dir = 'wikipedia_images'
tsv_file_path = 'wiki_dataset.tsv'

subfolders = [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]

# Create and open the TSV file for writing
with open(tsv_file_path, 'w', encoding='utf-8') as tsv_file:
    # Write the header row
    tsv_file.write("Image File Name\tCaption\tLink\tTitle\n")
    cnt = 0

    # Iterate through HTML files in the folder and extract img src, and caption
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        html_files = [f for f in os.listdir(subfolder_path) if f.endswith('.html')]

        for filename in tqdm(html_files, desc="Reading HTML"):
            html_path = os.path.join(subfolder_path, filename)

            # Read the HTML content from the file
            with open(html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all figure elements
            figures = soup.find_all('figure')

            for figure in figures:
                # Find the image source
                img_element = figure.find('img')

                # Check if an img element was found
                if img_element is not None:
                    img_src = img_element.get('src')
                else:
                    continue

                # Find the caption and remove newlines
                caption = figure.find('figcaption').text
                caption = remove_newlines(caption)
                if not caption:
                    continue

                extension = os.path.splitext(os.path.basename(img_src))[1]
                image_filename = str(cnt) + extension

                # Download and save the image with the shortened file name
                if img_src[:6] != 'https:':
                    img_url = f"https:{img_src}"
                else:
                    img_url = img_src
                img_path = os.path.join(output_dir, image_filename)

                # Ensure the directory structure exists
                os.makedirs(os.path.dirname(img_path), exist_ok=True)

                img_data = requests.get(img_url, headers=headers).content

                try:
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)
                except Exception as e:
                    continue

                if not is_image_openable(img_path):
                    os.remove(img_path)
                    continue

                title = filename[:-5]
                wikipedia_page_url = "https://en.wikipedia.org/wiki/" + title

                # Write the data to the TSV file
                tsv_file.write(f"{image_filename}\t{caption}\t{wikipedia_page_url}\t{title}\n")
                cnt += 1
