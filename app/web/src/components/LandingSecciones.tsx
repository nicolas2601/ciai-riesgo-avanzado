import { useState, type ReactNode } from 'react'
import { Link } from '../router.tsx'
import { SWAGGER } from './InicioGraficas.tsx'

export const REPO = 'https://github.com/nicolas2601/ciai-riesgo-avanzado'
const DOC = `${REPO}/blob/main/docs/DOCUMENTACION.md`

const trazo = {
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.6,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
}

function Svg({ children }: { children: ReactNode }) {
  return (
    <svg viewBox="0 0 32 32" width="32" height="32" role="presentation" aria-hidden="true">
      {children}
    </svg>
  )
}

const ICONO_CONCENTRA = (
  <Svg>
    <circle cx="16" cy="16" r="3" fill="currentColor" />
    <circle cx="16" cy="16" r="8" {...trazo} />
    <circle cx="16" cy="16" r="13" {...trazo} strokeDasharray="2 3" />
  </Svg>
)
const ICONO_CATALOGO = (
  <Svg>
    <path d="M4 26V6M4 26h24" {...trazo} />
    <path d="M9 22v-4M14 22v-6M19 22v-9M24 22v-14" {...trazo} />
  </Svg>
)
const ICONO_DANIO = (
  <Svg>
    <path d="M4 18c3-6 5 6 8 0s5 6 8 0 5 6 8 0" {...trazo} />
    <path d="M10 8h12M16 8V4" {...trazo} />
  </Svg>
)

export function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-titulo">
      <div className="hero__onda" aria-hidden="true" />
      <h1 id="hero-titulo" className="hero__titulo">
        Sismo,
        <br />
        <span className="hero__linea2">no previsible</span>
      </h1>
      <p className="hero__bajada">
        Santander tiembla a diario. Este proyecto ayuda a decidir qué municipios mirar primero el próximo mes.
        No predice sismos y no es una alerta oficial.
      </p>
      <div className="land-botones">
        <Link to="/avanzado" className="btn btn--primario">Ver priorización</Link>
        <a href={REPO} target="_blank" rel="noreferrer" className="btn btn--secundario">
          Ver documentación en GitHub
        </a>
      </div>
    </section>
  )
}

interface Dato { valor: string; texto: string; nota?: string }

export function Problematica({ total }: { total: string }) {
  const datos: Dato[] = [
    { valor: total, texto: 'sismos registrados por el Servicio Geológico Colombiano entre 1993 y 2026' },
    { valor: '55,2 %', texto: 'de los sismos del sistema nuevo ocurren en un solo municipio: Los Santos', nota: 'Fuente: docs/research/13-eda-sgc.md' },
  ]
  return (
    <section className="bloque land-seccion" aria-labelledby="problematica">
      <p className="eyebrow">La problemática</p>
      <h2 id="problematica" className="land-titulo">Santander tiembla todo el tiempo</h2>
      <p className="land-lead">
        Santander es uno de los departamentos con mayor actividad sísmica de Colombia. Bajo la Mesa
        de Los Santos está el Nido Sísmico de Bucaramanga (sismicidad intermedia, a unos 150 km de
        profundidad): genera cientos de sismos cada mes y el SGC publica cada evento.
      </p>
      <div className="land-datos">
        {datos.map((d) => (
          <div key={d.valor} className="land-dato">
            <p className="land-dato__valor">{d.valor}</p>
            <p className="land-dato__texto">{d.texto}</p>
            {d.nota ? <p className="land-dato__nota mono">{d.nota}</p> : null}
          </div>
        ))}
        <div className="land-dato">
          <p className="land-dato__valor">M 6,4</p>
          <p className="land-dato__texto">
            Sismo del 2015-03-10 en Los Santos. Tres fuentes, tres cifras, sin igualarlas:
          </p>
          <ul className="land-cifras mono">
            <li>6,4 Mw (SGC)</li>
            <li>6,2 (USGS)</li>
            <li>6,6 (comunicado)</li>
          </ul>
        </div>
      </div>
      <blockquote className="land-pregunta">
        ¿Dónde conviene mirar primero el próximo mes? Sin prometer predecir sismos.
      </blockquote>
    </section>
  )
}

