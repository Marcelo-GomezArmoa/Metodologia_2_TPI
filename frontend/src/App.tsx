import React, { useEffect, useState } from 'react';

interface Solicitud {
  id: number;
  tipo: string;
  descripcion: string;
  email_estudiante: string;
  estado: string;
  prioridad: number;
  fecha_creacion: string;
}

export default function App() {
  const [solicitudes, setSolicitudes] = useState<Solicitud[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/solicitudes')
      .then(res => res.json())
      .then(data => setSolicitudes(data))
      .catch(err => console.error("Error al conectar con la API:", err));
  }, []);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>UTN - Gestión de Solicitudes Académicas</h1>
      <p>Panel de control y visualización de calidad externa (Calidad Externa vs Interna).</p>
      
      <h2>Solicitudes Registradas</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {solicitudes.map(s => (
          <li key={s.id} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px', borderRadius: '5px' }}>
            <strong>[{s.estado}] {s.tipo}</strong> (Prioridad: {s.prioridad})<br/>
            <span>{s.descripcion}</span><br/>
            <small>Estudiante: {s.email_estudiante} | Fecha: {s.fecha_creacion}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}