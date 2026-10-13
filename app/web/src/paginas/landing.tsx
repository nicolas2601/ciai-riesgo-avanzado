import '../estilos.ts'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Shell } from '../components/Shell.tsx'
import { BannerEjemplo } from '../components/BannerEjemplo.tsx'
import { ChipCifra } from '../components/ChipCifra.tsx'
import { EstadoVacio } from '../components/EstadoVacio.tsx'
import { useMunicipios, useMetricas, usePriorizacion } from '../lib/datos.ts'

// Landing: la presentacion es la portada. Un scroll por las secciones del pitch.
const SECCIONES = [
  {
    id: 'problema',
    eyebrow: 'Problema',
    titulo: 'Santander está dentro del Nido de Bucaramanga',
    cuerpo:
      'Bajo la Mesa de Los Santos hay una de las zonas de sismicidad intermedia más activas del mundo. Nuestra pregunta no es cuándo ni dónde habrá un sismo: es dónde conviene poner la atención técnica primero.',
  },
  {
    id: 'datos',
    eyebrow: 'Datos',
    titulo: 'Todo sale del catálogo del SGC',
    cuerpo:
      'Un único origen oficial, con URL, fecha de descarga y filtros registrados. La unidad es el municipio: 87 en Santander.',
  },
  {
    id: 'modelos',
    eyebrow: 'Modelos',
    titulo: 'Clasificación, supervisado y refuerzo',
    cuerpo:
      'Tres bloques: un modelo de clasificación por niveles, un conjunto supervisado de referencia y un agente de refuerzo que elige los municipios antes de ver el mes siguiente.',
  },
  {
    id: 'resultados',
    eyebrow: 'Resultados',
    titulo: 'Qué eligió y qué pasó después',
    cuerpo:
      'Recorremos los cortes y miramos la priorización del agente junto a la actividad que realmente ocurrió.',
  },
  {
    id: 'impacto',
    eyebrow: 'Impacto',
    titulo: 'Decidir dónde mirar primero',
    cuerpo:
      'Ordenar la atención técnica con la información disponible en el momento del corte. No es un sistema de alerta temprana.',
  },
  {
    id: 'limites',
    eyebrow: 'Límites',
    titulo: 'Lo que este trabajo no es',
    cuerpo:
      'No prevee sismos, no mide daño y no es severidad. Los niveles son frecuencia relativa de reportes. La sacudida es una estimación con atenuación declarada, no una observación.',
  },
  {
    id: 'equipo',
    eyebrow: 'Equipo',
    titulo: 'Syntax error II — UNAB',
    cuerpo: 'N. Moreno · J. Arteaga · Z. Quintero. Hackathon CIAI UTSmart 2026, categoría Avanzado.',
  },
]

const MODELOS = [
  {
    href: '/modelo-clasificacion.html',
    titulo: 'Modelo de clasificación',
    texto: 'Las tres clases de riesgo por municipio y el mapa de los 87 municipios, mes a mes.',
  },
  {
    href: '/modelo-supervisado.html',
    titulo: 'Modelo supervisado',
    texto: 'Algoritmos de referencia, validación cronológica por bloques y métricas con su intervalo.',
  },
  {
    href: '/modelo-refuerzo.html',
    titulo: 'Modelo de refuerzo',
    texto: 'El agente elige K municipios antes de ver el futuro. La máquina del tiempo muestra si acertó.',
  },
]

function Contenido() {
  const mun = useMunicipios()
  const met = useMetricas()
  const pri = usePriorizacion()
  const ejemplo = mun.ejemplo || met.ejemplo || pri.ejemplo

  return (
    <>
      <section className="hero">
        <p className="hero__onda" aria-hidden="true" />
        <h1 className="hero__titulo">
          SISMO,
          <br />
          <span className="hero__linea2">NO PREVISIBLE</span>
        </h1>
        <p className="hero__bajada">
          Analizamos el catálogo sísmico del Servicio Geológico Colombiano con aprendizaje por
          refuerzo para priorizar dónde mirar primero. El agente elige sus municipios{' '}
          <strong>antes</strong> de saber qué mes viene. Esto cuenta qué acertó.
        </p>
        <a href="/modelo-refuerzo.html" className="btn btn--primario">
          Ver la máquina del tiempo
        </a>
      </section>

      {ejemplo ? <BannerEjemplo /> : null}

      <EstadoVacio cargando={mun.cargando} error={mun.error} />
      <p className="eyebrow">Cifras del experimento</p>
      <div className="filete" />
      <div className="fila-chips">
        <ChipCifra valor={mun.datos?.municipios.length ?? null} etiqueta="municipios" />
        <ChipCifra valor={pri.datos?.k ?? null} etiqueta="K priorizados" />
        <ChipCifra valor={met.datos?.basico.f1_macro ?? null} etiqueta="F1 macro" ejemplo={ejemplo} />
      </div>

      {SECCIONES.map((s) => (
        <section key={s.id} id={s.id} className="pitch">
          <p className="eyebrow">{s.eyebrow}</p>
          <div className="filete" />
          <h2 className="pitch__titulo">{s.titulo}</h2>
          <p className="pitch__texto">{s.cuerpo}</p>
        </section>
      ))}

      <p className="eyebrow" style={{ marginTop: 'var(--s-9)' }}>
        Los tres modelos
      </p>
      <div className="filete" />
      <div className="rejilla">
        {MODELOS.map((m) => (
          <a key={m.href} href={m.href} className="tarjeta">
            <h3 className="tarjeta__titulo">{m.titulo}</h3>
            <p className="tarjeta__texto">{m.texto}</p>
          </a>
        ))}
      </div>
    </>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Shell actual="Presentación">
      <div className="contenedor">
        <Contenido />
      </div>
    </Shell>
  </StrictMode>,
)
