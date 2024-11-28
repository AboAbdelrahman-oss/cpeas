import sqlite3

class Database:
    def __init__(self, db_name="results.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        # إنشاء جدول لحفظ الدردشات
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer_llama TEXT,
                answer_openai TEXT
            )
        """)
        self.conn.commit()

    def insert_chat(self, question, answer_llama, answer_openai):
        # إدخال محادثة جديدة
        self.cursor.execute("""
            INSERT INTO chats (question, answer_llama, answer_openai)
            VALUES (?, ?, ?)
        """, (question, answer_llama, answer_openai))
        self.conn.commit()

    def close(self):
        self.conn.close()