const DIFICIL = [
  { icono: ICONO_CONCENTRA, t: 'La actividad se concentra', s: 'El Nido domina el catálogo y puede volver constante cualquier ranking.' },
  { icono: ICONO_CATALOGO, t: 'El catálogo cambia', s: 'Hay más eventos desde 2009 por la instrumentación. Es una hipótesis, no una causa probada.' },
  { icono: ICONO_DANIO, t: 'Actividad no es daño', s: 'Es una priorización exploratoria, no una alerta oficial.' },
]

export function PorQueEsDificil() {
  return (
    <section className="bloque land-seccion" aria-labelledby="dificil">
      <p className="eyebrow">Por qué es difícil</p>
      <h2 id="dificil" className="land-titulo">Tres razones para no confiarse</h2>
      <div className="land-tarjetas">
        {DIFICIL.map((d) => (
          <article key={d.t} className="land-tarjeta">
            <span className="land-tarjeta__icono">{d.icono}</span>
            <h3 className="land-tarjeta__titulo">{d.t}</h3>
            <p className="land-tarjeta__texto">{d.s}</p>
          </article>
        ))}
      </div>
    </section>
  )
}

export interface Hallazgo { to: string; nivel: string; modelo: string; cifra: string; texto: string }

export function Hallazgos({ items }: { items: Hallazgo[] }) {
  return (
    <section className="bloque land-seccion" aria-labelledby="hallazgos">
      <p className="eyebrow">Qué encontramos</p>
      <h2 id="hallazgos" className="land-titulo">Resultados, tal como salieron</h2>
      <div className="land-tarjetas">
        {items.map((h) => (
          <Link key={h.to} to={h.to} className="tarjeta land-hallazgo">
            <p className="eyebrow">{h.nivel} · {h.modelo}</p>
            <p className="land-dato__valor">{h.cifra}</p>
            <p className="tarjeta__texto">{h.texto}</p>
          </Link>
        ))}
      </div>
    </section>
  )
}

const LIMITES = [
  'El conjunto de prueba ya fue consultado: el resultado es confirmatorio, no un examen intacto.',
  'Las proyecciones de población del DANE son retrospectivas.',
  'Los polígonos de municipios son un espejo no oficial.',
  'No es una alerta oficial ni sustituye al SGC.',
]

export function Limites() {
  return (
    <section className="bloque land-seccion" aria-labelledby="limites">
      <p className="eyebrow">Límites y honestidad</p>
      <h2 id="limites" className="land-titulo">Lo que no podemos afirmar</h2>
      <ul className="land-limites">
        {LIMITES.map((l) => <li key={l}>{l}</li>)}
      </ul>
      <p className="land-enlace"><Link to="/metodologia">Ver metodología completa</Link> · <Link to="/pruebas">Ver pruebas</Link></p>
    </section>
  )
}

export function Equipo() {
  return (
    <section className="bloque land-seccion" aria-labelledby="equipo">
      <p className="eyebrow">Equipo</p>
      <h2 id="equipo" className="land-titulo">Syntax error II · UNAB</h2>
      <p className="land-lead">Nicolás Moreno, Julián Arteaga, Zabdiel Quintero.</p>
      <p className="land-enlaces">
        <a href={SWAGGER} target="_blank" rel="noreferrer">Swagger de la API</a>
        <a href={DOC} target="_blank" rel="noreferrer">docs/DOCUMENTACION.md</a>
        <a href={REPO} target="_blank" rel="noreferrer">Repositorio</a>
      </p>
    </section>
  )
}

export function Diagrama({ id, titulo, intro, archivo, alt }: {
  id: string
  titulo: string
  intro: string
  archivo: string
  alt: string
}) {
  const [fallo, setFallo] = useState(false)
  const src = `${import.meta.env.BASE_URL}diagramas/${archivo}`
  return (
    <section className="bloque land-seccion" aria-labelledby={id}>
      <h2 id={id} className="land-titulo">{titulo}</h2>
      <p className="land-lead">{intro}</p>
      {fallo ? (
        <p role="status" className="land-diagrama__falla">Diagrama no disponible.</p>
      ) : (
        <figure className="land-diagrama">
          <img src={src} alt={alt} loading="lazy" onError={() => setFallo(true)} />
          <figcaption>
            <a href={src} target="_blank" rel="noreferrer">Abrir el diagrama en grande</a>
          </figcaption>
        </figure>
      )}
    </section>
  )
}
