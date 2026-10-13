// Meta de cada nivel: color + etiqueta. El nivel nunca va solo con color.
import type { Nivel } from './tipos.ts'

export interface NivelMeta {
  color: string
  etiqueta: string
}

export const NIVELES: Record<Nivel, NivelMeta> = {
  bajo: { color: 'var(--risk-bajo)', etiqueta: 'Bajo' },
  medio: { color: 'var(--risk-medio)', etiqueta: 'Medio' },
  alto: { color: 'var(--risk-alto)', etiqueta: 'Alto' },
  'sin-dato': { color: 'var(--risk-nodato)', etiqueta: 'Sin dato' },
  'sin-priorizacion': { color: 'var(--risk-sinpri)', etiqueta: 'Sin priorización' },
}

export function etiquetaNivel(nivel: Nivel | null): string {
  if (nivel === null) return 'Sin dato'
  return NIVELES[nivel].etiqueta
}
