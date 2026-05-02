import os
from pathlib import Path
from pypdf import PdfReader

chunks_dir = Path(r'C:\Users\austi\Downloads\chunks')
text_dir = Path(r'C:\Users\austi\Downloads\chunked_text')
text_dir.mkdir(exist_ok=True)

stem = 'calculus-volume-1_-_WEB'
pdfs = sorted(chunks_dir.glob(f'{stem}_*.pdf'))

for pdf_path in pdfs:
    txt_path = text_dir / (pdf_path.stem + '.txt')
    if txt_path.exists():
        print(f'SKIP (exists): {txt_path.name}')
        continue
    
    reader = PdfReader(str(pdf_path))
    text = ''
    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
            if page_text:
                text += f'\n--- Page {i+1} ---\n{page_text}\n'
        except Exception as e:
            text += f'\n--- Page {i+1} [ERROR: {e}] ---\n'
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'DONE: {txt_path.name} | Pages: {len(reader.pages)} | Chars: {len(text)}')

print(f'\nFinished. {len(list(text_dir.glob("*.txt")))} total txt files in {text_dir}')
