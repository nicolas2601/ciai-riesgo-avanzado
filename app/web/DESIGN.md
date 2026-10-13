# DESIGN.md: sistema visual de la web de analisis sismico

Fuente unica de verdad visual para `app/web/`. No se toman decisiones de color,
tipografia, espacio ni movimiento que no esten declaradas aqui.

Esto **no** es el sitio del evento: es la aplicacion de analisis que **es** la
presentacion del equipo. Alcance funcional en
`docs/plan/10-roles-web-presentacion.md` (secciones 4 y 5).

---

## 1. Concepto

**Cajon claro, lectura seria.** Un documento editorial que contiene un laboratorio de
lectura sismica. Nada-catastrofismo: esto trata datos.

Publico: jurado, estudiantes e ingenieros de sistemas y ciencia de datos. Idioma de la
interfaz: espanol (Colombia).

**Tono de voz:** tecnico, claro, sin sensacionalismo. La app nunca dice "alerta", nunca
dice "peligro", nunca dice "prediccion de un sismo". Dice **"priorizacion
exploratoria"**. El mismo termino para la misma cosa en todo el producto.

**Modo claro, en todo el sitio.** Incluido el mapa. No hay panel oscuro ni isla
instrumento: un solo sistema de color sobre fondo claro.

**Motivo visual:** la onda sismica, como textura de fondo de baja opacidad y como
divisor. Nunca como ilustracion ni como animacion continua.

### 1.1 La idea memorable

La **maquina del tiempo**: un riel de cortes mensuales que se arrastra y muestra que
habria priorizado el agente **antes** de los sismos de referencia, contra lo que
realmente paso. Es el unico elemento con movimiento protagonista. Todo lo demas, sobrio
y estatico por decision.

---

## 2. Referencias: que se toma y que se descarta

| Referencia | Se toma | Se descarta | Por que |
|---|---|---|---|
| **Anna K**<br>crema + cobalto | Disciplina de dos colores (tinta + un cobalto). Titular display partido en dos lineas. Filete de 2px como separador. Numeracion 01/02/03. Servicios y proceso en dos columnas. | Retrato, firma manuscrita, crema calido, banda de pie a sangre | La disciplina de dos colores es lo transfersible. El crema amarillea los colores de nivel. El retrato es contenido de portafolio. |
| **Aarav Singh**<br>vidrio perlado lavanda | Frosting en superficies flotantes. Chip de cifra. Boton en pildora. Icono en cuadro redondeado. | Degradado lavanda de fondo, objetos 3D de vidrio, texto diminuto de bajo contraste | El frosting sobre un mapa claro da profundidad sin ruido. El lavanda de fondo no: ensucia el dato. |
| **Design Futures**<br>blanco + lima | Titular en tipografia extendida con una linea en color. Micro-etiqueta con tracking amplio y bullet cuadrado. Franja de cifras con filetes. Flecha circular. | **El lima como color de interfaz** | Todo menos el color. El lime es verde: **se lee como nivel "Bajo"**. Un acento no puede parecerse a un riesgo. |

### 2.1 Contradicciones resueltas

1. **Claro vs. oscuro.** Las tres referencias son claras. **Todo claro**, incluido el
   mapa. Se evaluo un panel oscuro tipo instrumento para el mapa y **quedo descartado**:
   no es lo que pide el producto y obliga a mantener dos juegos de la escala de riesgo.
   Un solo sistema de color.
2. **Acento vs. escala de riesgo.** Acento **cobalto `#2438C8`**. La escala va
   teal -> ambar -> carmesi, deliberadamente **sin ningun azul**, para que el cobalto
   nunca se lea como riesgo. El lima de la referencia 3 se descarta por esto.
3. **Mayusculas y tracking.** Si, de forma acotada: hero display y micro-etiquetas de
   una a tres palabras. **Nunca** en parrafos, cifras ni datos.
4. **Vidrio vs. AA.** Frosting solo en superficies flotantes (navbar, panel de mapa,
   panel de detalle), con texto AA verificado. El contenido va con borde solido.
5. **Contenido de portafolio.** No hay retratos, testimonios, "servicios" ni cifras de
   relleno. Si una cifra no viene del JSON, no existe.
6. **Tres heroes.** Uno: el hero tipografico editorial. El momento con movimiento es la
   maquina del tiempo. Nada mas se mueve solo.

---

## 3. Tokens

### 3.1 Color base

Fondo casi blanco **frio** (nunca crema calido, nunca `#FFFFFF` como fondo global).

