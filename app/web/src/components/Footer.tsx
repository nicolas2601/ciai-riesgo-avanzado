import { Link } from '../router.tsx'

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
          <h3 className="footer__titulo">Los tres niveles</h3>
          <p className="footer__texto">
            <Link to="/basico">Básico: clasificación</Link>
          </p>
          <p className="footer__texto">
            <Link to="/medio">Medio: grupos</Link>
          </p>
          <p className="footer__texto">
            <Link to="/avanzado">Avanzado: priorización</Link>
          </p>
        </div>
        <div>
          <h3 className="footer__titulo">Fuentes</h3>
          <p className="footer__texto">
            <a href="https://bdrsnc.sgc.gov.co/paginas1/catalogo/">Catálogo SGC</a>
          </p>
          <p className="footer__texto">
            <Link to="/metodologia">Metodología y límites</Link>
          </p>
        </div>
      </div>
    </footer>
  )
}
