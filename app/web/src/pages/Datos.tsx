import { EstadoVacio } from '../components/EstadoVacio.tsx'
import { useClusters, useDiccionario, useFuentes } from '../lib/datos.ts'
import { fmtDecimal } from '../lib/formato.ts'

export function Grupos() {
  const cl = useClusters()
  return (
    <div className="contenedor">
      <p className="eyebrow">Grupos del Medio</p>
      <div className="filete" />
      <EstadoVacio cargando={cl.cargando} error={cl.error} />
      <div className="rejilla">
        {(cl.datos?.clusters ?? []).map((c) => (
          <article key={c.id} className="tarjeta">
            <h2 className="tarjeta__titulo">{c.nombre}</h2>
            <p className="tarjeta__texto">{c.descripcion}</p>
            <ul className="barras">
              {c.variables.map((v, i) => (
                <li key={v}>
                  <span className="mono">{v}</span>
                  <span className="barra">
                    <span
                      className="barra__relleno"
                      style={{ width: `${Math.round((c.importancia[i] ?? 0) * 100)}%` }}
                    />
                  </span>
                  <span className="mono">{fmtDecimal(c.importancia[i] ?? null, 2)}</span>
                </li>
              ))}
            </ul>
            <p className="tarjeta__pie">{c.municipios.length} municipios</p>
          </article>
        ))}
      </div>
    </div>
  )
}

export function Metodologia() {
  const dic = useDiccionario()
  const fue = useFuentes()
  return (
    <div className="contenedor">
      <p className="eyebrow">Qué significa y qué no</p>
      <div className="filete" />
      <div className="acordeon">
        <p>
          <strong>Los niveles son frecuencia relativa de reportes</strong> del catálogo del SGC, no
          severidad ni daño. No son una alerta oficial.
        </p>
        <p>
          <strong>La sacudida no se observa.</strong> El catálogo no registra lo que se sintió en
          una ciudad; eso tendría que derivarse de magnitud, profundidad y distancia con una
          atenuación declarada.
        </p>
        <p>
          <strong>La validación es cronológica y por bloques.</strong> Nunca aleatoria sobre
          municipios vecinos: eso filtraría el espacio y el tiempo.
        </p>
      </div>

      <p className="eyebrow" style={{ marginTop: 'var(--s-8)' }}>
        Fuentes
      </p>
      <div className="filete" />
      <EstadoVacio cargando={fue.cargando} error={fue.error} />
      <div className="tabla-scroll">
        <table className="tabla">
          <thead>
            <tr>
              <th>Fuente</th>
              <th>URL</th>
              <th>Fecha</th>
              <th>Filtros</th>
            </tr>
          </thead>
          <tbody>
            {(fue.datos?.fuentes ?? []).map((f) => (
              <tr key={f.nombre}>
                <td>{f.nombre}</td>
                <td className="mono">{f.url}</td>
                <td className="mono">{f.fecha}</td>
                <td>{f.filtros}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="eyebrow" style={{ marginTop: 'var(--s-8)' }}>
        Diccionario de variables
      </p>
      <div className="filete" />
      <EstadoVacio cargando={dic.cargando} error={dic.error} />
      <div className="tabla-scroll">
        <table className="tabla">
          <thead>
            <tr>
              <th>Variable</th>
              <th>Tipo</th>
              <th>Unidad</th>
              <th>Fuente</th>
              <th>Por qué entra</th>
            </tr>
          </thead>
          <tbody>
            {(dic.datos?.variables ?? []).map((v) => (
              <tr key={v.nombre}>
                <td className="mono">{v.nombre}</td>
                <td>{v.tipo}</td>
                <td>{v.unidad}</td>
                <td>{v.fuente}</td>
                <td>{v.porque}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
