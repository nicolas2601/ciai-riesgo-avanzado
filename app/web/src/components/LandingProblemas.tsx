import type { ReactNode } from 'react'
import { Link } from '../router.tsx'
import { REPO } from './LandingSecciones.tsx'

export type Sello = 'HECHO' | 'HIPÓTESIS' | 'LIMITACIÓN'

const trazo = {
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.6,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
}

function Svg({ children }: { children: ReactNode }) {
  return (
    <svg viewBox="0 0 32 32" width="48" height="48" role="presentation" aria-hidden="true">
      {children}
    </svg>
  )
}

const I = {
  mapa: <Svg><path d="M5 8l7-3 8 3 7-3v19l-7 3-8-3-7 3z" {...trazo} /><path d="M12 5v19M20 8v19" {...trazo} /></Svg>,
  catalogo: <Svg><rect x="5" y="4" width="22" height="24" rx="2" {...trazo} /><path d="M10 11h12M10 16h12M10 21h7" {...trazo} /></Svg>,
  pregunta: <Svg><circle cx="16" cy="16" r="12" {...trazo} /><path d="M12 13a4 4 0 118 0c0 3-4 3-4 6M16 23h.01" {...trazo} /></Svg>,
  reto: <Svg><path d="M6 26V6l8 4-8 4M6 26h20" {...trazo} /><circle cx="23" cy="11" r="4" {...trazo} /></Svg>,
  concentra: <Svg><circle cx="16" cy="16" r="3" fill="currentColor" /><circle cx="16" cy="16" r="8" {...trazo} /><circle cx="16" cy="16" r="13" {...trazo} strokeDasharray="2 3" /></Svg>,
  red: <Svg><path d="M4 26h24" {...trazo} /><path d="M7 22l5-6 5 3 8-11" {...trazo} /><circle cx="25" cy="8" r="2" {...trazo} /></Svg>,
  balanza: <Svg><path d="M16 5v21M9 26h14M5 10h22" {...trazo} /><path d="M5 10l-3 8h8zM27 10l-3 8h8z" {...trazo} /></Svg>,
  danio: <Svg><path d="M4 18c3-6 5 6 8 0s5 6 8 0 5 6 8 0" {...trazo} /><path d="M10 8h12M16 8V4" {...trazo} /></Svg>,
  colapso: <Svg><path d="M6 8h20M6 16h20M6 24h20" {...trazo} /><circle cx="16" cy="8" r="2" fill="currentColor" /><circle cx="16" cy="16" r="2" fill="currentColor" /><circle cx="16" cy="24" r="2" fill="currentColor" /></Svg>,
  candado: <Svg><rect x="7" y="14" width="18" height="13" rx="2" {...trazo} /><path d="M11 14V10a5 5 0 0110 0v4" {...trazo} /></Svg>,
  fuente: <Svg><ellipse cx="16" cy="8" rx="9" ry="4" {...trazo} /><path d="M7 8v8c0 2 4 4 9 4s9-2 9-4V8M7 16v8c0 2 4 4 9 4s9-2 9-4v-8" {...trazo} /></Svg>,
}
export const ICONOS = I

export function SelloTag({ tipo }: { tipo: Sello }) {
  const glifo = tipo === 'HECHO' ? '■' : tipo === 'HIPÓTESIS' ? '◆' : '▲'
  return (
    <span className={`sello sello--${tipo === 'HECHO' ? 'hecho' : tipo === 'HIPÓTESIS' ? 'hipotesis' : 'limitacion'}`}>
      <span aria-hidden="true">{glifo}</span> {tipo}
    </span>
  )
}

export type Bloque = {
  icono: ReactNode
  titulo: string
  cifra: string
  evidencia: string
  sello: Sello
  fuente?: string
}

export function BloqueCifra({ b }: { b: Bloque }) {
  return (
    <article className="prob-card">
      <span className="prob-card__icono">{b.icono}</span>
      <h3 className="prob-card__titulo">{b.titulo}</h3>
      <p className="prob-card__cifra">{b.cifra}</p>
      <p className="prob-card__texto">{b.evidencia}</p>
      <p className="prob-card__pie">
        <SelloTag tipo={b.sello} />
        {b.fuente ? <a href={`${REPO}/blob/main/${b.fuente}`} target="_blank" rel="noreferrer">Fuente: {b.fuente}</a> : null}
      </p>
    </article>
  )
}

