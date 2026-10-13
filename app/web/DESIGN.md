# DESIGN.md: sistema visual de la web de analisis sismico

Fuente unica de verdad visual para `app/web/`. La construccion (este o una IA) no toma
decisiones de color, tipografia, espacio ni movimiento que no esten declaradas aqui.

No es el sitio del evento: es la aplicacion de analisis que **es** la presentacion del
equipo. Alcance funcional en `docs/plan/10-roles-web-presentacion.md` (secciones 4 y 5).

---

## 1. Concepto

**"Laboratorio de datos sismicos"**: una herramienta de analisis, no una landing de
marketing. Se lee como instrumentacion cientifica: sobria, densa en
informacion y honesta sobre lo que no sabe.

Público: estudiantes de ingenieria, sistemas y ciencia de datos. Perfil tecnico, joven,
que valora lo serio y lo claro. Idioma de la interfaz: español (Colombia).

**Tono de voz:** tecnico, claro, sin sensacionalismo. La app nunca dice "alerta", nunca dice "peligro", nunca dice "prediccion de un sismo".
Dice "priorizacion exploratoria". El
vocabulario del interfaz es la senalizacion: la misma palabra para la misma cosa en todo
el producto.

**Motivo visual recurrente:** la onda sismica. Se usa como textura de fondo (trazo fino
de baja opacidad), como divisor de secciones y como repique de carga. **No** se usa como
ilustracion decorativa ni como animacion de fondo continua.

### 1.1 La idea memorable (un solo lugar)

La **maquina del tiempo**: un deslizador de cortes mensuales que, al moverse, muestra que
habria priorizado el agente **antes** de que ocurrieran los sismos de referencia, y
contrasta esa priorizacion con lo que realmente paso despues. Es el unico elemento con
movimiento propio y protagonistico. Todo lo demas es sobrio y estatico por decision.

Regla de Chanel aplicada: gastamos la boldness ahi y en ningun otro lado.

---

## 2. Referencias visuales: que se toma y que se descarta

| Referencia | Se toma | Se descarta |
|---|---|---|
| Aakriti (arquitectura, oscuro) | Titulo gigante tipo marca en el hero con transparencia; tarjetas de vidrio translucido con borde sutil; chips de estadistica flotando en el hero; tarjetas oscuras con icono lineal fino; CTA en pildora; ritmo vertical amplio | Tono de lujo residencial, tipografia serif elegante, paleta calida dorada |
| ISK (contabilidad, claro) | Unicamente la estructura de tres pilares con icono circular, y el bloque final con formulario | Fondo claro, aspecto corporativo generico, tipografia y composicion |
| Ocean Crown (logistica, grises) | Rejilla estricta; pasos conectados por linea; tarjetas con contorno fino sobre fondo negro; footer en columnas; jerarquia tipografica sobria | La escala de grises pura: aqui el color de acento tiene funcion semantica |

### 2.1 Resolucion explicita de contradicciones

1. **Referencia 2 es clara y las otras dos son oscuras.** Gana el oscuro (1 y 3), porque
   el brief fija modo oscuro y ademas un mapa con datos sismicos sobre fondo claro pierde
   el contraste de los colores de nivel. De la referencia 2 solo se conserva la
   *estructura* de tres pilares y el bloque de formulario.
2. **Referencia 1 usa dorado calido y la 3 no tiene color.** Gana un acento unico frio
   (seccion 3.1) y se le asigna una funcion: cromo de interfaz. Los colores de nivel y de
   datos son un sistema aparte y nunca se usan en el cromo.
3. **"Tarjetas de vidrio" (ref 1) contra "rejilla estricta" (ref 3).** No se contradicen si
   el vidrio se limita a superficies flotantes (navbar, panel del mapa, panel de detalle)
   y las tarjetas de contenido usan contorno fino opaco, sin desenfoque. Se evita el
   efecto "SaaS de tarjetas identicas": ver seccion 3.3 (radios) y 6.
4. **El contexto pedia color por nivel de competencia (Basico / Medio / Avanzado) y la app
   muestra riesgo por municipio (bajo / medio / alto).** Gana el riesgo. Los bloques de
   competencia se nombran como texto en Metodologia; no se codifican con color, porque ese
   color significaria otra cosa y el jurado lo leeria como riesgo.

---

## 3. Tokens

### 3.1 Color

**Base y superficies** (azul-negro frio; nunca negro puro ni `#0B0B0B`/"tinted near-black"
como fondo, y nunca crema calido).

| Token | Hex | Uso |
|---|---|---|
| `--bg-base` | `#07090E` | Fondo global de la aplicacion |
| `--bg-raised` | `#0E1219` | Tarjetas, paneles, celdas de tabla |
| `--bg-inset` | `#151B25` | Campos de formulario,hover de fila, codigo |
| `--bg-overlay` | `#1A212D` | Modales, menus desplegables |
| `--border-hairline` | `rgba(255,255,255,0.09)` | Contorno fino de tarjetas y divisores |
| `--border-strong` | `rgba(255,255,255,0.16)` | Contorno de control en hover/focus |
| `--text-primary` | `#E8EDF5` | Titulos, cifras, contenido |
| `--text-secondary` | `#97A3B6` | Parrafos, descripciones, etiquetas |
| `--text-muted` | `#78859A` | Metadatos, unidades, notas al pie |

