import type { ReactNode } from 'react'
import { Footer } from './Footer.tsx'

export const PAGINAS = [
  { href: '/index.html', texto: 'Presentación' },
  { href: '/modelo-clasificacion.html', texto: 'Clasificación' },
  { href: '/modelo-supervisado.html', texto: 'Supervisado' },
  { href: '/modelo-refuerzo.html', texto: 'Refuerzo' },
] as const

export function Shell({
  actual,
  children,
  ejemplo,
}: {
  actual: string
  children: ReactNode
  ejemplo?: boolean
}) {
  return (
    <>
      <header className="navbar">
        <div className="navbar__interno">
          <a href="/index.html" className="navbar__marca">
            Sismo, no previsible
          </a>
          <nav className="navbar__nav" aria-label="Páginas">
            {PAGINAS.map((p) => (
              <a
                key={p.href}
                href={p.href}
                className={`navbar__enlace${p.texto === actual ? ' active' : ''}`}
                aria-current={p.texto === actual ? 'page' : undefined}
              >
                {p.texto}
              </a>
            ))}
          </nav>
          {ejemplo ? <span className="navbar__marca-sello">datos de ejemplo</span> : null}
        </div>
      </header>
      <main className="main">{children}</main>
      <Footer />
    </>
  )
}
