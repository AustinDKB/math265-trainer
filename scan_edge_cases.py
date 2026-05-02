import re
from pathlib import Path
from collections import defaultdict

text_dir = Path(r'C:\Users\austi\Downloads\chunked_text')
files = sorted(text_dir.glob('*.txt'))

# Patterns to look for
exercise_headers = re.compile(r'\b(Exercises|Review Exercises|Checkpoint|Example|Problem)\b', re.IGNORECASE)
question_patterns = re.compile(r'\n\s*(\d{1,3})[\.\)]\s+(.{0,300})')

# Keywords that suggest edge cases / weird problems
edge_keywords = [
    'absolute value', 'piecewise', 'floor', 'ceiling', 'greatest integer',
    'one-sided', 'one sided', 'vertical asymptote', 'horizontal asymptote',
    'slant asymptote', 'oblique asymptote', 'hole', 'removable discontinuity',
    'essential discontinuity', 'infinite discontinuity', 'oscillat',
    'epsilon', 'delta', 'squeeze theorem', 'intermediate value',
    'mean value theorem', 'rolle', "l'hopital", 'lhospital', 'indeterminate',
    'implicit', 'related rates', 'optimization', 'constraint',
    'parametric', 'polar', 'vector', 'arc length', 'surface area',
    'improper integral', 'comparison test', 'partial fraction',
    'integration by parts', 'trig substitution', 'weierstrass',
    'frustum', 'torus', 'cylindrical shell', 'washer', 'disk',
    'centroid', 'center of mass', 'fluid force', 'work', 'pump',
    'hyperbolic', 'inverse trig', 'inverse hyperbolic',
    'tabular integration', 'reduction formula', 'recursion',
    'series', 'convergence', 'divergence', 'ratio test', 'root test',
    ' alternating', 'conditional convergence', 'power series',
    'taylor', 'maclaurin', 'error bound', 'lagrange error',
    'binomial series', 'fourier',
]

edge_re = re.compile(r'\b(' + '|'.join(re.escape(k) for k in edge_keywords) + r')\b', re.IGNORECASE)

found = defaultdict(list)

for fpath in files:
    text = fpath.read_text(encoding='utf-8')
    # Find all potential exercise blocks
    lines = text.splitlines()
    context = []
    for i, line in enumerate(lines):
        match = edge_re.search(line)
        if match:
            # Grab surrounding context
            start = max(0, i-3)
            end = min(len(lines), i+6)
            snippet = '\n'.join(lines[start:end])
            found[fpath.name].append({
                'keyword': match.group(0),
                'line': i+1,
                'snippet': snippet
            })

# Output summary
output_path = Path(r'C:\Users\austi\Desktop\MATH TRAINER\edge_case_scan.md')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('# Edge Case Question Scan\n\n')
    out.write(f'Scanned {len(files)} text chunks.\n\n')
    
    for fname, items in sorted(found.items()):
        if not items:
            continue
        out.write(f'## {fname}\n\n')
        seen_snippets = set()
        for item in items:
            key = (item['keyword'], item['line'])
            if key in seen_snippets:
                continue
            seen_snippets.add(key)
            out.write(f'**Keyword:** `{item["keyword"]}` (line {item["line"]})\n')
            out.write('```\n')
            out.write(item['snippet'])
            out.write('\n```\n\n')
        out.write('---\n\n')

print(f"Scan complete. Found edge-case mentions in {len([k for k,v in found.items() if v])} files.")
print(f"Results written to {output_path}")
