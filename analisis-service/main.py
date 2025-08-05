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

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String, nullable=True)
    keywords = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    id: int
    text: str
    sentiment: str
    keywords: str

@app.post("/analyze/", response_model=AnalysisResult)
def analyze(request: AnalysisRequest):
    # --- Lógica "dummy" de análisis ---
    texto = request.text.lower()
    sentimiento = "positivo" if "feliz" in texto or "bien" in texto else "neutral"
    palabras_clave = ", ".join([w for w in texto.split() if len(w) > 4])

    db = SessionLocal()
    analysis = Analysis(
        text=request.text,
        sentiment=sentimiento,
        keywords=palabras_clave
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    db.close()
    return analysis

@app.get("/analyses/{analysis_id}", response_model=AnalysisResult)
def get_analysis(analysis_id: int):
    db = SessionLocal()
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    db.close()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
