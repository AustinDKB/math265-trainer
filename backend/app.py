import random
import json
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

from generators import (
    factoring, exponents, fractions,
    trig_circle, logs, composition,
    limits, derivatives, integration_basic, integration_advanced,
)
from generators import ALL_MODULES
from module_config import UNLOCK_TIERS
from checker import check_answer, check_dual_answer, check_norm_answer
from checker_registry import get_checker
import jsonl_engine
from db import (
    init_db, record_attempt, dispute_attempt,
    stats_overview, stats_trend, stats_problem, stats_weak,
    record_bug_report, list_bug_reports,
    award_xp, get_total_xp, xp_for_level,
    time_to_fsrs_rating, update_fsrs_skill, get_fsrs_due_skills,
)

NUM_DIFFICULTIES = 5

from module_config import UNLOCK_TIERS, MODULES

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


def _get_unlocked_modules(pair_stats):
    mod_totals = {}
    for row in pair_stats:
        m = row["module"]
        if m not in mod_totals:
            mod_totals[m] = {"attempts": 0, "correct": 0}
        mod_totals[m]["attempts"] += row["attempts"]
        mod_totals[m]["correct"] += row["correct"]

    unlocked = []
    for tier_idx, tier in enumerate(UNLOCK_TIERS):
        unlocked.extend(tier)
        if tier_idx == len(UNLOCK_TIERS) - 1:
            break
        tier_ready = all(
            mod_totals.get(m, {}).get("attempts", 0) >= 5
            and mod_totals[m]["correct"] / mod_totals[m]["attempts"] >= 0.8
            for m in tier
        )
        if not tier_ready:
            break
    return unlocked


def _compute_xp(difficulty, time_sec, session_streak, correct):
    if not correct:
        return 0
    base = 10 + difficulty * 5
    t_capped = min(time_sec, 30)
    speed_bonus = max(0, int((30 - t_capped) * 0.5))
    if session_streak >= 10:
        mult = 2.0
    elif session_streak >= 5:
        mult = 1.5
    else:
        mult = 1.0
    return int((base + speed_bonus) * mult)


def _build_problem(fn, module, diff, **extra):
    problem = fn()
    problem["module"] = module
    problem["difficulty"] = diff
    if "originalExpanded" in problem and isinstance(problem["originalExpanded"], dict):
        problem["originalExpanded"] = {str(k): v for k, v in problem["originalExpanded"].items()}
    problem.update(extra)
    return problem


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

    fn = random.choice(pools[diff])
    return jsonify(_build_problem(fn, module, diff))


@app.get("/api/problem/auto")
def get_auto_problem():
    avg_time = request.args.get("avg_time", type=float, default=40.0)

    pair_stats = stats_overview()
    stats_map = {(r["module"], r["difficulty"]): r for r in pair_stats}
    unlocked = _get_unlocked_modules(pair_stats)

    # FSRS due skills (most overdue first)
    due_skills = get_fsrs_due_skills(unlocked)

    # Flow adjustment: shift challenge probability based on recent solve speed
    # avg_time < 40 (fast) → push harder; avg_time > 40 (slow) → ease up
    raw_prob = 0.4 + (40.0 - avg_time) / 200.0
    challenge_prob = max(0.2, min(0.6, raw_prob))

    # Serve SRS review at 35% cap when skills are due
    if due_skills and random.random() < 0.35:
        module, diff = due_skills[0]  # most overdue skill
        fn = random.choice(GENERATORS[module][diff])
        return jsonify(_build_problem(fn, module, diff, bucket="review"))

    # Build challenge / success buckets
    challenge, success = [], []
    for module in unlocked:
        for diff in sorted(GENERATORS[module].keys()):
            row = stats_map.get((module, diff))
            attempts = row["attempts"] if row else 0
            correct = row["correct"] if row else 0
            if attempts < 3:
                challenge.append({"module": module, "diff": diff, "weight": 0.5})
            else:
                acc = correct / attempts
                if acc < 0.5:
                    challenge.append({"module": module, "diff": diff, "weight": 1 - acc})
                else:
                    success.append({"module": module, "diff": diff, "weight": acc})

    if not challenge:
        pool, bucket = success, "win"
    elif not success:
        pool, bucket = challenge, "challenge"
    elif random.random() < challenge_prob:
        pool, bucket = challenge, "challenge"
    else:
        pool, bucket = success, "win"

    if not pool:
        pool = [{"module": unlocked[0], "diff": 1, "weight": 1.0}]
        bucket = "challenge"

    total_w = sum(p["weight"] for p in pool)
    r = random.random() * total_w
    picked = pool[-1]
    for p in pool:
        r -= p["weight"]
        if r <= 0:
            picked = p
            break

    module, diff = picked["module"], picked["diff"]
    fn = random.choice(GENERATORS[module][diff])
    return jsonify(_build_problem(fn, module, diff, bucket=bucket))


