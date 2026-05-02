"""Extract text from PDF chunks to .txt files."""
import sys
from pathlib import Path
from pypdf import PdfReader

def extract_text(pdf_path, output_dir=None):
    reader = PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {i+1} ---\n{page_text}\n"
        except Exception as e:
            text += f"\n--- Page {i+1} [ERROR: {e}] ---\n"

    if output_dir is None:
        output_dir = Path(pdf_path).parent / "text"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = Path(pdf_path).stem
    out_path = output_dir / f"{stem}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted: {pdf_path} -> {out_path}")
    print(f"  Pages: {len(reader.pages)} | Chars: {len(text)}")

if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        print("Usage: python pdf_to_text.py <path.pdf>")
        sys.exit(1)
    extract_text(pdf)
