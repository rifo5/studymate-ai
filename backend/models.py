# StudyMate AI - Veritabanı Modelleri

from sqlalchemy import Column, Integer, String
from database import Base


# Görev tablosu
class Gorev(Base):
    __tablename__ = "gorevler"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, nullable=False)
    oncelik = Column(String, default="normal")