@app.post("/api/check")
def post_check():
    data = request.get_json(force=True)
    problem = data.get("problem", {})
    time_sec = int(data.get("timeSec", 0))
    session_streak = int(data.get("sessionStreak", 0))

    if "originalExpanded" in problem and isinstance(problem["originalExpanded"], dict):
        problem["originalExpanded"] = {int(k): v for k, v in problem["originalExpanded"].items()}

    if problem.get("requiresDualAnswer"):
        inputs = data.get("inputs", [])
        i1 = inputs[0].strip() if len(inputs) > 0 else ""
        i2 = inputs[1].strip() if len(inputs) > 1 else ""
        if not i1 or not i2:
            return jsonify({"result": "empty"})
        result = check_dual_answer(problem, i1, i2)
    else:
        user_input = data.get("input", "")
        result = check_answer(problem, user_input)

    attempt_id = None
    if problem.get("module") and problem.get("problemTex"):
        attempt_id = record_attempt(
            module=problem["module"],
            difficulty=problem.get("difficulty", 1),
            problem_tex=problem["problemTex"],
            correct=(result["result"] == "correct"),
            time_sec=time_sec,
        )

    correct = result["result"] == "correct"
    difficulty = problem.get("difficulty", 1)

    # XP
    xp_earned = _compute_xp(difficulty, time_sec, session_streak, correct)
    if xp_earned > 0:
        award_xp(xp_earned)

    # FSRS update — skip AFK times (rating=None)
    if problem.get("module") and problem.get("difficulty") is not None:
        rating = time_to_fsrs_rating(correct, time_sec)
        if rating is not None:
            update_fsrs_skill(problem["module"], difficulty, rating)

    xp_info = get_total_xp()
    total_xp = xp_info["total_xp"]
    level = xp_info["level"]
    current_level_xp = xp_for_level(level)
    next_level_xp = xp_for_level(level + 1)

    result["attemptId"] = attempt_id
    result["xpEarned"] = xp_earned
    result["totalXp"] = total_xp
    result["level"] = level
    result["currentLevelXp"] = current_level_xp
    result["nextLevelXp"] = next_level_xp
    return jsonify(result)


@app.get("/api/xp")
def get_xp():
    info = get_total_xp()
    total_xp = info["total_xp"]
    level = info["level"]
    return jsonify({
        "totalXp": total_xp,
        "level": level,
        "currentLevelXp": xp_for_level(level),
        "nextLevelXp": xp_for_level(level + 1),
    })


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


