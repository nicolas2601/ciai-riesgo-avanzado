// Okabe-Ito based palette: distinguishable under common color-vision deficiencies.
// Each group also has its own marker shape and outline dash pattern.
export const ESTILOS = [
  { color: '#0072b2', forma: 'círculo', dash: [1, 0] },
  { color: '#e69f00', forma: 'cuadrado', dash: [4, 2] },
  { color: '#cc79a7', forma: 'rombo', dash: [1, 2] },
] as const

export function estilo(cluster: number) {
  return ESTILOS[cluster % ESTILOS.length]
}

export const BASE_STYLE = {
  version: 8 as const,
  sources: {
    carto: {
      type: 'raster' as const,
      // CARTO raster tiles now return an "API KEY REQUIRED" watermark without a key,
      // so the keyless OpenStreetMap standard tiles are used instead.
      tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
      tileSize: 256,
      attribution: '© OpenStreetMap contributors',
    },
  },
  layers: [{ id: 'carto', type: 'raster' as const, source: 'carto' }],
}

const KEYS = ['divipola', 'DIVIPOLA', 'MPIO_CDPMP', 'mpio_cdpmp', 'cod_mpio', 'COD_MPIO']

export function divipolaDe(props: Record<string, unknown> | null): string | null {
  if (!props) return null
  for (const k of KEYS) if (props[k] != null) return String(props[k]).padStart(5, '0')
  return null
}

export interface Coleccion {
  type: string
  features: { type: string; properties: Record<string, unknown> | null; geometry: unknown }[]
}

export const GEOJSON_URL = '/data/santander_municipios.geojson'

// The SPA fallback serves index.html with 200 for unknown paths, so parse defensively.
export async function cargarGeojson(): Promise<Coleccion | null> {
  try {
    const r = await fetch(GEOJSON_URL)
    if (!r.ok) return null
    const j = (await r.json()) as Coleccion
    return j.type === 'FeatureCollection' && j.features.length > 0 ? j : null
  } catch {
    return null
  }
}
