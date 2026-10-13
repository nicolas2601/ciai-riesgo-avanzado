# 17. Pruebas E2E del despliegue (Playwright)

Fecha: 2026-10-13. Objetivo: https://ciai.nicolasmoreno.site y https://ciai-api.nicolasmoreno.site. Navegador: Chromium headless vía Playwright. Capturas en `docs/figures/e2e/`.

| Paso | Resultado | Evidencia |
|---|---|---|
| 1. Rutas `/`, `/basico`, `/medio`, `/avanzado`, `/metodologia`, `/presentacion` | OK: HTTP 200, sin errores de consola, sin peticiones fallidas ni 4xx/5xx | `home.png`, `basico.png`, `medio.png`, `avanzado.png`, `metodologia.png`, `presentacion.png` |
| 2. `/basico`: Bucaramanga + 2025-03 → Clasificar | OK: POST `/api/v1/clasificar` 200; UI muestra clase "bajo" y probabilidades; respuesta directa: `{"clase":"bajo","probabilidades":{"bajo":0.9306,"medio":0.0661,"alto":0.0032},"version":"c770e486d631","exploratorio":true}` | `basico-resultado.png` |
| 3. `/medio`: mapa con 87 puntos en 3 grupos; selección de municipio muestra grupo | PARCIAL: la leyenda lista Grupo 0 (19), Grupo 1 (66), Grupo 2 (2) = 87. El DOM solo contiene 20 `svg circle`; no confirmé 87 puntos pintados. No probé la selección de municipio en el mapa. | `medio-mapa.png` |
| 4. `/avanzado`: GET `/priorizacion` con estático, aleatorio y PPO | OK en red: GET 200 (corte 2024-06, k=5). UI muestra "Ranking estático (línea base)" y nota; "Ejecutar agente" deshabilitado. No verifiqué visualmente aleatorio ni PPO vacío por separado. | `avanzado-priorizacion.png` |
| 5. Texto "ejemplo", "Get started", "Count is", "localhost", "127.0.0.1" en HTML y bundle JS | OK: 0 coincidencias | script (bundle `/assets/index-D1s5xyd6.js`) |
| 6. `/docs` de la API abre; "Try it out" de `/health` y `/municipios` | PARCIAL: `/docs` carga (título Swagger UI, 6 operaciones, bloques de `health` y `municipios` presentes). No pulsé "Try it out" ni ejecuté la petición. | `docs.png` |
| Extra: 403 con User-Agent Python-urllib | Reproducido antes con urllib (403, error 1010 de Cloudflare). No repetido en esta prueba. | — |

Fallos reales encontrados: ninguno bloqueante. Limitaciones: (a) el mapa de `/medio` tiene 20 círculos en el DOM frente a 87 esperados; (b) no se probó la interacción de "Try it out" en Swagger.
