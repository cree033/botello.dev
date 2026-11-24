# Elenco

Los objetos (tabla de arriba) más tres personas (sección siguiente). Son fáciles de animar porque no necesitan expresiones complejas.

Diseño v2 (2026-11-24): estilo de producto tech, sobrio y pulido. Superficies con degradado y luz desde arriba a la izquierda, sombra de piso suave, caras en pantallas y un solo color de acento por personaje. Reemplaza el diseño v1, que se veía infantil.

| Personaje | Qué es | Cómo suena | Costumbre fija | Diseño v2 (acento) |
| --- | --- | --- | --- | --- |
| Prod | El servidor de producción | Voz aguda y nerviosa, respira rápido | Pide que nadie toque nada; sufre cada viernes | Servidor de rack con display frontal: ojos de LED que se inclinan y pasan de cian a ámbar bajo estrés, boca en zigzag, baliza roja y gota de sudor (rojo `#ff6b6b`) |
| El Legacy | Un stored procedure de 2009 | Voz grave y lenta, de abuelo | Lanza advertencias sombrías y nunca explica nada | Monitor CRT beige amarillento con ojos de fósforo verde, párpados pesados, etiqueta "sp_2009 NO TOCAR" y cables colgando (verde `#5dff9a`) |
| Vibe | La IA asistente | Voz dulce y muy segura | Dice "te lo juro" y se equivoca sin culpa | Burbuja de cristal oscuro con borde degradado violeta-rosa, brillo y sonrisa segura (violeta `#a78bfa`) |
| El Ticket | Una tarjeta de tarea | Casi no habla; todo en texto | Cuenta días y su barra de progreso nunca termina | Tarjeta de gestor de tareas con "#4521", chevrones de prioridad, carita mínima, chip "En progreso" y barra al 90 % (ámbar `#f2a93b`) |
| El cliente | Una silueta con voz | Voz tranquila que pide cosas enormes | Empieza con "solo un detalle" | Silueta de traje sin cara, con luz de borde y corbata roja (gris azulado `#8892b8`) |
| El dev | El testigo, sin aparecer | Voz en off seca o solo texto | Reacciona con una frase corta | Solo un cursor parpadeante con prompt `>` y brillo (verde neón `#39ff88`) |

## Las personas (v3, Magnific)

Tres humanos fijos, dibujados en Magnific con el mismo estilo editorial (ver `05-assets/personajes/magnific/README.md`). La situación que los define: **Nacho hace de todo (Scrum, PMO y QA), Memo siempre trabaja con IA y Ruth siempre presiona.** Los objetos siguen mandando: las personas reaccionan, minimizan y aprueban cosas que no deberían.

| Persona | Qué es | Cómo suena | Costumbre fija | Diseño v3 (acento) |
| --- | --- | --- | --- | --- |
| Memo | El dev, delgado, siempre con IA | Tranquilo; dice "es rapidito" y "ya se lo pregunté a la IA" | Minimiza todo y le pregunta a Vibe antes que a nadie; sonríe antes del desastre | Flaco, ojeras, barba corta, sudadera verde azulado, audífonos al cuello, laptop con chat violeta (cian) |
| Nacho | El Scrum Manager cuarentón, gordo y casi calvo, que además hace de PMO y de QA | Cansado y amable; dice "yo lo reviso" | Carga tres gafetes (SCRUM, PMO, QA), papelitos pegados al cuerpo, sudor y celular en mano; aprueba porque no hay nadie más | Camisa azul claro, corbata, bigote, laptop bajo el brazo (ámbar) |
| Ruth | La PMO que siempre presiona | Seca y puntual; "¿Para cuándo?" | Tableta con Gantt en rojo, toca el reloj y sonríe apretado | Blazer gris azulado, lentes, chongo, pin de rosa (rosa) |

Caro (QA) queda en reserva: sus tareas las absorbe Nacho, que es parte del chiste.

Reglas de las personas:
- Que no se parezcan a personajes de otras series ni a personas reales: sin oficina de fondo ni cubículos.
- Al inicio, máximo 2 personas y 1 objeto por pieza.
- La gracia sale del contraste: el humano minimiza o presiona y el objeto sufre.
- La IA (Vibe) es la tercera voz de Memo; no sustituye a los humanos.

## Servidores (rediseño v3)

- **Prod:** servidor de rack 2U con tira OLED de cara (ojos cian preocupados), baliza roja, gota de sudor, patitas y cables enredados (rojo).
- **Staging (nuevo):** servidor de rack azul-verdoso con sonrisa de LED, palomita verde y etiqueta "STAGING"; dice "todo está bien" y nunca refleja producción (verde azulado).

Los otros objetos (El Legacy, Vibe, El Ticket, El cliente, El dev) siguen en versión v1 de Magnific; Vibe es el siguiente a rediseñar.

## Reglas de animación

- Máximo 2 personajes por pieza.
- Fondo oscuro y liso, misma paleta en todas las piezas.
- Movimiento mínimo: temblor, cabeceo, parpadeo de luz y cambio de expresión.
- Los personajes no son personas reales ni se parecen a personajes de otras series.
- Cada personaje queda fijo en una hoja de referencia antes de producir el primer Reel (guardarla en `05-assets/personajes/`: `hoja-de-personajes.png` para los objetos y `hoja-de-personas.png` para las personas).