@app.post("/api/report")
def post_report():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "invalid request body"}), 400
        problem = data.get("problem", {})
        if not problem.get("module") or not problem.get("problemTex"):
            return jsonify({"error": "missing problem data"}), 400
        attempt_id = data.get("attemptId")
        record_bug_report(
            module=problem["module"],
            difficulty=problem.get("difficulty", 1),
            problem_tex=problem["problemTex"],
            answer_tex=problem.get("answerTex", ""),
            user_answer=data.get("userAnswer", ""),
            note=data.get("note", ""),
            attempt_id=attempt_id,
        )
        if attempt_id:
            dispute_attempt(attempt_id)
        return jsonify({"ok": True})
    except Exception as e:
        app.logger.exception("Bug report failed")
        return jsonify({"error": str(e)}), 500


@app.get("/api/reports")
def get_reports():
    limit = int(request.args.get("limit", 100))
    return jsonify(list_bug_reports(limit))


@app.get("/api/modules")
def get_modules():
    return jsonify({
        "modules": ALL_MODULES,
        "unlockTiers": UNLOCK_TIERS,
        "labels": {m: MODULES[m]["label"] for m in ALL_MODULES},
    })


@app.get("/api/unlock-status")
def get_unlock_status():
    pair_stats = stats_overview()
    unlocked = _get_unlocked_modules(pair_stats)
    unlocked_tiers = []
    for tier_idx, tier in enumerate(UNLOCK_TIERS):
        unlocked_tiers.append(tier)
        if tier_idx == len(UNLOCK_TIERS) - 1:
            break
        tier_ready = all(
            any(r["module"] == m and r["attempts"] >= 5 and r["correct"] / r["attempts"] >= 0.8
                for r in pair_stats)
            for m in tier
        )
        if not tier_ready:
            break
    return jsonify({
        "unlockedModules": unlocked,
        "unlockedTiers": unlocked_tiers,
        "nextLockedTier": UNLOCK_TIERS[len(unlocked_tiers)] if len(unlocked_tiers) < len(UNLOCK_TIERS) else None,
    })


# ── JSONL / Word Problem Endpoints ──

@app.get("/api/problem/jsonl")
def get_jsonl_problem():
    course = request.args.get("course", "calc1")
    topic = request.args.get("topic")
    difficulty = request.args.get("difficulty", type=int)
    prob = jsonl_engine.get_next_problem(
        course=course,
        topic=topic,
        difficulty=difficulty,
    )
    if prob is None:
        return jsonify({"error": "no templates available"}), 404
    return jsonify(prob)


@app.post("/api/check/mode")
def check_mode_answer():
    """Check answers for mode-specific problems (justify, backwards, break, derive).

    v1 strategy:
      - justify / backwards / derive: accept any non-empty input, show model answer.
      - break: check error-type match + optional fix against answerNorm.
    """
    data = request.get_json(force=True) or {}
    mode = data.get("mode", "solve")
    user_input = data.get("userInput", "")
    problem = data.get("problem", {})

    if mode in ("justify", "backwards", "derive"):
        correct = bool(user_input and str(user_input).strip())
        return jsonify({
            "result": "correct" if correct else "wrong",
            "modelAnswer": problem.get("answerTex", problem.get("answerNorm", "")),
            "reason": None if correct else "empty_input",
        })

    if mode == "break":
        selected_error = data.get("selectedError", "")
        mode_data = problem.get("modeData", {})
        expected_error = mode_data.get("error", {}).get("type", "")
        error_correct = selected_error == expected_error if expected_error else True

        user_fix = data.get("userFix", "")
        fix_check = None
        if user_fix and problem.get("answerNorm"):
            fix_check = check_norm_answer(problem, user_fix)

        if error_correct and (fix_check is None or fix_check.get("result") == "correct"):
            return jsonify({
                "result": "correct",
                "modelAnswer": problem.get("answerTex", problem.get("answerNorm", "")),
                "reason": None,
            })
        return jsonify({
            "result": "wrong",
            "modelAnswer": problem.get("answerTex", problem.get("answerNorm", "")),
            "reason": "error_type_mismatch" if not error_correct else "fix_incorrect",
        })

    # Fallback to standard checker for solve mode
    return jsonify(check_answer(problem, user_input))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
