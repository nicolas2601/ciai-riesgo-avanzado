# 18. Revisión final del sitio publicado

Fecha: 2026-10-13, ~12:45 (hora local). Sitio: https://ciai.nicolasmoreno.site · API: https://ciai-api.nicolasmoreno.site. Herramienta: Playwright MCP (Chromium), curl. Capturas: `docs/figures/e2e2/`. Tiempo limitado: cobertura parcial, ver "No cubierto".

| # | severidad | dónde | qué pasa | evidencia | arreglo sugerido |
|---|---|---|---|---|---|
| 1 | alta | `/` y `/como-funciona` (texto de etiquetas "HECHO", "HIPÓTESIS") | 30 nodos de texto a 12px en desktop (4 en /como-funciona). Umbral de legibilidad 14px. | script `getComputedStyle` (medido en 1440 y 390) | Subir a 14px o más las etiquetas de estado. |
| 2 | media | `/` a 390px, tabla `.prob-tabla` | La tabla mide 536px dentro de un viewport de 390px. No hay scroll de página (scrollWidth 375), pero la tabla se corta; se ve fuera del ancho útil. | `docs/figures/e2e2/m390-home.png` | Envolver la tabla en contenedor con `overflow-x:auto` o pasar a tarjetas en móvil. |
| 3 | media | `/` y `/como-funciona` | Enlaces `.png` de diagramas a `?v=2` y `.html` interactivos: 200. Enlaces GitHub y SGC: 35/35 con 200 en la segunda pasada (una primera pasada dio 503/000 transitorios). | curl sobre 35 URL | Ninguno. Vigilar 503 transitorios de GitHub. |
| 4 | media | `/clusters` (API) | La clave del municipio es `municipio`; el contrato pedía `nombre`. La web lo consume tal cual. | `curl /api/v1/clusters` | Alinear el nombre con el contrato o documentarlo en Swagger. |
| 5 | baja | `/xyz-no-existe` | Responde HTTP 200 y muestra la página de Inicio ("soft 404"). | curl: 200; Playwright muestra Inicio | Página 404 real en el fallback de nginx o en la SPA. |
| 6 | baja | `/presentacion` | Cae a Inicio, como se anotó antes. | Playwright | Ruta o redirección explícita si se quiere. |
| 7 | baja | `/` y `/como-funciona` | Una imagen sin alt: `logo.svg` (en /como-funciona la única; en / una). | evaluate `img.alt` | `alt` vacío si es decorativo o descriptivo si no. |
| 8 | baja | API 422 en `/panel?mes=2026-13` | El mensaje expone el regex interno `^\d{4}-(0[1-9]|1[0-2])$`. | curl | Mensaje humano: "mes con formato AAAA-MM". |
| 9 | ok | `/basico` | Los Santos 2024-06 → Alto 89,4 %. Zapatoca 2026-09 → Bajo 47,4 %, real del mes siguiente "Sin dato" (correcto: no hay 2026-10 en el panel). | Playwright (texto del resultado) | — |
| 10 | ok | API | `/priorizacion` k=0 y k=88 → 422. Corte 2030-01 → 404 `month_not_found`. `/clasificar` zona 99999 → 404 `zone_not_found`; sin divipola → 422. | curl | — |

## Cubierto
- Rutas: `/`, `/como-funciona`, `/basico` (1 de 5 municipios, 2 de 3 meses), `/presentacion`, `/xyz-no-existe`, móvil 390x844 en `/`.
- Consola: 0 errores en las rutas probadas (ver punto 9 de la lista de pruebas anteriores).
- Enlaces: internos y externos de `/` y `/como-funciona`.
- API: `/health`, `/municipios`, `/clusters`, `/priorizacion` y `/panel` con cortes/meses válidos e inválidos, `/clasificar` con error.

## No cubierto (pendiente)
- `/medio`: hover/clic en municipios, tooltip, tarjeta lateral, teclado y tabla alternativa. Conteo de polígonos (el mapa es canvas; no se puede contar desde el DOM).
- `/avanzado`: k distintos (3/8/10) y cortes distintos.
- `/basico`: 3 municipios más y el mes fuera de rango en la UI (la API responde 404).
- Móvil 390 de `/basico`, `/medio`, `/avanzado`, `/pruebas`, `/metodologia`.
- Lighthouse (rendimiento y accesibilidad) de `/` y `/medio`.
- Swagger "Try it out" de `/clasificar`, `/priorizacion` y `/clusters` (sólo se probó la API con curl, no el botón).