**Acento de interfaz** (cromo: navegacion, enlaces, boton primario, foco).

| Token | Hex | Uso |
|---|---|---|
| `--accent` | `#4C8DFF` | Enlaces, boton primario, anillo de foco, control activo |
| `--accent-hover` | `#6BA0FF` | Hover del acento |
| `--accent-press` | `#3A79E8` | Estado activo del acento |
| `--accent-quiet` | `rgba(76,141,255,0.14)` | Fondo de chip activo, resaltado de fila |
| `--data-series` | `#7DD3FC` | Lineas de series temporales en graficos |

**Regla dura:** el acento **nunca** se usa como relleno de un nivel de riesgo ni de una
serie de datos. Si el azul aparece junto a un nivel, significa "interfaz", no "riesgo".
Esta regla es lo que permite que un unico acento cohabite con una escala de riesgo.

**Estados.**

| Token | Hex | Uso |
|---|---|---|
| `--danger` | `#FF4D6D` | Errores de validacion, fallo de carga |
| `--warning` | `#FFB020` | Advertencia (datos de ejemplo, fuente sin verificar) |
| `--success` | `#2DD4A7` | Confirmacion, estado listo |
| `--focus-ring` | `#4C8DFF` | Anillo de foco; nunca se elimina sin reemplazo |

### 3.2 Color semantico por nivel de riesgo

**El nivel nunca se comunica solo por color.** Cada nivel lleva color **mas** icono **mas**
etiqueta de texto. Es una regla del repo (`skills/web-app/SKILL.md`) y una requisito de
accesibilidad, no una preferencia.

| Nivel | Token | Hex | Icono (lineal, 1.5px) | Etiqueta obligatoria |
|---|---|---|---|---|
| Bajo | `--risk-low` | `#2DD4A7` | circulo con punto interior | "Bajo" |
| Medio | `--risk-med` | `#FFB020` | triangulo con barra interior | "Medio" |
| Alto | `--risk-high` | `#FF4D6D` | rombo con corte diagonal | "Alto" |
| Sin dato | `--risk-none` | `--text-muted` | circulo con guion | "Sin dato" |
| Abstenido | `--risk-abstain` | `--text-secondary` | circulo con puntos suspensivos | "Sin priorizacion" |

Notas de diseno relevantes:

- Los tres niveles tienen **luminosidad parecida a proposito**: ninguno grita mas que otro.
  Por eso la distincion no puede depender del color y el par icono+etiqueta es
  obligatorio. Es una decision, no una limitacion.
- **No se usa rojo contra verde como unico par.** El nivel alto es magenta-rojo y el bajo
  es teal, no verde puro; ademas cada uno tiene forma propia.
- `--risk-none` y `--risk-abstain` existen porque "municipio sin datos" y "el agente no
  pudo priorizar" **no son nivel bajo**. Confundirlos con "Bajo" es el error de
  comunicacion mas grave posible en esta app, y esta prohibida visualmente.
- "Sin dato" usa contorno discontinuo; "Abstenido" usa trama diagonal sutil. Diferentes
  texturas para diferentes ausencias.

### 3.3 Tipografia

Dos familias mas una monoespaciada, de Google Fonts.

| Rol | Familia | Uso |
|---|---|---|
| Display (titulos) | **Archivo** (variable, ejes `wght` y `wdth`) | Titulo gigante del hero, titulos de seccion, cifras destacadas |
| Cuerpo | **IBM Plex Sans** | Parrafos, tablas, etiquetas, botones |
| Datos | **IBM Plex Mono** | Magnitudes, coordenadas, fechas, cortes, `model_version`, `data_version`, conteos |

Por que esta combinacion: IBM Plex nace de una empresa de instrumentacion cientifica y
arrastra ese registro sin ser "corporativo". Archivo es grotesca y geometricaétrica, claramente
distinta de Plex; su eje de ancho permite que el titulo gigante tenga presion sin
necesitar una serif.

**Escala** (rem, base 16px; `clamp` en las tres primeras filas).

