---
name: web-app
description: Reglas del prototipo web (bun, mapa, ranking, explicabilidad). Usar antes de tocar app/web.
---

# Web app

1. Consumir solo el contrato `docs/plan/03-contrato-api.md`; empezar contra el mock.
2. Vistas: mapa de riesgo por celda, ranking, detalle de zona (score, intervalo, factores), metricas, como usarlo.
3. Mostrar la incertidumbre siempre junto al score; nunca un nivel sin intervalo.
4. Mostrar `model_version` y `data_version` en la UI.
5. Metricas de la pagina de metricas vienen de `/metrics`, no se escriben a mano.
6. Accesibilidad: contraste, foco visible, no depender solo del color para el nivel (usar texto/icono).
7. Motion sobrio: respetar `prefers-reduced-motion`; transiciones cortas.
8. TypeScript estricto, componentes pequenos, cliente tipado desde OpenAPI.
