import type { ReactNode } from 'react'
import { Link } from '../router.tsx'
import { Footer } from './Footer.tsx'

export const PAGINAS = [
  { to: '/', texto: 'Inicio' },
  { to: '/basico', texto: 'Básico' },
  { to: '/medio', texto: 'Medio' },
  { to: '/avanzado', texto: 'Avanzado' },
  { to: '/pruebas', texto: 'Pruebas' },
  { to: '/metodologia', texto: 'Metodología' },
] as const

export function Shell({ path, children }: { path: string; children: ReactNode }) {
  return (
    <>
      <header className="navbar">
        <div className="navbar__interno">
          <Link to="/" className="navbar__marca">
            <img src="/logo.svg" alt="" width="28" height="28" className="navbar__logo" />
            Sismo, no previsible
          </Link>
          <nav className="navbar__nav" aria-label="Páginas">
            {PAGINAS.map((p) => (
              <Link
                key={p.to}
                to={p.to}
                className={`navbar__enlace${p.to === path ? ' active' : ''}`}
                aria-current={p.to === path ? 'page' : undefined}
              >
                {p.texto}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="main">{children}</main>
      <Footer />
    </>
  )
}
