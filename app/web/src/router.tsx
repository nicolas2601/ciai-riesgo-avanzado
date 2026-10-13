// Minimal SPA router on the History API. Basename is the site root.
import { useEffect, useState } from 'react'
import type { MouseEvent, ReactNode } from 'react'

const EVENTO = 'ciai:navegar'

export function usePath(): string {
  const [path, setPath] = useState(window.location.pathname)
  useEffect(() => {
    const sync = () => setPath(window.location.pathname)
    window.addEventListener('popstate', sync)
    window.addEventListener(EVENTO, sync)
    return () => {
      window.removeEventListener('popstate', sync)
      window.removeEventListener(EVENTO, sync)
    }
  }, [])
  return path
}

export function navegar(to: string) {
  window.history.pushState(null, '', to)
  window.dispatchEvent(new Event(EVENTO))
  window.scrollTo(0, 0)
}

export function Link({
  to,
  className,
  children,
  ...aria
}: {
  to: string
  className?: string
  children: ReactNode
  'aria-current'?: 'page'
}) {
  const onClick = (ev: MouseEvent<HTMLAnchorElement>) => {
    if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return
    ev.preventDefault()
    navegar(to)
  }
  return (
    <a href={to} className={className} onClick={onClick} {...aria}>
      {children}
    </a>
  )
}