const CONTEXTO: Bloque[] = [
  { icono: I.mapa, titulo: 'Santander y el Nido Sísmico', cifra: '87 municipios', evidencia: 'Santander completo, con el Nido Sísmico de Bucaramanga como foco de actividad casi continua.', sello: 'HECHO', fuente: 'docs/research/13-eda-sgc.md' },
  { icono: I.catalogo, titulo: 'El SGC publica cada evento', cifra: '208.215 eventos', evidencia: 'El catálogo oficial del Servicio Geológico Colombiano registra cada evento con fecha, magnitud y lugar.', sello: 'HECHO', fuente: 'data/sgc/provenance.json' },
  { icono: I.pregunta, titulo: 'La pregunta', cifra: '1 mes', evidencia: '¿Dónde mirar primero el próximo mes? Sin prometer predecir sismos: se ordena la actividad esperada.', sello: 'HIPÓTESIS', fuente: 'docs/DOCUMENTACION.md' },
  { icono: I.reto, titulo: 'Lo que pide el reto', cifra: 'Clasificar y priorizar', evidencia: 'El reto pide clasificar y priorizar zonas. No pide alertar, y este sistema no emite alertas.', sello: 'LIMITACIÓN', fuente: 'docs/AUDITORIA_REQUISITOS.md' },
]

const PROBLEMAS: Bloque[] = [
  { icono: I.concentra, titulo: '1. Concentración', cifra: '55,2 %', evidencia: 'Los Santos reúne el 55,2 % de los eventos del catálogo nuevo (56.552 de 102.487). Cualquier ranking tiende a repetir los mismos municipios.', sello: 'HECHO', fuente: 'docs/research/13-eda-sgc.md' },
  { icono: I.red, titulo: '2. Cambio de instrumentación', cifra: '2.560 → 8.547', evidencia: 'Eventos por año: 2.560 (2008), 5.030 (2009) y 8.547 (2012). Consistente con mejoras de la red; no está demostrado que sea la causa.', sello: 'HIPÓTESIS', fuente: 'docs/research/13-eda-sgc.md' },
  { icono: I.balanza, titulo: '3. Desbalance', cifra: '8.466 / 242 / 166', evidencia: 'Bajo / medio / alto. Prediciendo siempre "bajo" se logra ~95 % de accuracy, por eso engaña. La clase medio no se detecta en test: F1 0 con 41 casos.', sello: 'LIMITACIÓN', fuente: 'artifacts/ml/critical_analysis.md' },
  { icono: I.danio, titulo: '4. Actividad no es daño', cifra: '0 alertas', evidencia: 'Medimos actividad sísmica registrada, no daño ni riesgo oficial. La priorización es exploratoria y no sustituye alertas oficiales.', sello: 'LIMITACIÓN', fuente: 'artifacts/ml/rl/limitaciones.md' },
  { icono: I.colapso, titulo: '5. El agente de refuerzo colapsa', cifra: '5 municipios fijos', evidencia: 'El PPO elige siempre los mismos 5 municipios. Validación: estático 0,5231 contra PPO 0,4974 (promedio de 3 semillas). Test: 0,4667 los dos, empate.', sello: 'HECHO', fuente: 'artifacts/ml/rl/final_audit.md' },
  { icono: I.candado, titulo: '6. El test ya fue consultado', cifra: '28 cortes', evidencia: 'El test del agente ya estaba expuesto por la pista de referencia: es lectura confirmatoria, no una evaluación independiente.', sello: 'LIMITACIÓN', fuente: 'docs/DOCUMENTACION.md' },
  { icono: I.fuente, titulo: '7. Fuente complementaria delgada', cifra: '1 variable', evidencia: 'El DANE aporta una sola variable (población, proyección retrospectiva) y los polígonos son un espejo no oficial sin licencia declarada.', sello: 'LIMITACIÓN', fuente: 'docs/research/14-fuente-oficial-2.md' },
]

type Medida = { problema: string; medida: string; ver: [string, string] }

