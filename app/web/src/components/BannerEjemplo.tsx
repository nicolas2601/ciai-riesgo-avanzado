import { IconoAlerta } from './Icono.tsx'

// Banner obligatorio mientras exista un JSON con "ejemplo": true.
// En modo presentacion no se puede cerrar.
export function BannerEjemplo({ fijo }: { fijo?: boolean }) {
  return (
    <div className={`banner${fijo ? ' banner--fijo' : ''}`} role="status">
      <IconoAlerta />
      <p className="banner__texto">
        <strong>Datos de ejemplo: no son resultados reales.</strong> Las cifras que se muestran son
        sintéticas y sirven para probar la interfaz.
      </p>
    </div>
  )
}
