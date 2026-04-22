import random
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from generators import factoring, exponents, fractions
from checker import check_answer

app = Flask(__name__)
CORS(app)

GENERATORS = {
    "factoring": factoring.POOLS,
    "exponents": exponents.POOLS,
    "fractions": fractions.POOLS,
}


@app.get("/api/problem")
def get_problem():
    module = request.args.get("module", "factoring")
    diff = int(request.args.get("difficulty", 1))

    if module not in GENERATORS:
        return jsonify({"error": f"unknown module: {module}"}), 400

    pools = GENERATORS[module]
    # Clamp to available difficulties
    available = sorted(pools.keys())
    if diff not in available:
        diff = available[0]

    pool = pools[diff]
    fn = random.choice(pool)
    problem = fn()
    problem["module"] = module
    problem["difficulty"] = diff

    # originalExpanded may be a dict (sparse poly) — serialize to list of [deg, coef] pairs
    if "originalExpanded" in problem and isinstance(problem["originalExpanded"], dict):
        problem["originalExpanded"] = {
            str(k): v for k, v in problem["originalExpanded"].items()
        }

    return jsonify(problem)


@app.post("/api/check")
def post_check():
    data = request.get_json(force=True)
    problem = data.get("problem", {})
    user_input = data.get("input", "")

    # Restore originalExpanded string-key dict back to int-key dict for poly comparison
    if "originalExpanded" in problem and isinstance(problem["originalExpanded"], dict):
        problem["originalExpanded"] = {
            int(k): v for k, v in problem["originalExpanded"].items()
        }

    result = check_answer(problem, user_input)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
