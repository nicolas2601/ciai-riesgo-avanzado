import { Seccion, Sello } from '../../components/Explica.tsx'

const LINEA = [
  ['Descarga SGC', 'Catálogo de sismicidad del Servicio Geológico Colombiano, descarga 2026-10-13.'],
  ['Unión de dos sistemas', 'Se unifican los catálogos y se eliminan duplicados (35 eliminados).'],
  ['Panel sin fuga del futuro', 'Una fila por municipio y mes; cada variable usa solo datos pasados.'],
  ['Particiones cronológicas', 'Train, validación y test en orden temporal, nunca mezcladas al azar.'],
  ['3 modelos', 'Random Forest (básico), KMeans (medio) y PPO (avanzado).'],
  ['API', 'Sirve resultados ya calculados a la web.'],
  ['Web', 'Esta aplicación: consulta, explica y declara límites.'],
]

export function MetodologiaExplica() {
  return (
    <>
      <Seccion eyebrow="Flujo" titulo="De la descarga a la web">
        <ol className="linea">
          {LINEA.map(([t, d]) => (
            <li key={t} className="linea__item">
              <strong>{t}</strong>
              {d}
            </li>
          ))}
        </ol>
      </Seccion>
      <Seccion eyebrow="Fuentes" titulo="Procedencia y fecha">
        <div className="tabla-wrap">
          <table>
            <caption className="visually-hidden">Fuentes de datos</caption>
            <thead><tr><th>Fuente</th><th>Uso</th><th>Fecha</th></tr></thead>
            <tbody>
              <tr>
                <td><a href="https://bdrsnc.sgc.gov.co/paginas1/catalogo/">SGC, catálogo de sismicidad</a></td>
                <td>Eventos sísmicos</td>
                <td className="mono">descarga 2026-10-13</td>
              </tr>
              <tr>
                <td>DANE, proyecciones de población retrospectivas</td>
                <td>Población por municipio</td>
                <td className="mono">descarga 2026-10-13</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Seccion>
      <Seccion eyebrow="Sesgo" titulo="Sesgo de detección">
        <ul className="lista-sellos">
          <li><Sello tipo="hecho" /> Hay más eventos registrados en 2009-2012.</li>
          <li><Sello tipo="hipotesis" /> Es consistente con mejoras de instrumentación, no es una causa demostrada.</li>
          <li><Sello tipo="hecho" /> Por eso las clases se definen por magnitud y se usa Mc móvil (magnitud de completitud) como variable.</li>
        </ul>
      </Seccion>
      <Seccion eyebrow="Límites" titulo="Lo que no se debe concluir">
        <ul className="lista-sellos">
          <li><Sello tipo="limitacion" /> No es alerta oficial ni predice sismos.</li>
          <li><Sello tipo="limitacion" /> Test ya consultado: sirve de confirmación, no de examen intacto.</li>
          <li><Sello tipo="limitacion" /> Clase «alto» con muy pocos casos: las métricas por clase son inestables.</li>
          <li><Sello tipo="limitacion" /> El PPO no supera la línea base estática.</li>
        </ul>
      </Seccion>
    </>
  )
}
