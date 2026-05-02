# ── Static derive-mode problem library ──
# Matched by method name.  Each entry is a dict with problem text + steps.

DERIVE_CALC1 = {
    "limit_definition": {
        "theorem": "Limit of a linear function",
        "problem": "Using the epsilon-delta definition, prove that $\\lim_{x \\to a} (bx + c) = ba + c$ for constants $b$ and $c$.",
        "steps": [
            {"label": "State the definition", "math": "\\forall \\varepsilon > 0, \\exists \\delta > 0 \\text{ such that } 0 < |x - a| < \\delta \\implies |(bx+c) - (ba+c)| < \\varepsilon", "note": "Start with the formal definition"},
            {"label": "Simplify the difference", "math": "|(bx+c) - (ba+c)| = |b(x-a)| = |b||x-a|", "note": "Factor out $b$"},
            {"label": "Choose delta", "math": "\\delta = \\varepsilon / |b| \\text{ (if } b \\neq 0\\text{)}", "note": "For $b=0$, any $\\delta$ works"},
            {"label": "Verify", "math": "0 < |x-a| < \\varepsilon/|b| \\implies |b||x-a| < \\varepsilon", "note": "QED"},
        ],
    },
    "product_rule": {
        "theorem": "Product Rule",
        "problem": "Prove $\\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)$ using the limit definition of the derivative. Then apply it to $2x^2 \\sin(x)$.",
        "steps": [
            {"label": "Write the difference quotient", "math": "\\frac{f(x+h)g(x+h) - f(x)g(x)}{h}", "note": "Limit definition"},
            {"label": "Add and subtract", "math": "\\frac{f(x+h)g(x+h) - f(x+h)g(x) + f(x+h)g(x) - f(x)g(x)}{h}", "note": "Clever zero"},
            {"label": "Factor", "math": "f(x+h)\\frac{g(x+h)-g(x)}{h} + g(x)\\frac{f(x+h)-f(x)}{h}", "note": "Split the limit"},
            {"label": "Take limits", "math": "f(x)g'(x) + g(x)f'(x)", "note": "Use continuity of $f$"},
        ],
    },
    "quotient_rule": {
        "theorem": "Quotient Rule",
        "problem": "Derive the quotient rule for $\\frac{d}{dx}[f(x)/g(x)]$ from the product rule and chain rule.",
        "steps": [
            {"label": "Rewrite as product", "math": "f(x) \\cdot [g(x)]^{-1}", "note": "Use negative exponent"},
            {"label": "Apply product rule", "math": "f'(x)[g(x)]^{-1} + f(x) \\cdot \\frac{d}{dx}[g(x)]^{-1}", "note": ""},
            {"label": "Apply chain rule", "math": "f'(x)[g(x)]^{-1} + f(x) \\cdot (-1)[g(x)]^{-2}g'(x)", "note": ""},
            {"label": "Simplify", "math": "\\frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}", "note": "Common denominator"},
        ],
    },
    "chain_rule": {
        "theorem": "Chain Rule",
        "problem": "Prove $\\frac{d}{dx}[f(g(x))] = f'(g(x))g'(x)$ using the limit definition. State where continuity is required.",
        "steps": [
            {"label": "Difference quotient", "math": "\\lim_{h \\to 0} \\frac{f(g(x+h)) - f(g(x))}{h}", "note": ""},
            {"label": "Multiply by 1", "math": "\\lim_{h \\to 0} \\frac{f(g(x+h)) - f(g(x))}{g(x+h)-g(x)} \\cdot \\frac{g(x+h)-g(x)}{h}", "note": "Valid when $g(x+h) \\neq g(x)$"},
            {"label": "Identify limits", "math": "f'(g(x)) \\cdot g'(x)", "note": "Use continuity of $g$ to handle the $g(x+h)=g(x)$ case"},
        ],
    },
    "ftc_part1": {
        "theorem": "Fundamental Theorem of Calculus, Part 1",
        "problem": "Derive $\\frac{d}{dx} \\int_a^x f(t) \\, dt = f(x)$. State the continuity requirement.",
        "steps": [
            {"label": "Define $F(x)$", "math": "F(x) = \\int_a^x f(t) \\, dt", "note": ""},
            {"label": "Difference quotient", "math": "\\frac{F(x+h) - F(x)}{h} = \\frac{1}{h} \\int_x^{x+h} f(t) \\, dt", "note": ""},
            {"label": "Apply MVT for integrals", "math": "\\frac{1}{h} \\int_x^{x+h} f(t) \\, dt = f(c) \\text{ for some } c \\in [x, x+h]", "note": "Requires $f$ continuous on $[x, x+h]$"},
            {"label": "Take limit", "math": "\\lim_{h \\to 0} f(c) = f(x)", "note": "As $h \\to 0$, $c \\to x$ by continuity"},
        ],
    },
    "ftc_part2": {
        "theorem": "Fundamental Theorem of Calculus, Part 2",
        "problem": "Prove $\\int_a^b f(x) \\, dx = F(b) - F(a)$ where $F$ is any antiderivative of $f$.",
        "steps": [
            {"label": "Define $G(x)$", "math": "G(x) = \\int_a^x f(t) \\, dt", "note": ""},
            {"label": "By FTC Part 1", "math": "G'(x) = f(x)", "note": "So $G$ is an antiderivative"},
            {"label": "Antiderivatives differ by constant", "math": "F(x) = G(x) + C", "note": ""},
            {"label": "Evaluate at bounds", "math": "F(b) - F(a) = [G(b)+C] - [G(a)+C] = G(b) - G(a) = \\int_a^b f(t)\\,dt", "note": "QED"},
        ],
    },
    "mean_value_theorem": {
        "theorem": "Mean Value Theorem",
        "problem": "Prove the Mean Value Theorem: if $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, then $\\exists c \\in (a,b)$ such that $f'(c) = \\frac{f(b)-f(a)}{b-a}$.",
        "steps": [
            {"label": "Define auxiliary function", "math": "g(x) = f(x) - \\left[ \\frac{f(b)-f(a)}{b-a}(x-a) + f(a) \\right]", "note": "Secant line subtracted"},
            {"label": "Check $g(a)$ and $g(b)$", "math": "g(a) = 0, \\quad g(b) = 0", "note": ""},
            {"label": "Apply Rolle's Theorem", "math": "\\exists c \\in (a,b) \\text{ with } g'(c) = 0", "note": "Requires $g$ continuous on $[a,b]$ and differentiable on $(a,b)$"},
            {"label": "Compute $g'(c)$", "math": "g'(c) = f'(c) - \\frac{f(b)-f(a)}{b-a} = 0", "note": "Rearrange to get MVT"},
        ],
    },
    "rolles_theorem": {
        "theorem": "Rolle's Theorem",
        "problem": "Prove Rolle's Theorem: if $f$ is continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a)=f(b)$, then $\\exists c \\in (a,b)$ with $f'(c)=0$.",
        "steps": [
            {"label": "Extreme Value Theorem", "math": "f \\text{ attains a max and min on } [a,b]", "note": "Because $f$ is continuous"},
            {"label": "Case 1: max or min inside $(a,b)$", "math": "\\text{If } f \\text{ is not constant, at least one extremum is in } (a,b)", "note": ""},
            {"label": "Fermat's Theorem", "math": "\\text{At an interior extremum } c, \\quad f'(c) = 0", "note": "Requires differentiability at $c$"},
            {"label": "Case 2: $f$ constant", "math": "f'(x) = 0 \\text{ for all } x \\in (a,b)", "note": "Trivially satisfied"},
        ],
    },
    "lhopital": {
        "theorem": "L'Hôpital's Rule",
        "problem": "State and prove L'Hôpital's Rule for the $\\frac{0}{0}$ case as $x \\to a$.",
        "steps": [
            {"label": "State the rule", "math": "\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)} \\text{ if } \\frac{0}{0} \\text{ form}", "note": "Provided the right-hand limit exists"},
            {"label": "Use Cauchy MVT", "math": "\\frac{f(x)-f(a)}{g(x)-g(a)} = \\frac{f'(c)}{g'(c)} \\text{ for some } c \\in (a,x)", "note": "Requires $f,g$ continuous at $a$ and differentiable nearby"},
            {"label": "Take limit", "math": "\\text{As } x \\to a, c \\to a, \\text{ so } \\frac{f'(c)}{g'(c)} \\to L", "note": ""},
        ],
    },
    "riemann_sum": {
        "theorem": "Definite integral as a limit of Riemann sums",
        "problem": "Prove $\\int_a^b x \\, dx = \\frac{b^2-a^2}{2}$ using the definition of the definite integral as a limit of Riemann sums.",
        "steps": [
            {"label": "Partition", "math": "\\Delta x = \\frac{b-a}{n}, \\quad x_i = a + i\\Delta x", "note": ""},
            {"label": "Riemann sum", "math": "\\sum_{i=1}^n x_i \\Delta x = \\sum_{i=1}^n \\left(a + i\\frac{b-a}{n}\\right)\\frac{b-a}{n}", "note": ""},
            {"label": "Split the sum", "math": "a(b-a) + \\frac{(b-a)^2}{n^2} \\sum_{i=1}^n i", "note": ""},
            {"label": "Use formula", "math": "\\sum_{i=1}^n i = \\frac{n(n+1)}{2}", "note": ""},
            {"label": "Simplify and take limit", "math": "a(b-a) + \\frac{(b-a)^2}{2} \\cdot \\frac{n+1}{n} \\to a(b-a) + \\frac{(b-a)^2}{2} = \\frac{b^2-a^2}{2}", "note": "QED"},
        ],
    },
    "integration_by_parts": {
        "theorem": "Integration by Parts",
        "problem": "Derive $\\int u \\, dv = uv - \\int v \\, du$ from the product rule.",
        "steps": [
            {"label": "Start with product rule", "math": "\\frac{d}{dx}[u(x)v(x)] = u'(x)v(x) + u(x)v'(x)", "note": ""},
            {"label": "Integrate both sides", "math": "u(x)v(x) = \\int u'(x)v(x)\\,dx + \\int u(x)v'(x)\\,dx", "note": ""},
            {"label": "Rearrange", "math": "\\int u(x)v'(x)\\,dx = u(x)v(x) - \\int u'(x)v(x)\\,dx", "note": ""},
            {"label": "Substitute $dv = v'(x)dx$, $du = u'(x)dx$", "math": "\\int u \\, dv = uv - \\int v \\, du", "note": "QED"},
        ],
    },
}

# Flat lookup by method name
def get_derive_entry(method):
    return DERIVE_CALC1.get(method)
