// Formato colombiano: miles con punto, decimal con coma. Magnitudes con unidad.
export function fmtEntero(valor: number | null): string {
  if (valor === null) return '—'
  return valor.toLocaleString('es-CO', { maximumFractionDigits: 0 })
}

export function fmtDecimal(valor: number | null, digitos = 1): string {
  if (valor === null) return '—'
  return valor.toLocaleString('es-CO', {
    minimumFractionDigits: digitos,
    maximumFractionDigits: digitos,
  })
}

export function fmtMagnitud(valor: number | null): string {
  if (valor === null) return '—'
  return `M ${fmtDecimal(valor)}`
}
