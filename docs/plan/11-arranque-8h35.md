# Arranque 08:35: próximos 90 minutos, sin volver a planificar

Fecha: 2026-10-13, Colombia. Ventana: **08:35–10:05**; entrega oficial sigue **12:00**. Este documento operacionaliza 08–10, no los modifica. **Nico: datos/Medio/integración; Zabdiel: ML+RL; Julián: React y pitch en web.**

## Estado verificado y límites

- **HECHO:** `git pull --rebase` ejecutado; repo actualizado. `ml/src/` no tenía archivos de implementación al inspeccionar este arranque; no hay CLI real de training/inferencia que pueda prometerse aquí.
- **HECHO:** imports locales pasan: Gymnasium1.4.0, `sb3_contrib.MaskablePPO`, pandas3.0.6, torch2.14.1+cpu. Esto prueba entorno, **no** entrenamiento real ni datos disponibles.
- **HECHO:** React/Vite/bun existen; scripts `dev`, `build`, `lint`, `test` leídos en package.json. Tests web pueden pasar sin casos; no es evidencia funcional por sí sola.
- **HECHO:** UTS reclama prueba/descarga SGC; esta sesión no duplica consultas masivas. Coordinar `ciai/datos/sgc` en Engram uts. Aquí ese MCP no está disponible: coordinación realizada por mensaje a UTS; no fingir escritura en servidor compartido.
- **PROPUESTA:** un tranche SGC de meses completos basta para empezar pipeline y validar formas; no declarar modelo territorial validado con muestra mínima.
- **SUPOSICIÓN:** K=5 es capacidad de demo, no dato de autoridad. Tiene que haber ≥5 municipios elegibles; si no, falla gate, no elegir repetidos.

## 1. Acciones por persona, hora y criterio de hecho

| Hora | Nico: datos/Medio/integración | Zabdiel: ML+RL | Julián: web | Hecho / handoff |
|---|---|---|---|---|
| 08:35–08:45 | Reclamar/trabajar con UTS en SGC; recibir primer export real y metadatos; no abrir otra descarga paralela. DANE como segunda fuente | Ejecutar smoke de entorno/máscara de sección3, fijar features/target/K; escribir entorno y tests en su área | Levantar React, leer contrato de sección4; fixtures con marca visible, fuentes/métricas null | Imports+smoke pasan; esquema común firmado. «Sin datos» visible si export aún no llega |
| 08:45–09:00 | Unificar tranche, UTC/unidades/tipos, dedup, DIVIPOLA+fuentes; CSV/diccionario con ≥20 covariables reales | Gate **solo train**: clases, cobertura, positivos, degeneración; congelar ventanas/splits/reward. Preparar supervisado y policy | Mapa/grupos/priorización leen schema; no usar API mock vieja como modelo sísmico | CSV v0 con periodos completos, dict+hash+filtros; test temporal reservado. Si no, reportar bloqueo y recortar descarga |
| 09:00–09:20 | Comprobar fechas/joins y export a web. **Medio solo si datos/panel/export pasan gate**: KMeans mínimo, revisión de Zabdiel | Entrenar Básico real y arrancar MaskablePPO real CPU; guardar config/curvas/checkpoint fuera de git | Reemplazar fixtures por bundle real conforme llegue; preparar `/presentacion` | Modelos propios realmente entrenados y artifacts identificados. Si gate datos falla, Zabdiel asume Medio simple cuando reciba panel |
| 09:20–09:40 | Integrar checkpoint→selección→JSON→React; pruebas mismo cutoff/mapping/hash. No construir infraestructura extra | Evaluar baseline aleatorio, estático y supervisado en validación; masks al predecir; congela candidata | Resultados/limitaciones reales; replay explícito, control K fijo; modo pitch | Camino end-to-end mínimo con evidencia, aunque RL no gane. Nada de scores sintéticos |
| 09:40–10:05 | Smoke demo live por consola/carga de resultado o servicio fino; export/coherencia de snapshots | Policy congelada, evaluación temporal y soporte; no reentrenar usando test. Sostener demo de aprendizaje real | Navegar pitch con los tres; build y prueba de lectura/inferencia local | **10:05** flujo ejecutable y lista concreta de fallos. Fallback web se decide10:45; entrega anticipada11:45 |

**Si hoy no hay tabla:** no esperar quietos. Zabdiel escribe/testea entorno sobre fixtures; Julián UI sobre fixtures; Nico+UTS resuelven export real. Fixtures no se usan como entrenamiento final ni evidencia oficial.

### Comandos que sí existen hoy

Desde raíz del repo en cada máquina; sustituyan ruta local al clonar:

