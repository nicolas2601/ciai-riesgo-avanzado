# Hackathon CIAI UTSmart 2026: riesgo sismico en Santander (categoria AVANZADO)

Equipo **Syntax error II** (UNAB): Nicolas Moreno, Julian Arteaga y Zabdiel Quintero. Reto oficial: con datos reales del Servicio Geologico Colombiano (SGC), analizar y clasificar el riesgo sismico de zonas de Santander. En Avanzado: cumplir los retos Basico (supervisado) y Medio (no supervisado) e integrar otra fuente oficial para una **priorizacion exploratoria de zonas con un agente de aprendizaje por refuerzo**.

**Plan vigente (2026-10-13): [docs/plan/08-reto-oficial-plan-4h.md](docs/plan/08-reto-oficial-plan-4h.md).** Desarrollo de 8:00 a 12:00; entrega a las 12:00 m.; presentacion a las 4:10 p. m. en 315A. El texto oficial, sin editar, esta en [docs/research/source/](docs/research/source/) y su resumen citado en [docs/research/08-enunciado-oficial.md](docs/research/08-enunciado-oficial.md). El diseno de RL esta en [docs/research/09-rl-diseno.md](docs/research/09-rl-diseno.md).

Roles y presentacion (la web React es el pitch): [docs/plan/10-roles-web-presentacion.md](docs/plan/10-roles-web-presentacion.md). Brechas e ideas con evidencia: [docs/research/12-brechas-e-ideas.md](docs/research/12-brechas-e-ideas.md).

Los documentos `00` a `07` de `docs/plan/` corresponden al plan anterior (amenazas varias, API y web desplegada): quedan **congelados**, no borrados.

## Estado

| Pieza | Estado |
|---|---|
| Plan oficial del reto (4 h), riesgos, opciones y rubrica | Listo (`docs/plan/08-reto-oficial-plan-4h.md`) |
| Plan anterior (API, contrato, tareas por persona) | Congelado (`docs/plan/00` a `07`) |
| Investigacion de datos, modelos, validacion y MLOps | Lista (`docs/research/`) |
| Contrato de la API (v0.2) y API mock con 30 tests | Listo; CI en verde |
| Web | Andamiaje con la plantilla de Vite + React; sin pantallas todavia |
| Entorno de RL, datos y demo (`uv sync --group reto --group demo`) | Listo y verificado; CPU |
| Datos, modelos y metricas | NO hechos: el reto empieza a las 8:00; no hay resultados todavia |
| Memoria compartida del equipo (Engram uts, MCP) | Operativa y temporal |

Los resultados se publican aqui cuando salgan de MLflow, nunca antes.

## Equipo y tareas

| Persona | Rol | Tareas | Diagrama |
|---|---|---|---|
| Zabdiel | ML | [04-tareas-zabdiel-ml.md](docs/plan/04-tareas-zabdiel-ml.md) | [flujo-ml](docs/flows/flujo-ml.html) |
| Julian | Web | [05-tareas-julian-web.md](docs/plan/05-tareas-julian-web.md) | [flujo-web](docs/flows/flujo-web.html) |
| Nico | Integracion y despliegue | [06-tareas-nico-integracion.md](docs/plan/06-tareas-nico-integracion.md) | [flujo-integracion](docs/flows/flujo-integracion.html) |

Hitos de las 5 h y reglas de apoyo: [01-roles-cronograma.md](docs/plan/01-roles-cronograma.md).

## Arquitectura del reto

**Un dataset, tres bloques** ([interactivo](docs/flows/reto-oficial.html))

![Reto oficial: un dataset, tres bloques](docs/flows/reto-oficial.png)

## Arquitectura y flujos del plan anterior (congelado)

Los diagramas son interactivos: descarga el HTML y abrelo en el navegador (busqueda, zoom, recorrido de rutas). Abajo, su captura.

**Arquitectura del sistema** ([interactivo](docs/flows/arquitectura-sistema.html))

![Arquitectura del sistema](docs/flows/arquitectura-sistema.png)

**Flujo del proyecto, del dato a la web** ([interactivo](docs/flows/flujo-proyecto.html))

![Flujo del proyecto](docs/flows/flujo-proyecto.png)

**Zabdiel: ML**

![Flujo de Zabdiel](docs/flows/flujo-ml.png)

**Julian: web**

![Flujo de Julian](docs/flows/flujo-web.png)

**Nico: integracion y despliegue**

![Flujo de Nico](docs/flows/flujo-integracion.png)

## Empezar

