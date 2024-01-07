import sqlite3 as sq

db = sq.connect("vpn.db")
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "username TEXT)")
    
    db.commit()