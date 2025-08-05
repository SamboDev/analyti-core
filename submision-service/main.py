from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de SQLite (crea analyti_core.db en la carpeta actual)
DATABASE_URL = "sqlite:///analyti_core.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla jobs
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    status = Column(String, default="PENDIENTE")
    sentiment = Column(String, nullable=True)
    keywords = Column(String, nullable=True)

# Crea la base de datos y la tabla automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Habilita CORS para pruebas (luego puedes ajustar el dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema para recibir textos
class JobCreate(BaseModel):
    text: str

# Esquema para mostrar los resultados
class JobOut(BaseModel):
    id: int
    text: str
    status: str
    sentiment: str | None = None
    keywords: str | None = None

@app.post("/jobs/", response_model=JobOut)
def create_job(job: JobCreate):
    db = SessionLocal()
    db_job = Job(text=job.text, status="PENDIENTE")
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
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
