# Datos y cluster UNABIA: guia para Zabdiel (y su IA)

Pensada para que un agente de IA pueda leerla y trabajar sin preguntar. Las afirmaciones llevan su origen: HECHO (verificado el 2026-10-13), INFERENCIA o SUPOSICION.

## 1. Datos disponibles

| Archivo | Que es | Origen |
|---|---|---|
| `data/sgc/new_<anio>.csv.gz` | Catalogo SGC de Santander, sistema nuevo (2018-03 en adelante) | HECHO: POST a `Consulta_Experta_Seiscomp/consulta_sismo.php` |
| `data/sgc/old_<anio>.csv.gz` | Catalogo SGC de Santander, sistema antiguo (1993-06 a 2018-02) | HECHO: POST a `Consulta_Experta/consulsismo3.php` |
| `data/sgc/provenance.json` | URL, filtros, fecha de descarga UTC, filas y sha256 de cada archivo | HECHO |
| `scripts/sgc_download.py` | Reproduce la descarga completa | HECHO |

Reproducir: `uv run --group reto python scripts/sgc_download.py` (los CSV crudos caen en `data/raw/sgc/`, que no se versiona).

Columnas sin encabezado en los CSV (el orden difiere entre sistemas):
- Sistema nuevo (17 columnas, HTML): fecha-hora UTC, lat, lon, prof_km, mag, tipo_mag, fases, rms, gap, err_lat, err_lon, err_prof, region (`Municipio - Santander, Colombia`), 3 vacias, estado.
- Sistema antiguo (16 columnas, export Excel): fecha, hora UTC, lat, lon, prof_km, Ml, Mw, departamento, municipio (ej. `LOS_SANTOS`), fases, rms, gap, err_lat, err_lon, err_prof, estado.

Advertencias de modelado (no las ignores):
1. HECHO: el HTML del sistema antiguo pagina a 35 filas; por eso el script usa el export Excel del propio SGC y verifica que las filas leidas igualen `tregistros` (marzo de 2015: 681). Los conteos de los dos sistemas no son comparables a simple vista; lo que cambio entre ellos (deteccion, red o metodo) es una hipotesis, no un hecho: comprueba con una magnitud minima de completitud y entrena dentro de un periodo homogeneo.
2. INFERENCIA: el Nido de Bucaramanga (Los Santos, prof ~150 km) domina el catalogo. Si el top-K por municipio casi no cambia entre meses, el agente aprende una constante. Aplicar el gate de degeneracion de `docs/plan/09-decisiones-dos-vistas.md` (medido solo con entrenamiento).
3. SUPOSICION: el municipio de los sistemas nuevo y antiguo usa nombres distintos (con tildes y espacios vs `MAYUSCULAS_CON_GUION`); hay que normalizar antes de unir con DANE (poblacion municipal 1985-2042, xlsx de dane.gov.co, retrospectiva y declarada).

## 2. Contrato para el entorno de RL

Estado por (municipio, mes de corte): variables solo con informacion anterior al corte. Accion: elegir K=5 municipios distintos con mascara. Recompensa: solo al final del episodio, con la actividad observada del mes siguiente. Detalle y justificacion en `docs/research/09-rl-diseno.md`. Algoritmo: MaskablePPO de `sb3-contrib` (actor-critico con dos MLP).

## 3. Hace falta el cluster?

INFERENCIA: no para el RL. El estado es de 87 municipios por unas 20 variables; MaskablePPO con MLP pequenos entrena en CPU en minutos. El cluster solo vale la pena si se agrega una red grande (por ejemplo secuencias largas) o un barrido de muchas semillas.

## 4. Cluster UNABIA (si se decide usarlo)

Datos HECHOS en la sesion del 2026-09-16/17 (pueden haber cambiado; verifica con `nvidia-smi` y `df -h ~/work`):
- Plataforma: https://unabia.unab.edu.co (Facultad de Ingenieria UNAB, contacto: profesor Alfredo Diaz, adiaz@unab.edu.co). Cada persona entra con su propia cuenta; la de Nico es personal y NO se comparte. Si Zabdiel no tiene usuario, pedirlo al profesor.
- Pod JupyterHub: 2 GPU NVIDIA RTX PRO 4000 Blackwell de 24 GB, Xeon 24 nucleos / 48 hilos, 123 GiB de RAM, Python 3.13, PyTorch con CUDA.
- Persistencia: solo `~/work` (NFS, 40 TB). El disco `/` es efimero (se pierde al reiniciar el pod).
- Servicios internos: MLflow en `mlflow.unabia.unab.edu.co`, Postgres, Redis, Jenkins, entre otros.

Flujo recomendado:
1. Abrir la terminal desde JupyterHub: `/hub/user-redirect/terminals/1`.
2. `cd ~/work && git clone https://github.com/nicolas2601/ciai-riesgo-avanzado && cd ciai-riesgo-avanzado` (el repo es privado: usar un token de GitHub propio, nunca pegarlo en el repo).
3. Instalar uv y sincronizar: `curl -LsSf https://astral.sh/uv/install.sh | sh && uv sync --group reto`.
4. Entrenar: `uv run python -m ml.<modulo>` (el modulo de RL lo define Zabdiel).
5. Registrar corridas en MLflow y traer de vuelta solo el checkpoint y las metricas (`git add` de archivos pequenos).

Trampas conocidas (HECHO, del probe del 2026-09-17):
- `/dev/shm` es de 67 MB: usar `num_workers=0` en DataLoader.
- Nunca `pip install torch` en el entorno base (ya lo dejo en CPU una vez); usar un entorno propio.
- Las GPU son compartidas: mirar `nvidia-smi` antes de lanzar.
- Los archivos viejos de `~/work` pueden estar bloqueados por permisos NFS; crear directorios nuevos.

## 5. Para la demo en vivo

El checkpoint se ejecuta en el computador del equipo (puente local: `uv run uvicorn ml.serve:app` o `uv run python -m ml.select --cutoff YYYY-MM`), no en el cluster, para no depender de la red durante la presentacion. Ver `docs/plan/10-roles-web-presentacion.md`, seccion 6.
