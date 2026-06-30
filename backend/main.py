# StudyMate AI - Backend
# Author: Rıfat Talha Keşkek

from fastapi import FastAPI
from pydantic import BaseModel


# FastAPI uygulamamızı oluşturuyoruz
app = FastAPI(
    title="StudyMate AI",
    description="AI-powered learning assistant for students",
    version="0.1.0"
)


# Görev modeli - POST için şablon
class YeniGorev(BaseModel):
    baslik: str
    oncelik: str = "normal"


# Görev listesi (geçici, bilgisayar belleğinde)
gorev_listesi = []


# Ana sayfa - Karşılama mesajı
@app.get("/")
def root():
    return {
        "message": "Merhaba! StudyMate AI'a hoş geldin! 🎓",
        "developer": "Rıfat Talha Keşkek",
        "status": "running",
        "version": "0.1.0"
    }


# Sağlık kontrolü - Server çalışıyor mu?
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Server çalışıyor ✅"
    }


# Hakkında - Proje bilgileri
@app.get("/about")
def about():
    return {
        "project": "StudyMate AI",
        "description": "Öğrenciler için yapay zeka destekli çalışma asistanı",
        "features": [
            "📚 PDF özetleme",
            "🤖 AI ile soru-cevap",
            "⏱️ Pomodoro zamanlayıcı",
            "📊 İlerleme takibi",
            "💡 Akıllı flashcard'lar"
        ],
        "tech_stack": {
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL",
            "ai": "OpenAI GPT-4"
        }
    }


# Selamlama - Parametre alma örneği
@app.get("/selam/{isim}")
def selamla(isim: str):
    return {
        "mesaj": f"Selam {isim}! StudyMate AI'a hoş geldin! 🎉",
        "tavsiye": "Bugün hangi konuyu çalışacaksın?"
    }


# Pomodoro - Zamanlayıcı bilgisi
@app.get("/pomodoro")
def pomodoro():
    return {
        "calisma_suresi_dk": 25,
        "kisa_mola_dk": 5,
        "uzun_mola_dk": 15,
        "tekrar_sayisi": 4,
        "mesaj": "Hazır mısın? Pomodoro başlasın! 🍅"
    }


# Görev listesini getir - Dinamik
@app.get("/gorevler")
def gorevler():
    return {
        "toplam": len(gorev_listesi),
        "gorevler": gorev_listesi
    }


# Yeni görev ekle - POST
@app.post("/gorev-ekle")
def gorev_ekle(gorev: YeniGorev):
    gorev_listesi.append({
        "baslik": gorev.baslik,
        "oncelik": gorev.oncelik
    })
    return {
        "mesaj": f"'{gorev.baslik}' görevi eklendi! ✅",
        "toplam_gorev": len(gorev_listesi),
        "tum_gorevler": gorev_listesi
    }

# Görev sil - DELETE
@app.delete("/gorev-sil/{index}")
def gorev_sil(index: int):
    if index < 0 or index >= len(gorev_listesi):
        return {
            "hata": "Bu numarada görev yok!",
            "toplam_gorev": len(gorev_listesi)
        }
    
    silinen = gorev_listesi.pop(index)
    return {
        "mesaj": f"'{silinen['baslik']}' silindi! 🗑️",
        "toplam_gorev": len(gorev_listesi),
        "kalan_gorevler": gorev_listesi
    }

# Görev güncelle - PUT
@app.put("/gorev-guncelle/{index}")
def gorev_guncelle(index: int, gorev: YeniGorev):
    if index < 0 or index >= len(gorev_listesi):
        return {
            "hata": "Bu numarada görev yok!",
            "toplam_gorev": len(gorev_listesi)
        }
    
    eski_baslik = gorev_listesi[index]["baslik"]
    gorev_listesi[index] = {
        "baslik": gorev.baslik,
        "oncelik": gorev.oncelik
    }
    
    return {
        "mesaj": f"'{eski_baslik}' → '{gorev.baslik}' olarak güncellendi! ✏️",
        "guncellenen_gorev": gorev_listesi[index],
        "tum_gorevler": gorev_listesi
    }

