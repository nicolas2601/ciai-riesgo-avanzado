// Estado de carga y de error. No hay invento de datos: si falla, se dice.
export function EstadoVacio({
  cargando,
  error,
}: {
  cargando: boolean
  error: string | null
}) {
  if (cargando) {
    return (
      <p className="estado" role="status">
        Cargando datos…
      </p>
    )
  }
  if (error) {
    return (
      <p className="estado estado--error" role="alert">
        No se pudieron cargar los datos: {error}
      </p>
    )
  }
  return null
}
