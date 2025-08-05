const API_URL = process.env.REACT_APP_API_URL;
const SUBMISSION_URL = process.env.REACT_APP_SUBMISSION_URL;

// Crear job de análisis
export async function createJob(text) {
    const res = await fetch(`${API_URL}/jobs/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error("Error al crear el job");
    return await res.json();
}

// Obtener resultado de job
export async function getJob(id) {
    const res = await fetch(`${API_URL}/jobs/${id}`);
    if (!res.ok) throw new Error("Job no encontrado");
    return await res.json();
}

// Ejemplo: enviar datos a otro servicio (submission)
export async function submitAnalysis(data) {
    const res = await fetch(`${SUBMISSION_URL}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error al enviar los datos");
    return await res.json();
}
