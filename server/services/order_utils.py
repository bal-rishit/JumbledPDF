import re
import os
from dotenv import load_dotenv
load_dotenv()

USE_GEMINI = bool(os.getenv("GEMINI_API_KEY"))

if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    MODEL = "gemini-2.5-flash-lite"

PATTERNS = [
    re.compile(r"^\s*[-–—]+\s*(\d{1,4})\s*[-–—]+\s*$"),  
    re.compile(r"^\s*(\d{1,4})\s*$"),                    
    re.compile(r"^Page\s*(\d{1,4})$", re.IGNORECASE), 
    re.compile(r"(?<!\d)-?\s*(\d{1,4})\s*-?(?!\d)")  
]

def extract_number(text: str):
    if not text:
        return None

    for line in text.splitlines():
        line = line.strip()
        for pat in PATTERNS:
            m = pat.match(line)
            if m:
                return int(m.group(1))
    return None


def llm_sort_unnumbered(pages):
    """
    pages = [
        {"index": 0, "fulltext": "..."},
        {"index": 1, "fulltext": "..."},
    ]
    """

    if not pages or not USE_GEMINI:
        return [p["index"] for p in pages]
    
    prompt = """
You are helping reorder pages of a legal document.
You are given several pages without page numbers.
Your job: return the correct logical order (from start to end).

Respond ONLY with a JSON array of page indices in correct order.
"""

    for p in pages:
        prompt += f"\nPageIndex {p['index']}:\n{p['fulltext']}\n---\n"

    response = genai.GenerativeModel(MODEL).generate_content(prompt)

    
    text = response.text
    idx = eval(text)  

    return idx


def order_pages(metas, unnumbered_fulltexts):
    numbered = []
    unnumbered = []

    
    fulltext_map = {p["index"]: p["fulltext"] for p in unnumbered_fulltexts}

    for m in metas:
        num = extract_number(m["header_text"]) or extract_number(m["footer_text"])

        if num is None:
            unnumbered.append({
                "index": m["index"],
                "fulltext": fulltext_map.get(m["index"], "")
            })
        else:
            numbered.append({"index": m["index"], "num": num})

    
    un_sorted = llm_sort_unnumbered(unnumbered)

    
    num_sorted = [p["index"] for p in sorted(numbered, key=lambda x: x["num"])]

    return un_sorted + num_sorted
