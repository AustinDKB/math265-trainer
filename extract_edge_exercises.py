import re
from pathlib import Path

text_dir = Path(r'C:\Users\austi\Downloads\chunked_text')
files = sorted(text_dir.glob('*.txt'))

# Patterns for actual exercises
exercise_section = re.compile(r'(SECTION\s+\d+\.\d+\s+EXERCISES|EXERCISES|Review\s+Exercises)', re.IGNORECASE)
numbered_exercise = re.compile(r'\n\s*(\d{1,3})\s*[\.\)]\s+(.*?)(?=\n\s*\d{1,3}\s*[\.\)]|$)', re.DOTALL)

# Edge case indicators in the question text
edge_patterns = {
    'piecewise': re.compile(r'piecewise|piece-wise', re.IGNORECASE),
    'absolute_value': re.compile(r'absolute\s+value|\|.*\|', re.IGNORECASE),
    'floor_ceiling': re.compile(r'floor|ceiling|greatest\s+integer|\[\s*x\s*\]', re.IGNORECASE),
    'one_sided_limit': re.compile(r'one-sided|one\s+sided|\\lim_{x\\to\\d+\\^', re.IGNORECASE),
    'epsilon_delta': re.compile(r'epsilon|delta|prove.*limit|\\delta|\\varepsilon', re.IGNORECASE),
    'squeeze': re.compile(r'squeeze', re.IGNORECASE),
    'lhopital_unusual': re.compile(r"l'h[oô]pital|indeterminate.*form|0\\^0|1\\^\\infty|\\infty\\^0|\\infty-\\infty", re.IGNORECASE),
    'improper_integral': re.compile(r'improper|diverge|converge.*integral|infinity.*integral', re.IGNORECASE),
    'reduction_formula': re.compile(r'reduction\s+formula|reduction\s+formulas', re.IGNORECASE),
    'ibp_multiple': re.compile(r'integration\s+by\s+parts.*twice|integration\s+by\s+parts.*multiple|tabular', re.IGNORECASE),
    'partial_fraction_hard': re.compile(r'partial\s+fraction.*repeated|partial\s+fraction.*quadratic', re.IGNORECASE),
    'trig_sub_hard': re.compile(r'trig.*substitution|hyperbolic.*substitution', re.IGNORECASE),
    'unusual_volume': re.compile(r'torus|frustum|spherical\s+cap|napkin\s+ring|cylinder\s+with\s+hole', re.IGNORECASE),
    'work_pump_unusual': re.compile(r'pump|work.*pump|fluid\s+force|hydrostatic', re.IGNORECASE),
    'center_of_mass_hard': re.compile(r'center\s+of\s+mass|centroid.*variable\s+density|variable\s+density', re.IGNORECASE),
    'hyperbolic': re.compile(r'sinh|cosh|tanh|csch|sech|coth', re.IGNORECASE),
    'inverse_trig_hyperbolic': re.compile(r'\\sin\\^\\{-1\\}|\\cos\\^\\{-1\\}|\\tan\\^\\{-1\\}|arcsin|arccos|arctan|arsinh|arcosh|artanh', re.IGNORECASE),
    'limit_infinity_radical': re.compile(r'\\lim.*\\sqrt|limit.*infinity.*root', re.IGNORECASE),
    'implicit_second': re.compile(r'implicit.*second|second.*derivative.*implicit', re.IGNORECASE),
    'related_rate_angle': re.compile(r'related.*rate.*angle|angle.*related.*rate', re.IGNORECASE),
    'optimization_boundary': re.compile(r'optimization|maximize|minimize.*constraint|closed\s+interval', re.IGNORECASE),
    'newton_method': re.compile(r"newton's\s+method|newton\s+method", re.IGNORECASE),
    'mean_value_theorem': re.compile(r'mean\s+value\s+theorem', re.IGNORECASE),
    'rolle_theorem': re.compile(r"rolle's\s+theorem|rolle\s+theorem", re.IGNORECASE),
    'continuity_unusual': re.compile(r'removable|jump|essential|infinite.*discontinuity', re.IGNORECASE),
    'asymptote_slant': re.compile(r'slant|oblique.*asymptote', re.IGNORECASE),
    'average_value': re.compile(r'average\s+value\s+of\s+a\s+function', re.IGNORECASE),
    'shell_washer_comparison': re.compile(r'shell|washer|disk.*method', re.IGNORECASE),
    'arc_length_surface': re.compile(r'arc\s+length|surface\s+area\s+of\s+revolution', re.IGNORECASE),
    'logistic_growth': re.compile(r'logistic|carrying\s+capacity', re.IGNORECASE),
}

results = []

for fpath in files:
    text = fpath.read_text(encoding='utf-8')
    # Split by exercise sections to focus on exercises
    sections = exercise_section.split(text)
    if len(sections) <= 1:
        continue
    
    for section_text in sections[1:]:  # Skip preamble
        # Only take a reasonable window after the header
        section_lines = section_text.splitlines()
        # Find where the next major heading starts (heuristic)
        end_idx = len(section_lines)
        for idx, line in enumerate(section_lines):
            if re.match(r'\d+\.\d+\s+\w+', line) and idx > 5:
                end_idx = idx
                break
        section_body = '\n'.join(section_lines[:end_idx])
        
        for m in numbered_exercise.finditer(section_body):
            num = m.group(1)
            question = m.group(2).strip()
            # Clean up excessive whitespace
            question = ' '.join(question.split())
            if len(question) < 10:
                continue
            
            matched_tags = []
            for tag, pattern in edge_patterns.items():
                if pattern.search(question):
                    matched_tags.append(tag)
            
            if matched_tags:
                results.append({
                    'file': fpath.name,
                    'number': num,
                    'tags': matched_tags,
                    'question': question[:500]  # Limit length
                })

# Deduplicate by file+number+first 100 chars
seen = set()
unique_results = []
for r in results:
    key = (r['file'], r['number'], r['question'][:100])
    if key not in seen:
        seen.add(key)
        unique_results.append(r)

# Write results
output_path = Path(r'C:\Users\austi\Desktop\MATH TRAINER\edge_case_exercises.md')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('# Edge Case & Weird Exercise Questions\n\n')
    out.write(f'Found {len(unique_results)} candidate exercises across {len(files)} chunks.\n\n')
    
    # Group by tag
    by_tag = {}
    for r in unique_results:
        for tag in r['tags']:
            by_tag.setdefault(tag, []).append(r)
    
    for tag, items in sorted(by_tag.items()):
        out.write(f'## {tag}\n\n')
        for r in items[:20]:  # Limit per tag
            out.write(f"**{r['file']}** — Q{r['number']}\n")
            out.write(f"```\n{r['question']}\n```\n\n")
        if len(items) > 20:
            out.write(f'... and {len(items)-20} more.\n\n')
        out.write('---\n\n')

print(f"Found {len(unique_results)} unique candidate exercises.")
print(f"Results written to {output_path}")
