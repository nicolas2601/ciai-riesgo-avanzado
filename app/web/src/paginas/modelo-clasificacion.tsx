import '../estilos.ts'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Shell } from '../components/Shell.tsx'
import { BannerEjemplo } from '../components/BannerEjemplo.tsx'
import { Mapa } from '../pages/Mapa.tsx'
import { useMunicipios } from '../lib/datos.ts'

// Pagina del modelo de clasificacion: las tres clases y el mapa de los 87 municipios.
function Clasificacion() {
  const mun = useMunicipios()
  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Modelo de clasificación</p>
        <h1 className="pitch__titulo">Tres clases de riesgo por municipio</h1>
        <p className="pitch__texto">
          El objetivo es el nivel de riesgo sísmico del municipio en el mes siguiente, derivado del
          conteo de eventos registrados en el catálogo. La unidad es el municipio: 87 en Santander.
        </p>
      </section>

      {mun.ejemplo ? <BannerEjemplo /> : null}

      <section className="pitch">
        <p className="eyebrow">Qué significa cada nivel</p>
        <div className="filete" />
        <div className="acordeon">
          <p>
            <strong>Bajo, medio y alto son frecuencia relativa de reportes</strong> en el mes, no
            severidad ni daño. Un municipio con más registros aparece más alto porque tiene más
            actividad registrada, no porque el sismo haya sido más fuerte.
          </p>
          <p>
            <strong>Sin dato y sin priorización no son Bajo.</strong> Un municipio sin registro en
            el corte no es un municipio tranquilo: es un municipio del que no sabemos. La interfaz
            los distingue con color, icono y etiqueta propios.
          </p>
          <p>
            La incertidumbre acompaña siempre al nivel. Ninguna vista muestra un nivel sin su
            conjunto de predicción o su motivo de abstención.
          </p>
        </div>
      </section>

      <Mapa />
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Shell actual="Clasificación">
      <Clasificacion />
    </Shell>
  </StrictMode>,
)
