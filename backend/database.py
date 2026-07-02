# StudyMate AI - Veritabanı Ayarları

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite veritabanı dosyasının yolu
DATABASE_URL = "sqlite:///./studymate.db"

# Veritabanı motoru
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Oturum (session) fabrikası
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm modellerin temel sınıfı
Base = declarative_base()


# Veritabanı bağlantısı yardımcısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()