Requisitos: git, [Node.js](https://nodejs.org) 18+, [bun](https://bun.sh) y [uv](https://docs.astral.sh/uv/). Linux y macOS: `curl -fsSL https://bun.sh/install | bash` y `curl -LsSf https://astral.sh/uv/install.sh | sh`; para Windows, ver `docs/plan/02-entorno-dependencias.md`.

```bash
git clone https://github.com/nicolas2601/ciai-riesgo-avanzado && cd ciai-riesgo-avanzado

# API mock (http://localhost:8000, is_mock = true)
uv sync --group dev
uv run pytest app/api -q
uv run uvicorn app.api.main:app --reload

# Web (http://localhost:5173)
cd app/web && bun install && bun dev
```

Detalle del web (scripts, estructura, tipos generados): [app/web/README.md](app/web/README.md).

## Memoria compartida: Engram uts (MCP)

Una sola memoria para los tres y sus agentes. Es temporal: se elimina al terminar el hackathon. La contrasena NO esta en el repo: la da Nico en privado.

- URL: `https://engram-uts.nicolasmoreno.site/mcp`
- Claude Code: `claude mcp add --transport http engram-uts https://engram-uts.nicolasmoreno.site/mcp`, luego `/mcp`, elegir `engram-uts` y `Authenticate`.
- opencode: en `opencode.json`, dentro de `mcp`: `"engram-uts": { "type": "remote", "url": "https://engram-uts.nicolasmoreno.site/mcp", "oauth": {}, "enabled": true }`, y `opencode mcp auth engram-uts`.
- Proyecto unico: `ciai-riesgo`. Reglas, prompts de arranque y trabajo entre sesiones y computadores: seccion Engram uts de [AGENTS.md](AGENTS.md) y [07-engram-uts.md](docs/plan/07-engram-uts.md).

## Herramientas para agentes

- MCP de Playwright: `claude mcp add playwright -- npx @playwright/mcp@latest` (opencode: `"playwright": { "type": "local", "command": ["npx", "-y", "@playwright/mcp@latest"], "enabled": true }`) y `npx playwright install chromium`.
- Skills recomendadas, con su comando de instalacion y la advertencia de revisarlas antes: [AGENTS.md](AGENTS.md). Skills propias del repo en `skills/`.

## Decisiones clave (con evidencia en docs/research)

- Etiqueta real: emergencias UNGRD 2019-2025 (2 641 eventos en Santander), panel municipio x mes. Las coordenadas de la fuente son inservibles y el DIVIPOLA de 2025 esta corrupto, por eso la unidad es el municipio (87).
- Modelos: baseline, GBDT, red PyTorch propia, TabPFN opcional (pesos no comerciales); validacion por bloques de municipios y particion temporal.
- Incertidumbre: calibracion, conjunto de prediccion con cobertura empirica y abstencion cuando no hay soporte.
- Los tres niveles son frecuencia relativa de emergencias reportadas, no severidad ni alerta oficial.
- Contrato ML-web ejecutable: `app/api/tests`; cualquier cambio se avisa a los tres.

## Estructura

| Ruta | Contenido |
|---|---|
| `app/api/` | API FastAPI y mock del contrato, con tests |
| `app/web/` | Web: bun + Vite + React + TypeScript |
| `ml/` | Notebooks, codigo y configuracion de ML (`notebooks/`, `src/`, `configs/`) |
| `infra/` | Docker, tunel y despliegue |
| `data/` | Datos locales; no se versionan |
| `docs/plan/` | Plan, requisitos, entorno, contrato API, tareas y guia de Engram |
| `docs/research/` | Investigacion de datos, modelos, validacion, MLOps y estado del arte |
| `docs/flows/` | Diagramas Archify (HTML interactivo y PNG) |
| `skills/` | Instrucciones por area: ML, web, MLOps, Engram |
| `AGENTS.md` | Reglas del equipo y de los agentes de IA |

## Reglas de trabajo

- Commits convencionales, pequenos y atomicos; sin secretos en git (`.env` ignorado, `.env.example` versionado).
- Toda cifra que se publique sale de una corrida de MLflow, no de una transcripcion.
- Revision cruzada antes de congelar un contrato, un modelo o un resultado.
- Python 3.11 a 3.13 con `uv`; web con `bun`; documentacion en espanol.

Documentos de referencia: [requisitos y evidencia](docs/plan/00-requisitos-entregables.md), [entorno y dependencias](docs/plan/02-entorno-dependencias.md), [contrato de la API](docs/plan/03-contrato-api.md), [datasets](docs/research/01-datasets.md), [datos de Colombia](docs/research/06-datos-colombia.md).
