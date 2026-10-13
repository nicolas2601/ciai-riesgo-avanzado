export function Metodologia() {
  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Metodología</p>
        <h1 className="pitch__titulo">Fuentes, método y límites</h1>
      </section>

      <section className="pitch">
        <p className="eyebrow">Fuentes</p>
        <div className="filete" />
        <ul className="lista-fuentes">
          <li>
            <a href="https://bdrsnc.sgc.gov.co/paginas1/catalogo/">
              Servicio Geológico Colombiano (SGC): catálogo de sismicidad
            </a>
            . Origen único de los eventos; la unidad de análisis es el municipio (87 en
            Santander).
          </li>
          <li>
            <a href="https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion">
              DANE: proyecciones de población
            </a>{' '}
            por municipio, usadas como variable de contexto.
          </li>
        </ul>
      </section>

      <section className="pitch">
        <p className="eyebrow">Método</p>
        <div className="filete" />
        <div className="acordeon">
          <p>
            <strong>Básico.</strong> Random Forest sobre un panel municipio-mes con
            rasgos de actividad de los meses anteriores. Predice la clase (bajo, medio, alto) del
            mes siguiente. Macro-F1 de 0,593 en validación.
          </p>
          <p>
            <strong>Medio.</strong> KMeans sin supervisión sobre el perfil sísmico de cada
            municipio. Los grupos no usan la clase objetivo.
          </p>
          <p>
            <strong>Avanzado.</strong> Selección de K municipios por corte con un agente PPO, un
            ranking estático por eventos recientes y una elección aleatoria determinista como
            referencias.
          </p>
        </div>
      </section>

      <section className="pitch">
        <p className="eyebrow">Límites</p>
        <div className="filete" />
        <div className="acordeon">
          <p>
            <strong>No predice sismos ni es alerta oficial.</strong> Los niveles son frecuencia
            relativa de eventos registrados en el catálogo, no severidad ni daño.
          </p>
          <p>
            <strong>Desbalance de clases.</strong> La clase «bajo» domina; una accuracy alta no
            demuestra aprendizaje. Se reporta macro-F1.
          </p>
          <p>
            <strong>El PPO no supera la línea base.</strong> Colapsa a una selección constante y
            rinde como el ranking estático.
          </p>
          <p>
            <strong>Resultados exploratorios.</strong> La actividad del catálogo se
            concentra en muy pocos municipios (el grupo 2 del nivel medio agrupa solo a Los
            Santos y Zapatoca), así que las conclusiones no son estadísticamente firmes.
          </p>
        </div>
      </section>
    </div>
  )
}
