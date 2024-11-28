from database.db_manager import DBManager

def initialize_db():
    db_manager = DBManager()
    db_manager.create_tables()
    db_manager.close()

if __name__ == "__main__":
    initialize_db()
