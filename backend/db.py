import sqlite3
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'attempts.db')


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
                time_sec    INTEGER DEFAULT 0
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_module_diff ON attempts(module, difficulty)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ts ON attempts(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_problem_tex ON attempts(problem_tex)")
        conn.commit()


def record_attempt(module, difficulty, problem_tex, correct, time_sec=0):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO attempts(ts,module,difficulty,problem_tex,correct,time_sec) VALUES(?,?,?,?,?,?)",
            (int(time.time()), module, difficulty, problem_tex, int(correct), int(time_sec))
        )
        conn.commit()


def stats_overview():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT module, difficulty,
                   COUNT(*) as attempts,
                   SUM(correct) as correct
            FROM attempts
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
            WHERE ts >= ?
            GROUP BY day
            ORDER BY day
        """, (since,)).fetchall()
    return [dict(r) for r in rows]


def stats_problem(problem_tex):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT ts, correct, time_sec
            FROM attempts
            WHERE problem_tex = ?
            ORDER BY ts
        """, (problem_tex,)).fetchall()
    return [dict(r) for r in rows]


def stats_weak(min_attempts=3, limit=10):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT problem_tex, module, difficulty,
                   COUNT(*) as attempts,
                   SUM(correct) as correct,
                   CAST(SUM(correct) AS REAL) / COUNT(*) as accuracy
            FROM attempts
            GROUP BY problem_tex
            HAVING attempts >= ?
            ORDER BY accuracy ASC, attempts DESC
            LIMIT ?
        """, (min_attempts, limit)).fetchall()
    return [dict(r) for r in rows]
