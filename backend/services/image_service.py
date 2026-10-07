import fitz  # PyMuPDF
import os

def extract_images(pdf_path: str, output_dir: str, document_id: str):
    images_by_page = {}
    try:
        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            page = doc[i]
            image_list = page.get_images()
            page_images = []
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                image_id = f"{document_id}_page_{i+1}_img_{img_index}.png"
                image_path = os.path.join(output_dir, image_id)
                if pix.n - pix.alpha < 4:       # this is GRAY or RGB
                    pix.save(image_path)
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(image_path)
                    pix1 = None
                pix = None
                page_images.append(image_id)
            if page_images:
                images_by_page[i+1] = page_images
    except Exception as e:
        print(f"Error extracting images: {e}")
    return images_by_page
