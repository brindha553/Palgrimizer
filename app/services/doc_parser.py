import os
from PyPDF2 import PdfReader
import docx

class DocumentParserService:
    """Parses uploaded files (PDF, DOCX, TXT, RTF) into plain text."""

    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        file_type = file_type.lower().strip('.')

        if file_type == 'txt':
            return DocumentParserService._parse_txt(file_path)
        elif file_type == 'pdf':
            return DocumentParserService._parse_pdf(file_path)
        elif file_type == 'docx':
            return DocumentParserService._parse_docx(file_path)
        elif file_type == 'rtf':
            return DocumentParserService._parse_rtf(file_path)
        else:
            # Fallback text read
            return DocumentParserService._parse_txt(file_path)

    @staticmethod
    def _parse_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f"Error reading text file: {str(e)}"

    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            extracted_pages = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(page_text.strip())
            return "\n\n".join(extracted_pages) if extracted_pages else "No readable text found in PDF."
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"

    @staticmethod
    def _parse_docx(file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs) if paragraphs else "No readable paragraphs in DOCX file."
        except Exception as e:
            return f"Error reading DOCX file: {str(e)}"

    @staticmethod
    def _parse_rtf(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_rtf = f.read()
            # Simple RTF tag cleanup
            import re
            clean_text = re.sub(r'{\\.*?}', '', raw_rtf)
            clean_text = re.sub(r'\\[a-z0-9]+\s?', '', clean_text)
            return clean_text.strip() or raw_rtf
        except Exception as e:
            return f"Error reading RTF file: {str(e)}"

doc_parser = DocumentParserService()
