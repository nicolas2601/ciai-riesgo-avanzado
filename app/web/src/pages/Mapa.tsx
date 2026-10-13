import { useEffect, useMemo, useRef, useState } from 'react'
import type { Map as MapLibreMap, Marker } from 'maplibre-gl'
import * as maplibregl from 'maplibre-gl'
import maplibreglWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import 'maplibre-gl/dist/maplibre-gl.css'

// optimizeDeps.exclude solo arregla el worker en dev. En build hay que darle
// la URL del worker ya emitido, o el mapa sale en blanco con "Worker failed to load".
maplibregl.setWorkerUrl(maplibreglWorkerUrl)
import { TarjetaNivel } from '../components/TarjetaNivel.tsx'
import { EstadoVacio } from '../components/EstadoVacio.tsx'
import { useMunicipios, useSerie } from '../lib/datos.ts'
import { NIVELES } from '../lib/niveles.ts'
import { fmtEntero, fmtMagnitud } from '../lib/formato.ts'
import type { Municipio, Nivel } from '../lib/tipos.ts'

const RELLENO: Record<string, string> = {
  bajo: '#a1c5d1',
  medio: '#d6bda0',
  alto: '#dea3b3',
  'sin-dato': '#bbc0c6',
  'sin-priorizacion': '#cbc3b4',
}
const ANILLO: Record<string, string> = {
  bajo: '#0e7490',
  medio: '#a85b00',
  alto: '#c01038',
  'sin-dato': '#5a6472',
  'sin-priorizacion': '#8a6d3b',
}

export function Mapa() {
  const mun = useMunicipios()
  const serie = useSerie()
  const contenedor = useRef<HTMLDivElement>(null)
  const capa = useRef<MapLibreMap | null>(null)
  const marcadores = useRef<Marker[]>([])
  const [mes, setMes] = useState('')
  const [sel, setSel] = useState<Municipio | null>(null)
  const [mapaError, setMapaError] = useState<string | null>(null)

  const cortes = serie.datos?.cortes ?? []
  const mesActivo = mes || cortes[cortes.length - 1] || null
  const municipios = useMemo(() => mun.datos?.municipios ?? [], [mun.datos])

  const punto = useMemo(() => {
    if (!sel || !mesActivo) return null
    return serie.datos?.serie.find((p) => p.municipio === sel.id && p.mes === mesActivo) ?? null
  }, [sel, mesActivo, serie.datos])

  // El mapa se crea una vez. El worker de maplibre exige excluirlo del
  // pre-empaquetado; sin eso sale en blanco con "Worker failed to load".
  useEffect(() => {
    if (!contenedor.current || capa.current) return
    try {
      const m = new maplibregl.Map({
        container: contenedor.current,
        style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
        center: [-73.12, 7.08],
        zoom: 8.3,
        attributionControl: false,
      })
      m.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right')
      m.on('error', () =>
        setMapaError('El basemap no cargó. Revisa la red: la tabla de abajo es el equivalente textual.'),
      )
      capa.current = m
    } catch (e) {
      setMapaError(e instanceof Error ? e.message : 'No se pudo iniciar el mapa')
    }
    return () => {
      marcadores.current.forEach((mk) => mk.remove())
      marcadores.current = []
      capa.current?.remove()
      capa.current = null
    }
  }, [])

  // Los circulos se redibujan al cambiar el corte o los municipios.
  useEffect(() => {
    const m = capa.current
    if (!m || municipios.length === 0) return
    marcadores.current.forEach((mk) => mk.remove())
    marcadores.current = municipios.map((mun2) => {
      const niv: Nivel = mun2.nivel ?? 'sin-dato'
      const el = document.createElement('button')
      el.type = 'button'
      el.className = 'punto'
      el.style.background = RELLENO[niv]
      el.style.borderColor = ANILLO[niv]
      el.title = `${mun2.nombre}: ${NIVELES[niv].etiqueta}`
      el.setAttribute('aria-label', `${mun2.nombre}: ${NIVELES[niv].etiqueta}`)
      el.addEventListener('click', () => setSel(mun2))
      return new maplibregl.Marker({ element: el }).setLngLat([mun2.lon, mun2.lat]).addTo(m)
    })
  }, [municipios, mesActivo, mun.datos])

  return (
    <div className="contenedor">
      <p className="eyebrow">Mapa de riesgo</p>
      <div className="filete" />
      <EstadoVacio cargando={mun.cargando} error={mun.error} />

      <div className="controles">
        <label className="campo campo--inline">
          <span className="campo__etiqueta">Mes de corte</span>
          <select value={mesActivo ?? ''} onChange={(e) => setMes(e.target.value)}>
            {cortes.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        <div className="leyenda">
          {(Object.keys(NIVELES) as Nivel[]).map((n) => (
            <TarjetaNivel key={n} nivel={n} variante="contorno" />
          ))}
        </div>
      </div>

      <div className="mapa-bloque">
        <div
          className="mapa"
          ref={contenedor}
          role="application"
          aria-label="Mapa de los 87 municipios de Santander"
        />
        {mapaError ? (
          <p className="estado estado--error" role="alert">
            {mapaError}
          </p>
        ) : null}
        {sel ? (
          <div className="panel detalle">
            <h2 className="detalle__nombre">{sel.nombre}</h2>
            <TarjetaNivel nivel={sel.nivel} />
            <dl className="detalle__lista">
              <div>
                <dt>Eventos en el mes</dt>
                <dd className="mono">{fmtEntero(punto?.eventos ?? null)}</dd>
              </div>
              <div>
                <dt>Magnitud máxima</dt>
                <dd className="mono">{fmtMagnitud(punto?.mag_max ?? null)}</dd>
              </div>
              <div>
                <dt>Población</dt>
                <dd className="mono">{fmtEntero(sel.poblacion)}</dd>
              </div>
            </dl>
            <p className="detalle__nota">
              Corte {mesActivo ?? '—'}. El nivel es frecuencia relativa de reportes, no severidad.
            </p>
          </div>
        ) : null}
      </div>

      <p className="eyebrow" style={{ marginTop: 'var(--s-8)' }}>
        Equivalente textual del mapa
      </p>
      <div className="filete" />
      <div className="tabla-scroll">
        <table className="tabla">
          <caption className="visualmente-oculto">
            Municipios con su nivel: el mismo contenido del mapa en texto
          </caption>
          <thead>
            <tr>
              <th>Municipio</th>
              <th>Nivel</th>
              <th>Eventos</th>
              <th>Magnitud máx.</th>
              <th>Población</th>
            </tr>
          </thead>
          <tbody>
            {municipios.map((m) => {
              const p = serie.datos?.serie.find((x) => x.municipio === m.id && x.mes === mesActivo)
              return (
                <tr key={m.id} data-activa={sel?.id === m.id}>
                  <td>
                    <button type="button" className="enlace-tabla" onClick={() => setSel(m)}>
                      {m.nombre}
                    </button>
                  </td>
                  <td>
                    <TarjetaNivel nivel={m.nivel} variante="contorno" />
                  </td>
                  <td className="mono">{fmtEntero(p?.eventos ?? null)}</td>
                  <td className="mono">{fmtMagnitud(p?.mag_max ?? null)}</td>
                  <td className="mono">{fmtEntero(m.poblacion)}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
