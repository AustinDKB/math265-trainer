import random
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from generators import (
    factoring, exponents, fractions,
    trig_circle, logs, composition,
    limits, derivatives, integration_basic, integration_advanced,
)
from checker import check_answer
from db import init_db, record_attempt, stats_overview, stats_trend, stats_problem, stats_weak

app = Flask(__name__)
CORS(app)

init_db()

GENERATORS = {
    "factoring": factoring.POOLS,
    "exponents": exponents.POOLS,
    "fractions": fractions.POOLS,
    "trig": trig_circle.POOLS,
    "logs": logs.POOLS,
    "composition": composition.POOLS,
    "limits": limits.POOLS,
    "derivatives": derivatives.POOLS,
    "integration": integration_basic.POOLS,
    "adv_integration": integration_advanced.POOLS,
}


@app.get("/api/problem")
def get_problem():
    module = request.args.get("module", "factoring")
    diff = int(request.args.get("difficulty", 1))

    if module not in GENERATORS:
        return jsonify({"error": f"unknown module: {module}"}), 400

    pools = GENERATORS[module]
    available = sorted(pools.keys())
    if diff not in available:
        diff = available[0]

    pool = pools[diff]
    fn = random.choice(pool)
    problem = fn()
    problem["module"] = module
    problem["difficulty"] = diff

    if "originalExpanded" in problem and isinstance(problem["originalExpanded"], dict):
        problem["originalExpanded"] = {str(k): v for k, v in problem["originalExpanded"].items()}

    return jsonify(problem)


@app.post("/api/check")
def post_check():
    data = request.get_json(force=True)
    problem = data.get("problem", {})
    user_input = data.get("input", "")
    time_sec = int(data.get("timeSec", 0))

    if "originalExpanded" in problem and isinstance(problem["originalExpanded"], dict):
        problem["originalExpanded"] = {int(k): v for k, v in problem["originalExpanded"].items()}

    result = check_answer(problem, user_input)

    if problem.get("module") and problem.get("problemTex"):
        record_attempt(
            module=problem["module"],
            difficulty=problem.get("difficulty", 1),
            problem_tex=problem["problemTex"],
            correct=(result["result"] == "correct"),
            time_sec=time_sec,
        )

    return jsonify(result)


@app.get("/api/stats/overview")
def get_stats_overview():
    return jsonify(stats_overview())


@app.get("/api/stats/trend")
def get_stats_trend():
    days = int(request.args.get("days", 30))
    return jsonify(stats_trend(days))


@app.get("/api/stats/problem")
def get_stats_problem():
    tex = request.args.get("tex", "")
    return jsonify(stats_problem(tex))


@app.get("/api/stats/weak")
def get_stats_weak():
    min_att = int(request.args.get("min_attempts", 3))
    limit = int(request.args.get("limit", 10))
    return jsonify(stats_weak(min_att, limit))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
