from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import tempfile, os, shutil, traceback

from services.pdf_utils import render_all_pages_to_pil, crop_header, crop_footer, rebuild_pdf_from_images
from services.ocr_utils import ocr_text
from services.ocr_utils import ocr_full_page
from services.order_utils import order_pages
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.post("/reorder-pdf")
async def reorder_pdf(file: UploadFile = File(...)):
    tmpdir = tempfile.mkdtemp()

    try:
        path = os.path.join(tmpdir, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())

        pages = render_all_pages_to_pil(path, zoom=3.5)

        metas = []
        unnumbered_fulltexts = []
        for i, img in enumerate(pages):
            header = crop_header(img, 0.10)
            footer = crop_footer(img, 0.10)

            #header.save(f"debug_header_{i}.png")
            #footer.save(f"debug_footer_{i}.png")


            header_text = ocr_text(header)
            footer_text = ocr_text(footer)

            fulltext = ""   # only filled for unnumbered pages


            if not header_text and not footer_text:
                fulltext = ocr_full_page(img)   
                unnumbered_fulltexts.append({"index": i, "fulltext": fulltext})


            metas.append({
                "index": i,
                "header_text": header_text,
                "footer_text": footer_text
            })

        #order = order_pages(metas)
        order = order_pages(metas, unnumbered_fulltexts)


        ordered_images = [pages[i] for i in order]

        output = os.path.join(tmpdir, "reordered.pdf")
        rebuild_pdf_from_images(ordered_images, output)

        shutil.copy(output, "reordered.pdf")

        return {
            "download_url": "/download",
            "logs": metas + [{"final_order": order}]
        }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@app.get("/download")
def download():
    if not os.path.exists("reordered.pdf"):
        return JSONResponse(status_code=404, content={"error": "No file"})
    return FileResponse("reordered.pdf", filename="reordered.pdf")
