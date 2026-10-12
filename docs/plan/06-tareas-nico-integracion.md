# Tareas de Nico: integracion y plataforma

Lee: `docs/plan/02-entorno-dependencias.md`, `docs/research/04-mlops.md`, `skills/mlops-trazabilidad/SKILL.md`. Nico cubre el bloque que se atrase (ML o web).

## Tareas

### 1. H0: base del repo (hecho)
- [x] Repo privado, invitaciones a zquintero246 y Andrejulian21.
- [x] AGENTS.md, skills, plan, contrato API, diagramas.
- [x] `pyproject.toml` + `uv.lock` (239 paquetes resueltos en Python 3.13).

### 2. API (H1 a H4)
- [ ] `app/api/main.py` (FastAPI) con los endpoints de `03-contrato-api.md` y el mock (`model_version = "mock"`).
- [ ] Carga del bundle en `lifespan`; readiness falla si falta el bundle; nunca devolver una clase por defecto ante un fallo.
- [ ] Validacion de entrada (DIVIPOLA valido, hazard permitido, fecha), errores tipados, CORS especifico.
- [ ] `/metrics` lee de MLflow; `/zones` precalculado.
- [ ] Tests con `pytest` y el cliente de FastAPI.

### 3. Infra y despliegue (H2 y H5)
- [ ] `infra/Dockerfile.api`, `infra/docker-compose.yml` (API + web).
- [ ] Elegir el PC de despliegue y probar `docker compose up` en la hora 2 con el esqueleto.
- [ ] Cloudflare Tunnel; verificar la URL con `curl` a `/api/v1/health` antes de publicarla. Tunel con nombre si hay cuenta; si es rapido, anotar que la URL cambia al reiniciar.
- [ ] `.env.example` completo.

### 4. Verificacion (H5 y H6)
- [ ] Prueba de carga simple de `/predict` y `/zones/ranking`; registrar latencia p95 en el README (medida, no estimada).
- [ ] Recorrido end-to-end: URL publica, mapa, ranking, detalle, metricas.
- [ ] README final con instrucciones, resultados desde MLflow y limites.

### 5. H7: entrega
- [ ] Mensaje al grupo de WhatsApp "Perras" con el repo y el enlace de cada persona a su documento de tareas.

## Riesgos propios

| Riesgo | Mitigacion |
|---|---|
| Tunel cae durante la demostracion | Demo local de respaldo, capturas, URL anotada |
| Bundle incompatible con la API | Test de paridad offline vs API en CI |
| Invitaciones a colaboradores sin aceptar | Confirmar con ambos que aceptaron antes de H2 |
