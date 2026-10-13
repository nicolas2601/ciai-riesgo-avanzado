import { useState } from 'react'
import { usePriorizacion } from '../api/hooks.ts'
import { Estado } from '../components/Estado.tsx'
import { fmtDecimal } from '../lib/formato.ts'
import { AvanzadoExplica } from './explicaciones/AvanzadoExplica.tsx'

const KS = [3, 5, 8, 10]
const ROTULO_METODO: Record<string, string> = {
  estatico: 'Ranking estático (línea base)',
  aleatorio: 'Aleatorio determinista',
  ppo: 'Agente PPO',
}

export function Avanzado() {
  const [corte, setCorte] = useState('2024-06')
  const [k, setK] = useState(5)
  const pr = usePriorizacion(corte, k)

  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Nivel avanzado</p>
        <h1 className="pitch__titulo">Priorización de K municipios</h1>
        <p className="pitch__texto">
          Dado un corte mensual, cada método elige K municipios para mirar primero. Se compara la
          elección con lo que realmente ocurrió después.
        </p>
      </section>

      <section className="panel formulario">
        <div className="campo">
          <label className="campo__etiqueta" htmlFor="corte">
            Corte (AAAA-MM)
          </label>
          <input id="corte" type="month" value={corte} onChange={(e) => setCorte(e.target.value)} />
        </div>
        <div className="campo">
          <label className="campo__etiqueta" htmlFor="k">
            K (municipios a elegir)
          </label>
          <select id="k" value={k} onChange={(e) => setK(Number(e.target.value))}>
            {KS.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>
        <div className="acciones">
          <span className="btn btn--primario" aria-current="true">
            Reproducir resultado guardado
          </span>
          <button
            type="button"
            className="btn btn--secundario"
            disabled
            title="La API v1 no expone la ejecución del agente."
          >
            Ejecutar agente
          </button>
        </div>
        <p className="detalle__nota">
          «Reproducir resultado guardado» consulta la selección ya calculada para este corte.
          «Ejecutar agente» no está disponible en la API v1 y por eso está deshabilitado.
        </p>
      </section>

      <Estado e={pr} que="la priorización" />

      {pr.data ? (
        <section className="bloque" aria-live="polite">
          <p className="eyebrow">
            Corte {pr.data.corte} · K = {pr.data.k}
            {pr.data.exploratorio ? ' · exploratorio' : ''}
          </p>
          <div className="grupos">
            {pr.data.metodos.map((m) => (
              <article key={m.metodo} className="tarjeta tarjeta--estatica">
                <h3 className="tarjeta__titulo">{ROTULO_METODO[m.metodo] ?? m.metodo}</h3>
                {m.municipios.length === 0 ? (
                  <p className="estado" role="status">
                    Sin selección: este método no devolvió municipios en el despliegue actual.
                  </p>
                ) : (
                  <ol className="ranking">
                    {m.municipios.map((x) => (
                      <li key={x.divipola}>
                        <span className="mono">{x.rank}</span> {x.nombre}
                      </li>
                    ))}
                  </ol>
                )}
                <p className="mono">
                  Recompensa real:{' '}
                  {m.recompensa_real === null ? 'no disponible' : fmtDecimal(m.recompensa_real, 2)}
                </p>
              </article>
            ))}
          </div>
          <p className="nota">{pr.data.nota}</p>
        </section>
      ) : null}

      <AvanzadoExplica />
    </div>
  )
}
