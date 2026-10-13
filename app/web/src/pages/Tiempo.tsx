import { useMemo, useState } from 'react'
import { EstadoVacio } from '../components/EstadoVacio.tsx'
import { useMunicipios, useSerie } from '../lib/datos.ts'
import { fmtEntero, fmtMagnitud } from '../lib/formato.ts'
import { TarjetaNivel } from '../components/TarjetaNivel.tsx'

// Sismos de referencia del plan. El de 2015 se cita con las DOS magnitudes:
// USGS y SGC, nunca promediadas.
export const REFERENCIAS = [
  { corte: '2015-03', municipio: 'Cepita', usgs: 6.2, sgc: 6.6 },
  { corte: '2023-11', municipio: 'Aratoca', usgs: 5.4, sgc: null },
  { corte: '2025-12', municipio: 'San Andrés', usgs: 5.5, sgc: null },
]

export function Tiempo() {
  const serie = useSerie()
  const mun = useMunicipios()
  const cortes = serie.datos?.cortes ?? []
  const [idx, setIdx] = useState<number>(() => Math.max(cortes.length - 1, 0))
  const corte = cortes[idx] ?? null

  const nombreDe = useMemo(() => {
    const mapa = new Map((mun.datos?.municipios ?? []).map((m) => [m.id, m.nombre]))
    return (id: string) => mapa.get(id) ?? id
  }, [mun.datos])

  const delCorte = useMemo(
    () => (serie.datos?.serie ?? []).filter((p) => p.mes === corte),
    [serie.datos, corte],
  )

  const top5 = useMemo(
    () =>
      [...delCorte]
        .sort((a, b) => (b.eventos ?? 0) - (a.eventos ?? 0))
        .slice(0, 5),
    [delCorte],
  )

  const referenciaActiva = REFERENCIAS.find((r) => r.corte === corte) ?? null

  return (
    <div className="contenedor">
      <p className="eyebrow">Máquina del tiempo</p>
      <div className="filete" />
      <EstadoVacio cargando={serie.cargando} error={serie.error} />

      <p className="intro">
        Arrastra el corte. La web muestra qué habría priorizado el agente <strong>antes</strong> de
        saber qué venía, y qué pasó después. Los rombos son sismos de referencia.
      </p>

      <div className="riel">
        <label className="riel__etiqueta" htmlFor="riel-rango">
          Corte mensual
        </label>
        <input
          id="riel-rango"
          className="riel__rango"
          type="range"
          min={0}
          max={Math.max(cortes.length - 1, 0)}
          value={idx}
          onChange={(e) => setIdx(Number(e.target.value))}
          list="riel-marcas"
        />
        <datalist id="riel-marcas">
          {cortes.map((c) => (
            <option key={c} value={c} />
          ))}
        </datalist>
        <div className="riel__escala" aria-hidden="true">
          {cortes.map((c, i) => (
            <button
              key={c}
              type="button"
              className={`riel__marca${i === idx ? ' riel__marca--activa' : ''}${
                REFERENCIAS.some((r) => r.corte === c) ? ' riel__marca--evento' : ''
              }`}
              onClick={() => setIdx(i)}
            >
              {c.slice(0, 4)}
            </button>
          ))}
        </div>
      </div>

      <div className="tiempo-panel">
        <section className="tarjeta-panel">
          <h2 className="panel__titulo">Qué habría priorizado</h2>
          <p className="panel__nota">
            Orden por actividad del mes siguiente. El agente elige sin ver el futuro.
          </p>
          <ol className="ranking">
            {top5.length === 0 ? (
              <li className="ranking__vacio">Sin registro para este corte.</li>
            ) : (
              top5.map((p, i) => (
                <li key={p.municipio} className="ranking__item">
                  <span className="ranking__puesto mono">{String(i + 1).padStart(2, '0')}</span>
                  <span className="ranking__nombre">{nombreDe(p.municipio)}</span>
                  <span className="ranking__dato mono">{fmtEntero(p.eventos)} ev.</span>
                </li>
              ))
            )}
          </ol>
        </section>

        <section className="tarjeta-panel">
          <h2 className="panel__titulo">Qué pasó</h2>
          {referenciaActiva ? (
            <>
              <p className="panel__nota">
                Sismo de referencia en {referenciaActiva.municipio}. Las dos fuentes se citan por
                separado y no se promedian.
              </p>
              <dl className="evento">
                <div>
                  <dt>Fecha</dt>
                  <dd className="mono">{referenciaActiva.corte}</dd>
                </div>
                {referenciaActiva.usgs ? (
                  <div>
                    <dt>USGS</dt>
                    <dd className="mono">{fmtMagnitud(referenciaActiva.usgs)}</dd>
                  </div>
                ) : null}
                {referenciaActiva.sgc ? (
                  <div>
                    <dt>SGC</dt>
                    <dd className="mono">{fmtMagnitud(referenciaActiva.sgc)}</dd>
                  </div>
                ) : null}
              </dl>
            </>
          ) : (
            <p className="panel__nota">
              En este corte no hay sismo de referencia. Los datos del mes siguiente son los que el
              agente no podía ver al decidir.
            </p>
          )}
        </section>
      </div>

      <p className="eyebrow" style={{ marginTop: 'var(--s-8)' }}>
        Vista de tabla del corte
      </p>
      <div className="filete" />
      <div className="tabla-scroll">
        <table className="tabla">
          <caption className="visualmente-oculto">Municipios del corte, en texto</caption>
          <thead>
            <tr>
              <th>Municipio</th>
              <th>Nivel real</th>
              <th>Nivel predicho</th>
              <th>Eventos</th>
              <th>Magnitud máx.</th>
            </tr>
          </thead>
          <tbody>
            {delCorte.slice(0, 25).map((p) => (
              <tr key={p.municipio}>
                <td>{nombreDe(p.municipio)}</td>
                <td>
                  <TarjetaNivel nivel={p.nivel_real} variante="contorno" />
                </td>
                <td>
                  <TarjetaNivel nivel={p.nivel_predicho} variante="contorno" />
                </td>
                <td className="mono">{fmtEntero(p.eventos)}</td>
                <td className="mono">{fmtMagnitud(p.mag_max)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
