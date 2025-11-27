import fitz
from PIL import Image

pdf_path = "Loan-Agreement-Shuffled-Scanned.pdf"  
doc = fitz.open(pdf_path)

page = doc[18]   
zoom = 4.0      # 400 DPI
mat = fitz.Matrix(zoom, zoom)

pix = page.get_pixmap(matrix=mat)

img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
img.save("debug_render.png")

print("Saved debug_render.png")
