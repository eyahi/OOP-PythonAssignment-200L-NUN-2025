import sqlite3

def init_db():
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, score INTEGER)')
    conn.commit()
    conn.close()

def add_score(score):
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()

def get_top_scores(limit=5):
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('SELECT score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]
