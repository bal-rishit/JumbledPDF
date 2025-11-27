import fitz
from PIL import Image
import io

def render_all_pages_to_pil(pdf_path, zoom=3.0):
    doc = fitz.open(pdf_path)
    images = []

    try:
        for i in range(doc.page_count):
            page = doc.load_page(i)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            images.append(img)
    finally:
        doc.close()

    return images


def crop_header(img, frac=0.20):
    w, h = img.size
    return img.crop((0, 0, w, int(h * frac)))


def crop_footer(img, frac=0.20):
    w, h = img.size
    return img.crop((0, int(h * (1 - frac)), w, h))


def rebuild_pdf_from_images(images, out_path):
    for i in range(len(images)):
        if images[i].mode != "RGB":
            images[i] = images[i].convert("RGB")

    images[0].save(out_path, "PDF", save_all=True, append_images=images[1:])
