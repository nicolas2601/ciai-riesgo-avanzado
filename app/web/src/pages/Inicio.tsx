import '../styles/inicio.css'
import '../styles/landing-problemas.css'
import { Link } from '../router.tsx'
import {
  BalanceClases,
  EventosPorAnio,
  Flujo,
  useDatosInicio,
} from '../components/InicioGraficas.tsx'
import {
  Diagrama,
  Equipo,
  Hallazgos,
  Hero,
  Limites,
  PorQueEsDificil,
  Problematica,
  type Hallazgo,
} from '../components/LandingSecciones.tsx'
import { LandingImpacto, LandingContexto, LandingMedidas, LandingSiete } from '../components/LandingProblemas.tsx'
import { LandingCumplimiento } from '../components/LandingCumplimiento.tsx'

const HALLAZGOS: Hallazgo[] = [
  { to: '/basico', nivel: 'Básico', modelo: 'Random Forest', cifra: '0,593', texto: 'macro-F1 del Random Forest, contra 0,325 del baseline que siempre responde "bajo".' },
  { to: '/medio', nivel: 'Medio', modelo: 'KMeans k=3', cifra: '0,28', texto: 'silhouette con 3 grupos de municipios. Separación modesta, no tajante.' },
  { to: '/avanzado', nivel: 'Avanzado', modelo: 'PPO', cifra: '0,467', texto: 'El PPO empata con el ranking estático (0,467) y colapsa a una selección constante: no lo supera.' },
]

const ENLACES_MODELOS = [
  ['/basico', 'Básico'],
  ['/medio', 'Medio'],
  ['/avanzado', 'Avanzado'],
  ['/pruebas', 'Pruebas'],
  ['/metodologia', 'Metodología'],
] as const

export function Inicio() {
  const { datos, error } = useDatosInicio()
  const total = datos ? datos.total_eventos.toLocaleString('es-CO') : '208.215'
  return (
    <div className="contenedor land">
      <Hero />
      <div className="land-cta">
        <Link to="/como-funciona" className="btn btn--primario">Ver cómo funciona todo</Link>
      </div>
      <Problematica total={total} />
      <LandingContexto />
      <LandingSiete />
      <LandingMedidas />
      <PorQueEsDificil />

      <Diagrama
        id="como-funciona"
        titulo="Cómo funciona"
        intro="Tomamos los datos oficiales, los ordenamos por municipio y mes, y tres modelos distintos los analizan. Todo se consulta desde esta web."
        archivo="sistema-como-funciona.png"
        alt="Diagrama del sistema: fuentes oficiales, panel municipio por mes, tres modelos, API y web."
      />

      <section className="bloque land-seccion" aria-labelledby="hicimos">
        <p className="eyebrow">Qué hicimos</p>
        <h2 id="hicimos" className="land-titulo">De datos oficiales a una priorización</h2>
        <p className="land-lead">Cada caja es un paso. Los datos solo avanzan hacia la derecha: nunca se usa el futuro para predecir.</p>
        <Flujo />
        <p className="land-enlaces">
          {ENLACES_MODELOS.map(([to, t]) => (
            <Link key={to} to={to}>{t}</Link>
          ))}
        </p>
      </section>

      <Diagrama
        id="datos-panel"
        titulo="De los datos al panel"
        intro="El catálogo del SGC y la población del DANE se convierten en una tabla: una fila por municipio y por mes."
        archivo="datos-a-panel.png"
        alt="Diagrama de cómo los datos del SGC y del DANE se transforman en el panel municipio por mes."
      />
      <Diagrama
        id="tres-niveles"
        titulo="Los tres niveles"
        intro="Básico clasifica, Medio agrupa y Avanzado decide dónde mirar con un presupuesto limitado."
        archivo="tres-niveles.png"
        alt="Diagrama de los tres niveles de modelos: básico supervisado, medio no supervisado y avanzado por refuerzo."
      />

      <Hallazgos items={HALLAZGOS} />

      <section className="bloque land-seccion" aria-labelledby="graficas">
        <p className="eyebrow">Los datos reales</p>
        <h2 id="graficas" className="land-titulo">Qué tan desbalanceado está el problema</h2>
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

      <LandingImpacto />
      <LandingCumplimiento />

      <Diagrama
        id="agente"
        titulo="Cómo aprende el agente"
        intro="El agente de refuerzo elige municipios cada mes y recibe una recompensa. Aquí vemos si de verdad aprendió algo."
        archivo="agente-refuerzo.png"
        alt="Diagrama del agente de refuerzo: observa el estado, elige municipios y recibe una recompensa."
      />

      <Limites />

      <Diagrama
        id="donde-vive"
        titulo="Dónde vive"
        intro="La API y la web están publicadas. Puedes probar la API tú mismo en el Swagger."
        archivo="despliegue.png"
        alt="Diagrama del despliegue: servidor con la API, la web publicada y los datos."
      />

      <Equipo />
    </div>
  )
}