| Token | Tamano | Peso | Interlineado | Tracking | Uso |
|---|---|---|---|---|---|
| `--t-hero` | `clamp(3rem, 11vw, 9.5rem)` | 800 | 0.88 | -0.035em | Titulo gigante del hero |
| `--t-display` | `clamp(2rem, 5vw, 3.5rem)` | 700 | 1.02 | -0.02em | Titulo de seccion |
| `--t-title` | `1.375rem` | 600 | 1.2 | -0.01em | Titulo de tarjeta, de panel |
| `--t-body-lg` | `1.0625rem` | 400 | 1.55 | 0 | Parrafo introductorio |
| `--t-body` | `1rem` | 400 | 1.6 | 0 | Cuerpo |
| `--t-small` | `0.875rem` | 400 | 1.5 | 0 | Texto secundario, descripcion de control |
| `--t-label` | `0.8125rem` | 500 | 1.35 | 0 | Etiqueta de campo, encabezado de columna |
| `--t-data` | `0.9375rem` | 500 | 1.4 | 0.01em | Cifra en monoespaciada |
| `--t-data-lg` | `1.75rem` | 600 | 1.15 | -0.01em | Cifra destacada |
| `--t-micro` | `0.75rem` | 500 | 1.4 | 0.02em | Nota al pie, unidad |

**Reglas de uso del titulo gigante del hero.**

- Una sola vez por vista. Nunca en el encabezado de una seccion interior.
- Nunca mas de tres palabras. Se usa el nombre corto del equipo o del producto.
- El ancho del eje se juega aqui: se sube a `wdth 112` en movil y se baja a `wdth 88` en
  escritorio, para que ocupe el ancho disponible sin desbordar.
- Se permite transparencia hasta `rgba(232,237,245,0.14)` cuando va sobre el mapa o una
  textura de onda, pero **el texto mantiene contraste AA**: si el fondo queda claro
  detras, se sube la opacidad a `0.22` o se anade un degradado bajo.
- Nunca se resalta una sola palabra del titular con otro color o peso. El titular se
  trata como un bloque.

**Reglas generales.**

- Ancho de linea de cuerpo: **maximo 72 caracteres**. Las tablas y el codigo pueden llegar
  a 90.
- Nunca se usa `text-transform: uppercase` en etiquetas de interfaz. Se reserva para el
  nombre propio de la entidad en el pie y para siglas (SGC, UNAB, ML).
- Cifras siempre en monoespaciada con su unidad al lado, en `--text-muted`: `M 6,2` no
  `M6,2` suelto. Separador de miles con punto y decimal con coma (convencion colombiana).
- No se anteponen etiquetas tipograficas decorativas encima del contenido. Si un texto no
  aporta informacion, se quita.

### 3.4 Espaciado, radios, bordes, sombras

**Espaciado** (base 4px): `4, 8, 12, 16, 24, 32, 48, 64, 96, 128` como
`--s-1` a `--s-10`. Los multiples de 8 son el default; los de 4 solo para ajustes
pequenos. El ritmo vertical entre secciones es `--s-10` (128px) en escritorio y
`--s-7` (48px) en movil.

**Radios** (NO uno solo para todo: un unico radio es el sintoma del "SaaS card kit").

| Token | Valor | Uso |
|---|---|---|
| `--r-sharp` | `2px` | Chips de dato, celdas de matriz, marcas de corte |
| `--r-control` | `6px` | Botones, campos, selectores, pestanas |
| `--r-card` | `12px` | Tarjetas de contenido |
| `--r-panel` | `16px` | Paneles flotantes: mapa, detalle, navbar |
| `--r-pill` | `999px` | Solo CTA en pildora y badge |

**Bordes.** `1px` por defecto, `--border-hairline`. `2px` solo en el lado izquierdo de un
estado activo o en el anillo de foco. Los contornos son decorativos: **nunca** transmiten
informacion por si solos.

**Sombras.** El tema oscuro no usa sombras para elevar: usa diferencia de superficie y
borde. Solo dos sombras existen, y ninguna es decorativa de tarjeta:

| Token | Valor | Uso |
|---|---|---|
| `--shadow-panel` | `0 12px 40px rgba(0,0,0,0.55)` | Panel del mapa y de detalle |
| `--shadow-menu` | `0 8px 24px rgba(0,0,0,0.6)` | Menu desplegable y modal |

Regla: **cero sombras suaves tipo `rgba(0,0,0,0.1)` bajo cada tarjeta.**

**Efecto vidrio.** Solo superficies flotantes (navbar, panel de mapa, panel de detalle,
modal).

| Propiedad | Valor |
|---|---|
| Fondo | `rgba(20,26,36,0.72)` |
| `backdrop-filter` | `blur(18px) saturate(140%)` |
| Borde | `1px solid rgba(255,255,255,0.11)` |
| Radio | `--r-panel` |

Contraste verificado: el texto primario sobre vidrio con el mapa detras da **12.4:1**
(AAA). Si una superficie de vidrio queda sobre una zona clara del mapa, se sube la
opacidad del fondo a `0.86`.

**z-index** (escala cerrada, sin numeros sueltos).

| Token | Valor | Capa |
|---|---|---|
| `--z-base` | 0 | Contenido |
| `--z-sticky` | 100 | Encabezado de tabla, pie de la maquina del tiempo |
| `--z-header` | 200 | Navbar |
| `--z-panel` | 300 | Panel de detalle, drawer |
| `--z-modal` | 400 | Modal |
| `--z-toast` | 500 | Aviso emergente |
| `--z-tooltip` | 600 | Tooltip |