```bash
cd /home/nicolas/work/ciai-riesgo
git pull --rebase
uv sync --group dev --group dl --group reto --group demo
uv run python -c "import gymnasium, torch; from sb3_contrib import MaskablePPO; print('RL runtime ready')"
uv run pytest ml -q
uv run ruff check ml
```

`pytest ml` sin tests retorna falta de colección: crear casos antes de decir que RL pasa. Ningún test viejo de `app/api` prueba el agente nuevo. No invocar módulos `ml.train`, `ml.serve` o `ml.select` antes de que sus dueños los implementen.

Julián:

```bash
cd /home/nicolas/work/ciai-riesgo/app/web
bun install
bun run dev
# In another terminal, after each integration:
bun run build
bun run lint
bun run test
```

Nico, después de recibir tranche/export oficial:

```bash
cd /home/nicolas/work/ciai-riesgo
mkdir -p data/raw/sgc data/raw/dane data/processed artifacts
uv run python -c "from pathlib import Path; print(*Path('data/raw/sgc').glob('*'), sep='\n')"
sha256sum data/raw/sgc/*
```

No iniciar descarga en esas carpetas si UTS ya tiene tranche equivalente. `artifacts/` no está ignorado globalmente: checkpoints, fixtures, datos y salidas grandes **no** se agregan a git; acordar storage/rutas antes de guardar. `data/raw/` y `data/processed/` sí están ignorados.

## 2. Contrato mínimo dataset→ML

**PROPUESTA a congelar a08:45:** una fila por municipio/cutoff; CSV limpio integrado + diccionario separado. Metadata no sustituye ≥20 features.

| Columna/grupo | Tipo / regla |
|---|---|
| `zone_id` | string DIVIPOLA5, catálogo validado, mismo orden en todo rollout |
| `feature_cutoff` | fecha/instante normalizado, periodo cerrado; features ≤cutoff |
| `target_start`, `target_end` | ventana siguiente semiabierta `[start,end)`; misma para label/reward/baselines |
| `source_status` | `official` o `fixture`; entrenamiento final/export oficial exige `official` |
| `data_version`, `source_period` | snapshot/hash y origen de consulta SGC; provenance JSON con URLs/fecha/filtros |
| ≥20 columnas `feature_names` | numéricas, orden congelado y diccionario fuente/tipo/unidad/justificación; imputación train-only |
| `target_level` | low/medium/high de **ventana futura**, separado de features |
| `future_activity` | 0/1 de al menos un evento M≥3 en ventana futura completa; solo reward/label, nunca obs/info intermedio |
| `population` | fuente DANE real con año/tipo/provenance; si ausente, reward sin ponderación, pero segunda fuente oficial sigue requerida |
| `eligible` | cobertura/features habilitantes, no función del outcome futuro |

Features candidatas inmediatas: conteos1/3/12meses y M≥3/M≥4, magnitudes previas por tipo, profundidad/media/dispersión/bandas, recencia, calidad RMS/gap/fases si existen, centroides y exposición DANE. Lista justificada detallada en [09](../research/09-rl-diseno.md). Si faltan veinte reales, el gate falla: no rellenar con ruido/IDs ni contar target/máscara como features.

**Hecho de panel:** claves únicas; no duplicados; tipos/units/fechas coherentes; meses sin seguimiento excluidos, no ceros; datos sin eventos se distinguen de datos sin cobertura. Si cambia horizonte mensual→anual, cambiar **todo** el contrato y purgar solapamientos.

**Zabdiel recibe tres objetos separados:** `X[cutoff,municipality,feature]`, outcomes futuros `Y[cutoff,municipality]` y metadatos/mapping. Train/val/test por cutoff; outcomes aislados del actor. El umbral provisional no demuestra completitud uniforme; declarar registro y sensibilidad por tipo/red.

## 3. Entorno RL mínimo y arranque con fixtures

- **Estado:** features de todos los municipios al mismo corte, seleccionados y presupuesto restante; features no cambian durante picks.
- **Acción:** `Discrete(N)` elegir municipio; máscara impide repetición y unidades no elegibles. **K=5**, sin reemplazo.
- **Transición:** marcar elegido, decrementar presupuesto; no inventar intervención que cambie sismos.
- **Reward:** cero antes de quinto pick; terminal `sum(w[z]*future_activity[z] for z in selected)/5`. `w` de población real con escala train congelada; si no pasa gate, usar `w=1`, sin fingir exposición.
- **Fin:** `terminated=True` al completarK; evaluación también usa máscaras. Future outcomes solo se conocen después de cerrar selección.
- **Algoritmo:** MaskablePPO, inicializado nuevo, CPU. Actor probabilities son acciones, no probabilidad de sismo.

