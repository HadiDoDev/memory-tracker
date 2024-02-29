__all__ = ['MemoryTrackerDatabase']

import sqlite3

from memory_tracker.configs import SQLITE_DATABASE_URI


class MemoryTrackerDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DATABASE_URI, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memory_log(
                                timestamp INTEGER PRIMARY KEY, total INTEGER, free INTEGER, used INTEGER)''')

    def insert_mem_log(self, timestamp, total, free, used):
        self.cursor.execute('''INSERT INTO memory_log (timestamp, total, free, used)
                                VALUES (?, ?, ?, ?)''', (timestamp, total, free, used))
        self.conn.commit()
        return "success"

    def fetch_mem_logs(self, limit, skip):
        query = "SELECT * FROM memory_log ORDER BY timestamp DESC"
        if limit is not None:
            query += f" LIMIT {limit}"
            if skip is not None:
                query += f" OFFSET {skip}"
        elif skip is not None:
            query += f" OFFSET {skip}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.conn.close()
