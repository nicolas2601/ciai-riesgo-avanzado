# 17. Pruebas E2E del despliegue

Fecha: 2026-10-13. Objetivo: https://ciai.nicolasmoreno.site y https://ciai-api.nicolasmoreno.site. Capturas en `docs/figures/e2e/`. Dos pasadas: script Playwright (node) y Playwright MCP (navegador interactivo, sin scripts).

| Paso | Resultado | Evidencia |
|---|---|---|
| 1. Rutas `/`, `/basico`, `/medio`, `/avanzado`, `/metodologia`, `/presentacion` | OK: 200, sin errores de consola, sin 4xx/5xx | `home.png`, `basico.png`, `medio.png`, `avanzado.png`, `metodologia.png`, `presentacion.png` |
| 2. `/basico`: Bucaramanga + 2025-03 → Clasificar | OK (MCP y script): POST `/api/v1/clasificar` 200. Respuesta: clase "bajo", probabilidades 0,9306 / 0,0661 / 0,0032 | `mcp-basico-resultado.png`, `basico-resultado.png` |
| 3. `/medio`: 87 municipios en 3 grupos; al elegir municipio muestra su grupo | OK (MCP): 87 botones de mapa (grupo 0: 19, grupo 1: 66, grupo 2: 2). Al pulsar Los Santos el panel queda en "LOS SANTOS". Corrige el informe anterior: los 20 `svg circle` eran solo una parte; el resto son cuadrados y rombos. Lectura textual de la ficha de grupo no verificada en detalle. | `mcp-medio-seleccion.png` |
| 4. `/avanzado`: estático, aleatorio y PPO | OK (MCP): estático (LOS SANTOS, ZAPATOCA…), aleatorio (LOS SANTOS, BARBOSA…), PPO "Sin selección" con nota de runtime sin instalar. "Ejecutar agente" deshabilitado. Recompensa real "no disponible" en los tres. | `mcp-avanzado.png`, `avanzado-priorizacion.png` |
| 5. Texto "ejemplo", "Get started", "Count is", "localhost", "127.0.0.1" en HTML y bundle | OK: 0 coincidencias | script |
| 6. `/docs` de la API; "Try it out" + Execute en `/health` y `/municipios` | OK (MCP): `/health` 200 con `clusters: true`; `/municipios` 200 con 87 registros (primero Bucaramanga, 618548 hab.). | `docs.png` |
| Extra: 403 con User-Agent Python-urllib | Reproducido antes (error 1010 de Cloudflare). No repetido en esta pasada. | — |

Fallos reales: ninguno bloqueante. Limitaciones: (a) `/medio` no verifica el texto de la ficha de grupo al seleccionar; (b) `/clusters` y el "Ejecutar agente" no se probaron con ejecución real; (c) el User-Agent Python sigue bloqueado por Cloudflare.

## Redespliegue final (origin/main 0f5e3d9), 2026-10-13 12:06

| Paso | Resultado | Evidencia |
|---|---|---|
| Build | Falla en origin/main: `MapaSantander.tsx:31` usa `maplibregl.ExpressionSpecification`, que maplibre-gl 6.14.0 no exporta (tsc). Se compiló con un parche local (`as never`) no subido al repo. | — |
| Ficheros estáticos | OK: `/data/santander_municipios.geojson` 200 `application/geo+json`; `pruebas.json`, `inicio.json`, `panel-metadata.json` 200 `application/json`. Añadido el tipo geojson en `infra/web/nginx.conf`. | curl |
| CSP | No hay cabecera CSP ni en la web ni en la API. Los tiles de `basemaps.cartocdn.com` cargan (200). | curl, red |
| `/` | OK: sin errores de consola; sin peticiones fallidas | `final-home.png` |
| `/medio` | FALLA: 2 errores de consola "Worker failed to load" y `GET /assets/maplibre-gl-worker.mjs?v=6.14.0` → 404. El canvas del mapa existe (971x240) y los tiles cargan. El texto "Cargando los grupos…" no se resolvió en 15 s. Polígonos y tooltip NO verificados. | `final-medio.png` |
| `/avanzado`, `/pruebas`, `/metodologia`, `/basico` | OK: sin errores de consola | — |
