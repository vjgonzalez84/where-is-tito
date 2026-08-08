# Plan de Desarrollo: "¿Dónde está Tito?"

**Tipo de proyecto:** Aplicación web interactiva (desktop, tablet y smartphone)
**Estilo:** Búsqueda visual estilo *Where's Waldo?* — Tito, una mascota perdida, se esconde en 10 escenarios históricos ambientados por época.

> Este documento reemplaza un borrador previo generado con un modelo de menor calidad, que contenía dos matrices de escenarios contradictorias (una tabla histórica en la sección de dificultad y prompts de IA para temáticas distintas de fantasía/cyberpunk). Se resolvió la contradicción con el usuario: **la matriz histórica es la canónica**; los prompts de fantasía/cyberpunk se descartan.

## 0. Estado actual del repositorio

Ya existe un prototipo funcional de un solo archivo (`index.html`, ~310 líneas, JS vanilla sin dependencias) que cubre buena parte de la Fase 1:

| Implementado | Pendiente |
| :--- | :--- |
| Carga dinámica de nivel vía `fetch` a `levels/levelN.json` | Solo existe `level1.json`; faltan los 9 restantes |
| Pan y zoom con mouse y touch (drag, rueda, pinch-to-zoom) unificados vía Pointer Events | Zoom in máximo diferenciado por dispositivo (hoy fijo en 3.5x para todos) |
| Clamp de posición con rebote elástico (resistencia progresiva + snap-back animado) en los límites | |
| Minimapa con recuadro de viewport | Minimapa no es arrastrable/interactivo todavía |
| Barra superior con avatares de objetivos y estado "encontrado" | Sin transición automática al siguiente nivel tras ganar |
| Hitboxes en % (x/y/width/height) sobre el JSON | Hitboxes son `<div>` visibles (borde rojo punteado) — hoy están pensadas para calibración, deben ocultarse en producción |
| Modal de victoria | Sin selector de nivel / progreso persistente entre niveles |
| `imageSrc` de `level1.json` apunta a un placeholder de Picsum | Falta el arte final 4K de cada escenario |

Personajes ya definidos en `level1.json` y `assets/avatars/`:
- **Tito** (`tito_perdido.jpg`) — la mascota perdida, cuerpo de perro con gorro rojo/blanco y anteojos.
- **Lola** (`lola.jpg`) — humana, pelo rizado, campera azul con flores, una de las que busca a Tito.

Nota: `assets/avatars/asd` es un archivo vacío/basura de un commit anterior ("Create asd"); se puede eliminar cuando se limpie el repo.

## 1. Resumen del concepto

El jugador busca a **Tito**, una mascota perdida, dentro de escenarios históricos densamente ilustrados. Junto a Tito, otros personajes principales (empezando por **Lola**) también deben encontrarse en cada nivel — son quienes lo buscan o interactúan con la escena. El jugador hace clic/toca directamente sobre los personajes objetivo; al encontrar a todos, el nivel se completa y desbloquea el siguiente.

**Regla de identidad de personajes:** Tito, Lola y el resto de personajes principales **no cambian de vestuario por época**. El usuario provee las imágenes/modelos de estos personajes tal cual se ven hoy (perro con gorro rojo/blanco y anteojos; Lola con campera azul floral), y se insertan sin alterar en cada fondo durante la post-producción. Solo los **personajes secundarios de relleno** (la multitud de fondo generada por IA) se visten acorde a la época del escenario.

## 2. Interfaz de usuario (UI) y experiencia de juego

- **Barra superior (header de objetivos):** Rostros/avatares de los personajes a buscar, recortados en círculo. Al encontrar a un personaje recibe una marca visual (check + desaturado) — *ya implementado*.
- **Área principal de búsqueda (viewport):** Escenario en alta resolución, sin deformar la proporción de aspecto original.
  - *Desktop:* clic-y-arrastre, scroll, zoom con rueda de mouse — *ya implementado*.
  - *Dispositivos móviles:* touch drag + pinch-to-zoom, con rebote elástico en los límites — *ya implementado*.
