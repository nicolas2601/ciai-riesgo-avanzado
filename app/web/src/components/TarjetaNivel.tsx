import { NIVELES } from '../lib/niveles.ts'
import type { Nivel } from '../lib/tipos.ts'
import { IconoNivel } from './Icono.tsx'

// Color + icono + etiqueta de texto, siempre los tres.
export function TarjetaNivel({
  nivel,
  variante = 'solida',
}: {
  nivel: Nivel | null
  variante?: 'solida' | 'contorno'
}) {
  const clave: Nivel = nivel ?? 'sin-dato'
  const meta = NIVELES[clave]
  return (
    <span className={`nivel nivel--${variante}`} style={{ '--nivel-color': meta.color } as React.CSSProperties}>
      <IconoNivel nivel={clave} />
      <span className="nivel__texto">{meta.etiqueta}</span>
    </span>
  )
}
