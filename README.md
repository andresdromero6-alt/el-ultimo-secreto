# El Último Secreto

Página web del rally de investigación "El Último Secreto". Acompaña a un equipo de cuatro jugadores desde el salón de clase hasta la quinta estación.

## Cómo funciona

- La portada presenta el caso y termina en "Escoge tu rol". Cada persona elige un solo rol en su teléfono.
- Cada estación tiene un rol responsable. Los demás ven "Esta estación es para el…" y continúan cuando su compañero la resuelve.
- El inicio y la quinta estación se responden entre todos.
- Al terminar la quinta estación, la página entrega una última pista y el equipo sigue por su cuenta.

| Estación | Responde |
|---|---|
| Inicio | Todo el equipo |
| 1 | Estratega |
| 2 | Criptógrafo |
| 3 | Detective |
| 4 | Investigador |
| 5 | Todo el equipo |

## Publicarla con GitHub Pages

1. En el repositorio, abre Settings y luego Pages.
2. En "Source" elige "Deploy from a branch", rama `main`, carpeta `/ (root)`.
3. Guarda. En unos minutos la página queda en `https://USUARIO.github.io/el-ultimo-secreto/`.

## Archivos

- `index.html`: la página completa en un solo archivo. Es lo único que se necesita para publicarla.
- `src/build.py`: textos, preguntas, respuestas y ayudas. Genera `index.html`.
- `src/template.html`: diseño y funcionamiento de la página.
- `src/mkfont.py` y `src/door.woff`: la fuente con tildes y eñe añadidas.
- `fuente/`: la fuente original "And The Door Creeeaked" y su licencia (CC0).

Para cambiar una pregunta, edita `src/build.py` y ejecuta `python3 src/build.py`.

Aviso: `src/build.py` contiene las respuestas del juego en texto legible.
