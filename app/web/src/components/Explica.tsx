import type { ReactNode } from 'react'
import '../styles/explica.css'

export type TipoSello = 'hecho' | 'hipotesis' | 'limitacion'
const TEXTO_SELLO: Record<TipoSello, string> = {
  hecho: 'HECHO',
  hipotesis: 'HIPÓTESIS',
  limitacion: 'LIMITACIÓN',
}
const ICONO_SELLO: Record<TipoSello, string> = { hecho: '■', hipotesis: '◆', limitacion: '▲' }

export function Sello({ tipo }: { tipo: TipoSello }) {
  return (
    <span className={`sello sello--${tipo}`}>
      <span aria-hidden="true">{ICONO_SELLO[tipo]}</span> {TEXTO_SELLO[tipo]}
    </span>
  )
}

export function Seccion({ titulo, eyebrow, children }: { titulo: string; eyebrow: string; children: ReactNode }) {
  return (
    <section className="pitch explica">
      <p className="eyebrow">{eyebrow}</p>
      <h2 className="explica__titulo">{titulo}</h2>
      <div className="filete" />
      {children}
    </section>
  )
}

export function Pasos({ items }: { items: { titulo: string; texto: string }[] }) {
  return (
    <ol className="pasos">
      {items.map((p, i) => (
        <li key={p.titulo} className="pasos__item">
          <span className="pasos__n" aria-hidden="true">
            {i + 1}
          </span>
          <strong>{p.titulo}</strong>
          <span>{p.texto}</span>
        </li>
      ))}
    </ol>
  )
}

export interface FilaBarra {
  etiqueta: string
  valor: number
  texto: string
  destacada?: boolean
}

export function BarrasH({ filas, max, titulo }: { filas: FilaBarra[]; max: number; titulo: string }) {
  return (
    <ul className="hbarras" aria-label={titulo}>
      {filas.map((f) => (
        <li key={f.etiqueta} className={f.destacada ? 'hbarras__fila hbarras__fila--sel' : 'hbarras__fila'}>
          <span className="hbarras__nombre">{f.etiqueta}</span>
          <span className="hbarras__pista" aria-hidden="true">
            <span className="hbarras__valor" style={{ width: `${Math.max(0, (f.valor / max) * 100)}%` }} />
          </span>
          <span className="mono">{f.texto}</span>
        </li>
      ))}
    </ul>
  )
}
