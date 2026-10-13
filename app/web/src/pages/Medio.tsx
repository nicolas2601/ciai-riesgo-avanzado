import { useState } from 'react'
import { useClusters } from '../api/hooks.ts'
import type { MunicipioCluster } from '../api/types.ts'
import { Estado } from '../components/Estado.tsx'
import { MapaSantander } from '../components/MapaSantander.tsx'
import { estilo } from '../lib/gruposMapa.ts'
import { fmtDecimal } from '../lib/formato.ts'

export function Medio() {
  const cl = useClusters()
  const [sel, setSel] = useState<MunicipioCluster | null>(null)
  const datos = cl.data

  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Nivel medio</p>
        <h1 className="pitch__titulo">Grupos de municipios por perfil de actividad</h1>
        <p className="pitch__texto">
          Agrupamiento no supervisado (KMeans) sobre el perfil sísmico registrado de cada
          municipio. Los grupos describen cómo se comporta el catálogo, no cuánto riesgo hay.
        </p>
      </section>

      <section className="nota" aria-label="Cómo leer este mapa">
        <p className="eyebrow">Cómo leer este mapa</p>
        <ul className="grupo__rasgos">
          <li><strong>Qué es KMeans:</strong> un método no supervisado; agrupa municipios por parecido de perfil sísmico sin usar etiquetas de riesgo.</li>
          <li><strong>Por qué k = 3:</strong> silhouette de 0,28 y estabilidad entre semillas de 1,0 / 0,39 / 1,0. Es una elección modesta, no una separación nítida.</li>
          <li><strong>Qué NO significa:</strong> los grupos describen el perfil del catálogo, no una amenaza.</li>
        </ul>
      </section>

      <Estado e={cl} que="los grupos" />

      {datos ? (
        <>
          <section className="mapa-bloque" aria-label="Mapa de municipios por grupo">
            <MapaSantander municipios={datos.municipios} seleccionado={sel?.divipola ?? null} onSelect={setSel} />
            <div className="detalle panel" aria-live="polite">
              {sel ? (
                <>
                  <h2 className="detalle__nombre">{sel.municipio}</h2>
                  <p className="mono">
                    Grupo {sel.cluster} · {estilo(sel.cluster).forma}
                  </p>
                  <p className="detalle__nota">{sel.etiqueta}</p>
                </>
              ) : (
                <p className="detalle__nota">Selecciona un municipio en el mapa.</p>
              )}
            </div>
          </section>

          <details className="bloque tabla-mun">
            <summary>Tabla de municipios (alternativa de teclado)</summary>
            <table>
              <thead><tr><th>Municipio</th><th>Grupo</th><th>Etiqueta</th></tr></thead>
              <tbody>
                {datos.municipios.map((m) => (
                  <tr key={m.divipola}>
                    <td><button type="button" className="enlace-tabla" onClick={() => setSel(m)}>{m.municipio}</button></td>
                    <td>{m.cluster} · {estilo(m.cluster).forma}</td>
                    <td>{m.etiqueta}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </details>

          <section className="bloque">
            <p className="eyebrow">Leyenda y lectura de cada grupo</p>
            <div className="grupos">
              {datos.perfiles.map((g) => {
                const e = estilo(g.cluster)
                return (
                  <article key={g.cluster} className="tarjeta tarjeta--estatica">
                    <h3 className="tarjeta__titulo grupo__titulo">
                      <span className={`marca-leyenda marca--${e.forma}`} style={{ '--c': e.color } as React.CSSProperties} aria-hidden="true" />
                      Grupo {g.cluster} · {g.n_municipios} municipios
                    </h3>
                    <ul className="grupo__rasgos">
                      {g.rasgos.map((r) => (
                        <li key={r.variable}>
                          <span className="mono">{r.variable}</span> {r.direccion} (
                          {fmtDecimal(r.desviaciones_estandar, 1)} σ)
                        </li>
                      ))}
                    </ul>
                    <p className="tarjeta__texto">
                      Promedio de {fmtDecimal(g.medias.n_eventos_mes ?? null, 1)} eventos por mes y
                      magnitud máxima mensual media {fmtDecimal(g.medias.mag_max_mes ?? null, 1)}.
                    </p>
                  </article>
                )
              })}
            </div>
            <p className="detalle__nota">
              {datos.metadata.metodo}, k = {datos.metricas.k}, silhouette{' '}
              {fmtDecimal(datos.metricas.silhouette, 2)} (separación moderada-baja). Ajustado hasta{' '}
              {datos.metadata.fit_until}.
            </p>
          </section>
        </>
      ) : null}
    </div>
  )
}