| Token | Hex | Rol | Contraste verificado |
|---|---|---|---|
| `--shell` | `#F6F7F9` | Fondo del documento | — |
| `--surface` | `#FFFFFF` | Tarjetas, tablas, paneles | — |
| `--inset` | `#ECEEF2` | Campos, hover de fila, celda de codigo | — |
| `--ink` | `#101418` | Texto primario | 17.26 sobre shell / 18.50 sobre surface (AAA) |
| `--ink-2` | `#414B59` | Texto secundario | 8.25 / 8.84 (AAA) |
| `--ink-3` | `#5A6472` | Metadatos, unidades, notas al pie | 5.60 sobre shell / 5.16 sobre inset (AA) |
| `--accent` | `#2438C8` | Cromo: enlaces, filete, foco, control activo | 7.92 sobre shell / 8.49 sobre surface (AAA) |

Derivados del acento: `--accent-hover` `#1B2EA3`, `--accent-press` `#16258A`,
`--accent-quiet` `rgba(36,56,200,0.08)`, `--focus-ring` `#2438C8`.

**Regla dura:** el acento **nunca** es relleno de un nivel de riesgo ni de una serie de
datos. Es cromo. Si el azul aparece junto a un nivel, significa "interfaz", no "riesgo".

Estados: `--danger` `#B91C1C` (6.47 AA) · `--warning` `#A85B00` (5.05 AA) ·
`--success` `#047857` (5.48 AA).

### 3.2 Escala de riesgo

**El nivel nunca se comunica solo con color:** color + icono + etiqueta de texto, siempre.
No se usa rojo contra verde como unico par.

| Nivel | Texto y anillo | Relleno de mapa | Icono (lineal, 1.5px) | Etiqueta |
|---|---|---|---|---|
| Bajo | `#0E7490` (5.36) | `#A1C5D1` | circulo con punto interior | "Bajo" |
| Medio | `#A85B00` (5.05) | `#D6BDA0` | triangulo con barra interior | "Medio" |
| Alto | `#C01038` (6.23) | `#DEA3B3` | rombo con corte diagonal | "Alto" |
| Sin dato | `#5A6472` (6.00) | `#BBC0C6` | circulo con guion, borde discontinuo | "Sin dato" |
| Sin priorizacion | `#8A6D3B` (5.72) | `#CBC3B4` | circulo con puntos, trama diagonal | "Sin priorizacion" |

**Como se lee el mapa, y por que el relleno NO carga el significado:**

- El relleno es el color de nivel al **34%** sobre el basemap `#EDEFF2`. Se separa del
  basemap en 1.57 a 1.82:1.
- El **anillo de 2px al 100%** carga la lectura: se separa del propio relleno en 2.55 a
  3.00:1.
- La **etiqueta de texto al 100%** es el contenedor de la garantia AA.

Por que esta division: sobre fondo claro, un relleno al 100% tapa la geografia y uno al
10% desaparece. Concentrar el contraste en el anillo y la etiqueta es lo que permite un
mapa claro legible, y ademas coincide con la regla de que el significado va con texto.

**"Sin dato" y "Sin priorizacion" no son "Bajo".** Tokens, iconos y texturas propios. Es
el error de comunicacion mas grave posible en esta app y esta prohibido visualmente.
"Sin dato" usa borde discontinuo; "Sin priorizacion" usa trama diagonal.

### 3.3 Tipografia

Dos familias mas una monoespaciada, de Google Fonts.

| Rol | Familia | Uso |
|---|---|---|
| Display | **Bricolage Grotesque** (variable, `wght` + `wdth`) | Hero, titulos de seccion, cifras destacadas |
| Cuerpo | **IBM Plex Sans** | Parrafos, tablas, etiquetas, botones |
| Datos | **IBM Plex Mono** | Magnitudes, coordenadas, cortes, versiones |

Por que: Bricolage tiene terminales asimetricos y eje de ancho, y aporta el caracter
editorial sin caer en la tipografia por defecto de un dashboard. IBM Plex trae el
registro de documentacion tecnica y es excelente a 13 px. Plex Mono comparte esqueleto
con el cuerpo, asi que cifras y etiquetas se sienten de la misma familia.

Se descarto Archivo por ser el par que se pondria en cualquier dashboard.

