import sqlite3

conn = sqlite3.connect("results.db", check_same_thread=False)
cursor = conn.cursor()

# Jadval yaratish
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
user_id INTEGER,
username TEXT,
score INTEGER
)
""")

conn.commit()


# Natija saqlash
def save_result(user_id, username, score):

    cursor.execute(
        "INSERT INTO results VALUES (?, ?, ?)",
        (user_id, username, score)
    )

    conn.commit()


# Leaderboard
def get_top():

    cursor.execute("""
    SELECT username, MAX(score)
    FROM results
    GROUP BY user_id
    ORDER BY MAX(score) DESC
    LIMIT 10
    """)

    return cursor.fetchall()


# Foydalanuvchi statistikasi
def get_user_stats(user_id):

    cursor.execute(
        "SELECT COUNT(*), MAX(score), AVG(score) FROM results WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchone()


# Bot statistikasi
def get_global_stats():

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM results")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results")
    tests = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(score) FROM results")
    best = cursor.fetchone()[0]

    return users, tests, best