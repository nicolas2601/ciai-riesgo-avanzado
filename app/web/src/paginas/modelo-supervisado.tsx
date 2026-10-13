import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Shell } from '../components/Shell.tsx'
import { BannerEjemplo } from '../components/BannerEjemplo.tsx'
import { EstadoVacio } from '../components/EstadoVacio.tsx'
import { useMetricas } from '../lib/datos.ts'
import { fmtDecimal } from '../lib/formato.ts'

const PALETA = ['var(--risk-bajo)', 'var(--risk-medio)', 'var(--risk-alto)']

function Supervisado() {
  const met = useMetricas()
  const doc = met.datos

  // Matriz de confusion: null mientras no haya modelo entrenado. No se inventa.
  const matriz = doc?.basico.matriz ?? null
  const filas = matriz
    ? ['Real Bajo', 'Real Medio', 'Real Alto'].map((nombre, i) => ({
        nombre,
        bajo: matriz[i]?.[0] ?? 0,
        medio: matriz[i]?.[1] ?? 0,
        alto: matriz[i]?.[2] ?? 0,
      }))
    : []

  const curvas = doc?.rl.curvas ?? null
  const datosCurva = curvas
    ? curvas.map((v, i) => ({ paso: i + 1, retorno: v }))
    : []

  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Modelo supervisado</p>
        <h1 className="pitch__titulo">Línea base contra la que se compara el agente</h1>
        <p className="pitch__texto">
          Un modelo supervisado es obligatorio: sin él no hay forma de afirmar que el agente aporta
          algo. Se valida en orden cronológico y por bloques de municipios, nunca de forma
          aleatoria sobre vecinos.
        </p>
      </section>

      {met.ejemplo ? <BannerEjemplo /> : null}
      <EstadoVacio cargando={met.cargando} error={met.error} />

      <section className="pitch">
        <p className="eyebrow">Matriz de confusión</p>
        <div className="filete" />
        {matriz ? (
          <div className="grafica">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={filas}>
                <CartesianGrid stroke="var(--border-hairline)" vertical={false} />
                <XAxis dataKey="nombre" tick={{ fill: 'var(--ink-2)', fontSize: 12 }} />
                <YAxis tick={{ fill: 'var(--ink-2)', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: 'var(--surface)',
                    border: '1px solid var(--border-hairline)',
                    borderRadius: 'var(--r-control)',
                  }}
                />
                <Bar dataKey="bajo" name="Predice Bajo" fill={PALETA[0]} />
                <Bar dataKey="medio" name="Predice Medio" fill={PALETA[1]} />
                <Bar dataKey="alto" name="Predice Alto" fill={PALETA[2]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="estado">Sin matriz de confusión: el modelo no está entrenado todavía.</p>
        )}
      </section>

      <section className="pitch">
        <p className="eyebrow">Métricas del bloque</p>
        <div className="filete" />
        <div className="tabla-scroll">
          <table className="tabla">
            <thead>
              <tr>
                <th>Métrica</th>
                <th>Valor</th>
                <th>Origen</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>F1 macro (Básico)</td>
                <td className="mono">{fmtDecimal(doc?.basico.f1_macro ?? null, 3)}</td>
                <td>{doc?.basico.nota ?? '—'}</td>
              </tr>
              <tr>
                <td>Retorno medio (RL)</td>
                <td className="mono">{fmtDecimal(doc?.rl.retorno_medio ?? null, 3)}</td>
                <td>{doc?.rl.semillas.length ? `semillas: ${doc.rl.semillas.join(', ')}` : 'sin semillas'}</td>
              </tr>
              <tr>
                <td>Diferencia pareada</td>
                <td className="mono">{fmtDecimal(doc?.comparacion.diferencia_pareada ?? null, 3)}</td>
                <td>{doc?.comparacion.nota ?? '—'}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="panel__nota">
          Los intervalos vienen por remuestreo de bloques. Para decir que un modelo gana se usa el
          intervalo de la diferencia pareada: el solapamiento de intervalos marginales no demuestra
          empate ni diferencia.
        </p>
      </section>

      <section className="pitch">
        <p className="eyebrow">Curva de aprendizaje</p>
        <div className="filete" />
        {datosCurva.length > 0 ? (
          <div className="grafica">
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={datosCurva}>
                <CartesianGrid stroke="var(--border-hairline)" vertical={false} />
                <XAxis dataKey="paso" tick={{ fill: 'var(--ink-2)', fontSize: 12 }} />
                <YAxis tick={{ fill: 'var(--ink-2)', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: 'var(--surface)',
                    border: '1px solid var(--border-hairline)',
                    borderRadius: 'var(--r-control)',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="retorno"
                  name="Retorno"
                  stroke="var(--accent)"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="estado">Sin curvas: el agente no se ha entrenado todavía.</p>
        )}
      </section>

      <section className="pitch">
        <p className="eyebrow">Gate de degeneración</p>
        <div className="filete" />
        <div className="acordeon">
          <p>
            Antes de entrenar el refuerzo se mide, <strong>solo con entrenamiento</strong>, cuánto
            varía el top-K entre cortes. Si el top-K es casi constante no es un fallo: se compara
            contra el top-K estático y se declara.
          </p>
          <p>
            Usar validación o prueba para tomar esa decisión sería fuga de selección. K, empates y
            soporte quedan fijados de antemano.
          </p>
        </div>
      </section>
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Shell actual="Supervisado">
      <Supervisado />
    </Shell>
  </StrictMode>,
)
