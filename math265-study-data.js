const STUDY_DATA = {
  factoring: {
    searches: {
      1: ['factor GCF algebra tutorial', 'difference of squares factoring', 'factor trinomials x squared bx c'],
      2: ['AC method factoring trinomials', 'factor trinomials leading coefficient', 'trial and error factoring ax2+bx+c'],
      3: ['factoring by grouping 4 terms', 'sum difference of cubes factoring', 'factor completely algebra tutorial'],
      4: ['factoring GCF negative fractional exponents', 'factor variable out GCF', 'advanced factoring trig expressions'],
      5: ['trig trinomial factoring sin cos', 'u-substitution factoring disguised quadratic', 'advanced polynomial factoring techniques'],
    },
    prompts: {
      1: 'I am learning to factor polynomials at the introductory level: GCF factoring, difference of squares, and simple trinomials (x²+bx+c where the leading coefficient is 1). Teach me each technique step by step with 2 worked examples each. Then give me 3 practice problems to try.',
      2: 'I am learning to factor trinomials where the leading coefficient is not 1, like ax²+bx+c, using the AC method or trial and error. Walk me through the technique with 2 full examples, then give me 3 practice problems.',
      3: 'I am learning to factor by grouping (4-term polynomials) and to factor sum/difference of cubes (a³±b³). Explain both techniques with 2 examples each, then give me 3 practice problems.',
      4: 'I am learning advanced factoring: pulling out a GCF that contains fractional or negative exponents, and factoring expressions with trig functions. Show me 2 examples, explain the strategy, then give me 3 practice problems.',
      5: 'I am learning to factor trig trinomials like 2sin²x+5sinx+3 and to recognize disguised quadratics that need u-substitution before factoring. Walk me through the technique with 2 examples, then quiz me with 3 challenging problems.',
    }
  },
  exponents: {
    searches: {
      1: ['exponent rules product quotient power tutorial', 'multiplying dividing same base exponents', 'zero and one exponent rules'],
      2: ['negative exponents rewrite without negative', 'rational fractional exponents tutorial', 'negative exponent to fraction'],
      3: ['radical notation to rational exponent form', 'nth root as fractional exponent', 'convert between radicals and exponents'],
      4: ['fractional exponent arithmetic multiply divide', 'simplify expressions with rational exponents', 'add subtract fractional exponents same base'],
      5: ['higher index radicals cube 4th root simplify', 'complex radical expression simplification', 'advanced rational exponents algebra'],
    },
    prompts: {
      1: 'I am learning the basic exponent rules: product rule (x^a·x^b = x^(a+b)), quotient rule, power rule ((x^a)^b = x^(ab)), and rules for 0 and 1 as exponents. Explain each rule clearly with 2 examples, then give me 3 practice problems.',
      2: 'I am learning negative exponents and how to rewrite expressions so all exponents are positive. Teach me the rule x^(-n) = 1/x^n with 2 examples including fraction bases, then give me 3 practice problems.',
      3: 'I am learning to convert between radical notation and rational exponent form, for example ⁿ√(x^m) = x^(m/n). Explain the conversion rule with 2 examples in both directions, then give me 3 practice problems.',
      4: 'I am learning arithmetic with fractional exponents — multiplying, dividing, and simplifying expressions like x^(2/3) · x^(1/2). Teach me the rules with 2 worked examples, then give me 3 practice problems.',
      5: 'I am learning to simplify complex radical expressions with higher indices (cube roots, 4th roots) and multiple variable factors. Walk me through the simplification strategy with 2 full examples, then give me 3 challenging practice problems.',
    }
  },
  fractions: {
    searches: {
      1: ['adding subtracting fractions find LCD', 'dividing fractions multiply by reciprocal', 'simplify fractions reduce GCF'],
      2: ['simplifying rational expressions factor cancel', 'cancel common factors numerator denominator', 'rational expressions algebra tutorial'],
      3: ['adding rational expressions unlike denominators LCD', 'LCD rational expressions polynomial', 'complex fractions simplify algebra'],
      4: ['rational expressions multi-step simplification', 'factor polynomials rational expression simplify', 'algebra rational expressions factoring'],
      5: ['three term rational expressions LCD', 'complex rational expressions advanced', 'polynomial rational expressions advanced algebra'],
    },
    prompts: {
      1: 'I am learning to add, subtract, and divide basic fractions including finding the least common denominator. Teach me each operation with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to simplify rational expressions by factoring the numerator and denominator then canceling common factors. Walk me through the factor-then-cancel technique with 2 examples, then give me 3 practice problems.',
      3: 'I am learning to add and subtract rational expressions with different denominators by finding the LCD and combining. Walk me through the full process with 2 examples, then give me 3 practice problems.',
      4: 'I am learning to simplify multi-step rational expressions that require fully factoring polynomials in both numerator and denominator. Show me the complete process with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to work with complex rational expressions involving three or more terms, polynomial denominators, and multi-step factoring. Walk me through 2 challenging examples completely, then give me 3 practice problems.',
    }
  },
  trig: {
    searches: {
      1: ['unit circle sin cos tan exact values tutorial', 'memorize unit circle fast trick', 'trig values 0 30 45 60 90 degrees'],
      2: ['trig values all four quadrants reference angle', 'ASTC rule all students take calculus', 'find exact trig value any angle'],
      3: ['trig identities tutorial Pythagorean', 'solving trig equations general solution', 'trig with radians unit circle'],
    },
    prompts: {
      1: 'I am learning the unit circle: the exact values of sin, cos, and tan at the standard angles (0°, 30°, 45°, 60°, 90°). Teach me a memory trick or pattern, explain why the values are what they are, then quiz me on 6 specific values.',
      2: 'I am learning to find exact trig values for any angle in all four quadrants using reference angles and the ASTC sign rule. Explain the method step by step with 3 examples spread across different quadrants, then quiz me with 5 problems.',
      3: 'I am learning to apply trig identities (Pythagorean, reciprocal, quotient) and solve basic trig equations. Explain each identity and when to use it, walk me through 2 equation examples, then give me 3 practice problems.',
    }
  },
  logs: {
    searches: {
      1: ['logarithm rules product quotient power tutorial', 'log base definition b to y equals x', 'natural log ln tutorial'],
      2: ['expanding logarithms tutorial step by step', 'condensing log expressions into one log', 'change of base formula logarithm'],
      3: ['solving logarithmic equations algebra', 'exponential equations solve using logarithms', 'log equations precalculus tutorial'],
    },
    prompts: {
      1: 'I am learning the fundamental logarithm rules: log(ab)=log(a)+log(b), log(a/b)=log(a)−log(b), log(a^n)=n·log(a), and the definition logb(x)=y ↔ b^y=x. Teach each rule with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to expand and condense logarithmic expressions using log properties. Show me both directions — expanding a single log into sum/difference and condensing a sum/difference into a single log — with 2 examples each, then give me 3 practice problems.',
      3: 'I am learning to solve logarithmic and exponential equations by converting between log and exponential form and isolating the variable. Walk me through 2 solved examples step by step, then give me 3 practice problems.',
    }
  },
  composition: {
    searches: {
      1: ['function composition f of g of x tutorial', 'composite functions how to compute', 'f(g(x)) step by step algebra'],
      2: ['evaluating composite functions at a value', 'domain of composite function', 'decompose function into f and g'],
      3: ['composition with trig log exponential functions', 'inverse function composition verify', 'advanced function composition precalculus'],
    },
    prompts: {
      1: 'I am learning function composition: how to compute f(g(x)) and g(f(x)) and why the order matters. Explain the substitution process with 2 examples showing both f∘g and g∘f, then give me 3 practice problems.',
      2: 'I am learning to evaluate composite functions at specific values (like f(g(3))) and to find the domain of a composite function. Show 2 examples of each type, then give me 3 practice problems.',
      3: 'I am learning to compose functions involving trig, logarithmic, and exponential functions, and how to decompose a given composite into its component functions. Walk me through 2 examples, then give me 3 practice problems.',
    }
  },
  limits: {
    searches: {
      1: ['limits calculus introduction what is a limit', 'direct substitution limits tutorial', 'evaluating limits by substitution'],
      2: ['limits by factoring 0 over 0 indeterminate form', 'conjugate method limits square root', 'algebraic manipulation to evaluate limits'],
      3: ['limits at infinity horizontal asymptotes', 'divide by highest power limits at infinity', 'squeeze theorem limits calculus'],
      4: ['one-sided limits piecewise functions calculus', 'left and right hand limits', 'limit laws and limit rules calculus'],
    },
    prompts: {
      1: 'I am learning the concept of limits in calculus and how to evaluate limits using direct substitution. Explain intuitively what a limit means and when direct substitution works, with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to evaluate limits that give the indeterminate form 0/0 by factoring and canceling or using the conjugate method. Walk me through each technique with 2 full examples, then give me 3 practice problems.',
      3: 'I am learning to evaluate limits as x→∞ or x→−∞ by dividing through by the highest power of x to find horizontal asymptotes. Explain the strategy with 2 examples, then give me 3 practice problems.',
      4: 'I am learning one-sided limits (left-hand and right-hand) and how to use them to determine whether a limit exists for piecewise functions. Explain the concept with 2 examples, then give me 3 practice problems.',
    }
  },
  derivatives: {
    searches: {
      1: ['power rule derivatives tutorial calculus', 'derivative of polynomial function', 'basic differentiation rules constants sum'],
      2: ['product rule differentiation tutorial with examples', 'quotient rule calculus tutorial', 'when to use product vs quotient rule'],
      3: ['chain rule calculus tutorial step by step', 'chain rule with trig functions examples', 'outside inside rule chain rule'],
      4: ['implicit differentiation tutorial calculus', 'derivatives of ln x and e^x', 'logarithmic differentiation technique'],
      5: ['product rule quotient rule chain rule combined', 'higher order derivatives calculus', 'advanced differentiation techniques'],
    },
    prompts: {
      1: 'I am learning the power rule for differentiation: d/dx[x^n] = nx^(n-1), along with the constant rule and sum/difference rule. Explain each clearly with 2 worked examples including polynomials with multiple terms, then give me 3 practice problems.',
      2: 'I am learning the product rule and quotient rule for differentiation. State each formula, show 2 worked examples for each, and explain how to decide which to use, then give me 3 practice problems mixing both rules.',
      3: 'I am learning the chain rule for differentiating composite functions. Explain the outside-inside rule with 2 full examples including trig functions, then give me 3 practice problems.',
      4: 'I am learning implicit differentiation and differentiation of exponential and logarithmic functions (d/dx[ln x] = 1/x, d/dx[e^x] = e^x). Walk me through 2 examples of each type, then give me 3 practice problems.',
      5: 'I am learning to differentiate complex functions that require combining the product rule, quotient rule, and chain rule in a single problem. Walk me through 2 multi-rule examples completely, identifying each rule used at each step, then give me 3 challenging problems.',
    }
  },
  integration: {
    searches: {
      1: ['antiderivative rules calculus power rule integral', 'indefinite integral tutorial calculus', 'basic integration formulas list'],
      2: ['u-substitution integration tutorial step by step', 'how to choose u in u-substitution', 'u-sub integration calculus examples'],
      3: ['integrating trig functions sin cos tutorial', 'definite integral evaluation calculus', 'integration techniques calculus overview'],
    },
    prompts: {
      1: 'I am learning basic antiderivative rules for integration: the power rule ∫x^n dx = x^(n+1)/(n+1)+C, the constant multiple rule, and the sum rule. Explain each rule with 2 examples and clarify the +C, then give me 3 practice problems.',
      2: 'I am learning u-substitution for integration. Teach me how to choose u, compute du, rewrite the integral, integrate, and back-substitute, walking through 2 complete examples. Then give me 3 practice problems.',
      3: 'I am learning to integrate trigonometric functions (sin x, cos x, sec²x, etc.) and evaluate definite integrals. Walk me through 2 examples of trig integration and 1 definite integral, then give me 3 practice problems.',
    }
  },
  adv_integration: {
    searches: {
      1: ['integration by parts tutorial LIATE rule', 'int u dv formula derivation calculus', 'integration by parts step by step examples'],
      2: ['trig substitution integration when to use', 'partial fractions integration tutorial setup', 'calculus 2 integration techniques overview'],
      3: ['repeated integration by parts tabular method', 'partial fraction decomposition full examples', 'advanced integration by parts calculus 2'],
      4: ['improper integrals convergence divergence', 'powers of sin cos integral reduction', 'trig integral sin^m cos^n strategy'],
      5: ['calculus 2 integration strategy which method to use', 'tabular integration by parts shortcut', 'complete integration techniques review calculus 2'],
    },
    prompts: {
      1: 'I am learning integration by parts using ∫u dv = uv − ∫v du and the LIATE rule for choosing u. Explain the method thoroughly with 2 fully worked examples, then give me 3 practice problems.',
      2: 'I am learning trig substitution and partial fraction decomposition as integration techniques. Explain when each method applies, show 1 example each, then give me 3 practice problems.',
      3: 'I am learning advanced integration by parts including repeated application and the tabular (repeated IBP) shortcut. Walk me through 2 complex examples, then give me 3 challenging practice problems.',
      4: 'I am learning to evaluate improper integrals using limits and to integrate powers of trig functions like ∫sin^m(x)cos^n(x)dx. Explain the strategy for each type with 2 examples, then give me 3 practice problems.',
      5: 'I want a comprehensive review of all calculus 2 integration techniques: u-substitution, integration by parts, trig sub, partial fractions, and trig integrals. For each, give me the key identification signal and 1 example, then give me 5 mixed problems where I must identify which technique to use.',
    }
  },
  polynomials: {
    searches: {
      1: ['classify polynomial by degree name', 'identify polynomial coefficients standard form', 'polynomial terminology degree leading coefficient'],
      2: ['adding and subtracting polynomials like terms', 'polynomial addition and subtraction tutorial', 'combining like terms polynomials'],
      3: ['FOIL method multiplying binomials', 'special products squared binomial expansion', 'multiply polynomials step by step'],
      4: ['synthetic division polynomial tutorial', 'divide polynomial by binomial synthetic', 'synthetic division step by step examples'],
      5: ['factor theorem polynomial roots', 'remainder theorem synthetic division', 'fully factor polynomial using factor theorem'],
    },
    prompts: {
      1: 'I am learning to classify polynomials by degree (constant, linear, quadratic, cubic, quartic) and identify coefficients from standard form. Explain the terminology with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to add and subtract polynomials by grouping like terms. Walk me through the process with 2 examples including distributing the negative sign, then give me 3 practice problems.',
      3: 'I am learning to multiply polynomials using the FOIL method for binomials and special product formulas like (a+b)². Show 2 examples of each, then give me 3 practice problems.',
      4: 'I am learning synthetic division to divide a polynomial by a linear factor (x-c). Explain the algorithm step by step with 2 full examples, then give me 3 practice problems.',
      5: 'I am learning the Factor Theorem: if f(c)=0 then (x-c) is a factor. Show me how to use synthetic division to find roots and fully factor a polynomial with 2 examples, then give me 3 practice problems.',
    }
  },
  linear_equations: {
    searches: {
      1: ['solving one step two step linear equations', 'solve linear equations with fractions', 'isolating variable algebra tutorial'],
      2: ['translating word problems to algebra equations', 'two step word problems algebra', 'consecutive integer word problems algebra'],
      3: ['solving literal equations for a variable', 'rearrange formulas algebra tutorial', 'solve formula for specified variable'],
      4: ['solving linear inequalities flip sign', 'inequality notation algebra tutorial', 'one variable inequalities step by step'],
      5: ['consecutive integer word problems algebra', 'age word problems algebra equations', 'multi step word problems algebra tutorial'],
    },
    prompts: {
      1: 'I am learning to solve basic linear equations like ax+b=c and equations with fractions like (x+n)/d = rhs. Explain the isolation steps with 2 examples each, then give me 3 practice problems.',
      2: 'I am learning to translate word problems into algebra equations and solve them, such as "a number multiplied by 5 equals 35." Show 2 examples of translating and solving, then give me 3 word problems to try.',
      3: 'I am learning to solve literal equations — isolating a specific variable in a formula with multiple variables, like solving PV=nRT for T. Walk me through 2 examples, then give me 3 practice problems.',
      4: 'I am learning to solve linear inequalities and when to flip the inequality sign (when multiplying/dividing by a negative). Explain with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to set up and solve multi-step word problems involving consecutive integers and age relationships. Show me how to define variables and set up equations with 2 examples, then give me 3 practice problems.',
    }
  },
  sequences: {
    searches: {
      1: ['arithmetic sequence formula nth term', 'sum of arithmetic series formula', 'common difference arithmetic sequence'],
      2: ['geometric sequence formula nth term', 'sum of geometric series formula', 'common ratio geometric sequence'],
      3: ['infinite geometric series sum formula', 'convergence of geometric series', 'when does geometric series converge'],
      4: ['arithmetic sequence word problems', 'arithmetic series real world applications', 'sequences word problems algebra'],
      5: ['identify arithmetic vs geometric sequence', 'determine if sequence is arithmetic or geometric', 'sequence pattern recognition algebra'],
    },
    prompts: {
      1: 'I am learning arithmetic sequences: finding the nth term using a_n = a_1 + (n-1)d and the sum formula S_n = n(a_1 + a_n)/2. Explain each formula with 2 examples, then give me 3 practice problems.',
      2: 'I am learning geometric sequences: finding the nth term using a_n = a_1 · r^(n-1) and the sum formula S_n = a_1(r^n - 1)/(r - 1). Explain with 2 examples, then give me 3 practice problems.',
      3: 'I am learning the infinite geometric series formula S = a_1/(1-r) and the convergence condition |r| < 1. Explain when a geometric series converges with 2 examples, then give me 3 practice problems.',
      4: 'I am learning to apply arithmetic sequence formulas to word problems, like finding weights in a pattern or total items in a series. Walk me through 2 word problems completely, then give me 3 practice problems.',
      5: 'I am learning to identify whether a given sequence is arithmetic (constant difference) or geometric (constant ratio) from its terms. Show me the test method with 2 examples of each type, then give me 5 sequences to classify.',
    }
  },
  quadratic: {
    searches: {
      1: ['solving quadratic equations by factoring', 'zero product property tutorial', 'difference of squares quadratic'],
      2: ['quadratic formula step by step tutorial', 'solving quadratic word problems area', 'quadratic formula examples'],
      3: ['completing the square tutorial step by step', 'how to complete the square algebra', 'solve quadratic by completing the square'],
      4: ['discriminant quadratic equation solutions', 'b squared minus 4ac meaning', 'number of real solutions discriminant'],
      5: ['vertex of a parabola formula', 'find maximum minimum of quadratic function', 'vertex form of quadratic equation'],
    },
    prompts: {
      1: 'I am learning to solve quadratic equations by factoring and using the zero product property. Explain the process with 2 examples including difference of squares, then give me 3 practice problems.',
      2: 'I am learning to use the quadratic formula x = (-b ± √(b²-4ac))/(2a) and to set up quadratic word problems involving area. Show 2 examples of each, then give me 3 practice problems.',
      3: 'I am learning to solve quadratic equations by completing the square. Walk me through the full process: move constant, add (b/2)² to both sides, take square root. Show 2 complete examples, then give me 3 practice problems.',
      4: 'I am learning to use the discriminant Δ = b²-4ac to determine the number of real solutions (Δ>0: two, Δ=0: one, Δ<0: none). Explain with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to find the vertex of a parabola using x = -b/(2a) and determine whether it is a maximum or minimum. Show 2 complete examples, then give me 3 practice problems.',
    }
  },
  radicals: {
    searches: {
      1: ['simplifying square roots perfect squares', 'rationalize denominator square root tutorial', 'simplify radicals step by step'],
      2: ['adding and subtracting radicals like terms', 'combining like radicals tutorial', 'simplify radical expressions addition subtraction'],
      3: ['multiplying radicals FOIL with radicals', 'distributive property with square roots', 'multiply radical expressions tutorial'],
      4: ['solving radical equations square root', 'extraneous solutions radical equations', 'isolate square root and square both sides'],
      5: ['rational exponents tutorial fractional powers', 'convert radicals to rational exponents', 'evaluate fractional exponents step by step'],
    },
    prompts: {
      1: 'I am learning to simplify square roots by factoring out perfect squares and to rationalize denominators. Show 2 examples of each technique, then give me 3 practice problems.',
      2: 'I am learning to add and subtract radicals by combining like terms (same radicand). Explain the process with 2 examples, then give me 3 practice problems.',
      3: 'I am learning to multiply radicals using the product rule √a·√b = √(ab) and FOIL with radical expressions. Show 2 examples of each, then give me 3 practice problems.',
      4: 'I am learning to solve radical equations by isolating the square root and squaring both sides, including checking for extraneous solutions. Walk me through 2 complete examples, then give me 3 practice problems.',
      5: 'I am learning to evaluate rational exponents like 8^(2/3) and convert between radical and exponent notation. Explain the rule a^(m/n) = ⁿ√(a^m) with 2 examples each direction, then give me 3 practice problems.',
    }
  },
  rational_expressions: {
    searches: {
      1: ['simplifying rational expressions factor cancel', 'cancel common factors rational expressions', 'domain restrictions rational expressions'],
      2: ['multiplying rational expressions tutorial', 'dividing rational expressions multiply reciprocal', 'simplify before multiplying rational expressions'],
      3: ['adding rational expressions LCD', 'subtracting rational expressions common denominator', 'LCD polynomial denominators'],
      4: ['simplifying complex fractions algebra', 'complex rational expressions tutorial', 'fractions within fractions simplify'],
      5: ['solving rational equations LCD method', 'rate word problems rational equations', 'work problems algebra tutorial'],
    },
    prompts: {
      1: 'I am learning to simplify rational expressions by factoring the numerator and denominator, then canceling common factors. Explain the process with 2 examples including domain restrictions, then give me 3 practice problems.',
      2: 'I am learning to multiply and divide rational expressions by canceling common factors first and multiplying by the reciprocal for division. Show 2 examples of each, then give me 3 practice problems.',
      3: 'I am learning to add and subtract rational expressions by finding the LCD of polynomial denominators. Walk me through the full process with 2 examples, then give me 3 practice problems.',
      4: 'I am learning to simplify complex fractions (fractions within fractions) by rewriting numerator and denominator as single fractions, then dividing. Show 2 complete examples, then give me 3 practice problems.',
      5: 'I am learning to solve rational equations by multiplying through by the LCD, and to set up rate/work word problems. Walk me through 2 examples of each type, then give me 3 practice problems.',
    }
  },
  inequalities: {
    searches: {
      1: ['solving linear inequalities flip sign negative', 'one step inequalities tutorial', 'inequality rules algebra'],
      2: ['compound inequalities AND OR tutorial', 'interval notation tutorial algebra', 'solving three part inequalities'],
      3: ['solving quadratic inequalities sign chart', 'quadratic inequality test intervals', 'parabola method quadratic inequalities'],
      4: ['solving rational inequalities critical points', 'sign chart rational expressions tutorial', 'test intervals rational inequalities'],
      5: ['interval notation solutions inequalities', 'inequality word problems algebra', 'at most at least inequality translation'],
    },
    prompts: {
      1: 'I am learning to solve linear inequalities and when to flip the inequality sign (when multiplying or dividing by a negative). Explain with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to solve compound inequalities (AND and OR types) and write solutions in interval notation. Show 2 examples of each type, then give me 3 practice problems.',
      3: 'I am learning to solve quadratic inequalities by factoring, finding roots, and determining the sign between and outside the roots. Walk me through 2 complete examples, then give me 3 practice problems.',
      4: 'I am learning to solve rational inequalities by finding critical points (where numerator=0 and denominator=0) and using a sign chart. Show 2 complete examples, then give me 3 practice problems.',
      5: 'I am learning to write inequality solutions in interval notation and to translate word problems with phrases like "at most" and "at least" into inequalities. Show 2 examples of each, then give me 3 practice problems.',
    }
  },
  absolute_value: {
    searches: {
      1: ['solving absolute value equations two cases', 'absolute value equals negative no solution', 'split absolute value into two equations'],
      2: ['absolute value inequalities less than between', 'absolute value inequalities greater than outside', 'solve |ax+b| < c and |ax+b| > c'],
      3: ['compound absolute value equations', 'two absolute values equation tutorial', 'case analysis absolute value algebra'],
      4: ['absolute value as distance on number line', 'geometric meaning of absolute value', 'distance formula one dimension'],
      5: ['absolute value inequalities interval notation', 'distance between two points formula', 'absolute value word problems'],
    },
    prompts: {
      1: 'I am learning to solve absolute value equations |ax+b| = c by splitting into two cases, and recognizing no-solution cases when |expression| = negative. Show 2 examples including a no-solution case, then give me 3 practice problems.',
      2: 'I am learning to solve absolute value inequalities: |ax+b| < c becomes a compound inequality -c < ax+b < c, and |ax+b| > c becomes two separate cases. Show 2 examples of each, then give me 3 practice problems.',
      3: 'I am learning to solve equations with multiple absolute values like |x| + |x-2| = 6 using case analysis by intervals. Walk me through 2 complete examples, then give me 3 practice problems.',
      4: 'I am learning the geometric interpretation of absolute value as distance: |x - a| = d means x is exactly d units from a on the number line. Explain with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to solve absolute value inequalities with ≤ and write answers in interval notation, and to find the distance between two points using |b - a|. Show 2 examples of each, then give me 3 practice problems.',
    }
  },
  systems: {
    searches: {
      1: ['solving systems by substitution tutorial', 'substitution method systems of equations', 'nonlinear system substitution quadratic'],
      2: ['solving systems by elimination method', 'elimination method add subtract equations', 'multiply to align coefficients elimination'],
      3: ['systems of three variables tutorial', 'solve 3x3 system of equations', 'three variable elimination substitution'],
      4: ['systems of equations word problems tickets', 'mixture problems systems of equations', 'setting up systems from word problems'],
      5: ['inconsistent dependent systems of equations', 'no solution infinite solutions systems', 'classify system unique inconsistent dependent'],
    },
    prompts: {
      1: 'I am learning to solve systems of equations by substitution, including nonlinear systems where one equation is quadratic. Explain the process with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to solve systems by elimination: adding or subtracting equations to eliminate a variable, and multiplying to align coefficients. Show 2 examples of each, then give me 3 practice problems.',
      3: 'I am learning to solve systems of three variables with three equations using a combination of substitution and elimination. Walk me through 2 complete examples, then give me 3 practice problems.',
      4: 'I am learning to set up and solve systems of equations from word problems, like ticket sales with two types. Show me how to define variables and set up equations with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to classify systems as having a unique solution, no solution (inconsistent), or infinitely many solutions (dependent). Explain how to check by comparing equations with 2 examples, then give me 5 systems to classify.',
    }
  },
  probability: {
    searches: {
      1: ['basic probability favorable over total outcomes', 'complement rule probability 1 minus P', 'probability of an event tutorial'],
      2: ['independent events probability multiply', 'dependent events without replacement probability', 'conditional probability dependent events'],
      3: ['conditional probability formula P(B|A)', 'Bayes theorem introduction probability', 'given that probability tutorial'],
      4: ['permutations vs combinations tutorial', 'nCr nPr when to use which', 'counting principles probability'],
      5: ['expected value probability tutorial', 'weighted average probability outcomes', 'expected value formula examples'],
    },
    prompts: {
      1: 'I am learning basic probability: P(E) = favorable outcomes / total outcomes, and the complement rule P(E\') = 1 - P(E). Explain with 2 examples, then give me 3 practice problems.',
      2: 'I am learning the difference between independent events (P(A and B) = P(A)·P(B)) and dependent events without replacement. Show 2 examples of each, then give me 3 practice problems.',
      3: 'I am learning conditional probability: P(B|A) = P(A and B) / P(A). Explain the concept and formula with 2 worked examples, then give me 3 practice problems.',
      4: 'I am learning the difference between permutations P(n,r) = n!/(n-r)! (order matters) and combinations C(n,r) = n!/(r!(n-r)!) (order does not matter). Explain when to use each with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to calculate expected value: E(X) = Σ x·P(x), the weighted average of all possible outcomes. Walk me through 2 complete examples, then give me 3 practice problems.',
    }
  },
  asymptotes: {
    searches: {
      1: ['horizontal asymptotes degree numerator denominator', 'horizontal asymptote rules rational functions', 'leading coefficient ratio horizontal asymptote'],
      2: ['vertical asymptotes denominator equals zero', 'find vertical asymptotes factor denominator', 'holes vs vertical asymptotes rational functions'],
      3: ['slant oblique asymptotes polynomial long division', 'when does slant asymptote exist', 'oblique asymptote degree one higher'],
      4: ['find all asymptotes rational function', 'complete asymptote analysis rational function', 'horizontal vertical slant asymptotes together'],
      5: ['holes in rational functions removable discontinuity', 'canceled factors holes vs asymptotes', 'removable discontinuity vs vertical asymptote'],
    },
    prompts: {
      1: 'I am learning to find horizontal asymptotes by comparing the degrees of the numerator and denominator: deg(num)<deg(den) gives y=0, equal degrees gives ratio of leading coefficients, deg(num)>deg(den) gives none. Show 2 examples of each case, then give me 3 practice problems.',
      2: 'I am learning to find vertical asymptotes by setting the denominator to zero and checking that the numerator is not also zero (which would be a hole). Show 2 complete examples, then give me 3 practice problems.',
      3: 'I am learning to find slant (oblique) asymptotes by polynomial long division when deg(num) = deg(den) + 1. Walk me through 2 complete examples, then give me 3 practice problems.',
      4: 'I am learning to find ALL asymptotes (horizontal, vertical, and slant) for a rational function in one analysis. Walk me through 2 complete examples, then give me 3 practice problems.',
      5: 'I am learning to distinguish between holes (removable discontinuities from canceled common factors) and vertical asymptotes (remaining denominator zeros). Show 2 examples with both holes and asymptotes, then give me 3 practice problems.',
    }
  },
  epsilon_delta: {
    searches: {
      1: ['epsilon delta proof linear function tutorial', 'formal definition of limit epsilon delta', 'epsilon delta proof step by step'],
      2: ['finding delta given epsilon limit proof', 'epsilon delta choose delta tutorial', 'bound delta epsilon proof calculus'],
      3: ['one sided limit epsilon delta proof', 'right hand limit formal definition', 'epsilon delta sqrt function limit'],
      4: ['limit does not exist epsilon delta proof', 'left and right limits differ epsilon delta', 'show limit DNE formal proof'],
      5: ['squeeze theorem epsilon delta proof', 'sandwich theorem formal proof', 'epsilon delta floor function limit'],
    },
    prompts: {
      1: 'I am learning formal epsilon-delta proofs for limits of simple functions. Explain how to choose δ = ε/|slope| for linear functions and δ = min(1, ε/M) for quadratics. Walk me through 2 complete proofs, then give me 2 limits to prove.',
      2: 'I am learning to find a specific δ value for a given ε in an epsilon-delta proof. Show me the algebraic manipulation from |f(x) - L| < ε to |x - a| < δ with 2 examples, then give me 3 practice problems.',
      3: 'I am learning one-sided epsilon-delta proofs, like proving lim(x→0⁺) √x = 0. Explain how the proof changes for right-hand limits with 2 examples, then give me 2 practice proofs.',
      4: 'I am learning to show that a limit does not exist using the epsilon-delta definition, by showing left and right limits differ. Walk me through 2 examples (like the sign function), then give me 2 practice problems.',
      5: 'I am learning to use the squeeze theorem with epsilon-delta proofs, like proving lim(x→0) x²sin(1/x) = 0. Explain the bounding strategy with 2 examples, then give me 2 practice proofs.',
    }
  },
  increasing_decreasing: {
    searches: {
      1: ['increasing decreasing intervals derivative sign', 'first derivative test sign chart', 'where is function increasing f prime > 0'],
      2: ['find increasing decreasing intervals polynomial', 'differentiate and find sign chart', 'critical points increasing decreasing'],
      3: ['critical points of a function tutorial', 'classify intervals increasing decreasing', 'full sign analysis derivative'],
      4: ['increasing decreasing rational functions derivative', 'quotient rule increasing decreasing intervals', 'product rule exponential increasing decreasing'],
      5: ['multiple critical points sign chart', 'increasing decreasing trig functions interval', 'multiplicity critical points derivative'],
    },
    prompts: {
      1: 'I am learning to find where a function is increasing (f\'(x) > 0) or decreasing (f\'(x) < 0) given a factored derivative. Explain sign chart analysis with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to find increasing/decreasing intervals of a polynomial by first differentiating, then factoring f\'(x) and doing a sign chart. Walk me through 2 complete examples, then give me 3 practice problems.',
      3: 'I am learning to find all critical points (where f\'(x)=0 or undefined) and classify every interval as increasing or decreasing. Show 2 complete analyses, then give me 3 practice problems.',
      4: 'I am learning to find increasing/decreasing intervals for rational functions (using quotient rule) and exponential functions (using product rule). Show 2 examples of each type, then give me 3 practice problems.',
      5: 'I am learning to do full interval analysis with multiple critical points and for trigonometric functions on [0, 2π]. Walk me through 2 challenging examples, then give me 3 practice problems.',
    }
  },
  extrema: {
    searches: {
      1: ['first derivative test local max min', 'classify critical points sign change', 'local maximum minimum first derivative'],
      2: ['absolute extrema closed interval endpoints', 'extreme value theorem calculus', 'find absolute max min on interval'],
      3: ['second derivative test local max min', 'f double prime concavity extrema', 'second derivative test fails'],
      4: ['optimization word problems calculus', 'maximize revenue calculus tutorial', 'applied optimization problems step by step'],
      5: ['full extrema analysis local and absolute', 'extrema with parameters calculus', 'first and second derivative test combined'],
    },
    prompts: {
      1: 'I am learning to classify critical points using the first derivative test: sign change from + to − means local max, − to + means local min. Explain with 2 examples using sign charts, then give me 3 practice problems.',
      2: 'I am learning to find absolute extrema on a closed interval by evaluating at all critical points AND endpoints, then comparing values. Walk me through 2 complete examples, then give me 3 practice problems.',
      3: 'I am learning the second derivative test: f\'\'(c) > 0 means local min, f\'\'(c) < 0 means local max, f\'\'(c) = 0 means test fails. Show 2 examples including a case where the test fails, then give me 3 practice problems.',
      4: 'I am learning to solve optimization word problems: set up the function, differentiate, find the critical point, and verify it is a maximum or minimum. Walk me through 2 complete examples, then give me 3 practice problems.',
      5: 'I am learning to do a full extrema analysis combining local and absolute extrema on a closed interval, and to handle functions with parameters. Show 2 challenging examples, then give me 3 practice problems.',
    }
  },
  mvt: {
    searches: {
      1: ['mean value theorem tutorial step by step', 'find c that satisfies MVT calculus', 'average rate of change MVT'],
      2: ['Rolle\'s theorem tutorial calculus', 'verify Rolle\'s theorem conditions', 'find c where f prime c equals 0'],
      3: ['MVT with square root function', 'mean value theorem inequality application', 'MVT compare function values'],
      4: ['MVT corollary strictly increasing function', 'derivative positive implies increasing', 'MVT implications calculus'],
      5: ['MVT with trigonometric functions', 'mean value theorem inverse trig answer', 'MVT symmetric interval multiple c values'],
    },
    prompts: {
      1: 'I am learning to apply the Mean Value Theorem: find c in (a,b) such that f\'(c) = (f(b)-f(a))/(b-a). Walk me through 2 complete examples with polynomials, then give me 3 practice problems.',
      2: 'I am learning Rolle\'s Theorem: if f(a)=f(b), then there exists c where f\'(c)=0. Explain the conditions and show 2 complete examples, then give me 3 practice problems.',
      3: 'I am learning to apply MVT to functions like √x and to use MVT to compare function values and prove inequalities. Show 2 examples of each, then give me 3 practice problems.',
      4: 'I am learning MVT corollaries: if f\'(x) > 0 for all x in an interval, then f is strictly increasing. Explain the reasoning with 2 examples, then give me 3 practice problems.',
      5: 'I am learning to apply MVT to trigonometric functions and on symmetric intervals where there may be multiple valid c values. Walk me through 2 challenging examples, then give me 3 practice problems.',
    }
  },
  numerical_methods: {
    searches: {
      1: ['bisection method tutorial step by step', 'bisection method find root accuracy', 'bisection method iterations tolerance'],
      2: ['Newton\'s method tutorial calculus', 'Newton\'s method formula x sub n+1', 'Newton vs bisection convergence rate'],
      3: ['secant method tutorial numerical analysis', 'secant method formula two points', 'secant method vs Newton\'s method'],
      4: ['Taylor remainder error bound calculus', 'trapezoidal rule error bound', 'numerical integration error estimation'],
      5: ['Newton\'s method divergence why it fails', 'when does Newton\'s method fail', 'poor initial guess Newton\'s method'],
    },
    prompts: {
      1: 'I am learning the bisection method for finding roots: iteratively halving an interval [a,b] where f(a) and f(b) have opposite signs. Explain the algorithm and error bound (b-a)/2^n with 2 examples, then give me 3 practice problems.',
      2: 'I am learning Newton\'s method: x_{n+1} = x_n - f(x_n)/f\'(x_n). Explain the geometric intuition (tangent line) and show 2 complete examples computing x₂ from x₀, then give me 3 practice problems.',
      3: 'I am learning the secant method: x_{n+1} = x_n - f(x_n)·(x_n - x_{n-1})/(f(x_n) - f(x_{n-1})). Explain how it differs from Newton\'s method with 2 examples, then give me 3 practice problems.',
      4: 'I am learning error bounds for numerical methods: Taylor remainder R_n(x) and trapezoidal rule error E_T ≤ (b-a)³·max|f\'\'|/(12n²). Show 2 examples of computing error bounds, then give me 3 practice problems.',
      5: 'I am learning why Newton\'s method might fail or diverge: poor initial guess, f\' near zero, oscillatory behavior. Explain each failure mode with 2 examples, then give me 3 scenarios to analyze.',
    }
  },
  indeterminate_forms: {
    searches: {
      1: ['L\'Hospital\'s rule 0 over 0 tutorial', 'L\'Hospital\'s rule infinity over infinity', 'differentiate numerator and denominator limits'],
      2: ['limit 1 minus cos x over x squared', 'L\'Hospital\'s rule trig limits', 'exponential over polynomial limit infinity'],
      3: ['0 times infinity indeterminate form', 'infinity minus infinity indeterminate form', 'rewrite product as quotient L\'Hospital'],
      4: ['1 to the infinity indeterminate form', 'infinity to the 0 indeterminate form', 'take natural log limit L\'Hospital'],
      5: ['repeated L\'Hospital\'s rule multiple times', 'L\'Hospital\'s rule chain rule parameter', 'apply L\'Hospital three times limit'],
    },
    prompts: {
      1: 'I am learning L\'Hospital\'s Rule for 0/0 and ∞/∞ indeterminate forms: differentiate numerator and denominator separately. Explain when it applies with 2 examples of each form, then give me 3 practice problems.',
      2: 'I am learning to apply L\'Hospital\'s Rule to trig limits like (1-cos x)/x² and exponential limits like x/e^x, sometimes requiring multiple applications. Show 2 examples, then give me 3 practice problems.',
      3: 'I am learning to handle 0·∞ and ∞-∞ indeterminate forms by rewriting them as quotients before applying L\'Hospital\'s Rule. Show 2 examples of each form, then give me 3 practice problems.',
      4: 'I am learning to handle 1^∞ and ∞^0 indeterminate forms by taking the natural log, converting to 0/0 or ∞/∞, applying L\'Hospital\'s, then exponentiating back. Show 2 examples, then give me 3 practice problems.',
      5: 'I am learning to apply L\'Hospital\'s Rule repeatedly (2-3 times) for limits that remain indeterminate after the first application. Walk me through 2 challenging examples, then give me 3 practice problems.',
    }
  },
  hyperbolic_apps: {
    searches: {
      1: ['hyperbolic identities cosh squared minus sinh squared', 'derivatives of sinh and cosh tutorial', 'hyperbolic function definitions exponential'],
      2: ['integrals of sinh and cosh tutorial', 'antiderivative hyperbolic functions', 'integral sinh x cosh x calculus'],
      3: ['catenary curve calculus arc length', 'hanging chain catenary equation', 'arc length cosh function calculus'],
      4: ['inverse hyperbolic functions derivatives', 'derivative arcsinh arctanh tutorial', 'differentiating inverse hyperbolic functions'],
      5: ['surface area of revolution catenary', 'hyperbolic and trig functions Euler\'s formula', 'cos ix equals cosh x proof'],
    },
    prompts: {
      1: 'I am learning hyperbolic function identities (cosh²x - sinh²x = 1) and derivatives (d/dx sinh x = cosh x, d/dx cosh x = sinh x). Explain using exponential definitions with 2 examples, then give me 3 practice problems.',
      2: 'I am learning to integrate hyperbolic functions: ∫sinh x dx = cosh x + C and ∫cosh x dx = sinh x + C. Show 2 examples of each, then give me 3 practice problems.',
      3: 'I am learning about the catenary curve y = a·cosh(x/a): finding its slope and computing arc length using the identity √(1+sinh²u) = cosh u. Walk me through 2 examples, then give me 3 practice problems.',
      4: 'I am learning the derivatives of inverse hyperbolic functions: d/dx arsinh(x) = 1/√(1+x²) and d/dx artanh(ax) = a/(1-a²x²). Show 2 examples of each, then give me 3 practice problems.',
      5: 'I am learning advanced hyperbolic applications: surface area of catenary rotation and the connection between hyperbolic and trig functions via Euler\'s formula (cos(ix) = cosh x). Explain with 2 examples, then give me 3 practice problems.',
    }
  },
  function_construction: {
    searches: {
      1: ['initial value problem antiderivative find C', 'find function from derivative and point', 'indefinite integral initial condition calculus'],
      2: ['double integration second derivative initial conditions', 'find function from f double prime', 'two initial conditions integration calculus'],
      3: ['velocity from acceleration calculus', 'position from velocity initial conditions', 'kinematics integration calculus'],
      4: ['exponential growth differential equation', 'Newton\'s law of cooling solution', 'separation of variables differential equations'],
      5: ['construct sine wave from derivative', 'trigonometric antiderivative initial value', 'build function from trig derivative'],
    },
    prompts: {
      1: 'I am learning to find f(x) given f\'(x) and an initial condition like f(0) = c. Explain the process: integrate f\'(x) to get f(x)+C, then solve for C. Show 2 examples, then give me 3 practice problems.',
      2: 'I am learning to find f(x) given f\'\'(x) and two initial conditions (like f\'(0) and f(0)) by integrating twice. Walk me through 2 complete examples, then give me 3 practice problems.',
      3: 'I am learning to find velocity from acceleration and position from velocity using integration with initial conditions in physics contexts. Show 2 examples of each, then give me 3 practice problems.',
      4: 'I am learning to solve differential equations like P\'(t) = kP (exponential growth) and T\'(t) = -k(T - T_env) (Newton\'s Law of Cooling) using separation of variables. Walk me through 2 examples of each, then give me 3 practice problems.',
      5: 'I am learning to construct functions from trigonometric derivatives with initial conditions, like finding f(x) given f\'(x) = 2cos(x) - 1 and f(0) = 0. Show 2 complete examples, then give me 3 practice problems.',
    }
  },
  center_of_mass: {
    searches: {
      1: ['center of mass discrete point masses formula', 'center of mass two objects tutorial', 'weighted average center of mass'],
      2: ['center of mass continuous rod variable density', 'integral center of mass one dimension', 'density function center of mass calculus'],
      3: ['centroid of rectangle triangle symmetry', 'center of mass 2D lamina uniform', 'centroid formula triangle calculus'],
      4: ['lever principle torque balance tutorial', 'center of mass fulcrum balance point', 'torque equilibrium physics math'],
      5: ['Pappus centroid theorem volume of revolution', 'second theorem of Pappus Guldinus', 'volume equals area times path of centroid'],
    },
    prompts: {
      1: 'I am learning to find the center of mass of discrete point masses using x_cm = Σ(m_i · x_i) / Σm_i. Explain with 2 examples (including a two-mass system), then give me 3 practice problems.',
      2: 'I am learning to find the center of mass of a continuous rod with variable density δ(x) using x_cm = ∫x·δ(x)dx / ∫δ(x)dx. Walk me through 2 complete examples, then give me 3 practice problems.',
      3: 'I am learning to find the center of mass (centroid) of 2D shapes: uniform rectangles by symmetry and triangles using the centroid formula. Show 2 examples, then give me 3 practice problems.',
      4: 'I am learning to find the balance point (fulcrum) for a lever using the torque equation m₁·d₁ = m₂·d₂. Explain with 2 examples, then give me 3 practice problems.',
      5: 'I am learning Pappus\'s centroid theorem: the volume of a solid of revolution equals the area times the distance traveled by the centroid (V = Area · 2π·r). Show 2 complete examples, then give me 3 practice problems.',
    }
  }
};

const TOP_CHANNELS = [
  { name: 'Professor Leonard', search: 'Professor Leonard calculus', desc: 'Full college-length lectures — most thorough on YouTube' },
  { name: 'The Organic Chemistry Tutor', search: 'Organic Chemistry Tutor calculus', desc: 'Hundreds of worked examples, covers every topic' },
  { name: 'PatrickJMT', search: 'PatrickJMT math', desc: 'Short focused examples, great for quick concept review' },
  { name: 'blackpenredpen', search: 'blackpenredpen calculus', desc: 'College-level problems, fun style, challenging content' },
  { name: '3Blue1Brown', search: '3Blue1Brown essence of calculus', desc: 'Visual intuition — understand the deep "why"' },
  { name: 'Khan Academy', search: 'Khan Academy precalculus calculus', desc: 'Comprehensive coverage of all levels, free and beginner-friendly' },
  { name: 'Math with Professor V', search: 'Math with Professor V precalculus', desc: 'Clear precalc and calculus instruction, very approachable' },
];
