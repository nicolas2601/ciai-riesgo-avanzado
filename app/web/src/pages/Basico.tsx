import { useState } from 'react'
import type { FormEvent } from 'react'
import { ApiError, api } from '../api/client.ts'
import { useMunicipios, usePanel } from '../api/hooks.ts'
import type { Clase, Clasificacion } from '../api/types.ts'
import { Estado } from '../components/Estado.tsx'
import { Nivel } from '../components/Nivel.tsx'
import { fmtDecimal } from '../lib/formato.ts'

const CLASES: Clase[] = ['bajo', 'medio', 'alto']
const MES_INICIAL = '2024-06'

export function Basico() {
  const mun = useMunicipios()
  const [divipola, setDivipola] = useState('')
  const [mes, setMes] = useState(MES_INICIAL)
  const [res, setRes] = useState<Clasificacion | null>(null)
  const [error, setError] = useState<ApiError | null>(null)
  const [enviando, setEnviando] = useState(false)
  const panel = usePanel(res ? res.mes : null)
  const fila = panel.data?.filas.find((f) => f.divipola === res?.divipola) ?? null

  async function enviar(ev: FormEvent) {
    ev.preventDefault()
    if (!divipola) return
    setEnviando(true)
    setError(null)
    try {
      setRes(await api.clasificar({ divipola, mes }))
    } catch (e) {
      setRes(null)
      setError(e instanceof ApiError ? e : new ApiError('unknown', String(e)))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Nivel básico</p>
        <h1 className="pitch__titulo">Clasificar un municipio</h1>
        <p className="pitch__texto">
          Clase de riesgo (bajo, medio o alto) esperada para el mes siguiente al mes elegido. Es
          frecuencia relativa de eventos registrados, no severidad ni daño.
        </p>
      </section>

      <section className="panel formulario">
        <form onSubmit={enviar}>
          <div className="campo">
            <label className="campo__etiqueta" htmlFor="municipio">
              Municipio
            </label>
            <select
              id="municipio"
              value={divipola}
              onChange={(e) => setDivipola(e.target.value)}
              disabled={!mun.data}
              required
            >
              <option value="">Selecciona un municipio</option>
              {mun.data
                ?.slice()
                .sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))
                .map((m) => (
                  <option key={m.divipola} value={m.divipola}>
                    {m.nombre}
                  </option>
                ))}
            </select>
            <Estado e={mun} que="los municipios" />
          </div>
          <div className="campo">
            <label className="campo__etiqueta" htmlFor="mes">
              Mes (AAAA-MM)
            </label>
            <input
              id="mes"
              type="month"
              value={mes}
              onChange={(e) => setMes(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn--primario" disabled={enviando || !divipola}>
            {enviando ? 'Clasificando…' : 'Clasificar'}
          </button>
        </form>
      </section>

      {error ? (
        <p className="estado estado--error" role="alert">
          No se pudo clasificar: {error.message} <code>({error.code})</code>
        </p>
      ) : null}

      {res ? (
        <section className="resultado" aria-live="polite">
          <p className="eyebrow">Resultado · {res.mes}</p>
          <h2 className="resultado__clase">
            Clase esperada: <Nivel nivel={res.clase} />
          </h2>
          <ul className="barras" aria-label="Probabilidades por clase">
            {CLASES.map((c) => {
              const p = res.probabilidades[c]
              return (
                <li key={c} className="barras__fila">
                  <span className="barras__nombre">
                    <Nivel nivel={c} />
                  </span>
                  <span className="barras__pista" aria-hidden="true">
                    <span className={`barras__valor barras__valor--${c}`} style={{ width: `${p * 100}%` }} />
                  </span>
                  <span className="mono">{fmtDecimal(p * 100, 1)} %</span>
                </li>
              )
            })}
          </ul>
          <p className="mono">
            Modelo: {res.modelo}
            {res.exploratorio ? ' · exploratorio' : ''}
          </p>
          {fila ? (
            <p className="mono">
              Clase observada ese mes: <Nivel nivel={fila.clase_observada} /> · Clase real del mes
              siguiente: <Nivel nivel={fila.target_clase_mes_siguiente} />
            </p>
          ) : null}
        </section>
      ) : null}

      <aside className="nota" aria-label="Sobre el modelo">
        <p className="eyebrow">Sobre este modelo</p>
        <p>
          Es un <strong>Random Forest</strong> con <strong>macro-F1 de 0,593</strong> en
          validación. Una accuracy alta engaña: las clases están desbalanceadas (la mayoría de
          municipio-mes son «bajo»), así que predecir siempre la clase mayoritaria ya da una
          accuracy alta sin aprender nada. Por eso reportamos macro-F1, que pesa igual a cada
          clase.
        </p>
      </aside>
    </div>
  )
}
