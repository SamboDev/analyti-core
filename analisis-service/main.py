from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///analyti_core_analysis.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo para almacenar los análisis
class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String, nullable=True)
    keywords = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Analysis Service",
    description="Microservicio para análisis de sentimiento y extracción de palabras clave.",
    version="1.0.0"
)

# Esquema de entrada
class AnalysisRequest(BaseModel):
    text: str

# Esquema de salida
class AnalysisResult(BaseModel):
    id: int
    text: str
    sentiment: str
    keywords: str

@app.post("/analyze/", response_model=AnalysisResult)
def analyze(request: AnalysisRequest):
    texto = request.text.lower()
    # Análisis de sentimiento simple
    if any(word in texto for word in ["feliz", "bien", "excelente", "alegre"]):
        sentimiento = "positivo"
    elif any(word in texto for word in ["triste", "mal", "enojado", "horrible"]):
        sentimiento = "negativo"
    else:
        sentimiento = "neutral"
    # Extracción de palabras clave (palabras de más de 4 letras)
    palabras = [w.strip(".,;:¿?¡!") for w in texto.split()]
    palabras_clave = list({w for w in palabras if len(w) > 4})
    palabras_clave_str = ", ".join(palabras_clave)
    # Guardar en la base
    db = SessionLocal()
    analysis = Analysis(
        text=request.text,
        sentiment=sentimiento,
        keywords=palabras_clave_str
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    db.close()
    return {
        "id": analysis.id,
        "text": analysis.text,
        "sentiment": analysis.sentiment,
        "keywords": analysis.keywords
    }

@app.get("/analyses/{analysis_id}", response_model=AnalysisResult)
def get_analysis(analysis_id: int):
    db = SessionLocal()
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    db.close()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "id": analysis.id,
        "text": analysis.text,
        "sentiment": analysis.sentiment,
        "keywords": analysis.keywords
    }

@app.get("/")
def health_check():
    return {"status": "ok"}