| Token | Tamano | Peso | Interlineado | Tracking | Uso |
|---|---|---|---|---|---|
| `--t-hero` | `clamp(3rem, 10vw, 8.5rem)` | 800 | 0.88 | -0.03em | Hero display, mayusculas |
| `--t-display` | `clamp(1.75rem, 4vw, 3rem)` | 700 | 1.05 | -0.02em | Titulo de seccion |
| `--t-title` | `1.3125rem` | 600 | 1.25 | -0.01em | Titulo de tarjeta y panel |
| `--t-body-lg` | `1.0625rem` | 400 | 1.55 | 0 | Parrafo introductorio |
| `--t-body` | `1rem` | 400 | 1.6 | 0 | Cuerpo |
| `--t-small` | `0.875rem` | 400 | 1.5 | 0 | Texto secundario |
| `--t-label` | `0.8125rem` | 500 | 1.35 | 0 | Etiqueta de campo, columna |
| `--t-eyebrow` | `0.6875rem` | 600 | 1.3 | 0.16em | Micro-etiqueta en mayusculas |
| `--t-data` | `0.9375rem` | 500 | 1.4 | 0.01em | Cifra en mono |
| `--t-data-lg` | `1.75rem` | 600 | 1.15 | -0.01em | Cifra destacada |
| `--t-micro` | `0.75rem` | 500 | 1.4 | 0.02em | Nota al pie, unidad |

**Hero display.** Mayusculas, `wdth 125`, partido en dos lineas con la segunda completa en
`--accent`. Una sola vez por vista. Nunca mas de tres palabras en total. **Nunca se
resalta una palabra suelta**: la segunda linea va entera en acento o ninguna.

**Eyebrow.** `--t-eyebrow`, en mayusculas con tracking `0.16em`, en `--ink-3`, con bullet
cuadrado en `--accent` delante. Solo si aporta informacion: el nombre de la seccion.
Nunca en parrafos ni en datos.

**Reglas generales.** Ancho de linea de cuerpo **maximo 72 caracteres** (tablas y codigo,
hasta 90). Cifras siempre en mono con su unidad: `M 6,2`, no `M6,2` suelto. Separador de
miles con punto y decimal con coma. Toda cifra lleva su fuente debajo.

### 3.4 Espaciado, radios, bordes, sombras

**Espaciado** (base 4px), tokens `--s-1` a `--s-10`: `4, 8, 12, 16, 24, 32, 48, 64, 96,
128`. Ritmo vertical entre secciones: `--s-10` (128px) en escritorio, `--s-7` (48px) en
movil.

**Radios.** No uno solo para todo: un unico radio es el sintoma del "kit de tarjetas".

| Token | Valor | Uso |
|---|---|---|
| `--r-sharp` | `4px` | Chips, celdas de matriz, marcas de corte |
| `--r-control` | `8px` | Botones, campos, selectores |
| `--r-card` | `14px` | Tarjetas de contenido |
| `--r-panel` | `18px` | Superficies flotantes: mapa, detalle, navbar |
| `--r-pill` | `999px` | Solo CTA en pildora y badge |

**Bordes.** `1px solid #E2E6EC` por defecto. `2px solid --accent` en el filete de seccion
y en el lado izquierdo del estado activo. `2px solid --focus-ring` en el anillo de foco.
Los bordes son decorativos: **nunca** portan informacion solos.

**Sombras.** Tres, y ninguna es decorativa repetida en todas las tarjetas.

| Token | Valor | Uso |
|---|---|---|
| `--shadow-card` | `0 1px 2px rgba(16,20,24,.05), 0 4px 12px rgba(16,20,24,.04)` | Tarjeta en reposo |
| `--shadow-lift` | `0 4px 8px rgba(16,20,24,.07), 0 12px 28px rgba(16,20,24,.09)` | Hover de tarjeta |
| `--shadow-float` | `0 8px 28px rgba(16,20,24,.12), 0 2px 6px rgba(16,20,24,.06)` | Navbar, panel de mapa, panel de detalle, modal |

**Frosting (vidrio perlado).** Solo superficies flotantes, donde hay algo detras que
aporta: fondo `rgba(255,255,255,0.80)`, `backdrop-filter: blur(20px) saturate(160%)`,
borde `1px solid rgba(255,255,255,0.9)`, radio `--r-panel`, sombra `--shadow-float`.
Contraste de `--ink` sobre frosting con mapa detras: **13.90:1** (AAA). Si el frosting
queda sobre una zona cargada del mapa, la opacidad sube a `0.92`.

**z-index.** `--z-base` 0 · `--z-sticky` 100 · `--z-header` 200 · `--z-panel` 300 ·
`--z-modal` 400 · `--z-toast` 500 · `--z-tooltip` 600.

