import { Link } from '../router.tsx'
import {
  BalanceClases,
  EventosPorAnio,
  Flujo,
  SWAGGER,
  useDatosInicio,
} from '../components/InicioGraficas.tsx'

const REPO = 'https://github.com/nicolas2601/ciai-riesgo-avanzado'

const ACCIONES = [
  { to: '/basico', n: '01', t: 'Clasificar un municipio', s: 'Elige municipio y mes: clase de riesgo del mes siguiente.' },
  { to: '/medio', n: '02', t: 'Ver grupos en el mapa', s: 'Municipios agrupados por perfil de actividad.' },
  { to: '/avanzado', n: '03', t: 'Ver la priorización', s: 'Elecciones del PPO y su nota honesta.' },
]

export function Inicio() {
  const { datos, error } = useDatosInicio()
  const kpis = [
    { v: datos ? datos.total_eventos.toLocaleString('es-CO') : '…', l: `eventos del catálogo (${datos?.anio_min ?? 1993}-${datos?.anio_max ?? 2026})` },
    { v: '87', l: 'municipios' },
    { v: '32', l: 'variables en el panel' },
    { v: '103', l: 'meses (2018-03 a 2026-09)' },
  ]
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
          Priorización exploratoria de municipios de Santander con datos del SGC. No es una alerta
          oficial.
        </p>
      </section>

      <section className="kpis" aria-label="Cifras del proyecto">
        {kpis.map((k) => (
          <div key={k.l} className="kpi">
            <p className="kpi__valor">{k.v}</p>
            <p className="kpi__etiqueta">{k.l}</p>
          </div>
        ))}
      </section>

      <section className="bloque">
        <p className="eyebrow">Cómo fluye todo</p>
        <Flujo />
      </section>

      <section className="bloque">
        <p className="eyebrow">Los datos reales</p>
        {error ? (
          <p role="alert" className="mono">
            No se pudieron cargar las gráficas (data/inicio.json): {error}
          </p>
        ) : null}
        {datos ? (
          <div className="graficas-par">
            <BalanceClases b={datos.balance_clases} />
            <EventosPorAnio d={datos} />
          </div>
        ) : error ? null : (
          <p className="mono" role="status">Cargando gráficas…</p>
        )}
      </section>

      <section className="tarjetas-niveles" aria-label="Qué puedes hacer">
        {ACCIONES.map((a) => (
          <Link key={a.to} to={a.to} className="tarjeta">
            <p className="eyebrow">{a.n}</p>
            <h2 className="tarjeta__titulo">{a.t}</h2>
            <p className="tarjeta__texto">{a.s}</p>
          </Link>
        ))}
      </section>

      <section className="bloque enlaces">
        <a href={SWAGGER} target="_blank" rel="noreferrer">Swagger de la API</a>
        <a href={REPO} target="_blank" rel="noreferrer">Repositorio</a>
      </section>
    </div>
  )
}
