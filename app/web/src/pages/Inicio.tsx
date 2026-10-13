import { useHealth } from '../api/hooks.ts'
import { Link } from '../router.tsx'
import { Estado } from '../components/Estado.tsx'

const NIVELES = [
  {
    to: '/basico',
    n: '01',
    titulo: 'Básico: clasificar un municipio',
    texto: 'Elige municipio y mes y obtén la clase de riesgo del mes siguiente con sus probabilidades.',
  },
  {
    to: '/medio',
    n: '02',
    titulo: 'Medio: grupos de municipios',
    texto: 'Mapa de Santander con los municipios agrupados por perfil de actividad registrada.',
  },
  {
    to: '/avanzado',
    n: '03',
    titulo: 'Avanzado: priorización',
    texto: 'Qué municipios elige cada método con K cupos y qué recompensa real tuvo cada elección.',
  },
]

export function Inicio() {
  const salud = useHealth()
  return (
    <div className="contenedor">
      <section className="hero">
        <div className="hero__onda" aria-hidden="true" />
        <h1 className="hero__titulo">
          Sismo,
          <br />
          <span className="hero__linea2">no previsible</span>
        </h1>
        <p className="hero__bajada">
          Priorización exploratoria de los 87 municipios de Santander con el catálogo sísmico del
          SGC. No predice sismos ni es una alerta oficial: ordena dónde mirar primero.
        </p>
      </section>

      <section className="tarjetas-niveles" aria-label="Los tres niveles del reto">
        {NIVELES.map((n) => (
          <Link key={n.to} to={n.to} className="tarjeta">
            <p className="eyebrow">{n.n}</p>
            <h2 className="tarjeta__titulo">{n.titulo}</h2>
            <p className="tarjeta__texto">{n.texto}</p>
          </Link>
        ))}
      </section>

      <section className="bloque">
        <p className="eyebrow">Estado de la API</p>
        <Estado e={salud} que="el estado de la API" />
        {salud.data ? (
          <p className="mono">
            {salud.data.status} · versión {salud.data.version}
          </p>
        ) : null}
      </section>
    </div>
  )
}
