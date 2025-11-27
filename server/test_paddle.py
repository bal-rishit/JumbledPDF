from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang='en')

img = Image.open("test_ocr.png")
img_np = np.array(img)

print("Running OCR on test_ocr.png...")
result = ocr.predict(img_np)

print("\nOCR RESULT:")
print(result)
