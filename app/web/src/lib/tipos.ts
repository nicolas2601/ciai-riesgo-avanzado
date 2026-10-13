// Tipos del contrato de datos (docs/plan/10, seccion 4). La web lee JSON, no API.

export type Nivel = 'bajo' | 'medio' | 'alto' | 'sin-dato' | 'sin-priorizacion'

export interface Municipio {
  id: string
  nombre: string
  lat: number
  lon: number
  poblacion: number | null
  cluster: string | null
  nivel: Nivel | null
}

export interface MunicipiosDoc {
  ejemplo: boolean
  municipios: Municipio[]
}

export interface PuntoSerie {
  municipio: string
  mes: string
  eventos: number | null
  mag_max: number | null
  sacudida: number | null
  nivel_real: Nivel | null
  nivel_predicho: Nivel | null
}

export interface SerieDoc {
  ejemplo: boolean
  cortes: string[]
  serie: PuntoSerie[]
}

export interface Cluster {
  id: string
  nombre: string
  descripcion: string
  variables: string[]
  importancia: number[]
  municipios: string[]
}

export interface CortePriorizacion {
  corte: string
  agente: string[]
  baselines: Record<string, string[]>
  oraculo: string[]
  real: Record<string, 0 | 1>
}

export interface PriorizacionDoc {
  ejemplo: boolean
  k: number
  cortes: CortePriorizacion[]
}

export interface MetricasDoc {
  ejemplo: boolean
  basico: { matriz: number[][] | null; f1_macro: number | null; nota: string }
  rl: { curvas: number[] | null; retorno_medio: number | null; semillas: number[] }
  comparacion: { diferencia_pareada: number | null; intervalo: number[] | null; nota: string }
}

export interface VariableDiccionario {
  nombre: string
  tipo: string
  unidad: string
  fuente: string
  porque: string
}

export interface Fuente {
  nombre: string
  url: string
  fecha: string
  filtros: string
}
