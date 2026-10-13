// Iconos de nivel. Cada nivel tiene su propia forma: la distincion no depende
// del color (regla de accesibilidad y de DESIGN.md, seccion 3.2).
import type { ReactElement } from 'react'
import type { Nivel } from '../api/types.ts'

const trazo = {
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.5,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
}

const TRAZOS: Record<Nivel, ReactElement> = {
  bajo: (
    <svg viewBox="0 0 16 16" width="14" height="14" role="presentation">
      <circle cx="8" cy="8" r="6" {...trazo} />
      <circle cx="8" cy="8" r="2" fill="currentColor" />
    </svg>
  ),
  medio: (
    <svg viewBox="0 0 16 16" width="14" height="14" role="presentation">
      <path d="M8 1.8 14.2 13H1.8Z" {...trazo} />
      <path d="M8 7v3.4" {...trazo} />
    </svg>
  ),
  alto: (
    <svg viewBox="0 0 16 16" width="14" height="14" role="presentation">
      <path d="M8 1.4 14.6 8 8 14.6 1.4 8Z" {...trazo} />
      <path d="M5.4 11.6 10.6 4.4" {...trazo} />
    </svg>
  ),
  'sin-dato': (
    <svg viewBox="0 0 16 16" width="14" height="14" role="presentation">
      <circle cx="8" cy="8" r="6" {...trazo} strokeDasharray="2.5 2.5" />
      <path d="M5.6 8h4.8" {...trazo} />
    </svg>
  ),
  'sin-priorizacion': (
    <svg viewBox="0 0 16 16" width="14" height="14" role="presentation">
      <circle cx="8" cy="8" r="6" {...trazo} />
      <path d="M5.8 6.4h.01M8 6.4h.01M10.2 6.4h.01" {...trazo} strokeWidth="2" />
      <path d="M8 10v2.4" {...trazo} />
    </svg>
  ),
}

export function IconoNivel({ nivel }: { nivel: Nivel | null }) {
  const clave: Nivel = nivel ?? 'sin-dato'
  return TRAZOS[clave]
}

export function IconoAlerta({ size = 14 }: { size?: number }) {
  return (
    <svg viewBox="0 0 16 16" width={size} height={size} role="presentation">
      <path d="M8 2 15 14H1Z" {...trazo} />
      <path d="M8 6.4v3.2" {...trazo} />
      <circle cx="8" cy="11.8" r="0.9" fill="currentColor" />
    </svg>
  )
}

export function IconoFlecha({ size = 14 }: { size?: number }) {
  return (
    <svg viewBox="0 0 16 16" width={size} height={size} role="presentation">
      <path d="M3 8h9M8.5 4l4 4-4 4" {...trazo} />
    </svg>
  )
}
