import { fmtEntero } from '../lib/formato.ts'

// Cifra del JSON. Si es null muestra "—" y "no disponible": nunca 0.
export function ChipCifra({
  valor,
  etiqueta,
  ejemplo,
  unidad,
}: {
  valor: number | null
  etiqueta: string
  ejemplo?: boolean
  unidad?: string
}) {
  const falta = valor === null
  return (
    <div className="chip">
      <span className={`chip__valor chip__valor--data${falta ? ' chip__valor--vacio' : ''}`}>
        {falta ? '—' : fmtEntero(valor)}
        {!falta && unidad ? <span className="chip__unidad">{unidad}</span> : null}
      </span>
      <span className="chip__etiqueta">
        {ejemplo ? 'conjunto de ejemplo' : falta ? 'no disponible' : etiqueta}
      </span>
    </div>
  )
}