### 3.5 Grid y alineacion

Contenedor maximo `1280px`, 12 columnas, gutter `24px` (16px en movil), padding lateral
`32px` / `20px` / `16px`.

| Breakpoint | Ancho | Composicion |
|---|---|---|
| `mobile` | `< 640px` | Una columna. Mapa a 60vh. Maquina del tiempo a ancho completo. |
| `tablet` | `640-1023px` | 8 columnas utiles; tarjetas de dos en dos. |
| `desktop` | `1024-1439px` | 12 columnas; mapa y detalle en `7/5`. |
| `wide` | `>= 1440px` | Contenedor centrado a 1280; mapa en `8/4`. |

**Alineacion: todo a la izquierda.** Solo el hero y los estados vacios se centran. Nada
justificado: en columnas angostas es ilegible. Prueba obligatoria a **1440px y 390px**.

### 3.6 El mapa en claro

- **Basemap claro obligatorio**, tonos claros y desaturados. Estilo vectorial o raster.
  **Prohibido** un basemap oscuro: romperia el modo unico de color y competiria con la
  escala de riesgo.
- Calles y limites en `--border-strong` `#C9D0DA`, **nunca en negro**: el negro puro
  vibra sobre blanco y compite con la tinta.
- **Nombres de municipio del basemap ocultos.** El nombre lo pone la interfaz, no el mapa.
  Se habilitan solo al hacer zoom-out.
- Circulos con **halo blanco de 2px** para separarse de cualquier color del basemap.
- Los 87 municipios son **centroides**, no poligonos: `municipios_santander.json` solo
  trae `zone_id`, `municipality`, `lat`, `lon`. El tamano del circulo codifica el score,
  el color codifica el nivel.
- MapLibre GL **excluido del pre-empaquetado** de Vite (ya esta en `vite.config.ts`). Sin
  eso el mapa sale en blanco con "Worker failed to load".

---

## 4. Componentes

Siete. Todos con default, hover, focus, active, disabled.

### 4.1 Navbar

Altura `68px`, frosting, borde inferior `--border-hairline`. Marca del equipo a la
izquierda, navegacion en el centro, **snapshot en mono** (`model_version`, `data_version`)
y boton de modo presentacion a la derecha.

| Estado | Comportamiento |
|---|---|
| default | Frosting, enlaces en `--ink-2` |
| hover | Enlace a `--ink`; subrayado crece de 0 a 100% en 140ms |
| focus | Anillo `--focus-ring` de 2px, desplazamiento 2px, **nunca removido** |
| active | Subrayado 2px en `--accent`, texto `--ink`, `aria-current="page"` |
| disabled | No aplica |

Al hacer scroll, el frosting pasa a `rgba(255,255,255,0.94)` y suma `--shadow-float` en
220ms.

### 4.2 Boton primario

Pildora, alto `46px`, padding `20px 26px`, flecha circular a la derecha. Etiqueta en verbo
concreto: "Ver la priorizacion", "Ejecutar agente", "Reproducir resultado guardado".
Nunca "Enviar" ni "Mas informacion".

| Estado | Fondo | Texto | Transform |
|---|---|---|---|
| default | `--accent` | `#FFFFFF` | — |
| hover | `--accent-hover` | `#FFFFFF` | `translateY(-1px)` |
| focus | `--accent` + anillo 2px | `#FFFFFF` | — |
| active | `--accent-press` | `#FFFFFF` | `translateY(0) scale(0.98)` |
| disabled | `--inset` | `--ink-3` | opacidad 0.7, `cursor: not-allowed` |

### 4.3 Chip de cifra

Superficie blanca, borde `--border-hairline`, radio `--r-card`, sombra `--shadow-card`.
Cifra en mono `--t-data-lg` + etiqueta en `--t-small`.

- Si el valor es `null`: muestra **"—"** en `--ink-3` con etiqueta "no disponible".
  **Nunca `0`**.
- Si el JSON trae `"ejemplo": true`, lleva el badge de advertencia.
- Maximo tres en el hero.

Estados: `default` · `hover` (borde `--border-strong`, sombra `--shadow-lift`) · `focus` ·
`disabled` (cifra en `--ink-3`) · `sin-dato` (el de arriba, que es un estado de dato, no
visual).

### 4.4 Tarjeta de nivel

Chip con **icono + etiqueta de texto + color**, siempre los tres. Variante `solida`
(fondo al 12% del color, texto al 100%) para mapa y listas; variante `contorno` (borde al
45%) para tablas densas.

