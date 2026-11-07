from mysql_database import Base, engine
from models import StudentDB, AdminDB


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
