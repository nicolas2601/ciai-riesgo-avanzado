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
