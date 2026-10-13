import { REPO } from './LandingSecciones.tsx'

type Estado = 'CUMPLE' | 'PARCIAL'
type Fila = { req: string; estado: Estado; ev: string; ruta: string }

const BASICO: Fila[] = [
  { req: 'Limpiar y preparar datos de la zona', estado: 'CUMPLE', ev: 'build_panel.py', ruta: 'ml/eda/build_panel.py' },
  { req: 'Modelo supervisado de clasificación', estado: 'CUMPLE', ev: 'metrics.json', ruta: 'artifacts/ml/metrics.json' },
  { req: 'Niveles bajo, medio y alto definidos', estado: 'CUMPLE', ev: 'Diccionario', ruta: 'docs/data/diccionario.md' },
  { req: '10 variables mínimas justificadas', estado: 'CUMPLE', ev: 'Diccionario', ruta: 'docs/data/diccionario.md' },
  { req: 'Métricas para evaluar', estado: 'CUMPLE', ev: 'metrics.json', ruta: 'artifacts/ml/metrics.json' },
  { req: 'Entender en qué casos se equivoca', estado: 'CUMPLE', ev: 'Análisis crítico', ruta: 'artifacts/ml/critical_analysis.md' },
  { req: 'Producto con una entrada y su resultado', estado: 'CUMPLE', ev: 'Pruebas e2e', ruta: 'docs/research/17-pruebas-e2e.md' },
  { req: 'Exploración inicial con al menos 3 gráficas', estado: 'PARCIAL', ev: 'EDA del SGC', ruta: 'docs/research/13-eda-sgc.md' },
]

const MEDIO: Fila[] = [
  { req: 'Únicamente modelo no supervisado', estado: 'CUMPLE', ev: 'model.py', ruta: 'ml/medio/model.py' },
  { req: '15 variables mínimas, incluidas territoriales', estado: 'CUMPLE', ev: 'Informe de clusters', ruta: 'docs/research/16-medio-clusters.md' },
  { req: 'Comparar la zona con otras unidades territoriales', estado: 'CUMPLE', ev: 'clusters.json', ruta: 'app/web/public/data/clusters.json' },
  { req: 'Evaluación y comparación de enfoques', estado: 'PARCIAL', ev: 'Informe de clusters', ruta: 'docs/research/16-medio-clusters.md' },
  { req: 'Interpretación de grupos e importancia de variables', estado: 'PARCIAL', ev: 'Informe de clusters', ruta: 'docs/research/16-medio-clusters.md' },
  { req: 'Visualización territorial reproducible', estado: 'CUMPLE', ev: 'Mapa de clusters', ruta: 'docs/figures/medio-clusters.png' },
  { req: 'Explicación útil para estimar o clasificar el riesgo', estado: 'PARCIAL', ev: 'Informe de clusters', ruta: 'docs/research/16-medio-clusters.md' },
  { req: 'Arquitectura con diagrama', estado: 'CUMPLE', ev: 'Documentación', ruta: 'docs/DOCUMENTACION.md' },
]

const AVANZADO: Fila[] = [
  { req: 'Cumplir Básico y Medio', estado: 'PARCIAL', ev: 'Auditoría', ruta: 'docs/AUDITORIA_REQUISITOS.md' },
  { req: 'Aprendizaje por refuerzo (agente entrenado)', estado: 'PARCIAL', ev: 'Auditoría del RL', ruta: 'artifacts/ml/rl/final_audit.md' },
  { req: '20 variables mínimas justificadas', estado: 'CUMPLE', ev: 'metadata.json', ruta: 'data/panel/metadata.json' },
  { req: 'Integrar con otra fuente oficial', estado: 'PARCIAL', ev: 'Fuente oficial 2', ruta: 'docs/research/14-fuente-oficial-2.md' },
  { req: 'Evidencia de cómo se unió la información', estado: 'CUMPLE', ev: 'crosswalk', ruta: 'data/external_pub/crosswalk_municipios.csv' },
  { req: 'Priorización exploratoria de zonas de Santander', estado: 'CUMPLE', ev: 'pruebas.json', ruta: 'app/web/public/data/pruebas.json' },
  { req: 'Flujo funcional y verificable con demostración', estado: 'PARCIAL', ev: 'Documentación', ruta: 'docs/DOCUMENTACION.md' },
  { req: 'Validación que respete el orden temporal', estado: 'CUMPLE', ev: 'partitions.json', ruta: 'artifacts/ml/partitions.json' },
  { req: 'Evaluación del agente', estado: 'CUMPLE', ev: 'Auditoría del RL', ruta: 'artifacts/ml/rl/final_audit.md' },
  { req: 'Incertidumbre o explicación', estado: 'PARCIAL', ev: 'Análisis crítico', ruta: 'artifacts/ml/critical_analysis.md' },
  { req: 'Utilidad, supuestos, limitaciones, extensiones', estado: 'CUMPLE', ev: 'Limitaciones', ruta: 'artifacts/ml/rl/limitaciones.md' },
]

function Tabla({ titulo, filas }: { titulo: string; filas: Fila[] }) {
  return (
    <div className="tabla-scroll">
      <table className="prob-tabla">
        <caption className="prob-tabla__titulo">{titulo}</caption>
        <thead><tr><th scope="col">Requisito oficial</th><th scope="col">Estado</th><th scope="col">Evidencia</th></tr></thead>
        <tbody>
          {filas.map((f) => (
            <tr key={f.req}>
              <th scope="row">{f.req}</th>
              <td>
                <span className={`estado estado--${f.estado === 'CUMPLE' ? 'cumple' : 'parcial'}`}>
                  <span aria-hidden="true">{f.estado === 'CUMPLE' ? '✓' : '◐'}</span> {f.estado}
                </span>
              </td>
              <td><a href={`${REPO}/blob/main/${f.ruta}`} target="_blank" rel="noreferrer">{f.ev}</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function LandingCumplimiento() {
  return (
    <section className="bloque land-seccion" aria-labelledby="cumplimiento">
      <p className="eyebrow">Cumplimiento del reto</p>
      <h2 id="cumplimiento" className="land-titulo">Qué cumple y qué no, sin maquillar</h2>
      <p className="land-lead">Estados tomados tal cual de la auditoría de requisitos. Donde dice PARCIAL hay una salvedad real.</p>
      <Tabla titulo="Básico" filas={BASICO} />
      <Tabla titulo="Medio" filas={MEDIO} />
      <Tabla titulo="Avanzado" filas={AVANZADO} />
      <p className="land-enlace"><a href={`${REPO}/blob/main/docs/AUDITORIA_REQUISITOS.md`} target="_blank" rel="noreferrer">Ver la auditoría completa</a></p>
    </section>
  )
}