Estados: `default` · `hover` · `focus` · `active` · `disabled`, y en `disabled` se
convierte en "Sin priorizacion", **nunca oculta el nivel**.

### 4.5 Bloque de dato con fuente

Cifra grande en mono, unidad y definicion en `--t-small`, y **fuente debajo en
`--t-micro` `--ink-3`**: origen, fecha de descarga y filtros. Sin la linea de fuente el
bloque no se implementa: toda cifra publicada sale de un JSON con procedencia.

Si no esta verificado contra el SGC, se renderiza `[DATO A VERIFICAR CON SGC]` con estilo
`warning`, nunca como numero.

### 4.6 Fila de tabla de priorizacion

Puesto, municipio, agente, linea base, oraculo, que paso despues. El municipio es enlace
al mapa. Fila activa con `--accent-quiet` y filete 2px en `--accent` a la izquierda.

Estados: `default` · `hover` (`--accent-quiet`) · `focus` (anillo en la celda del
municipio) · `active` · `disabled`.

**Es tambien el equivalente textual del mapa.** No es un extra de accesibilidad: es la
forma en que la vista se lee sin ver color, y por eso debe existir siempre y ser
navegable por teclado.

### 4.7 Control del puente de agente

Campos en `--inset`, borde `--border-hairline`, radio `--r-control`.

| Campo | Tipo | Validacion | Error |
|---|---|---|---|
| Corte | Select de meses disponibles | Obligatorio; debe existir en `serie_mensual.json` | "Ese corte no esta en los datos" |
| K | Select de valores **entrenados** | Obligatorio; solo los declarados por Zabdiel | "K no entrenado: exige otra politica" |
| Modelo | Radio: agente / linea base / oraculo | Obligatorio | — |

Dos botones **separados y rotulados distinto**:

- Primario **"Ejecutar agente"**: ejecucion en vivo por el puente local. Es inferencia
  nueva.
- Secundario **"Reproducir resultado guardado"**: replay desde `priorizacion.json`.
  **No es inferencia nueva**, y la interfaz lo dice.

Presentarlos juntos sin distinguirlos seria un error metodologico, no de diseno.

Estados de campo: `default` · `hover` · `focus` (anillo 2px, borde `--accent`) · `active`
· `disabled` (durante la ejecucion) · `error` (borde `--danger`, mensaje `--danger`,
`aria-invalid="true"`). El boton pasa a `disabled` con texto "Ejecutando...".

### 4.8 Banner de datos de ejemplo

Barra fija bajo la navbar: fondo `--warning` al 10%, texto `#7C2D12`, borde inferior
`1px solid rgba(168,91,0,0.28)`, icono de alerta, texto: **"Datos de ejemplo: no son
resultados reales."**

- Aparece mientras exista un JSON con `"ejemplo": true`.
- En modo presentacion es una franja propia y **no se puede cerrar**.
- Mientras este visible, ranking y alertas no se presentan como reales: los chips
  muestran "—" cuando el valor es `null`, y la priorizacion rotula "conjunto de ejemplo".

### 4.9 Footer