- **Minimapa (esquina inferior izquierda):** Vista miniaturizada completa del escenario con recuadro verde que señala la porción visible. Debe poder arrastrarse para navegar — recuadro visual *implementado*, interactividad de arrastre *pendiente*.
- **Notificación de victoria (pop-up):** Mensaje animado "¡Ganador!" al completar la búsqueda, con opción de avanzar al siguiente nivel — modal base *implementado*, avance automático de nivel *pendiente*.

## 3. Especificaciones de lienzo, resolución y aspect ratio

- **Relación de aspecto canónica:** 16:9.
- **Resolución base de trabajo:** 3840 × 2160 px (4K UHD), para mantener nitidez al hacer zoom in de hasta 2x–4x en dispositivos móviles o pantallas 1080p.

## 4. Niveles de dificultad y matriz de escenarios

| Grupo de dificultad | Niveles / escenarios | Escala elementos | Densidad y dispersión | Visibilidad de objetivos | Negativos específicos del grupo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Fácil | 1. Egipto Antiguo · 2. Roma Antigua · 3. Edad Media | 1.0x | Baja cantidad de personajes y objetos. Mayor dispersión/espacio libre. | Cuerpo completo visible, sin obstrucciones principales. | `red and white striped clothing, red hats, densely packed crowd, overlapping figures, foreground objects covering the crowd` |
| Media | 4. Puerto Caribeño · 5. Ruta de la Seda · 6. Viejo Oeste | 0.9x | Cantidad media de personajes y objetos, menos espacio libre entre ellos. | Medio cuerpo visible, ligeramente camuflado entre la multitud. | `red and white striped clothing, large empty areas, isolated figures` |
| Alta | 7. París 1889 · 8. Años 20 (Jazz) · 9. Festival Hippie 60/70 | 0.8x | Alta densidad de personajes y objetos, muy poca dispersión. | Parcialmente ocultos: solo cara y alguna extremidad (ej. una mano). | `empty areas, sparse crowd, isolated figures, flat single-layer composition` (aquí el rojo/blanco **se busca**, como señuelo) |
| Muy alta | 10. Estación Espacial (futuro) | 0.7x | Saturación máxima, aglomeración continua. | Especialmente escondido: solo la cabeza visible (sin cuerpo). | `open space, gaps in the crowd, single-layer composition, calm or orderly arrangement` |

La columna de negativos aplica **además** de la lista negativa universal del §6. A cada nivel se le suma su propio negativo de anacronismos (ej. para Egipto: `modern clothing, phones, cars, electric lighting`), que se redacta junto al bloque variable.

`level1.json` hoy usa un placeholder Picsum de 3840×2160 — ya respeta la resolución base, falta reemplazar por el arte final de "Egipto Antiguo".

## 5. Lineamientos para inserción y ubicación de personajes principales

- **Definición por nivel:** cada mapa define la cantidad de personajes principales a buscar, con descripción de la acción/pose que realiza cada uno y su avatar para la barra superior.
- **Regla de dispersión máxima:** los personajes a buscar se distribuyen ampliamente por el mapa. Prohibido agruparlos en el mismo cuadrante o zona inmediata.
- **Integración con la escena:** cada personaje realiza una acción contextual coherente con la época (interactuando con un objeto o personaje secundario), respetando el nivel de visibilidad de la matriz de dificultad — pero sin alterar su vestuario/diseño base (ver regla de identidad en §1).

## 6. Metodología de generación de escenarios con IA y post-producción

Flujo híbrido para el arte de fondo en 4K de cada nivel:

1. **Generación del fondo base con IA:** prompts estandarizados en el estilo *Where's Wally?* (línea de tinta limpia, color plano sin sombras, croma medio, personajes de relleno vestidos según la época y con la densidad que marque el grupo de dificultad del §4), **sin incluir a Tito, Lola ni al resto de personajes principales** — esos se insertan a mano después.
2. **Upscale a 3840 × 2160:** el fondo sale del generador a resolución nativa (~1024–2048 px), así que se lleva a 4K con un upscale que reintroduce detalle (img2img por tiles o upscaler generativo), no con interpolación simple. Ver "Resolución" más abajo.
3. **Post-producción manual:** recién sobre el fondo ya en 4K se insertan las imágenes provistas de Tito, Lola y demás personajes principales, sin alterar su diseño, en ubicaciones estratégicas siguiendo la regla de dispersión.
4. **Calibración de hitboxes:** una vez posicionados en la escena final, se calculan sus coordenadas porcentuales exactas (`x`, `y`, `width`, `height`) y se registran en el JSON del nivel — el prototipo actual ya soporta este formato.

