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
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise
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
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise
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
# FSRS
# ---------------------------------------------------------------------------

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
    # module names come from GENERATORS keys — not user input — safe to interpolate
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



