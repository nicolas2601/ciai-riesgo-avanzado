# Tareas de Julian: web

Lider web. Lee antes: `docs/plan/03-contrato-api.md` (tu unica frontera con ML), `skills/web-app/SKILL.md`, `docs/research/05-ideas-creativas.md`. Trabajas desde el minuto 0 contra el mock; no esperes al modelo.

## Pila propuesta (decides tu)

bun + Vite + React + TypeScript estricto, MapLibre GL, TanStack Query, cliente tipado generado desde el OpenAPI de la API. Si ya tienes una pila que dominas, usala: lo que importa es el contrato.

```bash
cd app/web && bun install && bun dev
```

## Tareas

### 1. Esqueleto y mock (H1 a H2)
- [ ] Proyecto en `app/web/`, variable `VITE_API_URL`.
- [ ] Cliente tipado sobre el contrato; un mock local (MSW o JSON estatico) con las formas de `03`.
- [ ] Layout, rutas y estados de carga/error. Despliegue del esqueleto en la hora 2 (coordinar con Nico).

### 2. Vistas (H2 a H4)
- [ ] Mapa de Santander por municipio coloreado por nivel de riesgo. Si no hay poligonos, circulos en el centroide proporcionales al score. Selector de amenaza (`hazard`).
- [ ] Ranking de municipios (`/zones/ranking`) con score, nivel e intervalo.
- [ ] Detalle de municipio: score, intervalo, factores SHAP, serie reciente, estado de abstencion.
- [ ] Pagina de metricas (`/metrics`): lo que devuelva la API, incluyendo baseline y calibracion. Nada escrito a mano.
- [ ] Pagina "como usarlo": que significa cada nivel, que NO significa (frecuencia relativa de emergencias reportadas, no severidad ni alerta oficial), limites y fuentes con licencia.

### 3. Pulido y requisitos de UI (H4 a H5)
- [ ] Mostrar siempre incertidumbre junto al score y `model_version` / `data_version` en el pie.
- [ ] Idea diferenciadora 1 de `05`: "el mapa sabe cuando no sabe" (abstencion, municipios sin datos marcados distinto de "bajo").
- [ ] Accesibilidad: el nivel no depende solo del color (texto o icono), foco visible, `prefers-reduced-motion`.
- [ ] Responsive y prueba en el navegador a 1440 y 390 de ancho.

### 4. Integracion (H4)
- [ ] Cambiar `VITE_API_URL` del mock a la API real; comprobar `model_version != "mock"` en el pie.
- [ ] Acordar con Nico el origen CORS y la URL publica del tunel.

## Definition of Done

Todas las vistas funcionan contra la API real, build de produccion sin errores (`bun run build`), sin cifras escritas a mano, estados vacios y de error cubiertos.

## Si te atrasas

Recorta: animaciones, idea diferenciadora 2 (what-if). No recortes: mapa, ranking, detalle con intervalo, metricas, "como usarlo".
