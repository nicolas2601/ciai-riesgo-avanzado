# CIAI: priorizacion de zonas de riesgo (categoria AVANZADO)

Solucion de Machine Learning que estima y prioriza el riesgo de emergencias por municipio de Santander, con incertidumbre, explicabilidad, API y prototipo web.

Estado: planificacion y investigacion completas; implementacion en curso. Los resultados se publican aqui cuando salgan de MLflow, nunca antes.

## Donde esta cada cosa

| Documento | Contenido |
|---|---|
| `AGENTS.md` | Reglas del equipo y de los agentes de IA |
| `docs/plan/00-requisitos-entregables.md` | Los 12 requisitos AVANZADO y su evidencia |
| `docs/plan/01-roles-cronograma.md` | Roles, hitos y flujo de cada persona (5 h) |
| `docs/plan/02-entorno-dependencias.md` | uv, PyTorch, bun, cluster UNABIA, despliegue |
| `docs/plan/03-contrato-api.md` | Contrato entre ML y web |
| `docs/plan/04-tareas-zabdiel-ml.md` | Tareas de ML |
| `docs/plan/05-tareas-julian-web.md` | Tareas de la web |
| `docs/plan/06-tareas-nico-integracion.md` | Tareas de integracion y despliegue |
| `docs/research/` | Datasets, modelos, validacion, MLOps, ideas, datos de Colombia, estado del arte |
| `docs/flows/*.html` | Diagramas interactivos (abrir en el navegador) |
| `skills/` | Instrucciones por area (ML, web, MLOps) |

## Decisiones clave (con evidencia en docs/research)

- Etiqueta real: emergencias UNGRD 2019-2025, panel municipio x mes. Las coordenadas de la fuente son inservibles, por eso la unidad es el municipio (DIVIPOLA).
- Modelos: baseline, GBDT, red PyTorch propia, TabPFN opcional; validacion por bloques de municipios y particion temporal.
- Incertidumbre: calibracion y cobertura empirica; el sistema se abstiene cuando no hay soporte.
- Los tres niveles son frecuencia relativa de emergencias reportadas, no severidad ni alerta oficial.

## Inicio rapido

```bash
uv sync                                     # entorno Python
uv run uvicorn app.api.main:app --reload    # API (cuando exista)
cd app/web && bun install && bun dev        # web (cuando exista)
```

Fuentes de datos y licencias: ver `docs/research/01-datasets.md` y `06-datos-colombia.md`.
