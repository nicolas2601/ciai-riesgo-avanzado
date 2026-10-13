// Carga de los JSON de public/data. Sin API: fetch estatico a un archivo.
// Todo se marca como ejemplo si el propio archivo lo trae: el banner lo lee.
import { useEffect, useState } from 'react'
import type {
  Cluster,
  Fuente,
  MetricasDoc,
  MunicipiosDoc,
  PriorizacionDoc,
  SerieDoc,
  VariableDiccionario,
} from './tipos.ts'

const BASE = `${import.meta.env.BASE_URL}data`

export interface Estado<T> {
  datos: T | null
  cargando: boolean
  error: string | null
  ejemplo: boolean
}

async function cargar<T>(nombre: string): Promise<{ datos: T; ejemplo: boolean }> {
  const res = await fetch(`${BASE}/${nombre}`)
  if (!res.ok) throw new Error(`${nombre}: ${res.status}`)
  const json = (await res.json()) as T & { ejemplo?: boolean }
  return { datos: json, ejemplo: json.ejemplo === true }
}

function useDoc<T>(nombre: string): Estado<T> {
  const [estado, setEstado] = useState<Estado<T>>({
    datos: null,
    cargando: true,
    error: null,
    ejemplo: false,
  })

  useEffect(() => {
    let vivo = true
    cargar<T>(nombre)
      .then(({ datos, ejemplo }) => {
        if (vivo) setEstado({ datos, cargando: false, error: null, ejemplo })
      })
      .catch((e: unknown) => {
        if (vivo) {
          setEstado({
            datos: null,
            cargando: false,
            error: e instanceof Error ? e.message : 'Error de carga',
            ejemplo: false,
          })
        }
      })
    return () => {
      vivo = false
    }
  }, [nombre])

  return estado
}

export const useMunicipios = () => useDoc<MunicipiosDoc>('municipios.json')
export const useSerie = () => useDoc<SerieDoc>('serie_mensual.json')
export const useClusters = () => useDoc<{ ejemplo: boolean; clusters: Cluster[] }>('clusters.json')
export const usePriorizacion = () => useDoc<PriorizacionDoc>('priorizacion.json')
export const useMetricas = () => useDoc<MetricasDoc>('metricas.json')
export const useDiccionario = () =>
  useDoc<{ ejemplo: boolean; variables: VariableDiccionario[] }>('diccionario.json')
export const useFuentes = () => useDoc<{ ejemplo: boolean; fuentes: Fuente[] }>('fuentes.json')