### 3.5 Grid

| Token | Valor |
|---|---|
| Contenedor maximo | `1280px` (presentacion a pantalla completa: `100%`, sin padding) |
| Columnas | 12 |
| Gutter | `24px` en escritorio, `16px` en movil |
| Padding lateral | `32px` escritorio, `20px` tablet, `16px` movil |

**Breakpoints.**

| Nombre | Ancho | Cambio de composicion |
|---|---|---|
| `mobile` | `< 640px` | Una columna. El mapa pasa a altura fija de 60vh. La maquina del tiempo ocupa el ancho completo. |
| `tablet` | `640–1023px` | Grid de 8 columnas utiles; tarjetas de dos en dos. |
| `desktop` | `1024–1439px` | 12 columnas; mapa y detalle en `7/5`. |
| `wide` | `>= 1440px` | Contenedor centered a 1280; el mapa puede ocupar `8/4`. |

Alineacion: **todo a la izquierda**. Solo el titulo del hero y los estados vacios se
centran. No hay texto justificado en ningun punto: un panel de analisis con texto
justificado es ilegible en columnas angostas.

Prueba obligatoria antes de congelar: **1440px y 390px**.

---

## 4. Componentes

Todos con los cinco estados. Un estado sin definir se implementa como `default` y se
revisa tarde; se listan todos para evitarlo.

### 4.1 Navbar fija

Altura `64px`, fondo vidrio, borde inferior `--border-hairline`. Contiene marca (nombre
corto del equipo), navegacion de vistas, y a la derecha el **snapshot** en monoespaciada
discreta (`model_version`, `data_version`) mas el boton de modo presentacion.

| Estado | Comportamiento |
|---|---|
| default | Fondo vidrio, texto secundario |
| hover | El enlace toma `--text-primary`; el subrayado crece de 0 a 100% en 140ms |
| focus | Anillo `--focus-ring` de 2px con desplazamiento de 2px, nunca removido |
| active | Subrayado de 2px en `--accent` y texto primario; con `aria-current="page"` |
| disabled | No aplica en la navbar |

Al hacer scroll la navbar gana `--bg-raised` a opacidad 0.94 y pierde el desenfoque en
220ms, para no estorbar al mapa.

### 4.2 Boton primario en pildora

Radio `--r-pill`, altura 44px, padding `20px 24px`, icono de flecha circular a la derecha.
Etiqueta en verbo concreto: "Ver la priorizacion", "Ejecutar agente", "Reproducir
resultado guardado". Nunca "Enviar" ni "Mas informacion".

| Estado | Fondo | Texto | Transform |
|---|---|---|---|
| default | `--accent` | `--bg-base` | — |
| hover | `--accent-hover` | `--bg-base` | — |
| focus | `--accent` + anillo 2px desplazado 2px | `--bg-base` | — |
| active | `--accent-press` | `--bg-base` | `scale(0.98)` |
| disabled | `--bg-inset` | `--text-muted` | opacidad 0.6, `cursor: not-allowed` |

### 4.3 Boton secundario

Mismo tamano, fondo transparente, borde `1px solid --border-strong`, texto
`--text-primary`. El mismo grupo de estados; `hover` sube el borde a `--accent` sin
cambiar el fondo.

### 4.4 Chip de estadistica

Pildora pequena con borde fino: cifra en `--t-data-lg` monoespaciada + etiqueta en
`--t-small` `--text-secondary`. Es donde viven las cifras **que vienen del JSON**.

- Si el valor es `null` (como las metricas en datos de ejemplo), el chip muestra `—` en
  `--text-muted` y la etiqueta "no disponible". **Nunca** muestra `0`.
- Si el JSON trae `"ejemplo": true`, el chip lleva el badge de advertencia.
- Tres chips en el hero como maximo.

Estados: `default`, `hover` (borde a `--border-strong`), `focus`, `disabled` (cifra en
muted), `sin-dato` (el estado de arriba, que no es un estado visual sino de dato).

### 4.5 Tarjeta de vidrio

Superficie flotante con el vidrio de la seccion 3.4. Se usa para panel de mapa y panel de
detalle, **no** para el contenido en rejilla. Estados: `default`, `hover` (solo si es
interactiva: sube a `--bg-overlay`), `focus`, `active` (borde a `--accent`), `disabled`.

### 4.6 Tarjeta de contenido (contorno fino, no vidrio)

`--bg-raised`, borde `--border-hairline`, radio `--r-card`, padding 24px. Es la tarjeta por
defecto de la rejilla. **No lleva sombra.** Estados: `default`, `hover` (borde a
`--border-strong`, fondo a `--bg-overlay`, transicion 140ms), `focus` (anillo), `active`
(borde a `--accent`), `disabled` (opacidad 0.55).

