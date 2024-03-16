import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

# def get_wikipedia_html(title):
#     # Replace spaces with underscores in the title
#     title = title.replace(" ", "_")

#     # Wikipedia URL for the given title
#     url = f"https://en.wikipedia.org/wiki/{title}"

#     try:
#         # Send an HTTP GET request to the Wikipedia page
#         response = requests.get(url)
#         response.raise_for_status()  # Check for any errors in the request

#         # Parse the HTML content
#         html_content = response.text

#         return html_content

#     except requests.exceptions.HTTPError as e:
#         print(f"HTTP error: {e}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")

#     return None

def has_figcaption(html_content):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check if any "figcaption" element is found in the HTML
    return soup.find("figcaption") is not None

# Replace with the path to your folder containing HTML files
folder_path = 'NTCIR-12_MathIR_Wikipedia_Corpus/MathTagArticles'
subfolders = [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]

output_dir = "WikiHTML"

# Iterate through HTML files in the folder and extract img src attributes
for subfolder in subfolders:    
    subfolder_path = os.path.join(folder_path, subfolder)
    html_files = [f for f in os.listdir(subfolder_path) if f.endswith('.html')]
    if not os.path.exists(os.path.join(output_dir, subfolder)):
        os.makedirs(os.path.join(output_dir, subfolder))  # Create subfolders in WikiHTML

    for filename in tqdm(html_files, desc="reading html"):
        if filename.endswith('.html'):
            filename = filename[:-5]
            title = filename.replace(" ", "_")

            # html_content = get_wikipedia_html(title)
            title = title.replace(" ", "_")

            # Wikipedia URL for the given title
            url = f"https://en.wikipedia.org/wiki/{title}"

            # Send an HTTP GET request to the Wikipedia page
            response = requests.get(url)
            # response.raise_for_status()  # Check for any errors in the request
            if response.status_code != 200:
                continue

            # Parse the HTML content
            html_content = response.text
            if html_content and has_figcaption(html_content):
                output_file = os.path.join(output_dir, subfolder, filename + '.html')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)