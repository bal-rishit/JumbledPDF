import pytesseract
from PIL import Image, ImageFilter, ImageOps
import os
from dotenv import load_dotenv
load_dotenv()


TESS_PATH = os.getenv("TESSERACT_CMD")
if TESS_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESS_PATH




def ocr_text(img):
    # enlarge image 2x
    big = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

    # convert to grayscale
    gray = ImageOps.grayscale(big)

    # increase contrast
    gray = ImageOps.autocontrast(gray)

    # light sharpening
    gray = gray.filter(ImageFilter.SHARPEN)

    config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=-0123456789"
    
    try:
        return pytesseract.image_to_string(gray, config=config).strip()
    except:
        return ""

def ocr_full_page(img: Image.Image):
    
    config = r"--oem 3 --psm 3"
    try:
        return pytesseract.image_to_string(img, config=config)
    except:
        return ""