Regla anti-kit: dentro de una misma rejilla, **las tarjetas no son identicas**. La altura
la fija el contenido; no se estiran a una altura comun. Si tres tarjetas llevan el mismo
icono circular, la misma altura y el mismo padding, es el kit: hay que variar.

### 4.7 Tarjeta/badge de nivel

Chip con icono lineal + etiqueta de texto + color del nivel. Variante `solida` (fondo al
12% del color del nivel, texto en el color del nivel) para mapa y listas; variante
`contorno` (borde al 45%) para tablas densas.

Estados: `default`, `hover`, `focus`, `active`, `disabled` (se convierte en
"Sin priorizacion", nunca oculta el nivel).

### 4.8 Bloque de dato real

Cifra grande en monoespaciada (`--t-data-lg`), unidad y definicion en `--t-small`, y
**fuente debajo en `--t-micro` `--text-muted`**: origen, fecha de descarga y filtros. Sin
la linea de fuente, el bloque no se implementa: toda cifra publicada sale de un JSON con
procedencia.

Si la cifra no esta verificada contra el SGC, se renderiza `[DATO A VERIFICAR CON SGC]`
con el estilo de estado `warning`, nunca como numero.

### 4.9 Paso de linea de tiempo

Marcador de un corte o de un evento de referencia: punto de 8px con anillo, linea vertical
que une los pasos, mes en monoespaciada y etiqueta. Los **sismos de referencia** son un
variante con icono de rombo y la doble magnitud: `M 6,2 (USGS) / M 6,6 (SGC)`, ambas
visibles, nunca promediadas.

Estados: `default`, `hover` (fila completa resalta), `focus`, `active` (mes activo:
punto relleno y linea de acento a la izquierda, 2px), `future` (mes posterior al corte:
opacidad 0.5).

### 4.10 Acordeon de "que significa y que no"

Titulo del item en `--t-title`; al abrir, cuerpo en `--t-body`. El contenido por defecto
del primer item es el aviso de que **los tres niveles son frecuencia relativa de
reportes, no severidad ni alerta oficial**.

Estados: `default` (cerrado, chevron rotado 0), `hover` (titulo a primario),
`focus` (anillo en el boton del encabezado, no en el panel), `active`/`expanded`
(chevron 180deg, altura animada), `disabled`.

Un solo item abierto a la vez.

### 4.11 Formulario del puente de agente

Es el sustituto del formulario de contacto de la referencia 2, y es la pieza que ejecuta
la demo en vivo.

| Campo | Tipo | Validacion | Error |
|---|---|---|---|
| Corte | Select de meses disponibles | Obligatorio; debe existir en `serie_mensual.json` | "Ese corte no esta en los datos" |
| K | Select de valores **entrenados** | Obligatorio; solo ofrece los K declarados por Zabdiel | "K no entrenado: exige otra politica" |
| Modelo | Radio: agente / linea base / oraculo | Obligatorio | — |

Boton primario: **"Ejecutar agente"** (nivel 2, ejecucion en vivo via puente local) y
secundario: **"Reproducir resultado guardado"** (nivel 1, replay desde `priorizacion.json`).

Los dos botones estan **separados visualmente y rotulados distinto en pantalla**, porque
uno es inferencia nueva y el otro no. Presentarlos juntos sin distinguir seria un
error metodologico, no de diseno.

Estados de campo: `default`, `hover`, `focus` (anillo 2px), `active`, `disabled` (durante
la ejecucion), `error` (borde `--danger`, mensaje en `--danger`, `aria-invalid="true"`).
El boton entra en `disabled` con texto "Ejecutando..." durante la llamada.

### 4.12 Badge

Texto corto sobre fondo al 14% del color y texto en el color, radio `--r-sharp`, altura
20px. Uso restringido a: `datos de ejemplo`, `replay`, `en vivo`, `fuente por verificar`,
`abstencion: <motivo>`.

### 4.13 Banner de datos de ejemplo

Barra fija bajo la navbar, fondo `--warning` al 12%, texto `--t-small`, icono de alerta y
el texto: **"Datos de ejemplo: no son resultados reales."**

- Aparece mientras exista un JSON con `"ejemplo": true`.
- En modo presentacion ocupa una franja propia y no se puede cerrar.
- Mientras este visible, **el ranking y las alertas no se presentan como reales**: los
  chips de estadistica muestran `—` cuando el valor es `null`, y la vista de priorizacion
  rotula sus resultados como "conjunto de ejemplo".

### 4.14 Footer en columnas

Cuatro columnas: equipo y autoria; fuentes con URL y fecha; enlace a diccionario y
metodologia; aviso de alcance ("priorizacion exploratoria, no alerta oficial") y
versionado. Fondo `--bg-base`, borde superior `--border-hairline`.

Espacio reservado y marcado para el logo del SGC y de los aliados: nunca se usa el logo
del SGC sin permiso escrito, y el espacio reservado se documenta como tal.

---

## 5. Estructura y composicion

