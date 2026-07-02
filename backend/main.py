# StudyMate AI - Backend
# Author: Rıfat Talha Keşkek

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
import models


# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)


# FastAPI uygulamamızı oluşturuyoruz
app = FastAPI(
    title="StudyMate AI",
    description="AI-powered learning assistant for students",
    version="0.2.0"
)


# Görev modeli - POST için şablon
class YeniGorev(BaseModel):
    baslik: str
    oncelik: str = "normal"


# Ana sayfa
@app.get("/")
def root():
    return {
        "message": "Merhaba! StudyMate AI'a hoş geldin! 🎓",
        "developer": "Rıfat Talha Keşkek",
        "status": "running",
        "version": "0.2.0 - Veritabanı entegre!"
    }


# Sağlık kontrolü
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Server çalışıyor ✅"
    }


# Tüm görevleri getir (veritabanından)
@app.get("/gorevler")
def gorevler(db: Session = Depends(get_db)):
    tum_gorevler = db.query(models.Gorev).all()
    return {
        "toplam": len(tum_gorevler),
        "gorevler": tum_gorevler
    }


# Yeni görev ekle (veritabanına)
@app.post("/gorev-ekle")
def gorev_ekle(gorev: YeniGorev, db: Session = Depends(get_db)):
    yeni_gorev = models.Gorev(
        baslik=gorev.baslik,
        oncelik=gorev.oncelik
    )
    db.add(yeni_gorev)
    db.commit()
    db.refresh(yeni_gorev)
    return {
        "mesaj": f"'{gorev.baslik}' görevi eklendi! ✅",
        "yeni_gorev": yeni_gorev
    }


# Görev sil (veritabanından)
@app.delete("/gorev-sil/{gorev_id}")
def gorev_sil(gorev_id: int, db: Session = Depends(get_db)):
    gorev = db.query(models.Gorev).filter(models.Gorev.id == gorev_id).first()
    if not gorev:
        raise HTTPException(status_code=404, detail="Bu ID'de görev yok!")
    
    silinen_baslik = gorev.baslik
    db.delete(gorev)
    db.commit()
    return {
        "mesaj": f"'{silinen_baslik}' silindi! 🗑️"
    }


# Görev güncelle (veritabanında)
@app.put("/gorev-guncelle/{gorev_id}")
def gorev_guncelle(gorev_id: int, yeni_bilgi: YeniGorev, db: Session = Depends(get_db)):
    gorev = db.query(models.Gorev).filter(models.Gorev.id == gorev_id).first()
    if not gorev:
        raise HTTPException(status_code=404, detail="Bu ID'de görev yok!")
    
    eski_baslik = gorev.baslik
    gorev.baslik = yeni_bilgi.baslik
    gorev.oncelik = yeni_bilgi.oncelik
    db.commit()
    db.refresh(gorev)
    return {
        "mesaj": f"'{eski_baslik}' → '{gorev.baslik}' olarak güncellendi! ✏️",
        "guncellenen": gorev
    }