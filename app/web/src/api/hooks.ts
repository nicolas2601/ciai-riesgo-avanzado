import { useCallback, useEffect, useState } from 'react'
import { ApiError, api } from './client.ts'

export interface Estado<T> {
  data: T | null
  loading: boolean
  error: ApiError | null
  recargar: () => void
}

// Runs `fn` whenever `clave` changes. `clave === null` means "do not fetch yet".
export function useApi<T>(fn: () => Promise<T>, clave: string | null): Estado<T> {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<ApiError | null>(null)
  const [loading, setLoading] = useState(clave !== null)
  const [intento, setIntento] = useState(0)

  useEffect(() => {
    if (clave === null) return
    let vivo = true
    setLoading(true)
    setError(null)
    fn()
      .then((d) => vivo && setData(d))
      .catch((e: unknown) => {
        if (!vivo) return
        setData(null)
        setError(e instanceof ApiError ? e : new ApiError('unknown', String(e)))
      })
      .finally(() => vivo && setLoading(false))
    return () => {
      vivo = false
    }
    // fn is recreated each render; `clave` identifies the request.
    // oxlint-disable-next-line react-hooks/exhaustive-deps
  }, [clave, intento])

  const recargar = useCallback(() => setIntento((n) => n + 1), [])
  return { data, loading, error, recargar }
}

export const useMunicipios = () => useApi(() => api.municipios(), 'municipios')
export const useClusters = () => useApi(() => api.clusters(), 'clusters')
export const useHealth = () => useApi(() => api.health(), 'health')
export const usePanel = (mes: string | null) =>
  useApi(() => api.panel(mes ?? ''), mes && `panel:${mes}`)
export const usePriorizacion = (corte: string | null, k: number) =>
  useApi(() => api.priorizacion(corte ?? '', k), corte && `prio:${corte}:${k}`)