**Smoke ejecutable HOY** (solo shapes/lifecycle/entrenamiento de prueba; no crea archivos ni checkpoint oficial):

```bash
uv run python - <<'PY'
import gymnasium as gym
import numpy as np
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks

class FixtureEnv(gym.Env):
    """NOT OFFICIAL DATA: validates only shapes, masks and terminal reward."""

    def __init__(self):
        self.n, self.k = 6, 5
        self.action_space = gym.spaces.Discrete(self.n)
        self.observation_space = gym.spaces.Box(0, 1, shape=(127,), dtype=np.float32)

    def _obs(self):
        budget = np.array([(self.k - self.selected.sum()) / self.k], dtype=np.float32)
        return np.concatenate([self.features.ravel(), self.selected.astype(np.float32), budget])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.features = self.np_random.random((self.n, 20)).astype(np.float32)
        self.selected = np.zeros(self.n, dtype=bool)
        self.fixture_y = np.array([0, 1, 0, 1, 0, 1])
        return self._obs(), {"source_status": "fixture"}

    def action_masks(self):
        return ~self.selected

    def step(self, action):
        if not self.action_space.contains(action):
            raise ValueError("Action outside discrete space")
        if self.selected[action]:
            return self._obs(), 0.0, False, False, {"source_status": "fixture"}
        self.selected[action] = True
        done = bool(self.selected.sum() == self.k)
        reward = float(self.fixture_y[self.selected].sum() / self.k) if done else 0.0
        return self._obs(), reward, done, False, {"source_status": "fixture"}

env = FixtureEnv()
obs, _ = env.reset(seed=7)
for i in range(5):
    obs, reward, done, _, info = env.step(i)
    assert reward == 0 if i < 4 else done
    assert not env.action_masks()[i]
agent = MaskablePPO("MlpPolicy", env, n_steps=32, batch_size=16, seed=7, device="cpu")
agent.learn(total_timesteps=64)
obs, _ = env.reset(seed=8)
for _ in range(5):
    action, _ = agent.predict(obs, deterministic=True, action_masks=get_action_masks(env))
    obs, reward, done, _, info = env.step(action)
assert done and env.selected.sum() == 5
print("PASS FIXTURE_ONLY: masks, terminal reward and training lifecycle; NOT official ML")
PY
```

Tras smoke, Zabdiel implementa módulo real y tests en `ml/src/`, no copia fixture_y a dataset del reto. Casos mínimos: no futuro en observación; rewards intermedios0; no repetidos; resetseed; K≤elegibles; periodos incompletos rechazados; save/load; masks también al evaluar. Con fixtures no se afirma cumplimiento oficial ni desempeño.

## 4. Handoff web y demo viva, sin API obligatoria

Contrato de archivos vigente en [10](10-roles-web-presentacion.md): municipios/series/clusters/priorización/métricas/diccionario/fuentes. Un generador por JSON: Nico datos/grupos/fuentes; Zabdiel policy/métricas; Julián consumidor.

Añadir a cada bundle: `model_version`, `data_version`, cutoff/ventana, `source_status`, `is_fixture`, mapping/K y tipo de salida `replay`/`inference`. Outputs de replay no son nueva ejecución. Fixtures tienen banner y métricas null. No publicar labels futuros como inputs del agente.

**Arranque más pequeño:** consola ejecuta checkpoint real y genera JSON nuevo; React importa/carga resultado con hashes visibles. Servicio local delgado solo si ya existe al10:05; no reabrir API mock de amenazas/Cloudflare. CLI/servicio real aún no existía al inspeccionar: Zabdiel define interfaz, Nico conecta, Julián presenta resultado. K fijo5 hasta reentrenar o validar presupuestos soportados; no truncar top5 para fingir otro rollout.

## 5. Descarga SGC por tramos, coordinada con UTS

**HECHO:** catálogo oficial enlazado en reto; HTTPS confirmado por UTS en investigación previa: https://bdrsnc.sgc.gov.co/paginas1/catalogo/ . No repetir la descarga que UTS está probando.

**Reporte de UTS, no formulario enviado por esta sesión:** consultas POST `Consulta_Experta/consulsismo3.php` (1993-06..2018-02) y `Consulta_Experta_Seiscomp/consulta_sismo.php` (desde2018-03), departamento `27-Santander`, campos municipio/inicial/final y rangos de magnitud/profundidad/RMS/gap; salida HTML y botón Generar Excel.

**Formato de fecha de entrada: NO descubierto por esta sesión.** No deducir formato POST de fechas UTC de salida; no publicar curl/requests con payload inventado.

