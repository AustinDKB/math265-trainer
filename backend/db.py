import sqlite3
import time
import os
import math
import json
from datetime import datetime, timezone
from fsrs import Scheduler, Card, Rating

_FSRS = Scheduler()

DB_PATH = os.path.join(os.path.dirname(__file__), 'attempts.db')

AFK_THRESHOLD = 180  # seconds — above this = not active engagement


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ts          INTEGER NOT NULL,
                module      TEXT NOT NULL,
                difficulty  INTEGER NOT NULL,
                problem_tex TEXT NOT NULL,
                correct     INTEGER NOT NULL,
                time_sec    INTEGER DEFAULT 0,
                disputed    INTEGER DEFAULT 0
            )
        """)
        # Migrate existing DB — no-op if column already exists
        try:
            conn.execute("ALTER TABLE attempts ADD COLUMN disputed INTEGER DEFAULT 0")
        except Exception:
            pass
        conn.execute("CREATE INDEX IF NOT EXISTS idx_module_diff ON attempts(module, difficulty)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ts ON attempts(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_problem_tex ON attempts(problem_tex)")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bug_reports (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ts          INTEGER NOT NULL,
                module      TEXT NOT NULL,
                difficulty  INTEGER NOT NULL,
                problem_tex TEXT NOT NULL,
                answer_tex  TEXT NOT NULL,
                user_answer TEXT NOT NULL,
                note        TEXT DEFAULT '',
                attempt_id  INTEGER
            )
        """)
        try:
            conn.execute("ALTER TABLE bug_reports ADD COLUMN attempt_id INTEGER")
        except Exception:
            pass
        conn.execute("""
            CREATE TABLE IF NOT EXISTS srs_cards (
                problem_tex  TEXT PRIMARY KEY,
                module       TEXT NOT NULL,
                difficulty   INTEGER NOT NULL,
                problem_json TEXT NOT NULL,
                ef           REAL DEFAULT 2.5,
                interval     INTEGER DEFAULT 1,
                next_due     INTEGER DEFAULT 0,
                reps         INTEGER DEFAULT 0,
                last_seen    INTEGER DEFAULT 0
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_srs_due ON srs_cards(next_due, module)")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS srs_skills (
                module      TEXT NOT NULL,
                difficulty  INTEGER NOT NULL,
                card_json   TEXT NOT NULL,
                PRIMARY KEY (module, difficulty)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_xp (
                id       INTEGER PRIMARY KEY CHECK (id = 1),
                total_xp INTEGER DEFAULT 0
            )
        """)
        # Seed single XP row if missing
        conn.execute("INSERT OR IGNORE INTO user_xp(id, total_xp) VALUES(1, 0)")
        conn.commit()


def record_attempt(module, difficulty, problem_tex, correct, time_sec=0):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO attempts(ts,module,difficulty,problem_tex,correct,time_sec) VALUES(?,?,?,?,?,?)",
            (int(time.time()), module, difficulty, problem_tex, int(correct), int(time_sec))
        )
        conn.commit()
        return cur.lastrowid


def dispute_attempt(attempt_id):
    with get_conn() as conn:
        conn.execute("UPDATE attempts SET disputed=1 WHERE id=?", (attempt_id,))
        conn.commit()


def stats_overview():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT module, difficulty,
                   COUNT(*) as attempts,
                   SUM(correct) as correct
            FROM attempts
            WHERE disputed=0
            GROUP BY module, difficulty
            ORDER BY module, difficulty
        """).fetchall()
    return [dict(r) for r in rows]


def stats_trend(days=30):
    since = int(time.time()) - days * 86400
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT date(ts, 'unixepoch', 'localtime') as day,
                   COUNT(*) as attempts,
                   SUM(correct) as correct
            FROM attempts
            WHERE ts >= ? AND disputed=0
            GROUP BY day
            ORDER BY day
        """, (since,)).fetchall()
    return [dict(r) for r in rows]


def stats_problem(problem_tex):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT ts, correct, time_sec
            FROM attempts
            WHERE problem_tex = ? AND disputed=0
            ORDER BY ts
        """, (problem_tex,)).fetchall()
    return [dict(r) for r in rows]


def record_bug_report(module, difficulty, problem_tex, answer_tex, user_answer, note='', attempt_id=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO bug_reports(ts,module,difficulty,problem_tex,answer_tex,user_answer,note,attempt_id) VALUES(?,?,?,?,?,?,?,?)",
            (int(time.time()), module, difficulty, problem_tex, answer_tex, user_answer, note, attempt_id)
        )
        conn.commit()


def list_bug_reports(limit=100):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT id, ts, module, difficulty, problem_tex, answer_tex, user_answer, note, attempt_id
            FROM bug_reports
            ORDER BY ts DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def stats_weak(min_attempts=3, limit=10):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT problem_tex, module, difficulty,
                   COUNT(*) as attempts,
                   SUM(correct) as correct,
                   CAST(SUM(correct) AS REAL) / COUNT(*) as accuracy
            FROM attempts
            WHERE disputed=0
            GROUP BY problem_tex
            HAVING attempts >= ?
            ORDER BY accuracy ASC, attempts DESC
            LIMIT ?
        """, (min_attempts, limit)).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# XP
