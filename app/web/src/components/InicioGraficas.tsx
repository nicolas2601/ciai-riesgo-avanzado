import { useEffect, useState } from 'react'
import { Link } from '../router.tsx'

export interface DatosInicio {
  total_eventos: number
  anio_min: number
  anio_max: number
  eventos_por_anio: { anio: number; total: number }[]
  balance_clases: { bajo: number; medio: number; alto: number }
}

const fmt = (n: number) => n.toLocaleString('es-CO')

export function useDatosInicio() {
  const [datos, setDatos] = useState<DatosInicio | null>(null)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/inicio.json`)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then(setDatos)
      .catch((e: Error) => setError(e.message))
  }, [])
  return { datos, error }
}

export const SWAGGER = 'https://ciai-api.nicolasmoreno.site/docs'
const MODELOS = [
  { to: '/basico', t: 'Básico', s: 'Supervisado · Random Forest' },
  { to: '/medio', t: 'Medio', s: 'No supervisado · KMeans k=3' },
  { to: '/avanzado', t: 'Avanzado', s: 'Refuerzo · PPO' },
]

export function Flujo() {
  return (
    <figure className="grafica">
      <ol className="flujo" aria-label="Flujo de datos del proyecto">
        <li className="flujo__caja">
          <strong>Fuentes oficiales</strong>
          <span>SGC catálogo · DANE población</span>
        </li>
        <li className="flujo__caja">
          <strong>Panel municipio × mes</strong>
          <span>32 variables · sin fuga del futuro</span>
        </li>
        <li className="flujo__caja flujo__caja--modelos">
          <strong>Tres modelos</strong>
          {MODELOS.map((m) => (
            <Link key={m.to} to={m.to} className="flujo__modelo">
              <b>{m.t}</b> {m.s}
            </Link>
          ))}
        </li>
        <li className="flujo__caja">
          <strong>API FastAPI</strong>
          <a href={SWAGGER} target="_blank" rel="noreferrer">
            /docs
          </a>
        </li>
        <li className="flujo__caja">
          <strong>Esta web</strong>
          <Link to="/">Inicio</Link>
        </li>
      </ol>
      <figcaption className="grafica__nota">Cada flecha es un paso: los datos solo avanzan hacia la derecha.</figcaption>
    </figure>
  )
}

const BARRAS = [
  { k: 'bajo', n: 'Bajo', c: 'var(--risk-bajo)', patron: '' },
  { k: 'medio', n: 'Medio', c: 'var(--risk-medio)', patron: 'url(#rayas)' },
  { k: 'alto', n: 'Alto', c: 'var(--risk-alto)', patron: 'url(#puntos)' },
] as const

export function BalanceClases({ b }: { b: DatosInicio['balance_clases'] }) {
  const max = Math.max(b.bajo, b.medio, b.alto)
  const resumen = `Barras del objetivo: bajo ${fmt(b.bajo)}, medio ${fmt(b.medio)}, alto ${fmt(b.alto)}.`
  return (
    <figure className="grafica">
      <svg viewBox="0 0 420 220" role="img" aria-label={resumen} className="grafica__svg">
        <defs>
          <pattern id="rayas" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="3" height="6" fill="#fff" opacity="0.55" />
          </pattern>
          <pattern id="puntos" width="6" height="6" patternUnits="userSpaceOnUse">
            <circle cx="3" cy="3" r="1.4" fill="#fff" opacity="0.7" />
          </pattern>
        </defs>
        {BARRAS.map((r, i) => {
          const h = Math.max(4, (b[r.k] / max) * 150)
          const x = 40 + i * 125
          return (
            <g key={r.k}>
              <rect x={x} y={170 - h} width="90" height={h} fill={r.c} />
              {r.patron ? <rect x={x} y={170 - h} width="90" height={h} fill={r.patron} /> : null}
              <text x={x + 45} y={162 - h} textAnchor="middle" className="grafica__valor">
                {fmt(b[r.k])}
              </text>
              <text x={x + 45} y={192} textAnchor="middle" className="grafica__eje">
                {r.n}
              </text>
            </g>
          )
        })}
        <line x1="20" x2="400" y1="170" y2="170" stroke="var(--border-strong)" />
      </svg>
      <figcaption className="grafica__nota">
        Por eso la exactitud (accuracy) engaña: predecir siempre &laquo;bajo&raquo; acierta ~95 %. Se usa
        macro-F1.
      </figcaption>
    </figure>
  )
}

export function EventosPorAnio({ d }: { d: DatosInicio }) {
  const pts = d.eventos_por_anio
  const max = Math.max(...pts.map((p) => p.total))
  const W = 640
  const H = 240
  const x = (a: number) => 50 + ((a - d.anio_min) / (d.anio_max - d.anio_min)) * (W - 70)
  const y = (n: number) => 200 - (n / max) * 170
  const linea = pts.map((p) => `${x(p.anio)},${y(p.total)}`).join(' ')
  const resumen = `Eventos por año entre ${d.anio_min} y ${d.anio_max}. Máximo ${fmt(max)}. Salto marcado entre 2009 y 2012.`
  return (
    <figure className="grafica">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={resumen} className="grafica__svg">
        <rect x={x(2009)} y="20" width={x(2012) - x(2009)} height="180" fill="var(--accent-quiet)" />
        <text x={x(2010.5)} y="16" textAnchor="middle" className="grafica__eje">
          2009–2012
        </text>
        <line x1="50" x2={W - 20} y1="200" y2="200" stroke="var(--border-strong)" />
        <polyline points={linea} fill="none" stroke="var(--accent)" strokeWidth="2.5" />
        {pts.map((p) => (
          <circle key={p.anio} cx={x(p.anio)} cy={y(p.total)} r="2.5" fill="var(--accent)">
            <title>{`${p.anio}: ${fmt(p.total)} eventos`}</title>
          </circle>
        ))}
        {[d.anio_min, 2000, 2010, 2020, d.anio_max].map((a) => (
          <text key={a} x={x(a)} y="220" textAnchor="middle" className="grafica__eje">
            {a}
          </text>
        ))}
        <text x="44" y={y(max) + 4} textAnchor="end" className="grafica__eje">
          {fmt(max)}
        </text>
        <text x="44" y="204" textAnchor="end" className="grafica__eje">
          0
        </text>
      </svg>
      <figcaption className="grafica__nota">
        El salto 2009–2012 es una hipótesis: consistente con mejoras de instrumentación, no una causa
        demostrada.
      </figcaption>
    </figure>
  )
}