Cuatro columnas sobre `--shell`, con filete superior de 2px en `--accent`: equipo;
fuentes con URL y fecha; diccionario y metodologia; aviso de alcance ("priorizacion
exploratoria, no alerta oficial") y versionado.

Se descarto la banda de color a sangre de la referencia 1: compite con el contenido real
que vive en el pie, que es procedencia y limites.

Espacio reservado y marcado para logos de aliados. **No** se usa el logo del SGC sin
permiso escrito.

---

## 5. Estructura

| Ruta | Vista | Que debe lograr |
|---|---|---|
| `/` | Panorama | Estado del experimento y entrada a las vistas |
| `/mapa` | Mapa | 87 municipios por nivel o grupo, con selector de mes |
| `/priorizacion` | Priorizacion | K del agente frente a lineas base, oraculo y resultado real |
| `/tiempo` | Maquina del tiempo | Que habria priorizado el agente antes de los sismos de referencia |
| `/grupos` | Grupos | Perfil de cada cluster del Medio, leido en palabras |
| `/metodologia` | Metodologia y datos | Fuentes, diccionario, validacion cronologica, incertidumbre, limites |
| `/presentacion` | Modo presentacion | Pitch a pantalla completa con flechas |

### Panorama

```
+--------------------------------------------------------------+
| NAVBAR        ¿que sabe?  ¿que eligio?  ¿acerto?   [Modo]    |
+--------------------------------------------------------------+
|                                                              |
|  SISMO,               <- hero display, mayusculas,          |
|  NO PREVISIBLE           wdth 125, linea 2 en cobalto       |
|                                                              |
|  -- DATOS OFICIALES DEL SGC --        <- eyebrow + filete    |
|                                                              |
|  [ 87 ]      [ 5 ]       [ - ]      <- chips del JSON       |
|  MUNICIPIOS   K          F1            "-" si es null        |
|                                                              |
|  QUE SABE LA MAQUINA --                                    |
|  +------------+ +------------+ +------------+               |
|  | Riesgo por | | El agente  | | Incertidum|                |
|  | municipio  | | eligio K   | | bre       |                 |
|  +------------+ +------------+ +------------+               |
|                                                              |
|  -- QUE NO ES -------------------------------------         |
|  No es alerta oficial. No es severidad. [acordeon]          |
+--------------------------------------------------------------+
```

Las tarjetas de acceso son **tarjetas de contenido** (borde solido, `--r-card`), no
tarjetas de portafolio: sin flecha decorativa, sin icono de color, sin resplandor. La
altura la fija el contenido; no se estiran a una altura comun.

### Mapa

```
+--------------------------------------------------------------+
| NAVBAR                                                     |
+--------------------------------------------------------------+
|  [ frosting: filtro de mes | amenaza | nivel | grupo ]       |
|                                                              |
|            +-------------------------------------+          |
|            |   basemap claro #EDEFF2             |          |
|            |                                     |          |
|            |        o        O                   |          |
|            |   (Bajo)   (Medio)     <>           |          |
|            |   (Alto)              (Alto)         |          |
|            |                                     |          |
|            |   +------------------+              |          |
|            |   | DETALLE          | <- frosting,  |          |
|            |   | Bucaramanga      |    flota      |          |
|            |   | <> Alto          |              |          |
|            |   | conjunto de      |              |          |
|            |   | prediccion:      |              |          |
|            |   | {alto, medio}    |              |          |
|            |   | abstencion:      |              |          |
|            |   | soporte bajo     |              |          |
|            |   | [Ejecutar agente]|              |          |
|            |   +------------------+              |          |
|            +-------------------------------------+          |
|                                                              |
|  TABLA EQUIVALENTE (siempre presente, navegable con teclado)|
+--------------------------------------------------------------+
```

Mapa y detalle en `7/5` en escritorio; en `mobile` el mapa pasa a 60vh y el detalle baja
como hoja.

### Maquina del tiempo (el momento)

```
+--------------------------------------------------------------+
| NAVBAR                                                     |
+--------------------------------------------------------------+
|                                                              |
|  2019    2020    2021    2022    2023    2024    2025       |
|   |       |       |       |       |       |       |         |
|   |       |       |       |       v       |       |         |
|   |       |       |       |    sismo ref.   |       |        |
|  ================================================================ |
|                ^                                            |
|         cabeza arrastrable                                  |
|                                                              |
|  +-------------------+   +----------------------------+     |
|  | QUE HABRIA        |   | QUE PASO                   |     |
|  | PRIORIZADO        |   |                            |     |
|  |                   |   | Cepita, 2015-03-10        |     |
|  | 01 Bucaramanga    |   | M 6,2 (USGS)               |     |
|  | 02 Surata         |   | M 6,6 (SGC)                |     |
|  | 03 Barrancaberme  |   |                            |     |
|  |                   |   | el agente lo puso 03       |     |
|  +-------------------+   +----------------------------+     |
|                                                              |
|  mapa del corte, 87 circulos, sincronizado                  |
|                                                              |
|  VISTA DE TABLA EQUIVALENTE (teclado)                       |
+--------------------------------------------------------------+
```

La cabeza del riel es lo unico que se arrastra. Al cruzar un sismo de referencia, el
rombo se enciende **una vez**, aparece el panel de la derecha y el mapa recolorea al
corte. La doble magnitud se muestra siempre como par y **nunca se promedia**.

---

## 6. Movimiento

Movimiento que muestra **que cambio**. Nada se mueve porque si.

| Transicion | Duracion | Easing |
|---|---|---|
| Hover de control | 140ms | `cubic-bezier(0.2,0,0,1)` |
| Apertura de panel | 180ms | `cubic-bezier(0.2,0,0,1)` |
| Cambio de corte en la maquina del tiempo | 420ms | `cubic-bezier(0.4,0,0.2,1)` |
| Recalculo de la rejilla del mapa | 260ms | `ease-out` |
| Aviso emergente | 180ms entrada / 140ms salida | `cubic-bezier(0.2,0,0,1)` |

**Permitido:** pulso del punto de epicentro activo (4s, un solo punto, nunca todos);
trazado de la onda del hero una vez al cargar, no en bucle; `translateY(-2px)` en hover
de tarjeta.

**Prohibido:** entrada "fade and slide up" en cada seccion al hacer scroll; transicion en
cada tarjeta al pasar el mouse; parallax; animacion continua de fondo; contadores que
cuentan desde cero.

**`prefers-reduced-motion: reduce`:** transiciones y animaciones a `0.01ms`; el pulso se
desactiva; la onda del hero se muestra ya dibujada; el riel cambia de corte de inmediato;
**ninguna informacion queda oculta esperando a una animacion**.

---

## 7. Accesibilidad y rendimiento

Todos los pares declarados cumplen WCAG 2.1 AA, con la formula de contraste verificada.

| Par | Ratio | Nivel |
|---|---|---|
| `--ink` sobre `--shell` | 17.26 | AAA |
| `--ink` sobre `--surface` | 18.50 | AAA |
| `--ink-2` sobre `--shell` | 8.25 | AAA |
| `--ink-3` sobre `--shell` | 5.60 | AA |
| `--ink-3` sobre `--inset` | 5.16 | AA |
| `--accent` sobre `--shell` | 7.92 | AAA |
| `#FFFFFF` sobre `--accent` | 8.49 | AAA |
| Bajo `#0E7490` sobre surface | 5.36 | AA |
| Medio `#A85B00` sobre surface | 5.05 | AA |
| Alto `#C01038` sobre surface | 6.23 | AA |
| Sin priorizacion `#8A6D3B` sobre surface | 5.72 | AA |
| `--ink` sobre frosting con mapa detras | 13.90 | AAA |

Limites declarados, sin adornos:

- Los bordes `#E2E6EC` quedan en **1.25:1**. Intencional: son decorativos. Un borde que
  deba comunicar algo sube a `--border-strong` y se acompana de texto o icono.
- El relleno de mapa se separa del basemap en 1.57-1.82:1 y el anillo del relleno en
  2.55-3.00:1. **El significado lo carga la etiqueta de texto**, no el relleno.
- Los tres niveles tienen luminosidad parecida. **No se declara conformidad de
  daltonismo por el color**: la garantizan el icono y la etiqueta, que son obligatorios.

Reglas: foco visible siempre (anillo 2px, nunca eliminable) · navegacion completa por
teclado, incluido el modo presentacion (`←`, `→`, `Espacio`, `Esc`) · objetivo tactil
minimo **44x44px** · `lang="es-CO"` · el mapa tiene equivalente textual (la tabla de
priorizacion) y la maquina del tiempo tiene vista de tabla.

**Rendimiento:** JS inicial de `/` ≤ 200 KB gzip · build total ≤ 400 KB gzip · texto del
hero o textura de onda ≤ 180 KB · iconos SVG inline, nunca fuente de iconos · basemap ≤
120 KB por tesela, sin tiles 3D · los 87 municipios como circulos mientras no haya
geometria.

Si no hay red durante la demo, las fuentes tienen **fallback de sistema declarado** en el
CSS y preferiblemente se sirven localmente.

---

## 8. Hacer / no hacer

**Hacer**

- Mostrar la incertidumbre junto al nivel: conjunto de prediccion y abstencion con su
  motivo, en la misma vista.
- Mostrar el snapshot (`model_version`, `data_version`, `target_month`,
  `feature_cutoff`) de forma discreta pero siempre presente.
- Poner la fuente bajo cada cifra: origen, fecha de descarga, filtros.
- Marcar `[DATO A VERIFICAR CON SGC]` lo que no este verificado.
- Rotular por separado la ejecucion en vivo y el replay.
- Probar a 1440px y 390px antes de dar por cerrada una vista.

**Evitar**

- **No** inventar cifras. Si el JSON no trae el dato, la interfaz dice que no lo trae. Un
  `0` de mas es una mentira metodologica.
- **No** mostrar un nivel sin su incertidumbre al lado.
- **No** codificar un nivel solo con color, ni usar rojo contra verde como unico par.
- **No** confundir "sin dato" ni "sin priorizacion" con "Bajo".
- **No** usar basemap oscuro, ni fotos de desastres, ruinas, grietas o imagenes de
  emergencia. Esto trata datos, no catastrofismo.
- **No** usar ni sugerir el logo del SGC.
- **No** decir "alerta", "peligro" ni "prediccion de un sismo".
- **No** usar tarjetas de portafolio: sin flecha decorativa, sin icono de color con
  resplandor, sin franja de logos de clientes.
- **No** repetir la misma sombra suave en todas las tarjetas.
- **No** usar un unico radio en toda la interfaz.
- **No** subir el acento cobalto como relleno de un nivel de riesgo o de una serie.
- **No** poner el acento en mayusculas con tracking en parrafos ni en datos.
- **No** ocultar informacion detras de una animacion.
- **No** anadir funciones despues de las 11:45.

---

## 9. Supuestos

| # | Supuesto | Motivo | Como se revisa |
|---|---|---|---|
| 1 | Modo claro en todo el sitio, incluido el mapa | Las tres referencias son claras; el panel oscuro se evaluo y se descarto | Reversible: los tokens estan agrupados |
| 2 | Un solo acento cobalto `#2438C8` sobre tres acentos distintos de las referencias | El lima se lee como nivel Bajo; el lavanda confunde con incertidumbre | Si el mapa pasa a poligonos, se reevalua |
| 3 | La escala de riesgo es bajo / medio / alto | El plan define tres clases | Si el gate de las 8:45 cambia los umbrales, cambia el contrato JSON, no los tokens |
| 4 | El relleno del mapa no porta el significado; lo portan el anillo y la etiqueta | Sobre claro, un relleno al 100% tapa la geografia y uno al 10% desaparece | Si llega geometria, se reevalua el reparto |
| 5 | El titulo del hero es el nombre corto del equipo | El enunciado no fija nombre de producto | Se cambia el string, no la composicion |
| 6 | Bricolage Grotesque + IBM Plex | Caracter editorial y registro tecnico, y no son el par por defecto | Si no hay red, hay fallback de sistema declarado |
| 7 | Contenedor de 1280px | Ancho comodo para tablas densas sin scroll horizontal | Se ajusta en el token |
| 8 | Las cifras de sismicidad se marcan `[DATO A VERIFICAR CON SGC]` | Ninguna esta verificada contra el SGC al escribir esto | Se sustituyen cuando llegue `serie_mensual.json` con procedencia |
| 9 | El mapa usa circulos en el centroide | `municipios_santander.json` solo trae `zone_id`, `municipality`, `lat`, `lon`: no hay geometria | Si llega la geometria, cambia la capa, no los tokens |
| 10 | Los nombres del basemap se ocultan | El nombre lo pone la interfaz, no el mapa | Se habilitan al hacer zoom-out |
| 11 | El puente de agente es un formulario con corte y K | El plan define replay y ejecucion en vivo, no la interfaz | Cuando Zabdiel defina el endpoint, se ajusta |
| 12 | El select de K ofrece solo valores entrenados | Mover K a un valor no entrenado exige otra politica | Si Zabdiel entrena mas, se agregan |
| 13 | "Sin priorizacion" usa trama diagonal | El contrato no define esa categoria; se crea para no mentir | Si el JSON trae el campo, gana el campo |
| 14 | La doble magnitud del evento de 2015 se muestra siempre como par | El plan exige citar USGS y SGC por separado | No cambia: es regla metodologica |
| 15 | El espacio del logo del SGC queda reservado y vacio | El plan prohibe usarlo sin autorizacion | Si hay permiso escrito, se coloca con credited source |
| 16 | Grupos y Metodologia se documentan aqui pero se construyen al final | La linea de tiempo los situa despues de Mapa y Maquina del tiempo | Si sobra tiempo, se separan en subrutas |
| 17 | Se asume que existira al menos un JSON de ejemplo | La linea de tiempo asigna construir la UI con datos de forma a las 8:10 | Si no hay ninguno, se muestra el estado vacio |

---

## 10. Alcance

Este documento define la identidad visual y las reglas de interfaz. **No define el
producto**: que se calcula y con que validacion esta en
`docs/plan/08-reto-oficial-plan-4h.md`, `docs/research/09-rl-diseno.md` y en el contrato
de datos de `docs/plan/10-roles-web-presentacion.md` (seccion 4).

Si una duda de diseno choca con el contrato de datos, **manda el contrato** y se avisa por
Engram uts con `topic_key` `ciai/datos/contrato-json`. Si choca con una regla metodologica
del plan, **manda el plan**: esta interfaz no puede sugerir certeza donde el modelo no la
tiene.
