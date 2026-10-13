import { Link } from 'react-router-dom'

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer__columnas">
        <div>
          <h3 className="footer__titulo">Equipo</h3>
          <p className="footer__texto">Syntax error II — UNAB</p>
          <p className="footer__texto">N. Moreno · J. Arteaga · Z. Quintero</p>
        </div>
        <div>
          <h3 className="footer__titulo">Alcance</h3>
          <p className="footer__texto">
            Priorización exploratoria. No es alerta oficial ni mide severidad.
          </p>
        </div>
        <div>
          <h3 className="footer__titulo">Datos</h3>
          <p className="footer__texto">
            <Link to="/metodologia">Fuentes y diccionario</Link>
          </p>
        </div>
        <div>
          <h3 className="footer__titulo">Logos</h3>
          {/* Espacio reservado. El logo del SGC no se usa sin permiso escrito. */}
          <div className="footer__logos" aria-label="Espacio reservado para logos de aliados" />
        </div>
      </div>
    </footer>
  )
}