El hero de esta app **no es una portada de marketing**: es un panel de estado del
experimento. Conserva el recurso de la referencia 1 (titulo gigante con transparencia,
chips de estadistica) pero el contenido es dato real.

### 5.1 Rutas

| Ruta | Vista | Contenido |
|---|---|---|
| `/` | Panorama | Hero con estado, resumen de las seis vistas, disclaimer de alcance |
| `/mapa` | Mapa | Mapa de municipios por nivel o grupo, selector de mes y de amenaza |
| `/priorizacion` | Priorizacion | K del agente frente a lineas base y al resultado real |
| `/tiempo` | Maquina del tiempo | Deslizador de cortes, sismos de referencia, que habria priorizado |
| `/grupos` | Grupos | Perfil de cada cluster del Medio, leido en palabras |
| `/metodologia` | Metodologia y datos | Fuentes, diccionario, validacion cronologica, incertidumbre, limites |
| `/presentacion` | Modo presentacion | El pitch a pantalla completa |

### 5.2 Composicion por vista

**`/` Panorama.** Hero a sangre con la onda sismica de fondo (trazo SVG, opacidad 0.10),
titulo gigante del equipo en Archivo `wdth 88`, y tres chips de estadistica tomados del
JSON. Bajo el hero, una fila de tarjetas de acceso a las seis vistas con icono circular
(estructura de la referencia 2). Cierra con el bloque de alcance, que es el aviso "que NO
significa". Responsive: los tres chips apilan a columna; las tarjetas de acceso pasan de
tres en linea a dos y luego a una.

**`/mapa`.** Layout `7/5` en escritorio: mapa a la izquierda, panel de detalle pegado a la
derecha. El mapa es MapLibre GL con circulos proporcionales al score mientras no haya
poligonos municipales; el tamano codifica el valor y el color codifica el nivel, con
icono en el popup. En `mobile` el mapa pasa a 60vh y el panel de detalle baja debajo como
hoja deslizable. El selector de mes es un control deslizante con cortes discretos.

**`/priorizacion`.** Tabla a ancho completo con columnas: puesto, municipio, agente, linea
base, oraculo, y que paso despues. El municipio es un enlace al mapa. Fila activa con
resaltado `--accent-quiet`. Debajo, un bloque de disclaimer: la comparacion se hace con
la **diferencia pareada** y el solapamiento de intervalos marginales no demuestra empate.

**`/tiempo`.** Ocupa el ancho completo. Arriba, el deslizador de cortes con los sismos de
referencia marcados en la linea. Abajo, mapa y lista sincronizados: al mover el corte,
ambos cambian. Es la vista con mas movimiento y la unica con animacion protagonistsica.

**`/grupos`.** Una tarjeta por cluster: nombre del grupo, lectura en palabras, promedio
de variables clave, importancia de variables en barras horizontales, y los municipios que
lo integran. La lectura en palabras es texto, no solo grafico.

**`/metodologia`.** Acordeon de "que significa y que no" primero. Luego fuentes (tabla con
URL, fecha de descarga, filtros), diccionario (nombre, tipo, unidad, fuente, por que se
incluye), validacion cronologica e incertidumbre. Todo desde los JSON; si falta un dato,
la tabla lo dice.

**`/presentacion`.** Pantalla completa, sin scroll de pagina, navegacion con flechas del
teclado y botones. Secciones, en orden: problema, datos, modelos, resultados (con la
maquina del tiempo), impacto, limites, equipo. Controlador con `←`, `→`, `Espacio` y
`Esc`. Contador de seccion discreto. En el indice de la URL va la seccion, para poder
enlazar a una en concreto.

---

## 6. Movimiento

Animacion con proposito: muestra **que cambio**. Nada se mueve solo porque se puede.

| Transicion | Duracion | Easing |
|---|---|---|
| Hover de control | 140ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Aparicion de panel (abrir/cerrar) | 180ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Cambio de corte en la maquina del tiempo | 420ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Rejilla de mapa al recalcular | 260ms | `ease-out` |
| Aviso emergente | 180ms entrada, 140ms salida | `cubic-bezier(0.2, 0, 0, 1)` |

**Permitido:** pulso lento del punto de epicentro activo en el mapa (4s, opacidad 0.5 a
0.9, un solo punto, nunca todos); trazado de la onda sismica en el hero, una vez al
cargar y no en bucle; revelacion suave del contenido al entrar en viewport, una vez por
elemento.

**Prohibido:** entrada tipo "fade and slide up" en cada seccion al hacer scroll; transicion
en cada tarjeta al pasar el mouse; parallax; animacion continua de fondo; counters que
cuentan desde cero; cualquier movimiento que no responda a una accion de la persona.

**`prefers-reduced-motion: reduce`.** Regla estricta, aplicada en el reset global:

