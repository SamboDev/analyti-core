const API_URL = "http://localhost:8000"; // Cambia esto por la URL de Render en producción

// Enviar texto para análisis (POST /jobs/)
export async function createJob(text) {
    const res = await fetch(`${API_URL}/jobs/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error("Error al crear el job");
    return await res.json();
}

// Consultar resultado por ID (GET /jobs/{id})
export async function getJob(id) {
    const res = await fetch(`${API_URL}/jobs/${id}`);
    if (!res.ok) throw new Error("Job no encontrado");
    return await res.json();
}