const MEDIDAS: Medida[] = [
  { problema: '1. Concentración', medida: 'Clases por magnitud y Mc móvil, no por conteo bruto de eventos.', ver: ['docs/data/diccionario.md', 'Diccionario'] },
  { problema: '2. Cambio de instrumentación', medida: 'Panel sin fuga del futuro, con un test de no-fuga que lo comprueba.', ver: ['artifacts/ml/audit_report.md', 'Auditoría'] },
  { problema: '3. Desbalance', medida: 'Macro-F1 y F1 por clase en lugar de accuracy.', ver: ['artifacts/ml/metrics.json', 'Métricas'] },
  { problema: '4. Actividad no es daño', medida: 'Aviso "exploratorio" en la API y en la web.', ver: ['artifacts/ml/rl/limitaciones.md', 'Limitaciones'] },
  { problema: '5. Colapso del agente', medida: 'Comparación contra baselines y declaración abierta del colapso.', ver: ['artifacts/ml/rl/final_audit.md', 'Auditoría RL'] },
  { problema: '6. Test ya consultado', medida: 'Test marcado como ya usado; no se reajustó nada tras verlo.', ver: ['docs/DOCUMENTACION.md', 'Documentación'] },
  { problema: '7. Fuente delgada', medida: 'Fuentes y licencias declaradas, incluido el espejo no oficial.', ver: ['docs/data/geojson_santander.md', 'Polígonos'] },
]

export function LandingContexto() {
  return (
    <section className="bloque land-seccion" aria-labelledby="la-problematica">
      <p className="eyebrow">La problemática</p>
      <h2 id="la-problematica" className="land-titulo">Un reto de priorizar, no de alertar</h2>
      <p className="land-lead">Cuatro ideas para entender el contexto antes de ver los modelos.</p>
      <div className="prob-grid">{CONTEXTO.map((b) => <BloqueCifra key={b.titulo} b={b} />)}</div>
    </section>
  )
}

export function LandingSiete() {
  return (
    <section className="bloque land-seccion" aria-labelledby="siete-problemas">
      <p className="eyebrow">Lo que encontramos al revisar los datos</p>
      <h2 id="siete-problemas" className="land-titulo">Las 7 problemáticas que encontramos</h2>
      <p className="land-lead">Cada cifra sale de los archivos del repositorio. El sello dice si es un hecho, una hipótesis o una limitación.</p>
      <div className="prob-grid">{PROBLEMAS.map((b) => <BloqueCifra key={b.titulo} b={b} />)}</div>
    </section>
  )
}

export function LandingMedidas() {
  return (
    <section className="bloque land-seccion" aria-labelledby="que-hicimos-problema">
      <p className="eyebrow">Respuesta</p>
      <h2 id="que-hicimos-problema" className="land-titulo">Qué hicimos frente a cada problema</h2>
      <div className="tabla-scroll">
        <table className="prob-tabla">
          <caption className="sr-only">Medida concreta por cada problemática</caption>
          <thead><tr><th scope="col">Problema</th><th scope="col">Medida concreta</th><th scope="col">Evidencia</th></tr></thead>
          <tbody>
            {MEDIDAS.map((m) => (
              <tr key={m.problema}>
                <th scope="row">{m.problema}</th>
                <td>{m.medida}</td>
                <td><a href={`${REPO}/blob/main/${m.ver[0]}`} target="_blank" rel="noreferrer">{m.ver[1]}</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export function LandingImpacto() {
  return (
    <section className="bloque land-seccion" aria-labelledby="impacto">
      <p className="eyebrow">Impacto</p>
      <h2 id="impacto" className="land-titulo">Para quién sirve y cómo se usa</h2>
      <div className="prob-grid prob-grid--dos">
        <article className="prob-card">
          <h3 className="prob-card__titulo">Hoy: priorizar dónde mirar primero</h3>
          <p className="prob-card__texto">Sirve a quien revisa Santander mes a mes y debe decidir con tiempo limitado qué municipios mirar primero. Es una lista exploratoria, sin prometer alertas.</p>
          <p className="prob-card__pie"><SelloTag tipo="HECHO" /><Link to="/avanzado">Ver priorización</Link></p>
        </article>
        <article className="prob-card">
          <h3 className="prob-card__titulo">Para un uso real haría falta</h3>
          <ul className="land-limites">
            <li>Validación independiente, con un test que nadie haya visto.</li>
            <li>Más fuentes oficiales: amenaza sísmica y movimientos en masa del SGC.</li>
          </ul>
          <p className="prob-card__pie"><SelloTag tipo="LIMITACIÓN" /></p>
        </article>
      </div>
    </section>
  )
}
