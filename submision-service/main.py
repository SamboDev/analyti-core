from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
import os  # <-- Importa os para leer variables de entorno

DATABASE_URL = "sqlite:///analyti_core.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    status = Column(String, default="PENDIENTE")
    sentiment = Column(String, nullable=True)
    keywords = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Submision Service",
    description="Microservicio para recepción de textos y orquestación de análisis.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobCreate(BaseModel):
    text: str

class JobOut(BaseModel):
    id: int
    text: str
    status: str
    sentiment: str | None = None
    keywords: str | None = None

# Lee la variable de entorno, usa localhost si no está configurada
ANALYSIS_SERVICE_URL = os.getenv(
    "ANALYSIS_SERVICE_URL",
    "http://localhost:8001/analyze/"
)

@app.post("/jobs/", response_model=JobOut)
def create_job(job: JobCreate):
    db = SessionLocal()
    db_job = Job(text=job.text, status="PENDIENTE")
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    try:
        response = requests.post(ANALYSIS_SERVICE_URL, json={"text": job.text}, timeout=5)
        if response.status_code == 200:
            result = response.json()
            db_job.sentiment = result.get("sentiment")
            db_job.keywords = result.get("keywords")
            db_job.status = "COMPLETADO"
            db.commit()
            db.refresh(db_job)
        else:
            db_job.status = "ERROR_ANALISIS"
            db.commit()
            db.refresh(db_job)
    except Exception as e:
        db_job.status = "ERROR_CONEXION"
        db.commit()
        db.refresh(db_job)
    finally:
        db.close()
    return db_job

@app.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int):
    db = SessionLocal()
    db_job = db.query(Job).filter(Job.id == job_id).first()
    db.close()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.get("/")
def health_check():
    return {"status": "ok"}
