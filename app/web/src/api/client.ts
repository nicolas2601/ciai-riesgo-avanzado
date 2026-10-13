// Typed fetch client. 8 s timeout; every failure becomes an ApiError with code + message.
import type {
  ClasificarRequest,
  Clasificacion,
  Clusters,
  Health,
  Municipio,
  Panel,
  Priorizacion,
} from './types.ts'

export const API_URL: string = (
  (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000/api/v1'
).replace(/\/$/, '')
export const TIMEOUT_MS = 8000

export class ApiError extends Error {
  readonly code: string
  readonly status: number | null
  constructor(code: string, message: string, status: number | null = null) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.status = status
  }
}

interface ErrorBody {
  error?: { code?: string; message?: string }
}

async function leerError(res: Response): Promise<ApiError> {
  const body = (await res.json().catch(() => null)) as ErrorBody | null
  const code = body?.error?.code ?? `http_${res.status}`
  const message = body?.error?.message ?? `La API respondió ${res.status} ${res.statusText}`.trim()
  return new ApiError(code, message, res.status)
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const ctl = new AbortController()
  const timer = setTimeout(() => ctl.abort(), TIMEOUT_MS)
  try {
    const res = await fetch(`${API_URL}${path}`, {
      ...init,
      signal: ctl.signal,
      headers: { Accept: 'application/json', ...(init.headers ?? {}) },
    })
    if (!res.ok) throw await leerError(res)
    return (await res.json()) as T
  } catch (e) {
    if (e instanceof ApiError) throw e
    if (e instanceof DOMException && e.name === 'AbortError') {
      throw new ApiError('timeout', `La API no respondió en ${TIMEOUT_MS / 1000} s (${API_URL}).`)
    }
    throw new ApiError('network', `No se pudo conectar con la API (${API_URL}).`)
  } finally {
    clearTimeout(timer)
  }
}

const q = encodeURIComponent

export const api = {
  health: () => request<Health>('/health'),
  municipios: () => request<Municipio[]>('/municipios'),
  panel: (mes: string) => request<Panel>(`/panel?mes=${q(mes)}`),
  clasificar: (body: ClasificarRequest) =>
    request<Clasificacion>('/clasificar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),
  priorizacion: (corte: string, k: number) =>
    request<Priorizacion>(`/priorizacion?corte=${q(corte)}&k=${k}`),
  clusters: () => request<Clusters>('/clusters'),
}
