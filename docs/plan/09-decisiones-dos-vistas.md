# Decisiones de las dos vistas (uts y uts2)

Nico pidio que los dos modelos trabajen como **vistas independientes**: cada uno planifico por su cuenta y despues se atacaron mutuamente con evidencia. Vista **uts** (Claude): plan de 4 h, factibilidad de datos, roles y rubrica (`08-reto-oficial-plan-4h.md`). Vista **uts2** (otro modelo): enunciado citado y diseno de RL riguroso (`docs/research/08` y `09`). Esta tabla deja constancia de quien propuso que, que se concedio y por que.

| Tema | Vista uts | Vista uts2 | Decision | Por que |
|---|---|---|---|---|
| Episodio y recompensa del RL | 12 pasos por anio, recompensa por pick con el mes siguiente del municipio elegido | Un episodio por corte, K picks distintos antes de ver resultados, recompensa **solo terminal** | **uts2** | La recompensa por pick revela el futuro y adapta los siguientes picks con resultados que no existian al corte |
| Algoritmo | PPO o DQN de SB3 | **MaskablePPO** (SB3-Contrib) en Gymnasium | **uts2** | La mascara evita repetir municipios en entrenamiento e inferencia; verificado que instala y entrena en CPU (juguete: 0,489 contra 0,331 del aleatorio) |
| "Secuencial de verdad" | Lo afirmaba | Con utilidad aditiva y sismicidad exogena es top-K contextual | **uts2** | Se declara en la presentacion; no se afirma que RL sea necesario ni superior al ranker |
| Variable "cluster territorial" en el estado | La incluia | Es fuga si el clustering ve test | **uts2** | Solo se ajusta con entrenamiento o se omite |
| Ventana del objetivo | Anual (la guia oficial) | Mensual, si pasa el gate de clases, positivos y episodios | **uts2, provisional** | Mas episodios; el gate se mide a las 8:00 y el cambio de ventana arrastra objetivo, recompensa y lineas base |
| Cuantiles como alternativa de objetivo | "Clases balanceadas" | Falso con ceros y empates | **uts2** | Contraejemplo; se corrigio el plan |
| Fraccion de profundidad ">70 km" como "intermedia" | Si | Incluye sismos de mas de 300 km | **uts2** | Se usan bandas de profundidad (USGS) |
| Segunda fuente oficial | DANE + Gobernacion | Solo DANE bajo gate as-of | **Mixta** | DANE (1985-2042 por anio) como principal, retrospectiva y declarada; Gobernacion solo desde 2018-05, opcional |
| Acceso al catalogo SGC | Funciona por **HTTPS**; el enlace HTTP (puerto 80) da timeout; dos formularios POST | No lo habia podido verificar | **uts** | Verificado con curl, navegador y desde el VPS |
| DANE por anio | Existen proyecciones municipales 1985-2042 en xlsx | Siguen siendo retrospectivas, no "as-of" | **Ambas** | El dato existe (uts) y la limitacion se declara (uts2) |
| Cobertura por radio | Extension para romper la aditividad | Solo como sensibilidad, con R ex ante y sin doble conteo | **uts2 (condiciones)** | Analisis separado con greedy de union y oraculo del mismo objetivo; no se vende como area afectada |
| Preparar antes de las 8:00 | Solo entorno y planificacion | La pagina no lo prohibe; criterio conservador | **Ambas** | Se descarga y procesa desde las 8:00; confirmar en la ceremonia |
| Roles, cronograma y rubrica | Cronograma hora a hora y mapeo a los 100 puntos | No lo cubrio | **uts** | Es la parte operativa |
| Demo | Streamlit o Gradio (mismo entorno Python) frente a la web React | Notebook o flujo minimo reproducible; API o web opcional | **Streamlit, pendiente de Nico** | Producto minimo oficial: demostracion; sin API |

## Pendiente de decision de Nico

1. Demo en Streamlit (recomendado) frente a la web React ya preparada por Julian.
2. Quien lleva el RL (propuesta: Zabdiel) y quien Basico y Medio (Nico), segun fortalezas reales.
3. Preguntar al jurado en la apertura: la ambiguedad "Medio: unicamente no supervisado" frente a "cumplir Basico y Medio" (se entregan los tres bloques, cada uno con su tipo de modelo).

## Gates que se miden a las 8:00 (antes de comprometer el diseno)

- Catalogo SGC descargable por tramos (formato de fecha del formulario por descubrir).
- Clases bajo, medio y alto con soporte suficiente por mes; si no, ventana anual.
- Al menos 20 variables reales con justificacion; DANE unido por municipio y anio.
- Episodios completos para entrenamiento, validacion y prueba cronologicas.