**El orden entre 2 y 3 no es negociable.** Un upscaler generativo repinta todo lo que toca: si los personajes principales ya estuvieran pegados, les alteraría el diseño — el gorro rojo/blanco, los anteojos, la campera floral de Lola — y eso viola la regla de identidad del §1. El fondo se sube de resolución primero, y los personajes se pegan después sobre un lienzo que ya no vuelve a pasar por ningún modelo.

De ahí se desprende un requisito sobre los assets: las imágenes de Tito y Lola tienen que venir ya en resolución suficiente para el lienzo final. Con la convención de hitbox de 5% × 8%, un personaje ocupa **192 × 173 px** a 4K, así que el recorte de origen debe superar ese tamaño con margen. Los archivos de `assets/avatars/` sirven para los círculos de la barra superior, pero no necesariamente como fuente para pegar en el escenario.

### Prompt estandarizado (plantilla)

Cada prompt se arma con un **bloque de estilo fijo** (idéntico en los 10 niveles, para que la serie sea visualmente coherente) más un **bloque variable** por nivel. Ambos **excluyen explícitamente a los personajes principales**.

**Bloque de estilo fijo — todo en positivo:**

> `A massive, detailed panoramic illustration of [ENTORNO], in the style of Martin Handford's Where's Wally. Crisp uniform black ink outlines, flat cel-style color fills under even ambient light, every surface a single solid tone. Highly polychrome but low-to-medium chroma watercolour palette: chalky beiges, dusty blues, muted greens and soft ochres dominate, with generous neutral ground areas between the figures. High-angle oblique bird's-eye view, near-orthographic with minimal perspective diminishment — figures at the top of the frame are nearly the same size as at the bottom. Wide 16:9 aspect ratio, artwork bleeding to all four edges. Every background figure fully drawn with distinct period clothing and readable facial features. Signage and inscriptions rendered as abstract decorative marks. Anonymous background crowd only.`

**Lista negativa universal — va en el campo `negative prompt`, no en el prompt:**

> `cast shadows, drop shadows, soft shading, gradients, ambient occlusion, glossy 3D render, cinematic lighting, depth of field, blur, bokeh, legible text, lettering, numerals, watermark, signature, frame, border, vignette, Wally, Waldo, blobby or featureless crowd filler, photorealism`

A esa lista se le suman los negativos del grupo de dificultad y los de anacronismo del nivel (columna del §4).

**Por qué duplicado.** El negativo es un campo aparte, no texto del prompt: en los modelos de difusión entra por *classifier-free guidance*, que calcula una predicción condicionada al positivo y otra al negativo y se aleja activamente de la segunda. Pero varios modelos actuales (autorregresivos tipo GPT-image o Gemini) **no tienen ese campo**, y ahí escribir "no shadows" dentro del prompt puede ser contraproducente, porque el token queda igual en el condicionamiento. Por eso cada restricción se expresa dos veces: en positivo dentro del prompt, que funciona en cualquier arquitectura (`flat cel-style fills under even ambient light` en vez de `no shadows`; `signage as abstract decorative marks` en vez de `no text`), y como lista negativa para los modelos que la soporten.

**El negativo crítico son las rayas rojas y blancas.** Al invocar el estilo *Where's Wally*, el modelo genera figuras a rayas rojo/blanco por su cuenta — es el rasgo más asociado a la serie. En los niveles fáciles eso camuflaría a Tito por accidente y rompe la curva de dificultad, así que va como negativo duro; en los niveles altos se buscan deliberadamente como señuelos. Es la misma palanca de contraste de la nota de estilo, implementada del lado negativo.

**Bloque variable por nivel:** `[ENTORNO]` de época y props + densidad de multitud + escala de figuras + capas oclusoras + zonas libres reservadas repartidas en los cuatro cuadrantes + señuelos + negativos propios, todo según el grupo de dificultad del §4.

