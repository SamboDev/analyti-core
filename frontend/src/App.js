import React, { useState } from "react";
import * as style from "./AppStyles"; // importa los estilos

import { createJob, getJob } from "./services/api"; // tu archivo de servicios

export default function App() {
  const [input, setInput] = useState("");
  const [job, setJob] = useState(null);
  const [jobId, setJobId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Crear nuevo análisis
  const handleAnalyze = async () => {
    setError(""); setJob(null); setLoading(true);
    try {
      const data = await createJob(input);
      setJob(data);
      setJobId(data.id);
    } catch (e) {
      setError(e.message || "Ocurrió un error");
    } finally {
      setLoading(false);
    }
  };

  // Consultar análisis por ID
  const handleGetJob = async () => {
    setError(""); setJob(null); setLoading(true);
    try {
      const data = await getJob(jobId);
      setJob(data);
    } catch (e) {
      setError(e.message || "Ocurrió un error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={style.container}>
      <h2 style={style.headline}>📝 Analizador de Sentimientos</h2>

      <label style={style.label}>Texto a analizar:</label>
      <textarea
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Escribe aquí tu texto..."
        rows={3}
        style={{ ...style.input, resize: "vertical" }}
      />
      <button style={style.button} onClick={handleAnalyze} disabled={loading || !input.trim()}>
        {loading ? "Analizando..." : "Analizar"}
      </button>

      <label style={style.label}>Consultar análisis por ID:</label>
      <div style={{ display: "flex", gap: 8, marginBottom: 6 }}>
        <input
          type="number"
          value={jobId}
          onChange={e => setJobId(e.target.value)}
          placeholder="ID de análisis"
          style={{ ...style.input, width: "75%" }}
        />
        <button
          style={{ ...style.button, width: "25%", padding: 0, marginBottom: 0 }}
          onClick={handleGetJob}
          disabled={loading || !jobId}
        >
          Consultar
        </button>
      </div>

      {error && <div style={style.error}>{error}</div>}

      {job && (
        <div style={style.card}>
          <p><b>ID:</b> {job.id}</p>
          <p><b>Texto:</b> {job.text}</p>
          <p>
            <b>Estado:</b>{" "}
            <span style={{ color: job.status === "COMPLETADO" ? "#388e3c" : "#d32f2f" }}>
              {job.status}
            </span>
          </p>
          <p><b>Sentimiento:</b> {job.sentiment ?? <i>Pendiente</i>}</p>
          <p><b>Palabras clave:</b> {job.keywords ?? <i>Pendiente</i>}</p>
        </div>
      )}
    </div>
  );
}
