import { Shell } from './components/Shell.tsx'
import { usePath } from './router.tsx'
import { Inicio } from './pages/Inicio.tsx'
import { Basico } from './pages/Basico.tsx'
import { Medio } from './pages/Medio.tsx'
import { Avanzado } from './pages/Avanzado.tsx'
import { Metodologia } from './pages/Metodologia.tsx'
import Pruebas from './pages/Pruebas.tsx'
import ComoFunciona from './pages/ComoFunciona.tsx'

const RUTAS: Record<string, () => React.JSX.Element> = {
  '/': Inicio,
  '/como-funciona': ComoFunciona,
  '/basico': Basico,
  '/medio': Medio,
  '/avanzado': Avanzado,
  '/pruebas': Pruebas,
  '/metodologia': Metodologia,
}

export function App() {
  const path = usePath().replace(/\/+$/, '') || '/'
  const Pagina = RUTAS[path] ?? Inicio
  return (
    <Shell path={path in RUTAS ? path : '/'}>
      <Pagina />
    </Shell>
  )
}
