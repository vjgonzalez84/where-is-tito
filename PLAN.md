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
| Alta | 7. París 1889 · 8. Años 20 (Jazz) · 9. Festival Hippie 60/70 | 0.8x | Alta densidad de personajes y objetos, muy poca dispersión. | Parcialmente ocultos: solo cara y alguna extremidad (ej. una mano). | `large empty areas, sparse crowd, isolated figures, flat single-layer composition` (aquí el rojo/blanco **se busca**, como señuelo) |
| Muy alta | 10. Estación Espacial (futuro) | 0.7x | Saturación máxima, aglomeración continua. | Especialmente escondido: solo la cabeza visible (sin cuerpo). | `large empty areas, sparse crowd, isolated figures, single-layer composition, calm or orderly arrangement` |

La columna de negativos aplica **además** de la lista negativa universal del §6. A cada nivel se le suma su propio negativo de anacronismos (ej. para Egipto: `modern clothing, phones, cars, electric lighting`), que se redacta junto al bloque variable.

**Ojo con los toldos en los grupos Fácil y Media.** En la prueba del nivel 1, pedir `coloured awnings` en la sección `COLOUR` devolvió toldos a rayas rojas y blancas — justo el elemento camuflante que estos grupos deben negar, porque compite con el gorro de Tito. La ropa sí respetó el negativo; el problema entró por la escenografía. Para los niveles 1 a 6 conviene enumerar la paleta de toldos y telas excluyendo esa combinación (ej. `awnings in ochre, teal, olive and indigo`).

**Cláusula de legibilidad para los grupos Alta y Muy alta.** En esos niveles la densidad puede devolver un muro de figuras fusionadas, sin un solo punto de suelo libre donde apoyar a un personaje. Se agrega al bloque variable de esos niveles: `crowd remains legible, with narrow gaps of visible ground between clusters of figures`. Es lo mismo que evita la papilla de siluetas pegadas, así que sirve doble. Nótese que los negativos de esos grupos dicen `large empty areas`, no `empty areas`: el hueco estrecho se busca, el claro amplio no.

`level1.json` hoy usa un placeholder Picsum de 3840×2160 — ya respeta la resolución base, falta reemplazar por el arte final de "Egipto Antiguo".

## 5. Lineamientos para inserción y ubicación de personajes principales

- **Definición por nivel:** cada mapa define la cantidad de personajes principales a buscar, con descripción de la acción/pose que realiza cada uno y su avatar para la barra superior.
- **Regla de dispersión máxima:** los personajes a buscar se distribuyen ampliamente por el mapa. Prohibido agruparlos en el mismo cuadrante o zona inmediata.
- **Integración con la escena:** cada personaje realiza una acción contextual coherente con la época (interactuando con un objeto o personaje secundario), respetando el nivel de visibilidad de la matriz de dificultad — pero sin alterar su vestuario/diseño base (ver regla de identidad en §1).

### Elección del sitio de inserción

**El sitio no se reserva en el prompt, se elige después sobre la lámina terminada.** No se le puede pedir a un modelo un hueco en una coordenada dada — no tiene control espacial confiable desde texto, y pedir "áreas vacías" en abstracto ralea la composición entera de forma pareja, que es lo contrario de lo que sirve. Además un personaje parado en un espacio que estaba reservado para él se nota: queda con aura, recortado y apoyado encima. Lo que el prompt debe conseguir es que la lámina sea **pegable en muchos puntos**, no que traiga un lugar apartado.

Criterios para elegir cada sitio, una vez generado y escalado el fondo:

- **Hueco intersticial, no claro.** El espacio entre dos figuras de fondo, del tamaño de un personaje (~192 × 173 px a 1.0x, ver §6) más un pequeño margen. En los libros originales Wally nunca está en un descampado: está encajado en la multitud.
- **Suelo transitable debajo.** Con vista casi cenital el personaje tiene un punto de contacto implícito; si el hueco cae sobre agua, un techo o una pared, flota.
- **Vecinos de escala comparable.** El hueco debe lindar con figuras humanas de altura estándar, no con estatuas ni con elementos lejanos.
- **Contraste cromático local — la palanca real de dificultad.** Que Tito se encuentre fácil o difícil depende casi enteramente del color inmediatamente detrás de él, no de la densidad global. El gorro rojo/blanco contra un muro beige salta al instante por más cargada que esté la lámina; contra un toldo a rayas rojas y blancas desaparece. Por eso en los niveles altos conviene pedir **escenografía** rojo/blanco (toldos, banderines, sombrillas, carpas) y no solo gente a rayas.
- **Oclusor con silueta recortable** para los niveles de visibilidad parcial: hace falta un elemento en primer plano que se pueda enmascarar en el editor para meter al personaje por detrás. El estilo plano de color liso y contorno duro juega a favor acá; un fondo con degradados sería inviable de recortar.
- **Margen respecto de los bordes.** Acotar las hitboxes a ~3–95% en ambos ejes: un personaje pegado al borde del lienzo queda incómodo de inspeccionar con el clamp y el rebote elástico del §7B.