Receta manual para Nico/UTS, **una sola persona ejecuta cada tramo**:

1. Registrar claim `ciai/datos/sgc`: dueño, consulta/tramo, inicio y salida; UTS está al frente. Si MCP no está conectado, mensaje directo y posterior registro por quien sí tenga acceso, sin instalar/autenticar cuentas en medio del reto.
2. Abrir catálogo HTTPS con Playwright; seleccionar consulta según fecha. Inspeccionar etiquetas/placeholders y el request real de una consulta mínima; guardar nombres/payload/formato observados en provenance sin cookies/tokens.
3. Departamento Santander, valor reportado27-Santander; confirmar en formulario activo. No restringir municipio hasta definir zona; confirmar que magnitud mínima no elimina eventos necesarios para labels/completitud.
4. Primer tramo pequeño de **periodo cerrado**; comprobar que respuesta es tabla/export real y no error/login/vacío. Generar Excel, registrar filas/columnas y fecha/filtros/hash. Excel real podría llegar HTML: verificar contenido antes de elegir parser.
5. Ampliar por años si responde rápido, por meses si volumen/timeout lo exige. Nunca >1 consulta equivalente simultánea; registrar tramos completados para reanudar.
6. No cruzar corte marzo2018 en mismo formulario. Separar y armonizar antes de concatenar. Verificar límites inclusivos/exclusivos con muestras de frontera; dedup por identificador o combinación validada tiempo/localización, no por magnitud sola.
7. Nico recibe export primero, sin esperar catálogo entero. A09:00 sin export útil, recortar periodo/zona y usar interfaz manual; no sustituir SGC principal por datos sintéticos o USGS sin decisión de organizador.

Provenance mínimo por tramo: URL/endpoint, fecha descarga, fechas/rangos enviados, timezone, formato de entrada observado, escala de magnitud, fila mínima/máxima, count, hash y estado completo/incompleto. Comunicar formato cuando UTS lo confirme; no asumirlo mientras tanto.

## 6. Cambios precisos en flujos viejos (no regenerados aquí)

Se inspeccionaron JSON del repo. **PROPUESTA de sustitución**, no claim de HTML/PNG actualizado:

| Flujo | Qué quitar/sustituir | Qué debe mostrar |
|---|---|---|
| `flujo-ml` | UNGRD principal, GBDT/red como solución final, salida bundle API | SGC+DANE→panel/split temporal→gate train-only→Básico+entorno MaskablePPO K5→terminal reward→baselines/evaluación→checkpoint/JSON; Medio delegado según gate |
| `flujo-web` | Dependencia de API mock antigua y web sin rol de pitch | React lee bundle trazable; fixtures visibles→datos reales→mapa/grupos/priorización/métricas→`/presentacion`; replay separado de ejecutar policy real |
| `flujo-integracion` | API/Docker/túnel como ruta crítica | Claim descarga→SGC tramos+DANE→CSV/diccionario→Medio condicional→export/contrato→checkpoint a web→smoke live→entrega11:45 |
| `flujo-proyecto` | Modelo único supervisado y servicio obligatorio | Lanes Nico/Zabdiel/Julián; datos reales→tres bloques→evaluación→web-pitch; descarga y código/UI en paralelo; gates09:00/10:05/10:45 |
| `arquitectura-sistema` | Fuentes genéricas, predictor único/API/Cloudflare obligatorios | SGC principal+DANE→tabla+provenance/splits→supervisado/no-supervisado/Gymnasium+policy→artefactos/checkpoint→React; puente live local o consola, Streamlit backup |
| `reto-oficial` | Gate de degeneración ausente y RL sin reward terminal explícito | Gate SOLO train, K5 sin repetidos/masks, futuro oculto hasta terminal; utilidad proxy≠daño y policy probabilities≠sismo; React pitch y fallback local |

Conservar viejos exports como históricos, no usarlos en pitch como arquitectura vigente. Si alguien los regenera: JSON→HTML→PNG con mismo contenido, verificar los tres; no dedicar ahora ruta crítica a Archify. Ningún gráfico nuevo se generó en esta tarea.

## Fuentes

- [Oficial y citas completas](../research/08-enunciado-oficial.md).
- [RL, contratos de tiempo/recompensa y documentación Gymnasium/SB3](../research/09-rl-diseno.md).
- [Roles/sismología y límites de observación](../research/11-vista-uts2-roles-y-sismologia.md).
- Archivos locales verificados: `AGENTS.md`, `pyproject.toml`, `app/web/package.json`, seis JSON de `docs/flows/` y `.gitignore`.
