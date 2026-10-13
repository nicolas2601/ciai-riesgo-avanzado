// Contract v1 of the API. Types mirror the documented responses; nothing is invented client-side.
export type Nivel = 'bajo' | 'medio' | 'alto' | 'sin-dato' | 'sin-priorizacion'
export type Clase = 'bajo' | 'medio' | 'alto'

export interface Health {
  status: string
  modelos: unknown
  version: string
}

export interface Municipio {
  divipola: string
  nombre: string
  lat: number
  lon: number
  poblacion: number
}

export interface FilaPanel {
  divipola: string
  nombre: string
  features: Record<string, number | null>
  clase_observada: Clase | null
  target_clase_mes_siguiente: Clase | null
  target_actividad_m3: number | null
}

export interface Panel {
  mes: string
  filas: FilaPanel[]
}

export interface ClasificarRequest {
  divipola: string
  mes: string
}

export interface Clasificacion {
  divipola: string
  mes: string
  clase: Clase
  probabilidades: Record<Clase, number>
  modelo: string
  version?: string
  exploratorio: boolean
}

export interface MunicipioRank {
  divipola: string
  nombre: string
  rank: number
}

export interface MetodoPriorizacion {
  metodo: string
  municipios: MunicipioRank[]
  recompensa_real: number | null
}

export interface Priorizacion {
  corte: string
  k: number
  exploratorio: boolean
  nota: string
  metodos: MetodoPriorizacion[]
}

export interface RasgoCluster {
  variable: string
  direccion: string
  desviaciones_estandar: number
}

export interface PerfilCluster {
  cluster: number
  etiqueta: string
  n_municipios: number
  municipios: string[]
  rasgos: RasgoCluster[]
  medias: Record<string, number>
}

export interface MunicipioCluster {
  divipola: string
  municipio: string
  lat: number
  lon: number
  cluster: number
  etiqueta: string
}

export interface Clusters {
  municipios: MunicipioCluster[]
  perfiles: PerfilCluster[]
  metricas: { k: number; silhouette: number; davies_bouldin: number }
  metadata: { fit_until: string; metodo: string; scope: string }
}
