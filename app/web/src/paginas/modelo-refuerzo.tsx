import '../estilos.ts'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Shell } from '../components/Shell.tsx'
import { BannerEjemplo } from '../components/BannerEjemplo.tsx'
import { Tiempo } from '../pages/Tiempo.tsx'
import { Priorizacion } from '../pages/Priorizacion.tsx'
import { usePriorizacion } from '../lib/datos.ts'

// Pagina del modelo de refuerzo: como decide el agente y si acerto.
function Refuerzo() {
  const pri = usePriorizacion()
  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Modelo de refuerzo</p>
        <h1 className="pitch__titulo">El agente elige antes de ver el futuro</h1>
        <p className="pitch__texto">
          Un episodio por corte histórico. El agente selecciona K municipios distintos, la
          recompensa intermedia es cero y la terminal se calcula una sola vez, contra la actividad
          oficial del mes siguiente. Nunca recibe la señal futura antes de cerrar su plan.
        </p>
      </section>

      {pri.ejemplo ? <BannerEjemplo /> : null}

      <section className="pitch">
        <p className="eyebrow">Estado, acción y recompensa</p>
        <div className="filete" />
        <div className="rejilla">
          <article className="tarjeta">
            <h2 className="tarjeta__titulo">Observación</h2>
            <p className="tarjeta__texto">
              Matriz de variables del corte, máscara de municipios ya elegidos, presupuesto
              restante y banderas de datos ausentes.
            </p>
          </article>
          <article className="tarjeta">
            <h2 className="tarjeta__titulo">Acción</h2>
            <p className="tarjeta__texto">
              Elegir el índice de un municipio. La máscara impide repetir uno ya seleccionado. La
              acción no crea ni elimina sismos.
            </p>
          </article>
          <article className="tarjeta">
            <h2 className="tarjeta__titulo">Recompensa</h2>
            <p className="tarjeta__texto">
              Cero hasta cerrar K. La terminal es la actividad oficial del mes siguiente,
              ponderada por población: una preferencia declarada por zonas pobladas, no evidencia
              de personas afectadas.
            </p>
          </article>
        </div>
        <p className="panel__nota">
          Con utilidad aditiva y sin efectos de intervención, la selección equivale a una
          optimización top-K. No afirmamos que el refuerzo sea necesario ni superior: lo
          comparamos contra la línea base.
        </p>
      </section>

      <Tiempo />
      <Priorizacion />
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Shell actual="Refuerzo">
      <Refuerzo />
    </Shell>
  </StrictMode>,
)
