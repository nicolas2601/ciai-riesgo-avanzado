import { useMemo, useState } from 'react'
import { EstadoVacio } from '../components/EstadoVacio.tsx'
import { useMunicipios, usePriorizacion } from '../lib/datos.ts'
import { IconoFlecha } from '../components/Icono.tsx'
import { BannerEjemplo } from '../components/BannerEjemplo.tsx'

export function Priorizacion() {
  const pri = usePriorizacion()
  const mun = useMunicipios()
  const cortes = pri.datos?.cortes ?? []
  const [corteIdx, setCorteIdx] = useState(0)
  const corte = cortes[corteIdx]

  const nombreDe = useMemo(() => {
    const mapa = new Map((mun.datos?.municipios ?? []).map((m) => [m.id, m.nombre]))
    return (id: string) => mapa.get(id) ?? id
  }, [mun.datos])

  const filas = useMemo(() => {
    if (!corte) return []
    const ids = new Set([...corte.agente, ...corte.baselines.top_estatico ?? [], ...corte.oraculo])
    return [...ids].map((id) => ({
      id,
      agente: corte.agente.indexOf(id),
      estatico: (corte.baselines.top_estatico ?? []).indexOf(id),
      oraculo: corte.oraculo.indexOf(id),
      real: corte.real[id] ?? 0,
    }))
  }, [corte])

  return (
    <div className="contenedor">
      <p className="eyebrow">Qué eligió el agente</p>
      <div className="filete" />
      <EstadoVacio cargando={pri.cargando} error={pri.error} />

      {cortes.length > 0 ? (
        <label className="campo campo--inline">
          <span className="campo__etiqueta">Corte de prueba</span>
          <select value={corteIdx} onChange={(e) => setCorteIdx(Number(e.target.value))}>
            {cortes.map((c, i) => (
              <option key={c.corte} value={i}>
                {c.corte}
              </option>
            ))}
          </select>
        </label>
      ) : null}

      <div className="tarjeta-panel">
        <h2 className="panel__titulo">Agente contra líneas base</h2>
        <p className="panel__nota">
          K = {pri.datos?.k ?? '—'}. La comparación se hace con la diferencia pareada; el
          solapamiento de intervalos marginales no demuestra empate.
        </p>
        <div className="tabla-scroll">
          <table className="tabla">
            <thead>
              <tr>
                <th>Municipio</th>
                <th>Agente</th>
                <th>Top-K estático</th>
                <th>Oráculo</th>
                <th>¿Hubo actividad?</th>
              </tr>
            </thead>
            <tbody>
              {filas.map((f) => (
                <tr key={f.id} data-activa={f.agente >= 0}>
                  <td>{nombreDe(f.id)}</td>
                  <td className="mono">{f.agente >= 0 ? `#${f.agente + 1}` : '—'}</td>
                  <td className="mono">{f.estatico >= 0 ? `#${f.estatico + 1}` : '—'}</td>
                  <td className="mono">{f.oraculo >= 0 ? `#${f.oraculo + 1}` : '—'}</td>
                  <td className="mono">{f.real === 1 ? 'sí' : 'no'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="tarjeta-panel">
        <h2 className="panel__titulo">Ejecutar el agente</h2>
        <p className="panel__nota">
          Dos niveles distintos: el primero reproduce un resultado ya calculado, el segundo corre el
          modelo en vivo por el puente local. No son lo mismo.
        </p>
        <div className="puente">
          <button type="button" className="btn btn--secundario">
            Reproducir resultado guardado
          </button>
          <button type="button" className="btn btn--primario">
            Ejecutar agente
            <IconoFlecha />
          </button>
        </div>
        <p className="panel__nota">
          K entrenado por defecto: 5. Elegir un K no entrenado exige otra política, no es el mismo
          agente.
        </p>
      </div>

      {pri.ejemplo ? <BannerEjemplo fijo /> : null}
    </div>
  )
}
