import { NIVELES } from '../lib/niveles.ts'
import type { Nivel as NivelT } from '../api/types.ts'
import { IconoNivel } from './Icono.tsx'

// Color + icon + text label: the level is never conveyed by color alone.
export function Nivel({ nivel }: { nivel: NivelT | null }) {
  const clave: NivelT = nivel ?? 'sin-dato'
  const meta = NIVELES[clave]
  return (
    <span
      className="nivel nivel--solida"
      style={{ '--nivel-color': meta.color } as React.CSSProperties}
    >
      <IconoNivel nivel={clave} />
      <span className="nivel__texto">{meta.etiqueta}</span>
    </span>
  )
}
