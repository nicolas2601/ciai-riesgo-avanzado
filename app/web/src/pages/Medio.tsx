import { useMemo, useState } from 'react'
import { useClusters } from '../api/hooks.ts'
import type { MunicipioCluster } from '../api/types.ts'
import { Estado } from '../components/Estado.tsx'
import { fmtDecimal } from '../lib/formato.ts'

// Categorical palette, deliberately outside the risk scale (no teal/amber/crimson).
// Each group also has its own marker shape, so the group never depends on color alone.
const ESTILOS = [
  { color: '#2438c8', forma: 'círculo' },
  { color: '#6d28d9', forma: 'cuadrado' },
  { color: '#101418', forma: 'rombo' },
  { color: '#5a6472', forma: 'triángulo' },
  { color: '#0f766e', forma: 'cruz' },
] as const

const W = 640
const H = 560
const PAD = 28

function Marca({ forma, color, r = 6 }: { forma: string; color: string; r?: number }) {
  const p = { fill: color, stroke: '#fff', strokeWidth: 1.5 }
  if (forma === 'cuadrado') return <rect x={-r} y={-r} width={2 * r} height={2 * r} {...p} />
  if (forma === 'rombo') return <polygon points={`0,${-r - 1} ${r + 1},0 0,${r + 1} ${-r - 1},0`} {...p} />
  if (forma === 'triángulo') return <polygon points={`0,${-r - 1} ${r + 1},${r} ${-r - 1},${r}`} {...p} />
  if (forma === 'cruz') return <path d={`M${-r} 0H${r}M0 ${-r}V${r}`} stroke={color} strokeWidth={3} />
  return <circle r={r} {...p} />
}

function estilo(cluster: number) {
  return ESTILOS[cluster % ESTILOS.length]
}

function proyector(ms: MunicipioCluster[]) {
  const lats = ms.map((m) => m.lat)
  const lons = ms.map((m) => m.lon)
  const [minLat, maxLat] = [Math.min(...lats), Math.max(...lats)]
  const [minLon, maxLon] = [Math.min(...lons), Math.max(...lons)]
  const kx = Math.cos((((minLat + maxLat) / 2) * Math.PI) / 180)
  const ancho = (maxLon - minLon) * kx || 1
  const alto = maxLat - minLat || 1
  const esc = Math.min((W - 2 * PAD) / ancho, (H - 2 * PAD) / alto)
  const ox = (W - ancho * esc) / 2
  const oy = (H - alto * esc) / 2
  return (m: MunicipioCluster) => ({
    x: ox + (m.lon - minLon) * kx * esc,
    y: oy + (maxLat - m.lat) * esc,
  })
}

export function Medio() {
  const cl = useClusters()
  const [sel, setSel] = useState<MunicipioCluster | null>(null)
  const datos = cl.data
  const proy = useMemo(() => (datos ? proyector(datos.municipios) : null), [datos])

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

      <Estado e={cl} que="los grupos" />

      {datos && proy ? (
        <>
          <section className="mapa-bloque" aria-label="Mapa de municipios por grupo">
            <svg viewBox={`0 0 ${W} ${H}`} className="mapa-svg" role="group" aria-label="Municipios de Santander">
              {datos.municipios.map((m) => {
                const { x, y } = proy(m)
                const e = estilo(m.cluster)
                const activo = sel?.divipola === m.divipola
                return (
                  <g
                    key={m.divipola}
                    transform={`translate(${x} ${y})${activo ? ' scale(1.6)' : ''}`}
                    tabIndex={0}
                    role="button"
                    aria-label={`${m.municipio}, grupo ${m.cluster}, ${e.forma}`}
                    className="mapa-punto"
                    onClick={() => setSel(m)}
                    onFocus={() => setSel(m)}
                    onKeyDown={(ev) => ev.key === 'Enter' && setSel(m)}
                  >
                    <title>{`${m.municipio} · grupo ${m.cluster}`}</title>
                    <Marca forma={e.forma} color={e.color} />
                  </g>
                )
              })}
            </svg>
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

          <section className="bloque">
            <p className="eyebrow">Leyenda y lectura de cada grupo</p>
            <div className="grupos">
              {datos.perfiles.map((g) => {
                const e = estilo(g.cluster)
                return (
                  <article key={g.cluster} className="tarjeta tarjeta--estatica">
                    <h3 className="tarjeta__titulo grupo__titulo">
                      <svg width="20" height="20" viewBox="-10 -10 20 20" aria-hidden="true">
                        <Marca forma={e.forma} color={e.color} r={7} />
                      </svg>
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
