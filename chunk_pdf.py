"""chunk_pdf.py - Split PDF into N-page chunks."""
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def chunk_pdf(pdf_path, chunk_size=25, output_dir=None):
    reader = PdfReader(pdf_path)
    total = len(reader.pages)
    print(f"PDF: {pdf_path} | Pages: {total} | Chunks: {(total + chunk_size - 1) // chunk_size}")

    if output_dir is None:
        output_dir = Path(pdf_path).parent / "chunks"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = Path(pdf_path).stem
    for i in range(0, total, chunk_size):
        writer = PdfWriter()
        end = min(i + chunk_size, total)
        for j in range(i, end):
            writer.add_page(reader.pages[j])
        out_path = output_dir / f"{stem}_p{i+1}-p{end}.pdf"
        with open(out_path, "wb") as f:
            writer.write(f)
        print(f"  [{i+1}-{end}] -> {out_path.name}")

    print(f"\nDone. {len(list(output_dir.glob('*.pdf')))} chunks in {output_dir}")

if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    if not pdf:
        print("Usage: python chunk_pdf.py <path.pdf> [chunk_size]")
        sys.exit(1)
    chunk_pdf(pdf, size)
