import { MetodologiaExplica } from './explicaciones/MetodologiaExplica.tsx'

export function Metodologia() {
  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Metodología</p>
        <h1 className="pitch__titulo">Fuentes, método y límites</h1>
      </section>

      <MetodologiaExplica />
    </div>
  )
}
