import type { Estado as EstadoApi } from '../api/hooks.ts'

// Visible loading / error state. Never renders placeholder data.
export function Estado({
  e,
  que,
}: {
  e: Pick<EstadoApi<unknown>, 'loading' | 'error' | 'recargar'>
  que: string
}) {
  if (e.loading) {
    return (
      <p className="estado" role="status">
        Cargando {que}…
      </p>
    )
  }
  if (e.error) {
    return (
      <div className="estado estado--error" role="alert">
        <p>
          No se pudo cargar {que}: {e.error.message} <code>({e.error.code})</code>
        </p>
        <button type="button" className="btn btn--secundario" onClick={e.recargar}>
          Reintentar
        </button>
      </div>
    )
  }
  return null
}
