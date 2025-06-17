import os
import csv
from pdfminer.high_level import extract_text
import pytesseract
from PIL import Image

# Extract content from a txt file
def extract_text_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

# Extract content from a csv file
def extract_text_from_csv(filepath):
    texts = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            texts.append(' '.join(row))
    return '\n'.join(texts)

# Extract content from a pdf file
def extract_text_from_pdf(filepath):
    return extract_text(filepath)

# Extract content from a png file
def extract_text_from_png(filepath):
    img = Image.open(filepath)
    return pytesseract.image_to_string(img)

def extract_text_by_extension(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.txt':
        return extract_text_from_txt(filepath)
    elif ext == '.csv':
        return extract_text_from_csv(filepath)
    elif ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.png':
        return extract_text_from_png(filepath)
    else:
        return None
