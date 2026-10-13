# Web (Julian)

Andamiaje listo, sin pantallas todavia. Pila: bun + Vite + React 19 + TypeScript estricto, React Router, TanStack Query, MapLibre GL, Vitest.

```bash
bun install
bun dev              # http://localhost:5173
bun run typecheck && bun run test && bun run build
```

API mock (desde la raiz del repo): `uv run uvicorn app.api.main:app --reload` (http://localhost:8000). Copia `.env.example` a `.env.local` si la API esta en otra URL.

Los tipos de la API salen del contrato: `bun run gen:api` (con la API arriba) regenera `src/api/schema.d.ts`. No se edita a mano.

Carpetas en `src/`: `api/` (cliente y tipos), `components/`, `pages/`, `lib/` (utilidades), `styles/`, `test/`. Antes de tocar UI: crear `DESIGN.md` y leer `skills/web-app/SKILL.md`.
