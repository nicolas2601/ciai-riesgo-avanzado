# Web (Julian)

Plantilla oficial de Vite + React + TypeScript (`bun create vite --template react-ts`) con las dependencias del proyecto y la estructura de carpetas. Sin pantallas todavia: `src/App.tsx` es el ejemplo de la plantilla.

Pila instalada: React 19, React Router, TanStack Query, MapLibre GL, Vitest (jsdom + Testing Library), oxlint, `openapi-typescript`.

```bash
bun install
bun dev                 # http://localhost:5173
bun run build           # tsc -b + vite build
bun run lint            # oxlint
bun run test            # vitest (pasa sin tests)
```

API mock, desde la raiz del repo: `uv run uvicorn app.api.main:app --reload` (http://localhost:8000). Si la API corre en otra URL, copia `.env.example` a `.env.local` y cambia `VITE_API_URL`.

## Estructura de `src/`

| Carpeta | Para que |
|---|---|
| `api/` | Cliente y tipos de la API. `schema.d.ts` es generado: `bun run gen:api` (con la API arriba) lo regenera; no se edita a mano |
| `components/` | Componentes reutilizables |
| `pages/` | Una carpeta o archivo por ruta |
| `lib/` | Utilidades |
| `styles/` | Estilos y tokens |
| `test/` | Configuracion de tests (`setup.ts`) |

## Notas

- MapLibre arranca su propio worker: `vite.config.ts` excluye `maplibre-gl` del pre-empaquetado; sin eso el mapa sale en blanco con "Worker failed to load".
- TypeScript va en la version de la plantilla (6.x): TypeScript 7 rompe `openapi-typescript`.
- Antes de tocar UI: crear `DESIGN.md` y leer `skills/web-app/SKILL.md`. El contrato con ML esta en `docs/plan/03-contrato-api.md`.
