import pytesseract
from PIL import Image
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("debug_render.png")   
img_np = np.array(img)

print("Running Tesseract OCR...")
text = pytesseract.image_to_string(img)

print("\nOCR RESULT:")
print(text)
