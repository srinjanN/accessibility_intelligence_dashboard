"""
Multi-format Document and Text Ingestion Utility.
Supports: Pasted Text, TXT, PDF, DOCX, CSV, Excel, Images (OCR), and Web URLs.
"""

import io
import re
import requests
from bs4 import BeautifulSoup
from typing import Tuple, Optional

# File parsing library imports with safe fallbacks
try:
    import docx
except ImportError:
    docx = None

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from PIL import Image
except ImportError:
    Image = None

def parse_txt(file_bytes: bytes) -> str:
    """Parse UTF-8 or ASCII text from byte stream."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="replace")

def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file bytes."""
    if pypdf is None:
        return "PDF parsing library (pypdf) is missing."
    
    text = ""
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = pypdf.PdfReader(pdf_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        return f"Error extracting PDF content: {str(e)}"
    
    return text.strip() if text else "No extractable text found in PDF."

def parse_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX file bytes."""
    if docx is None:
        return "DOCX parsing library (python-docx) is missing."
    
    try:
        doc_file = io.BytesIO(file_bytes)
        document = docx.Document(doc_file)
        full_text = []
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        return "\n".join(full_text)
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"

def parse_csv_excel(file_bytes: bytes, filename: str, column_name: Optional[str] = None) -> str:
    """Extract text from CSV or Excel file dataframe."""
    if pd is None:
        return "Pandas library is missing."
    
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))
            
        if column_name and column_name in df.columns:
            text_series = df[column_name].dropna().astype(str)
            return "\n".join(text_series.tolist())
        else:
            # Flatten all text columns
            text_cols = df.select_dtypes(include=['object', 'string']).columns
            if len(text_cols) > 0:
                lines = []
                for col in text_cols:
                    lines.extend(df[col].dropna().astype(str).tolist())
                return "\n".join(lines)
            else:
                return df.to_string()
    except Exception as e:
        return f"Error parsing CSV/Excel file: {str(e)}"

def parse_image_ocr(file_bytes: bytes) -> str:
    """Extract text from image bytes via EasyOCR / PyTesseract / PIL text extraction."""
    # Attempt EasyOCR if available
    try:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(file_bytes, detail=0)
        if result:
            return " ".join(result)
    except Exception:
        pass
    
    # Fallback to PyTesseract if available
    try:
        import pytesseract
        if Image:
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
            if text.strip():
                return text.strip()
    except Exception:
        pass
        
    return "OCR engine not initialized or no text detected in image. Please paste text directly or provide a standard text/document file."

def parse_url(url: str) -> Tuple[str, str]:
    """Scrape and extract main body text from a webpage URL."""
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove scripts, styles, header, footer, nav
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        page_title = soup.title.string.strip() if soup.title else "Webpage Analysis"
        
        # Get text from paragraph tags and headings
        text_blocks = []
        for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            cleaned = tag.get_text().strip()
            if cleaned:
                text_blocks.append(cleaned)
                
        extracted_text = "\n".join(text_blocks)
        if not extracted_text:
            extracted_text = soup.get_text(separator="\n", strip=True)
            
        return page_title, extracted_text
    except Exception as e:
        return "URL Scraping Error", f"Failed to extract text from URL ({url}): {str(e)}"
