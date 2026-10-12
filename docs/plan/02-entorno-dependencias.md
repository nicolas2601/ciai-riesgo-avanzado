# Entorno y dependencias

## Verificado en la maquina de Nico (2026-10-12)

| Herramienta | Version | Estado |
|---|---|---|
| bun | 1.3.12 | instalado |
| uv | 0.9.11 | instalado |
| node | 26.2.0 | instalado |
| cloudflared | presente en /usr/bin | instalado |
| docker | presente | instalado |
| python del sistema | 3.14.5 | NO usar para el proyecto (wheels de torch/geo no garantizados) |
| GPU local | driver NVIDIA no responde | entrenar en el cluster |

Python del proyecto: 3.11-3.13 (el cluster usa 3.13). Lo fija `pyproject.toml`; `uv` descarga el interprete.

## Cluster UNABIA (dato de 2026-09-17, re-verificar con `nvidia-smi`)

- 2x RTX PRO 4000 Blackwell 24 GB, 123 GiB RAM, torch 2.11.0+cu128 con CUDA en el entorno base.
- `~/work` es NFS persistente; `/` es efimero. Todo el trabajo va en `~/work`.
- GPUs compartidas: `nvidia-smi` antes de entrenar.
- `/dev/shm` ~67 MB: `num_workers=0` en DataLoader.
- NUNCA `pip install torch` en el entorno base (ya lo rompio una vez a CPU). Crear entorno propio con `uv venv` y `--system-site-packages` solo si se reutiliza el torch del cluster, o instalar torch dentro del entorno nuevo con el indice correcto.
- Servicios: JupyterHub, MLflow (`mlflow.unabia.unab.edu.co`), Postgres, Redis.
- Archivos viejos del NFS pueden pertenecer a uid 65534 y no ser escribibles: usar directorios nuevos.

Fallback si el cluster no responde: modelos tabulares (GBDT) corren en CPU; la red PyTorch propia es pequena y entrena en CPU o en Colab/Kaggle.

## Python (ML + API)

Gestion con `uv`. Dependencias propuestas (versiones minimas; fijar con `uv lock`):

| Grupo | Paquetes |
|---|---|
| datos | pandas, polars, pyarrow, numpy |
| geo | geopandas, shapely, pyproj, rasterio, h3 |
| ML | scikit-learn, lightgbm, xgboost, catboost, optuna |
| deep learning | torch (indice CUDA en el cluster, CPU en local), pytorch-lightning |
| incertidumbre/explicabilidad | shap, mapie |
| MLOps | mlflow, dvc, hydra-core, evidently |
| serving | fastapi, uvicorn, pydantic, onnx, onnxruntime |
| notebooks | jupyterlab, ipykernel, matplotlib, plotly |
| calidad | pytest, ruff, pandera |

Opcional segun decision de `docs/research/02-modelos-sota.md`: torch-geometric (GNN espacio-temporal).

PyTorch: instalar siempre con el selector oficial (https://pytorch.org/get-started/locally/). En local sin GPU: build CPU. En el cluster: reutilizar el torch existente, no reinstalar.

## Web (bun)

```bash
cd app/web
bun install
bun dev
bun run build
```

Pila propuesta: Vite + React + TypeScript, MapLibre GL (mapa), deck.gl (capa de celdas H3), TanStack Query (cliente), cliente tipado generado desde OpenAPI. Decision final del lider web, respetando `skills/web-app/SKILL.md`.

## Despliegue

1. PC con VRAM adecuada (a definir) ejecuta `docker compose up` (API + web).
2. Cloudflare Tunnel expone el servicio:
   ```bash
   cloudflared tunnel --url http://localhost:8080   # tunel rapido, URL temporal
   ```
   Tunel con nombre y dominio propio si hay cuenta Cloudflare disponible (mas estable para el jurado).
3. Healthcheck en `/api/v1/health`; la URL final se verifica con `curl` antes de publicarla.

Riesgo: el tunel rapido cambia de URL al reiniciar. Mitigacion: tunel con nombre, o registrar la URL vigente en el README en cada reinicio.

## Variables de entorno

`.env.example` documenta cada una; `.env` esta en `.gitignore`. Nada de secretos en git.