# ---------------------------------------------------------------------------

def xp_to_level(xp):
    return int(math.sqrt(max(0, xp) / 10)) + 1


def xp_for_level(level):
    return max(0, level - 1) ** 2 * 10


def award_xp(amount):
    with get_conn() as conn:
        conn.execute("UPDATE user_xp SET total_xp = total_xp + ? WHERE id = 1", (amount,))
        conn.commit()


def get_total_xp():
    with get_conn() as conn:
        row = conn.execute("SELECT total_xp FROM user_xp WHERE id = 1").fetchone()
    total = row["total_xp"] if row else 0
    level = xp_to_level(total)
    return {"total_xp": total, "level": level}


# ---------------------------------------------------------------------------
# SRS (SM-2)
# ---------------------------------------------------------------------------

def time_to_quality(time_sec, correct):
    """Map solve time → SM-2 quality (0-5).
    Returns None if time_sec > AFK_THRESHOLD (user was inactive — skip update)."""
    if time_sec > AFK_THRESHOLD:
        return None
    if not correct:
        return 0
    t = min(time_sec, 120)
    if t < 15:
        return 5
    if t < 30:
        return 4
    if t < 60:
        return 3
    return 2


def _sm2_update(ef, interval, reps, quality):
    if quality < 3:
        reps = 0
        interval = 1
    else:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        reps += 1
    ef = max(1.3, ef + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    next_due = int(time.time()) + interval * 86400
    return ef, interval, reps, next_due


def update_srs_card(problem_tex, module, difficulty, problem_json_str, quality):
    """Upsert SRS card with SM-2 update."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT ef, interval, reps FROM srs_cards WHERE problem_tex = ?",
            (problem_tex,)
        ).fetchone()
        if row:
            ef, interval, reps = row["ef"], row["interval"], row["reps"]
        else:
            ef, interval, reps = 2.5, 1, 0
        ef, interval, reps, next_due = _sm2_update(ef, interval, reps, quality)
        conn.execute("""
            INSERT INTO srs_cards(problem_tex, module, difficulty, problem_json, ef, interval, next_due, reps, last_seen)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(problem_tex) DO UPDATE SET
                problem_json = excluded.problem_json,
                ef           = excluded.ef,
                interval     = excluded.interval,
                next_due     = excluded.next_due,
                reps         = excluded.reps,
                last_seen    = excluded.last_seen
        """, (problem_tex, module, difficulty, problem_json_str, ef, interval, next_due, reps, int(time.time())))
        conn.commit()


def time_to_fsrs_rating(correct, time_sec):
    """Map solve time → FSRS Rating, or None if AFK (skip SRS update)."""
    if time_sec > AFK_THRESHOLD:
        return None
    if not correct:
        return Rating.Again
    t = min(time_sec, 120)
    if t < 15:
        return Rating.Easy
    if t < 45:
        return Rating.Good
    return Rating.Hard


def update_fsrs_skill(module, difficulty, rating):
    """Upsert FSRS card state for a (module, difficulty) skill pair."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT card_json FROM srs_skills WHERE module=? AND difficulty=?",
            (module, difficulty)
        ).fetchone()
        card = Card.from_json(row["card_json"]) if row else Card()
        card, _ = _FSRS.review_card(card, rating)
        conn.execute("""
            INSERT INTO srs_skills(module, difficulty, card_json) VALUES(?,?,?)
            ON CONFLICT(module, difficulty) DO UPDATE SET card_json=excluded.card_json
        """, (module, difficulty, card.to_json()))
        conn.commit()


def get_fsrs_due_skills(unlocked_modules):
    """Return list of (module, difficulty) tuples due for review, most overdue first."""
    if not unlocked_modules:
        return []
    now_utc = datetime.now(timezone.utc)
    placeholders = ",".join("?" * len(unlocked_modules))
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT module, difficulty, card_json FROM srs_skills WHERE module IN ({placeholders})",
            list(unlocked_modules)
        ).fetchall()
    due = []
    for r in rows:
        card = Card.from_json(r["card_json"])
        if card.due <= now_utc:
            due.append((r["module"], r["difficulty"], card.due))
    due.sort(key=lambda x: x[2])
    return [(m, d) for m, d, _ in due]


def get_srs_due(unlocked_modules, limit=5):
    """Return list of problem dicts from srs_cards where next_due <= now and module is unlocked.
    Ordered by most overdue first."""
    now = int(time.time())
    placeholders = ",".join("?" * len(unlocked_modules))
    with get_conn() as conn:
        rows = conn.execute(f"""
            SELECT problem_tex, module, difficulty, problem_json, next_due
            FROM srs_cards
            WHERE next_due <= ? AND module IN ({placeholders})
            ORDER BY next_due ASC
            LIMIT ?
        """, [now] + list(unlocked_modules) + [limit]).fetchall()
    result = []
    for r in rows:
        try:
            p = json.loads(r["problem_json"])
            p["_srs_due"] = True
            result.append(p)
        except Exception:
            pass
    return result
