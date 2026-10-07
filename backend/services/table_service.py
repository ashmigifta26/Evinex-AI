import pdfplumber

def extract_tables(pdf_path: str):
    tables_by_page = {}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if tables:
                    tables_by_page[i+1] = tables
    except Exception as e:
        print(f"Error extracting tables: {e}")
    return tables_by_page