Lo que **no** hay que tener en cuenta es la luz: al ser todo plano y sin sombras no hay dirección lumínica que matchear. Ese es el rédito de la decisión de estilo del §6.

Si ningún sitio generado sirve, o se necesita al personaje en un punto concreto de la composición, la salida es **inpainting** de una región chica sobre la lámina terminada — mucho más barato que regenerar el escenario entero.

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

**Bloque de estilo fijo — todo en positivo. Validado con el nivel 1 (ver más abajo).** Se escribe en secciones rotuladas, que es la forma que dio mejor adherencia:

> `A massive, detailed panoramic illustration of [ENTORNO], in the style of Martin Handford's Where's Wally.`
>
> `FRAMING: the scene completely fills the frame from edge to edge — every part of the image is ground, water, buildings or crowd, seen from above. There is no sky and no horizon line anywhere in the picture. Flat orthographic projection with no perspective recession: every human figure is drawn at exactly the same height whether it stands at the top, the middle or the bottom of the frame.`
>
> `SCENE: [ENTORNO detallado, props y oficios de época]. [Cualquier masa de agua se describe como banda horizontal vista desde arriba, con la orilla opuesta igual de poblada y a la misma escala de figura.] Signage and inscriptions rendered as purely decorative abstract marks.`
>
> `COLOUR: a richly polychrome scene, not a monochrome one. [Fuentes de color propias de la época: ropas teñidas, arquitectura pintada, mercancías, vegetación.]`
>
> `DENSITY: [según grupo del §4]. Every figure fully visible head to foot standing at ground level. All garments in plain solid colours.`
>
> `STYLE: crisp uniform black ink outlines, flat cel-style colour fills under even ambient light, every surface a single solid tone, no shading and no cast shadows. Low-to-medium chroma watercolour palette — colours varied and numerous but softly muted rather than neon. Wide 16:9 aspect ratio, artwork bleeding to all four edges. Every background figure fully drawn with distinct period clothing and readable facial features. Anonymous background crowd only.`

**La sección `FRAMING` es la que más pesa, y no estaba en el borrador.** La primera prueba del nivel 1 salió con cielo y horizonte en el 15% superior, y eso arrastraba dos fallas más: obligaba al modelo a meter perspectiva (las figuras de abajo medían el triple que las del fondo, lo que **rompe la convención de hitbox fija en %**), y desperdiciaba lienzo donde no se puede parar a nadie a nivel de suelo. Las láminas de Handford no tienen cielo: la escena llena el cuadro entero. Al pedirlo explícitamente, junto con describir el Nilo como banda horizontal en vez de río que se aleja, las dos fallas se corrigieron de una vez.

**Sobre la paleta, corrección a la corrección.** El descriptor original `chalky beiges, dusty blues, muted greens and soft ochres dominate` produjo una lámina casi monocroma. El problema no era el croma sino el tema — lino blanco y arena en medio cuadro — así que la solución no fue subir saturación en el bloque fijo sino agregar una sección `COLOUR` que inyecte fuentes de color propias de cada época. El bloque fijo mantiene `softly muted rather than neon`.

**Lista negativa universal — va en el campo `negative prompt`, no en el prompt:**

> `cast shadows, drop shadows, soft shading, gradients, ambient occlusion, glossy 3D render, cinematic lighting, depth of field, blur, bokeh, legible text, lettering, numerals, watermark, signature, frame, border, vignette, Wally, Waldo, blobby or featureless crowd filler, photorealism`

A esa lista se le suman los negativos del grupo de dificultad y los de anacronismo del nivel (columna del §4).

**El campo negativo resultó prescindible.** Las dos pruebas del nivel 1 se hicieron con Gemini, que no lo ofrece, y aun así no se coló ningún rojo/blanco en la ropa, no aparecieron sombras y los jeroglíficos salieron como marcas decorativas sin texto garabateado. El positivo solo alcanzó. Tiene sentido: el negativo nació como parche para modelos con mala adherencia al prompt, y los instruction-tuned actuales siguen instrucciones afirmativas bien. Conclusión práctica: **no hay razón para elegir generador por tener campo negativo**, y la lista de arriba queda como refuerzo opcional para los modelos que sí lo soporten.

Con Gemini también se verificó que la negación explícita en lenguaje natural (`there is no sky and no horizon line`) se obedece sin efecto rebote. El riesgo de "no pienses en un elefante" es sobre todo un fenómeno de difusión condicionada por CLIP, no de modelos instruction-tuned. Aun así conviene redactar primero en afirmativo y dejar la negación como refuerzo.

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

