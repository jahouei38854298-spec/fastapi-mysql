from sqlalchemy import Column, Date, Integer, String

from mysql_database import Base


class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    birth_date = Column(Date, nullable=False)
    father_name = Column(String(50), nullable=False)
    birth_place = Column(String(100), nullable=False)
    phone = Column(String(11), nullable=False)
    email = Column(String(254), nullable=False)
    address = Column(String(200), nullable=True)


class AdminDB(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
