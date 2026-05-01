def problem(problem_tex, answer_tex, answer_norm, steps, **flags):
    return {
        "problemTex": problem_tex,
        "answerTex": answer_tex,
        "answerNorm": answer_norm,
        "steps": steps,
        **flags,
    }


def dual_problem(problem_tex, answer1_tex, answer1_norm, answer2_tex, answer2_norm, steps, **flags):
    return {
        "problemTex": problem_tex,
        "answerTex": answer1_tex,
        "answerNorm": answer1_norm,
        "answerTex2": answer2_tex,
        "answerNorm2": answer2_norm,
        "requiresDualAnswer": True,
        "steps": steps,
        **flags,
    }


def step(label, math, note=""):
    return {"label": label, "math": math, "note": note}