**Nota de estilo (corrección respecto del borrador previo):** Handford trabaja con contorno de pluma/rotulador y relleno de acuarela, sección por sección desde el ángulo superior izquierdo; de ahí el acabado **plano, sin sombras proyectadas ni volumen**. Esto no es solo fidelidad estilística: un fondo sin luz direccional es lo que permite pegar a Tito y Lola en post-producción sin que la ausencia de sombra propia los delate. El descriptor `vivid saturated color palette` del borrador venía de listados de prompts para IA, no del análisis de los libros, y además perjudica la jugabilidad — el fondo de croma medio es el *presupuesto de contraste* que hace que el objetivo sea encontrable. La saturación del fondo queda entonces como palanca de dificultad: apagada y sin rojos en los niveles fáciles (el gorro de Tito salta), más croma y más rojo/blanco sembrado en los difíciles (se camufla).

También se reemplazó `top-down isometric panoramic perspective`, que mezcla dos proyecciones incompatibles y los modelos resuelven de forma errática. La vista casi ortográfica tiene una ventaja de pipeline: sin escorzo, un personaje mide lo mismo en cualquier punto del cuadro, así que la convención de hitbox fija en % (5% × 8%) funciona en todo el lienzo.

Pendiente: redactar el bloque variable de cada uno de los 10 mapas de la tabla del §4 (hoy no existe ninguno redactado con esta plantilla corregida).

### Resolución: no se pide en el prompt, se resuelve en el pipeline

Escribir "4K" o "3840×2160" en el prompt **no cambia las dimensiones de salida**. Los modelos generan a su resolución nativa (hoy típicamente entre ~1024 y ~2048 px de lado) y el tamaño real se fija por parámetro de la API o la interfaz (`--ar`, `size`, `width`/`height`), no por texto. Un `High resolution 4K` en el prompt funciona a lo sumo como token estético, así que se quitó del bloque fijo; el objetivo de 3840×2160 del §3 pasa a los metadatos de cada nivel.

El camino real a 4K es un **upscale con reintroducción de detalle** (img2img por tiles o upscaler generativo), no una interpolación simple. La diferencia importa por el zoom: con `maxZoom` en 3.5x, una hitbox de 5% × 8% (192 × 173 px a 4K) que en la generación nativa medía ~70 px se vería en pantalla a ~670 px, casi diez veces su detalle real. El refinado por tiles genera detalle nuevo y legítimo en cada porción en vez de agrandar píxeles existentes.

A favor: este estilo es de los mejores casos posibles para super-resolución. Color plano, bordes duros y ausencia de textura fotográfica o ruido escalan mucho mejor que una imagen realista.

## 7. Arquitectura técnica y responsive

### A. Sistema de coordenadas y hitboxes invisibles
- No se usan píxeles fijos: las zonas de clic se calculan en porcentajes (%) relativos al ancho/alto original del escenario — **ya implementado** en `renderHitboxes()`.
- Para producción, las hitboxes deben ser invisibles (hoy tienen borde rojo punteado para fines de calibración) — ajuste pendiente.

### B. Reglas y límites de zoom (constraints)
- **Zoom out máximo (minZoom):** calculado dinámicamente para que la imagen ocupe el 100% de la ventana sin bordes vacíos (modo *contain*) — **ya implementado** en `calculateMinScale()`.
- **Zoom in máximo (maxZoom):** entre 2.5x y 4.0x según la resolución base — hoy fijo en 3.5x, falta diferenciar por dispositivo.
- **Comportamiento responsive objetivo:**
  | Dispositivo | Zoom inicial | Zoom in máximo |
  | :--- | :--- | :--- |
  | Desktop | 1.0x | 3.0x |
  | Tablet | 1.2x | 3.5x |
  | Smartphone | 1.5x | 4.0x |
- **Efectos UX:** rebote elástico (bounce back) al exceder límites, con resistencia progresiva durante el gesto y snap-back animado al soltar — *ya implementado*. Pendiente: re-centrado automático si la vista se sale del escenario.
- **Nota (bugs de layout en móvil, resueltos):** `body` usaba `height: 100vh`, que en navegadores móviles no descuenta el espacio de la barra de direcciones y sobreestima el viewport real, empujando el minimapa fuera del área visible — se agregó fallback a `100dvh`. Además, `#minimap-viewport` no tenía `top`/`left` explícitos, así que su posición de partida dependía del flujo normal del documento (quedaba corrida hacia abajo por ser hermana de un `<img>` inline) en vez de partir de `(0,0)` del contenedor — se fijaron explícitamente.