**Validado — y con una corrección importante.** Más arriba se dijo que hacía falta un upscaler *generativo* que reintrodujera detalle, y que la super-resolución clásica no alcanzaba. Para arte fotorrealista es cierto; **para este estilo no**. Acá no hay textura que inventar: la información es el borde y la región lisa, y eso la SR clásica lo reconstruye muy bien. Comparado contra un Lanczos simple, el modelo devuelve contornos negros sólidos y limpios donde el Lanczos deja halo gris, y no ensucia las zonas planas. Las caras chicas no ganan rasgos nuevos, pero las figuritas de Handford tampoco los tienen.

Consecuencia práctica: **no hace falta GPU.** La receta validada, corriendo en CPU:

- **Modelo:** `RealESRGAN_x4plus_anime_6B` (libre, 18 MB). La variante *anime* está entrenada para color plano y contorno duro; la genérica de foto inventaría textura en las zonas lisas.
- **Runner:** `spandrel` sobre PyTorch CPU, en un venv. Cuidado con instalar `torch` y `torchvision` del mismo índice (`--index-url .../whl/cpu`): mezclarlos con PyPI da `RuntimeError: operator torchvision::nms does not exist`.
- **Proceso:** inferencia por tiles de 192 px con 24 px de solape para acotar la RAM, 4x hasta 5504 × 3072, recorte centrado a 16:9 y reescalado Lanczos a 3840 × 2160. Bajar desde 4x en vez de escalar justo a 2.79x sale más nítido.
- **Costo:** ~4 minutos por lámina en 4 núcleos sin GPU. Para 10 niveles es irrelevante.
- **Script:** `~/tools/upscale/upscale.py` (fuera del repo).

La prueba también reveló que el problema real no era la resolución sino `maxScale` — ver §7B.

## 7. Arquitectura técnica y responsive

### A. Sistema de coordenadas y hitboxes invisibles
- No se usan píxeles fijos: las zonas de clic se calculan en porcentajes (%) relativos al ancho/alto original del escenario — **ya implementado** en `renderHitboxes()`.
- Para producción, las hitboxes deben ser invisibles (hoy tienen borde rojo punteado para fines de calibración) — ajuste pendiente.

### B. Reglas y límites de zoom (constraints)
- **Zoom out máximo (minZoom):** calculado dinámicamente para que la imagen ocupe el 100% de la ventana sin bordes vacíos — **ya implementado** en `calculateMinScale()`. Nota terminológica: el borrador lo llamaba modo *contain*, pero el código hace `Math.max(scaleX, scaleY)`, que es **cover**. La intención descrita (sin bordes vacíos) coincide con el código; el nombre estaba mal.
- **`scale` es absoluto, no relativo al ajuste.** Multiplica el tamaño nativo de la imagen: con un lienzo de 3840 px en un viewport de 1920, `minScale` da 0.5 y `scale = 1.0` significa 1 px de fuente por 1 px de pantalla.
- **Zoom in máximo (maxZoom): ~1.5x.** Corregido tras la prueba del nivel 1 — antes decía 2.5x–4.0x, que era un error de diseño. A 3.5x el viewport muestra apenas 549 × 309 px de fuente, un séptimo del ancho del lienzo: se ven dos o tres objetos sueltos. **Es inútil para jugar antes que borroso** — el zoom en un juego tipo Waldo sirve para inspeccionar una zona de multitud, no un objeto. A 1.5x se ven 1280 × 720 px de fuente, una porción de mercado entera y con las caras nítidas.
- **La tabla responsive queda pendiente de rehacer.** Los valores del borrador (desktop 3.0x, tablet 3.5x, smartphone 4.0x) solo tendrían sentido como múltiplo del `scale` de ajuste, no como absolutos. Si se diferencia por dispositivo, conviene expresarlo como `minScale * K` y no como constante.
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

1. ~~Elegir modelo generador y validar el bloque de estilo~~ — **hecho**. Gemini, validado con dos pruebas del nivel 1 (ver §6). Falta la mitad del pipeline: **validar el upscale**. Gemini entrega 1376 × 768, así que hacen falta 2.79x para llegar a 3840 y una figura mide apenas 61 px nativos. Hay que escalar la lámina de prueba y mirar un recorte al 100% de una cara del mercado: si se convierte en papilla, el zoom a 3.5x no vale nada y hay que replantear (generar por secciones y componer, o buscar mayor resolución nativa). Es el último riesgo sin retirar y bloquea todo lo demás.
2. Redactar los 10 prompts de escenario (§6) usando la plantilla ya validada, uno por fila del §4.
3. Hacer el minimapa interactivo (arrastrar el recuadro para navegar).
4. Definir y crear `levels/level2.json` … `level10.json` con la misma estructura que `level1.json`.
5. Ocultar las hitboxes en producción (mantener un modo debug opcional para calibración).
6. Implementar avance automático al siguiente nivel desde el modal de victoria.
7. Diferenciar el zoom in máximo por tipo de dispositivo (desktop/tablet/smartphone), según la tabla del §7B.
8. Aplicar una leve transparencia al contenedor del minimapa y al recuadro verde de viewport, para que estorben menos la visibilidad del escenario principal.
