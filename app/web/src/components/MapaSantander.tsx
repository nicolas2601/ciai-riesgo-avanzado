import * as maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useEffect, useRef, useState } from 'react'
import type { MunicipioCluster } from '../api/types.ts'
import { BASE_STYLE, ESTILOS, type Coleccion, cargarGeojson, divipolaDe, estilo } from '../lib/gruposMapa.ts'

interface Props {
  municipios: MunicipioCluster[]
  seleccionado: string | null
  onSelect: (m: MunicipioCluster) => void
}

function marcador(m: MunicipioCluster, onSelect: (m: MunicipioCluster) => void) {
  const e = estilo(m.cluster)
  const el = document.createElement('button')
  el.type = 'button'
  el.className = `marca marca--${e.forma}`
  el.style.setProperty('--c', e.color)
  el.title = `${m.municipio} · grupo ${m.cluster} · ${m.etiqueta}`
  el.setAttribute('aria-label', `${m.municipio}, grupo ${m.cluster}, ${e.forma}`)
  el.addEventListener('click', () => onSelect(m))
  return el
}

function pintarCoropletico(map: maplibregl.Map, gj: Coleccion, ms: MunicipioCluster[], onSelect: Props['onSelect']) {
  const porCod = new Map(ms.map((m) => [m.divipola.padStart(5, '0'), m]))
  for (const f of gj.features) {
    const m = porCod.get(divipolaDe(f.properties) ?? '')
    f.properties = { ...f.properties, _grupo: m ? m.cluster : -1, _cod: m?.divipola ?? '' }
  }
  const color = ['match', ['get', '_grupo'], ...ESTILOS.flatMap((e, i) => [i, e.color]), '#d0d4da'] as unknown as maplibregl.ExpressionSpecification
  map.addSource('mun', { type: 'geojson', data: gj })
  map.addLayer({ id: 'mun-fill', type: 'fill', source: 'mun', paint: { 'fill-color': color, 'fill-opacity': 0.6 } })
  ESTILOS.forEach((e, i) =>
    map.addLayer({ id: `mun-line-${i}`, type: 'line', source: 'mun', filter: ['==', ['get', '_grupo'], i],
      paint: { 'line-color': '#1f2933', 'line-width': 1, 'line-dasharray': [...e.dash] } }),
  )
  map.addLayer({ id: 'mun-sel', type: 'line', source: 'mun', filter: ['==', ['get', '_cod'], '__none__'], paint: { 'line-color': '#000', 'line-width': 3 } })
  const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false })
  map.on('mousemove', 'mun-fill', (ev) => {
    const m = porCod.get(divipolaDe(ev.features?.[0]?.properties ?? null) ?? '')
    map.getCanvas().style.cursor = m ? 'pointer' : ''
    if (m) popup.setLngLat(ev.lngLat).setText(`${m.municipio} · grupo ${m.cluster}`).addTo(map)
  })
  map.on('mouseleave', 'mun-fill', () => { popup.remove(); map.getCanvas().style.cursor = '' })
  map.on('click', 'mun-fill', (ev) => {
    const m = porCod.get(divipolaDe(ev.features?.[0]?.properties ?? null) ?? '')
    if (m) onSelect(m)
  })
}

export function MapaSantander({ municipios, seleccionado, onSelect }: Props) {
  const cont = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const selRef = useRef(onSelect)
  const [capa, setCapa] = useState<'cargando' | 'coropletico' | 'marcadores'>('cargando')
  useEffect(() => { selRef.current = onSelect })

  useEffect(() => {
    if (!cont.current || municipios.length === 0) return
    const map = new maplibregl.Map({ container: cont.current, style: BASE_STYLE, center: [-73.2, 6.7], zoom: 7 })
    mapRef.current = map
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right')
    const lons = municipios.map((m) => m.lon)
    const lats = municipios.map((m) => m.lat)
    map.fitBounds([[Math.min(...lons), Math.min(...lats)], [Math.max(...lons), Math.max(...lats)]], { padding: 40, animate: false })
    const marcas: maplibregl.Marker[] = []
    const pick = (m: MunicipioCluster) => selRef.current(m)
    let vivo = true
    const iniciar = async () => {
      const gj = await cargarGeojson()
      if (!vivo) return
      if (gj) {
        pintarCoropletico(map, gj, municipios, pick)
        setCapa('coropletico')
        return
      }
      for (const m of municipios) marcas.push(new maplibregl.Marker({ element: marcador(m, pick) }).setLngLat([m.lon, m.lat]).addTo(map))
      setCapa('marcadores')
    }
    map.on('load', () => void iniciar())
    return () => { vivo = false; marcas.forEach((k) => k.remove()); map.remove(); mapRef.current = null }
  }, [municipios])

  useEffect(() => {
    const map = mapRef.current
    if (capa === 'coropletico' && map?.getLayer('mun-sel')) map.setFilter('mun-sel', ['==', ['get', '_cod'], seleccionado ?? '__none__'])
  }, [seleccionado, capa])

  return (
    <div className="mapa-real" role="region" aria-label="Mapa de Santander por grupo" data-capa={capa}>
      <div ref={cont} className="mapa-real__canvas" />
      {capa === 'cargando' ? <p className="mapa-real__estado">Cargando mapa…</p> : null}
    </div>
  )
}
