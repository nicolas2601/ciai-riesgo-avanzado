import { BarrasH, Pasos, Seccion, Sello } from '../../components/Explica.tsx'
import { fmtDecimal, fmtEntero } from '../../lib/formato.ts'
import { useJson } from '../../lib/datos.ts'
import type { MetaPanel, Pruebas } from '../../lib/datos.ts'

const ROTULO: Record<string, string> = {
  A_dummy_majority: 'Dummy (siempre «bajo»)',
  B_logreg_balanced: 'Logística balanceada',
  C_ros_logreg: 'Logística + ROS',
  D_smote_logreg: 'Logística + SMOTE',
  E_rf_balanced: 'Random Forest balanceado',
}

const GRUPOS: { nombre: string; vars: string[] }[] = [
  { nombre: 'Actividad', vars: ['n_eventos_mes', 'n_eventos_3m', 'n_eventos_12m', 'dias_desde_ultimo_evento', 'dias_desde_ultimo_m3', 'hay_eventos_mes', 'n_eventos_vecinos_mes', 'n_eventos_departamento_mes'] },
  { nombre: 'Magnitud', vars: ['mag_max_mes', 'mag_max_3m', 'mag_media_mes', 'mag_std_mes', 'n_m_ge_3_mes', 'n_m_ge_3_12m', 'n_m_ge_4_mes', 'n_m_ge_4_12m', 'energia_log_3m'] },
  { nombre: 'Profundidad', vars: ['prof_media_mes', 'prof_std_mes', 'frac_prof_lt30', 'frac_30_70', 'frac_70_300', 'frac_gt300'] },
  { nombre: 'Calidad de red', vars: ['rms_media_mes', 'gap_media_mes', 'fases_media_mes'] },
  { nombre: 'Exposición', vars: ['centroid_lat', 'centroid_lon', 'poblacion'] },
  { nombre: 'Contexto de detección', vars: ['mc_maxc_12m', 'n_m_ge_mc_mes', 'year_context'] },
]

function Decision({ p }: { p: Pruebas }) {
  const modelos = p.supervisado.modelos
  return (
    <Seccion eyebrow="Decisión" titulo="Cómo se decidió el modelo">
      <p>
        Se compararon 5 modelos sobre la partición de validación. La métrica de elección es
        macro-F1 <Sello tipo="hecho" />
      </p>
      <BarrasH
        titulo="Macro-F1 de validación por modelo"
        max={1}
        filas={modelos.map((m) => ({
          etiqueta: ROTULO[m.modelo] ?? m.modelo,
          valor: m.macro_f1,
          texto: fmtDecimal(m.macro_f1, 3),
          destacada: m.modelo === p.supervisado.seleccionado,
        }))}
      />
      <div className="tabla-wrap">
        <table>
          <caption className="visually-hidden">Métricas de validación por modelo</caption>
          <thead>
            <tr><th>Modelo</th><th>Macro-F1</th><th>Exactitud balanceada</th><th>Accuracy</th><th>Elegido</th></tr>
          </thead>
          <tbody>
            {modelos.map((m) => {
              const sel = m.modelo === p.supervisado.seleccionado
              return (
                <tr key={m.modelo} className={sel ? 'fila-sel' : undefined}>
                  <td>{ROTULO[m.modelo] ?? m.modelo}</td>
                  <td className="mono">{fmtDecimal(m.macro_f1, 3)}</td>
                  <td className="mono">{fmtDecimal(m.balanced_accuracy, 3)}</td>
                  <td className="mono">{fmtDecimal(m.accuracy, 3)}</td>
                  <td>{sel ? 'Sí' : '—'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <p>
        <strong>¿Por qué macro-F1 y no accuracy?</strong> El dummy que siempre dice «bajo» saca
        accuracy {fmtDecimal(modelos[0].accuracy, 3)} sin aprender nada. Macro-F1 promedia el F1 de
        cada clase por igual, así que la clase rara pesa lo mismo.
      </p>
    </Seccion>
  )
}

function Desbalance({ m }: { m: MetaPanel }) {
  const t = m.target_balance
  const filas = ['bajo', 'medio', 'alto'].map((c) => ({
    etiqueta: c,
    valor: t[c],
    texto: fmtEntero(t[c]),
  }))
  return (
    <>
      <p>
        Desbalance del objetivo en las {fmtEntero(m.rows)} filas municipio-mes: la clase «alto»
        tiene solo {fmtEntero(t.alto)} <Sello tipo="hecho" />
      </p>
      <BarrasH titulo="Filas por clase objetivo" max={t.bajo} filas={filas} />
    </>
  )
}

function Variables({ m }: { m: MetaPanel }) {
  const conocidas = new Set(GRUPOS.flatMap((g) => g.vars))
  const otras = m.features.filter((f) => !conocidas.has(f))
  const grupos = otras.length ? [...GRUPOS, { nombre: 'Otras', vars: otras }] : GRUPOS
  return (
    <Seccion eyebrow="Entradas" titulo={`Qué entra: ${m.features.length} variables`}>
      <div className="dos-col">
        {grupos.map((g) => (
          <div key={g.nombre} className="mini-tarjeta">
            <h3>
              {g.nombre} <span className="mono">({g.vars.length})</span>
            </h3>
            <ul>
              {g.vars.map((v) => (
                <li key={v} className="mono">{v}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <p className="detalle__nota">
        Todas se calculan solo con información hasta el mes consultado, sin mirar el futuro.
        El agrupamiento en familias es editorial; la lista de variables viene del panel.
      </p>
    </Seccion>
  )
}

export function BasicoExplica() {
  const pruebas = useJson<Pruebas>('/data/pruebas.json')
  const meta = useJson<MetaPanel>('/data/panel-metadata.json')
  return (
    <>
      <Seccion eyebrow="Qué hace" titulo="Un municipio, un mes, la clase del mes siguiente">
        <Pasos
          items={[
            { titulo: 'Entrada', texto: 'Municipio y mes de consulta.' },
            { titulo: 'Panel', texto: 'Se leen sus variables de actividad hasta ese mes.' },
            { titulo: 'Random Forest balanceado', texto: 'Cada árbol vota con pesos por clase.' },
            { titulo: 'Salida', texto: 'Probabilidad de bajo, medio y alto; gana la mayor.' },
          ]}
        />
      </Seccion>
      {pruebas.data ? <Decision p={pruebas.data} /> : null}
      {pruebas.error ? <p className="estado estado--error" role="alert">No se pudo cargar pruebas.json: {pruebas.error}</p> : null}
      {meta.data ? (
        <Seccion eyebrow="Datos" titulo="Por qué importa el desbalance">
          <Desbalance m={meta.data} />
        </Seccion>
      ) : null}
      {meta.data ? <Variables m={meta.data} /> : null}
      <Seccion eyebrow="Lectura" titulo="Cómo leer el resultado">
        <ul className="lista-sellos">
          <li><Sello tipo="hecho" /> Las tres probabilidades suman 100 %; la clase es la de mayor probabilidad.</li>
          <li><Sello tipo="limitacion" /> Es exploratorio: no es alerta oficial ni predice sismos.</li>
          <li><Sello tipo="limitacion" /> Las particiones de test ya fueron consultadas en etapas previas.</li>
          <li><Sello tipo="hipotesis" /> Una probabilidad no calibrada no equivale a una frecuencia real.</li>
        </ul>
      </Seccion>
    </>
  )
}
