import sqlite3

class DBManager:
    def __init__(self, db_name="project_db.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # إنشاء الجداول اللازمة لتخزين البيانات
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer_llama TEXT,
                answer_openai TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                model_used TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_chat(self, question, answer_llama, answer_openai):
        # إدخال محادثة جديدة في قاعدة البيانات
        self.cursor.execute("""
            INSERT INTO chats (question, answer_llama, answer_openai)
            VALUES (?, ?, ?)
        """, (question, answer_llama, answer_openai))
        self.conn.commit()

    def insert_result(self, question, answer, model_used):
        # إدخال نتيجة جديدة في قاعدة البيانات
        self.cursor.execute("""
            INSERT INTO results (question, answer, model_used)
            VALUES (?, ?, ?)
        """, (question, answer, model_used))
        self.conn.commit()

    def get_all_chats(self):
        # استرجاع كل الدردشات المخزنة
        self.cursor.execute("SELECT * FROM chats")
        return self.cursor.fetchall()

    def get_all_results(self):
        # استرجاع كل النتائج المخزنة
        self.cursor.execute("SELECT * FROM results")
        return self.cursor.fetchall()

    def close(self):
        # إغلاق الاتصال بقاعدة البيانات
        self.conn.close()
