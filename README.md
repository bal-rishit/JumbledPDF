1. What I built and why this approach was chosen

I built a system that automatically reorders jumbled PDF documents using an OCR-based page number detection and LLM-based ordering for pages without page numbers. Since the documents were scanned, 
traditional text extraction did not work, so, the PDF pages were converted into PNG images using pymupdf after which Tesseract OCR was used to detect page numbers but from header/footer regions only. The pages that 
were not numbered were assumed to be initial pages of the document and those pages were then again scanned by OCR (this time whole pages were scanned) to extract text and provide it to LLM to analyse and reorder.
Gemini 2.5 Flash was used to infer their logical reading order based on text. This approach was chosen to make performance fast by OCR-processing only small cropped regions and reduce noice.

2. Assumptions, limitations, and trade-offs

The solution assumes that page numbers are present in the header or footer and follow simple formats like “-5-”, “5”, or “Page 5”. OCR results can be imperfect on noisy or low-quality scans, and LLM 
ordering depends on the readability of the extracted text. To keep installation simple, no heavy system-level tools or full-page OCR were used and only lightweight header/footer 
cropped images are processed. The UI is intentionally minimal, as the requirement was only for upload and download functionality.

3. What I would improve with more time

With more time, I would improve the UI and and more functions such as manual reordering and thumbnail previews. Apart from that I would also like to add multiple OCRs or add smarter heuristics 
(e.g., confidence thresholds, multi-zoom OCR) to reduce misread page numbers.