### C. Estructura de datos para niveles (JSON)

Formato ya validado y en uso por `level1.json` (se ajustan nombres de campo mínimamente respecto al borrador original para igualar la implementación real):

```json
{
  "levelNumber": 1,
  "title": "Nivel 1: Egipto Antiguo",
  "imageSrc": "assets/levels/egipto_antiguo.jpg",
  "imageWidth": 3840,
  "imageHeight": 2160,
  "targets": [
    {
      "id": "tito_perdido",
      "name": "Tito el Perrito",
      "avatar": "assets/avatars/tito_perdido.jpg",
      "hint": "Lleva puesto su infaltable gorro rojo con blanco y anteojos.",
      "hitbox": { "x": 45.0, "y": 50.0, "width": 5.0, "height": 8.0 }
    },
    {
      "id": "lola",
      "name": "Lola",
      "avatar": "assets/avatars/lola.jpg",
      "hint": "Tiene pelo rizado y viste una campera azul con estampado de flores.",
      "hitbox": { "x": 60.0, "y": 40.0, "width": 5.0, "height": 8.0 }
    }
  ]
}
```

## 8. Stack tecnológico

- **Prototipo actual:** JS vanilla + CSS transforms para pan/zoom, sin librerías — funcional para la Fase 1 en desktop.
- **Evaluar para Fase 2+ (si el prototipo vanilla se queda corto en gestos táctiles/performance):** Konva.js, PixiJS u OpenSeadragon para manejo de capas, límites de zoom y eventos sobre hitboxes.
- **Frontend UI:** HTML5, CSS3, JavaScript (estado del juego, minimapa, header de objetivos, modales) — sin cambios respecto al borrador original.

## 9. Fases de desarrollo

1. **Fase 1: Prototipo base (PoC)** — motor de pan/zoom con soporte mouse y táctil, rebote elástico, límites min/max, recuadro de minimapa, detección de clics en porcentaje. **~90% completo**: falta minimapa arrastrable y diferenciar zoom máximo por dispositivo.
2. **Fase 2: Interfaz de usuario y niveles** — barra superior, modales de victoria, carga dinámica de JSON por nivel. **Base completa**; falta flujo de avance automático entre niveles y selector/progreso de niveles.
3. **Fase 3: Integración de personajes y calibración** — generación de los 10 escenarios vía IA (con la plantilla de prompt del §6, sin personajes principales), upscale a 4K, inserción manual de Tito/Lola/demás sobre el fondo ya escalado y ajuste fino de hitboxes. **No iniciada** — solo existe el placeholder de Picsum en el nivel 1.
4. **Fase 4: Optimización mobile y pruebas** — gestos táctiles, comportamiento elástico del zoom, rendimiento en distintos dispositivos. **No iniciada.**

## 10. Próximos pasos sugeridos

1. Elegir modelo generador y upscaler, y validar el pipeline completo con una prueba del nivel 1 antes de redactar los 10 prompts. La elección define si la lista negativa del §6 se usa como campo aparte o hay que absorberla en positivo, cómo se pide el 16:9, y si el descriptor de paleta de croma medio da el resultado esperado.
2. Redactar los 10 prompts de escenario (§6) usando la plantilla, uno por fila del §4.
3. Hacer el minimapa interactivo (arrastrar el recuadro para navegar).
4. Definir y crear `levels/level2.json` … `level10.json` con la misma estructura que `level1.json`.
5. Ocultar las hitboxes en producción (mantener un modo debug opcional para calibración).
6. Implementar avance automático al siguiente nivel desde el modal de victoria.
7. Diferenciar el zoom in máximo por tipo de dispositivo (desktop/tablet/smartphone), según la tabla del §7B.
8. Aplicar una leve transparencia al contenedor del minimapa y al recuadro verde de viewport, para que estorben menos la visibilidad del escenario principal.