1. Todas las transiciones y animaciones pasan a `0.01ms`.
2. El pulso del epicentro se desactiva.
3. El trazado de la onda del hero se muestra ya dibujado, sin animacion.
4. El deslizador de la maquina del tiempo cambia de corte de inmediato.
5. Ninguna informacion queda oculta esperando a una animacion.

---

## 7. Accesibilidad y rendimiento

### 7.1 Contraste (verificado, no estimado)

Todos los pares declarados cumplen WCAG 2.1 AA.

| Par | Ratio | Nivel |
|---|---|---|
| `--text-primary` `#E8EDF5` sobre `--bg-base` `#07090E` | 16.94 | AAA |
| `--text-primary` sobre `--bg-raised` `#0E1219` | 15.96 | AAA |
| `--text-secondary` `#97A3B6` sobre `--bg-base` | 7.81 | AAA |
| `--text-secondary` sobre `--bg-raised` | 7.35 | AAA |
| `--text-muted` `#78859A` sobre `--bg-base` | 5.33 | AA |
| `--text-muted` sobre `--bg-raised` | 5.02 | AA |
| `--accent` `#4C8DFF` sobre `--bg-base` | 6.22 | AA |
| `--accent` sobre `--bg-raised` | 5.86 | AA |
| `--bg-base` sobre `--accent` (boton primario) | 6.22 | AA |
| `--risk-low` `#2DD4A7` sobre `--bg-base` | 10.51 | AAA |
| `--risk-med` `#FFB020` sobre `--bg-base` | 10.89 | AAA |
| `--risk-high` `#FF4D6D` sobre `--bg-base` | 6.20 | AA |
| `--data-series` `#7DD3FC` sobre `--bg-base` | 11.94 | AAA |
| `--text-primary` sobre vidrio con mapa detras | 12.40 | AAA |

Los bordes `--border-hairline` tienen 1.34:1 contra el fondo. **Es intencional y esta
declarado**: los bordes son decorativos, nunca portan informacion. Si un borde tiene que
comunicar algo, sube a `--border-strong` y se acompana de texto o icono.

Los tres colores de nivel tienen luminosidad parecida entre si (pares 1.04, 1.70 y 1.76
entre si). **No se declara conformidad de daltonismo por el color**: la distincion la
garantizan el icono y la etiqueta de texto, que son obligatorios.

### 7.2 Reglas de implementacion

- Foco visible siempre: anillo de 2px en `--focus-ring`, desplazamiento 2px. Se puede
  cambiar de forma, **nunca se elimina**.
- Navegacion completa por teclado, incluido el modo presentacion (`←`, `→`, `Esc`).
- Tamano tactil minimo **44x44px** en todo control.
- Texto alternativo en todo contenido no textual. El mapa tiene su equivalente textual:
  la tabla de priorizacion es la version accesible del mapa, no un extra.
- El nivel se expone en texto, no solo en color: cada municipio del mapa tiene etiqueta
  de nivel en su popup y en la fila de la tabla.
- Los datos de la maquina del tiempo tienen una vista de tabla equivalente, navegable con
  teclado.
- Foco visible tambien en el modo presentacion.
- Idioma `lang="es-CO"`.

### 7.3 Rendimiento

| Recurso | Limite |
|---|---|
| Imagen del hero o textura de onda | ≤ 180 KB, AVIF o SVG inline |
| Iconos de nivel y de interfaz | SVG inline, nunca fuente de iconos |
| Fuente de mapa (tiles) | ≤ 120 KB por tesela; sin tiles 3D ni de sombreado |
| Cifras en el mapa | 87 municipios; circulos, no poligonos, mientras no haya geometria |
| JS inicial (ruta `/`) | ≤ 200 KB gzip |
| Presupuesto total de `bun run build` | ≤ 400 KB gzip |

MapLibre GL **debe quedar excluido del pre-empaquetado** de Vite
(`optimizeDeps.exclude: ['maplibre-gl']`, ya configurado en `vite.config.ts`). Sin eso el
mapa sale en blanco con el error "Worker failed to load".

---

## 8. Do / Don't

**Hacer**

- Mostrar la incertidumbre junto al nivel: conjunto de prediccion y abstencion con su
  motivo, siempre en la misma vista que el nivel.
- Mostrar el snapshot (`model_version`, `data_version`, `target_month`,
  `feature_cutoff`) de forma discreta pero siempre presente.
- Poner la fuente debajo de cada cifra: origen, fecha de descarga y filtros.
- Marcar con `[DATO A VERIFICAR CON SGC]` lo que aun no esta verificado.
- Rotular por separado la ejecucion en vivo y el replay.
- Usar la onda sismica como textura y divisor, con baja opacidad.
- Probar a 1440px y 390px antes de dar por cerrada una vista.

**Evitar**

- **No** inventar cifras. Ninguna. Si el JSON no trae el dato, la interfaz dice que no lo
  trae. Un `0` de mas es una mentira metodologica.
