import { Link } from '../router.tsx'
import '../styles/como-funciona.css'

type Paso = {
  n: number
  titulo: string
  texto: string
  png: string
  alt: string
  enlaces?: readonly (readonly [string, string])[]
}

const API_DOCS = 'https://ciai-api.nicolasmoreno.site/docs'
const REPO = 'https://github.com/nicolas2601/ciai-riesgo-avanzado'

const PASOS: readonly Paso[] = [
  {
    n: 1,
    titulo: 'Los datos oficiales',
    texto: 'Usamos el catálogo sísmico del SGC (208.215 eventos) y la población del DANE (87 municipios).',
    png: 'sistema-como-funciona',
    alt: 'Diagrama del sistema: catálogo sísmico del SGC y población del DANE alimentan el panel, los tres modelos, la API y la web.',
  },
  {
    n: 2,
    titulo: 'Del dato al panel, sin fuga del futuro',
    texto: 'Armamos una tabla por municipio y mes: 32 variables en 103 meses. Cada mes solo ve el pasado.',
    png: 'datos-a-panel',
    alt: 'Diagrama del paso de datos oficiales a un panel municipio por mes, donde los datos solo avanzan hacia adelante en el tiempo.',
  },
  {
    n: 3,
    titulo: 'Los tres niveles del reto',
    texto: 'Básico clasifica el riesgo (macro-F1 0,593). Medio agrupa municipios parecidos (silhouette 0,28). Avanzado prioriza con un agente.',
    png: 'tres-niveles',
    alt: 'Diagrama de los tres niveles: básico clasifica, medio agrupa municipios y avanzado prioriza con aprendizaje por refuerzo.',
    enlaces: [['/basico', 'Ir a Básico'], ['/medio', 'Ir a Medio'], ['/avanzado', 'Ir a Avanzado']],
  },
  {
    n: 4,
    titulo: 'Cómo aprende el agente y qué encontramos',
    texto: 'El agente PPO colapsa a una selección constante y no supera al ranking estático. Lo mostramos tal cual.',
    png: 'agente-refuerzo',
    alt: 'Diagrama del agente de refuerzo PPO: observa el panel, elige municipios, recibe recompensa y se compara con el ranking estático.',
    enlaces: [['/pruebas', 'Ver las pruebas']],
  },
  {
    n: 5,
    titulo: 'Dónde vive',
    texto: 'API con documentación Swagger, esta web y la versión v0.1.0 publicada en el repositorio.',
    png: 'despliegue',
    alt: 'Diagrama de despliegue: la web consume la API publicada con Swagger; el código y la versión v0.1.0 están en el repositorio.',
  },
]

function Diagrama({ png, alt }: { png: string; alt: string }) {
  return (
    <>
      <img className="cf__img" src={`/diagramas/${png}.png`} alt={alt} loading="lazy" />
      <a href={`/diagramas/${png}.html`} target="_blank" rel="noopener noreferrer">Abrir interactivo</a>
    </>
  )
}

function PasoVista({ p }: { p: Paso }) {
  return (
    <section className="cf__paso" aria-labelledby={`paso-${p.n}`}>
      <span className="cf__num">Paso {p.n}</span>
      <h2 id={`paso-${p.n}`} className="cf__h">{p.titulo}</h2>
      <p className="cf__p">{p.texto}</p>
      <Diagrama png={p.png} alt={p.alt} />
      {p.enlaces && (
        <p className="cf__enlaces">
          {p.enlaces.map(([to, t]) => <Link key={to} to={to}>{t}</Link>)}
        </p>
      )}
      {p.n === 5 && (
        <p className="cf__enlaces">
          <a href={API_DOCS} target="_blank" rel="noopener noreferrer">API (Swagger)</a>
          <a href={REPO} target="_blank" rel="noopener noreferrer">Repositorio</a>
        </p>
      )}
    </section>
  )
}

export default function ComoFunciona() {
  return (
    <div className="cf">
      <h1 className="cf__titulo">Cómo funciona todo</h1>
      <p className="cf__lead">Cinco pasos, de los datos oficiales a la priorización.</p>
      {PASOS.map((p) => <PasoVista key={p.n} p={p} />)}
      <section className="cf__prueba" aria-labelledby="probar">
        <h2 id="probar" className="cf__h">Cómo probarlo en 1 minuto</h2>
        <ol>
          <li>Ve a <Link to="/basico">Básico</Link>, elige Bucaramanga y 2025-03 y pulsa Clasificar.</li>
          <li>Ve a <Link to="/medio">Medio</Link> y toca un municipio del mapa.</li>
          <li>Ve a <Link to="/avanzado">Avanzado</Link> y mira la priorización con el aviso del PPO.</li>
        </ol>
      </section>
    </div>
  )
}
