import os
from pypdf import PdfReader

def load_pdf(file_path):
    """Read a PDF file and return its complete text.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Concatenated text extracted from all pages.
    """

    print(f"Loading PDF file: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(file_path)
    full_text = ""

    for page_num ,page in enumerate(reader.pages):
        text=page.extract_text()
        if text:
            full_text+=text
            print(f"Loaded {page_num+1} successfully")
            
    print(f"\nNo of characters read from pdf is {len(full_text)}")
    return full_text

def split_into_chunks(text,chunk_size=500,overlap=0):
    print("\nsplitting text into chunks...")
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap 
    
    print(f"total chunks created: {len(chunks)}")
    return chunks


def save_chunks(chunks, output_file="data/scraped/chunks.txt"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- CHUNK {i+1} ---\n")
            f.write(chunk)
            f.write("\n\n")
    
    print(f"Chunks saved to {output_file}")

if __name__ == "__main__":
    pdf_path = "data/handbooks/handbook.pdf"
    
    text = load_pdf(pdf_path)
    chunks = split_into_chunks(text)
    
    print("\n-----------first 3 chunks----------")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i+1} ---")
        print(chunk)
        print("...")
    
    save_chunks(chunks)
    
    print(f"Everything Gone Well Hurrayyyy!!!!")
