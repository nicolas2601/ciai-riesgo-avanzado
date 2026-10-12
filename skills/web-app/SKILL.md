---
name: web-app
description: Reglas del prototipo web (bun, mapa, ranking, explicabilidad). Usar antes de tocar app/web.
---

# Web app

1. Consumir solo el contrato `docs/plan/03-contrato-api.md`; empezar contra el mock.
2. Vistas: mapa de riesgo por municipio, ranking, detalle de zona (probabilidades, conjunto de prediccion, factores), metricas, como usarlo.
3. Mostrar la incertidumbre siempre junto al nivel (conjunto de prediccion y abstencion con motivo); nunca un nivel sin ella.
4. Mostrar el snapshot (`model_version`, `data_version`, `target_month`, `feature_cutoff`) en la UI y un banner de demostracion mientras `is_mock` sea true.
5. Metricas de la pagina de metricas vienen de `/metrics`, no se escriben a mano.
6. Accesibilidad: contraste, foco visible, no depender solo del color para el nivel (usar texto/icono).
7. Motion sobrio: respetar `prefers-reduced-motion`; transiciones cortas.
8. TypeScript estricto, componentes pequenos, cliente tipado desde OpenAPI.