- **No** presentar un nivel sin su incertidumbre al lado.
- **No** codificar un nivel solo con color, y **no** usar rojo contra verde como par.
- **No** confundir "sin dato" con "Bajo", ni "abstencion" con "Bajo": son estados
  distintos con tokens, iconos y texturas distintos.
- **No** usar fotos de desastres, edificios en ruinas, grietas dramaticas ni imagenes de
  preparacion ante emergencia. Este proyecto trata datos, no catastrofismo.
- **No** usar ni sugerir el logo del Servicio Geologico Colombiano. Se deja un espacio
  reservado y marcado.
- **No** usar sensacionalismo: nada de "alerta", "peligro", "prevision de sismo".
- **No** saturar de vidrio: vidrio en superficies flotantes, contorno fino en el
  contenido.
- **No** aplicar una misma sombra suave a todas las tarjetas.
- **No** usar radios unicos en toda la interfaz.
- **No** subir el acento azul como relleno de un nivel de riesgo o de una serie de datos.
- **No** ocultar informacion detras de una animacion.
- **No** anadir funciones despues de las 11:45 (el corte del plan).

---

## 9. Decisiones de diseno y supuestos

Cada supuesto que se hizo por falta de informacion, con su motivo y como se revisa.

| # | Supuesto | Motivo | Como se revisa |
|---|---|---|---|
| 1 | El nombre del producto en el titulo gigante del hero es el nombre corto del equipo, no "riesgo sismico" | El enunciado no fija nombre de producto | Cuando el equipo lo defina: se cambia solo el string, no la composicion |
| 2 | La escala de riesgo es **bajo / medio / alto** | El plan define la clasificacion en tres clases | Si el gate de clases de las 8:45 cambia los umbrales, cambia el contrato JSON, no los tokens |
| 3 | Archivo e IBM Plex como familias | Elegidas por registro tecnico cientifico y por no ser los valores por defecto | Si no hay red durante la demo, hay fallback de sistema declarado en el CSS |
| 4 | Contenedor de 1280px | Ancho de lectura comodo para tablas densas sin desplazamiento horizontal | Se ajusta en el token `--container` |
| 5 | Las cifras de sismicidad se marcan como `[DATO A VERIFICAR CON SGC]` | Ninguna cifra de sismicidad esta verificada contra el SGC en el momento de escribir esto | Se sustituyen por el dato real cuando Nico entregue `serie_mensual.json` con procedencia |
| 6 | El mapa usa circulos en el centroide, no poligonos | El contrato solo entrega centroides de 87 municipios; la geometria municipal oficial aun no esta | Si llega la geometria, se cambia la capa, no los tokens |
| 7 | El puente de agente se presenta como un formulario con corte y K | El plan define nivel 1 (replay) y nivel 2 (puente local), no la interfaz | Cuando Zabdiel defina la forma del endpoint, se ajusta el formulario |
| 8 | La eleccion de K se limita a valores entrenados | El plan prohibe mover K a un valor no entrenado y llamarlo el mismo agente | Si Zabdiel entrena mas valores, se agregan al select |
| 9 | Las zonas de apoyo del mapa se marcan con contorno discontinuo | No hay en el contrato una categoria "dato incompleto"; se crea por necesidad de no mentir | Si el JSON trae el campo, se usa el campo y no la convencion visual |
| 10 | La doble magnitud del evento de 2015 se muestra siempre como par | El plan exige citar USGS y SGC por separado y nunca promediar | No cambia: es una decision metodologica del plan |
| 11 | El espacio del logo del SGC queda reservado y vacio | El plan prohibe usar el logo sin autorizacion | Si hay permiso escrito, se coloca con credited source visible |
| 12 | Las secciones de Metodologia se agrupan en un unico acordeon y no en subrutas | Una sola ruta menos que mantener con el tiempo disponible | Si queda tiempo, se separan en subrutas |
| 13 | Se asume que existe al menos un JSON de ejemplo antes de las 8:45 | La linea de tiempo asigna a Julian construir la UI con datos de forma a las 8:10 | Si no hay ningun JSON, la UI debe mostrar el estado vacio, que ya esta especificado en 4.13 y 5.2 |
| 14 | El modo presentacion no lleva barra de navegacion propia | Los 10 minutos se dan sobre la web a pantalla completa | Si se necesita referencia a rutas, se usa el indice de secciones del contador |

---

## 10. Nota sobre el alcance

Este documento define la identidad visual y las reglas de interfaz. **No define el
producto**: que se calcula, con que datos y con que validacion esta en
`docs/plan/08-reto-oficial-plan-4h.md`, `docs/research/09-rl-diseno.md` y en el
contrato de datos de `docs/plan/10-roles-web-presentacion.md` (seccion 4).

Si una duda de diseno choca con el contrato de datos, **manda el contrato** y se avisa
por Engram uts con `topic_key` `ciai/datos/contrato-json`. Si una duda de diseno choca
con la regla metodologica del plan, **manda el plan**: esta interfaz no puede sugerir
certeza donde el modelo no la tiene.
