import base64, json, os
HERE = os.path.dirname(os.path.abspath(__file__))

DECL = "Samuel: “Nunca conocí a Daniel”.\nMartín: “Estuve en la biblioteca”.\nLaura: “Vi a alguien cerca de la habitación”.\nAndrés: “No salí de casa”."
TEST = "“Vi a Daniel entrar a las 7:00”.\n“Escuché una discusión a las 7:30”.\n“A las 8:00, alguien salió apresuradamente”."

common = [
 dict(tag="Inicio", title="La primera señal", place="Salón de clase",
      intro=["Ya tienes tu tarjeta de rol, tu pulsera y el mensaje de Daniel. La primera señal le llega a cada investigador de una forma distinta. Esta es la tuya."],
      reveal=dict(label="Primera parada", text="Una banca del Bloque C. Una de ellas está marcada discretamente y guarda el primer sobre.", next="Vayan al Bloque C y encuentren la banca marcada.")),
 dict(tag="1", title="La primera evidencia", place="Banca del Bloque C",
      intro=["En el sobre de la banca hay una fotografía de Daniel y una nota: el tiempo es clave para reconstruir los hechos."],
      reveal=dict(label="Mensaje del QR 1", text="Busquen un reloj o la imagen de un reloj: a su lado está el QR 1. La siguiente señal los espera cerca de un armario.", next="Vayan a la estación 2: Bloque A.")),
 dict(tag="2", title="El mensaje oculto", place="Bloque A",
      intro=["Daniel escondió el mismo lugar de cuatro maneras, una para cada investigador."],
      reveal=dict(label="Nota dentro del armario", text="Daniel guardaba sus secretos donde nadie acostumbraba mirar. Sin embargo, alguien estuvo revisando sus pertenencias antes del asesinato.", next="La fotografía que acompaña la nota señala la estación 3: el kiosco que está al frente del Bloque D.")),
 dict(tag="3", title="El testigo silencioso", place="Kiosco al frente del Bloque D",
      intro=["Un testigo dejó tres declaraciones sobre esa noche. Cada investigador debe sacarles algo distinto."],
      reveal=dict(label="Mensaje del QR 2", text="El testigo recuerda algo más: esa noche, una persona tenía una llave que no debía tener.", next="Vayan a la estación 4: Bloque B.")),
 dict(tag="4", title="El objeto desaparecido", place="Bloque B",
      intro=["Sobre la mesa hay cinco objetos casi iguales. Antes de tocarlos, resuelve tu reto."],
      reveal=dict(label="La llave marcada", text="Es una llave. De las cinco que hay en la mesa, solo una tiene una marca distintiva. Encuéntrenla y lean lo que lleva escrito: “No todas las puertas conducen a una salida. Algunas conducen directamente a la verdad”.", next="La etiqueta de la llave marcada señala la estación 5: Bloque H.")),
 dict(tag="5", title="El código del sospechoso", place="Bloque H",
      intro=["Cuatro sospechosos dejaron su declaración. Compárala con lo que tu equipo ya sabe."],
      reveal=dict(label="Mensaje del QR 3", text="Guarden la coartada de Martín, la de la biblioteca, como una afirmación por comprobar. Todavía no han revisado toda la información: una evidencia anterior puede tener otro significado.", next="")),
]

BANCA = ["banca", "bancas", "banco", "bancos", "unabanca", "labanca"]
RELOJ = ["reloj", "relojes", "elreloj", "unreloj"]
ARMARIO = ["elarmario", "armario", "unarmario"]
LLAVE = ["llave", "llaves", "lallave", "unallave"]
MARTIN = ["martin"]
SUS = [dict(who="Samuel"), dict(who="Martín"), dict(who="Laura"), dict(who="Andrés")]

roles = dict(
 detective=dict(num=1, name="Detective", desc="Analiza las pistas, compara declaraciones y relaciona los hechos.", skill="Tus retos: deducción y contradicciones.",
  mission="Tu trabajo es dudar. En cada estación recibirás lo que Daniel dejó para quien sabe comparar versiones y encontrar lo que no encaja.",
  task="Tu parte, detective: compara cada declaración nueva con la cronología que ya tienes.",
  ch=[
   dict(type="text", clue="Tengo respaldo, pero no soy una persona; tengo asiento, pero no soy un salón. En mí descansan quienes recorren los pasillos. Búscame en el Bloque C y allí comenzará tu investigación.",
        question="¿Qué debes buscar en el Bloque C?", pattern="B_N__", accept=BANCA,
        hints=["Piensa en un lugar donde los estudiantes se sientan.", "Está en los pasillos del Bloque C y tiene respaldo.", "La respuesta es BANCA."]),
   dict(type="text", clue="No tengo boca, pero puedo hablar. No tengo piernas, pero siempre avanzo. Todos me miran, pero nadie puede detenerme. ¿Qué soy?",
        question="¿Qué es?", pattern="R_L__", accept=RELOJ,
        hints=["La respuesta mide el paso del tiempo.", "Suele estar en la pared o en la muñeca.", "La respuesta es RELOJ."]),
   dict(type="text", clue="Tengo puertas y no soy casa. Guardo ropa y también secretos. Cuando me cierran, nadie ve lo que llevo dentro.",
        question="¿Dónde escondería Daniel algo que nadie debe ver?", pattern="A_M__I_", accept=ARMARIO + ["closet", "elcloset", "ropero", "elropero", "guardarropa"],
        hints=["Es un mueble.", "Tiene puertas y sirve para guardar ropa.", "La respuesta es ARMARIO."]),
   dict(type="order", question="Toca las declaraciones en el orden en que ocurrieron.",
        items=[dict(text="A las 8:00, alguien salió apresuradamente."), dict(text="Vi a Daniel entrar a las 7:00."), dict(text="Escuché una discusión a las 7:30.")],
        correct=[1, 2, 0], wrong="Ese orden no cuadra con las horas. Inténtalo de nuevo.",
        hints=["Ordena las horas de menor a mayor.", "Primero la entrada, después la discusión y al final la salida.", "El orden es 7:00, 7:30 y 8:00."]),
   dict(type="text", clue="Tengo dientes, pero no como. Abro puertas, pero no tengo manos. ¿Qué soy?",
        question="¿Qué es?", pattern="L_A__", accept=LLAVE,
        hints=["Abre algo que está cerrado.", "Tiene dientes y entra en una cerradura.", "La respuesta es LLAVE."]),
   dict(type="choice", question="¿Qué declaración necesita ser comprobada?",
        items=[dict(who="Samuel", text="“Nunca conocí a Daniel”."), dict(who="Martín", text="“Estuve en la biblioteca”."), dict(who="Laura", text="“Vi a alguien cerca de la habitación”."), dict(who="Andrés", text="“No salí de casa”.")],
        correct=[1], wrong="Esa declaración todavía no choca con ninguna evidencia. Busca una coartada que dependa de un lugar y una hora.",
        hints=["Compara las declaraciones con la línea de tiempo.", "No aceptes una coartada sin contrastarla con las otras evidencias.", "Revisa la declaración de Martín."]),
  ]),
 criptografo=dict(num=2, name="Criptógrafo", desc="Descifra códigos, interpreta mensajes ocultos y coordina la lectura de los QR.", skill="Tus retos: claves y mensajes cifrados.",
  mission="Daniel escondió parte de sus mensajes en clave. En cada estación te toca descifrar lo que los demás no pueden leer.",
  task="Tu parte, criptógrafo: cualquier número, letra suelta o QR que aparezca es asunto tuyo.",
  ch=[
   dict(type="text", clue="Daniel escribía con números: A = 1, B = 2, C = 3…\n\n2 · 1 · 14 · 3 · 1\n\nEso te espera en el Bloque C.",
        question="¿Qué palabra forman los números?", pattern="B____", accept=BANCA,
        hints=["Cambia cada número por la letra que ocupa ese lugar en el abecedario.", "2 es B, 1 es A y 14 es N.", "La respuesta es BANCA."]),
   dict(type="text", clue="Cada letra de este mensaje está un paso adelante de la verdadera:\n\nS F M P K",
        question="¿Qué palabra escondió Daniel?", pattern="R____", accept=RELOJ,
        hints=["Retrocede cada letra una posición en el abecedario.", "S se convierte en R y F en E.", "La respuesta es RELOJ."]),
   dict(type="text", clue="Nueve letras revueltas. Forman dos palabras.", tiles=list("RAOEMLIRA"),
        question="¿Qué dicen las letras?", pattern="E_ A______", accept=ARMARIO,
        hints=["Forman el nombre de un mueble.", "La primera palabra es EL y la segunda termina en ARIO.", "La respuesta es EL ARMARIO."]),
   dict(type="text", clue="El testigo escribió una de sus declaraciones al revés para que nadie más la leyera:\n\n" + "A las 8:00, alguien salió apresuradamente."[::-1],
        question="¿A qué hora salió alguien apresuradamente?", accept=["800", "8", "ocho", "lasocho", "alasocho", "alas8", "alas800", "las8", "las800", "8pm", "8am"],
        hints=["Lee el mensaje de derecha a izquierda.", "La hora está casi al final del texto que ves.", "Salió a las 8:00."]),
   dict(type="text", clue="Daniel dejó esta palabra frente a un espejo:\n\nE V A L L",
        question="¿Qué palabra es?", pattern="L____", accept=LLAVE,
        hints=["Un espejo invierte el orden.", "Léela de derecha a izquierda.", "La respuesta es LLAVE."]),
   dict(type="text", clue="Junto a las declaraciones, Daniel anotó un nombre en clave. Cada letra está un paso adelante de la verdadera (abecedario sin la Ñ):\n\nN B S U J O",
        question="¿Qué nombre escondió?", pattern="M_____", accept=MARTIN,
        hints=["Es la misma clave de la estación 1: retrocede cada letra una posición.", "N se convierte en M y B en A.", "El nombre es MARTÍN."]),
  ]),
 investigador=dict(num=3, name="Investigador", desc="Busca los objetos señalados, revisa los espacios autorizados y examina las evidencias.", skill="Tus retos: observación y detalles.",
  mission="Tú eres los ojos del equipo. En cada estación tendrás que fijarte en lo que está escrito, en lo que falta y en los objetos que nadie mira.",
  task="Tu parte, investigador: revisa los objetos que el equipo ya vio. Alguno guarda más de lo que parece.",
  ch=[
   dict(type="text", clue="Tengo cuatro patas y no camino. Tengo espalda y nunca me canso. Espero en un pasillo del Bloque C a quien quiera detenerse un momento.",
        question="¿Qué objeto debes encontrar?", pattern="B_N__", accept=BANCA,
        hints=["Es un mueble de pasillo.", "Sirve para sentarse y caben varias personas.", "La respuesta es BANCA."]),
   dict(type="text", clue="La nota dice que el tiempo es clave. Busca a tu alrededor el objeto que lo vigila: tiene cara y no tiene ojos, tiene manecillas y no tiene brazos.",
        question="¿Qué objeto es?", pattern="R_L__", accept=RELOJ,
        hints=["Marca las horas.", "Puede estar colgado en una pared.", "La respuesta es RELOJ."]),
   dict(type="text", clue="A este mensaje alguien le arrancó todas las vocales. Devuélveselas.",
        question="¿Qué decía el mensaje?", pattern="_L _RM_R__", accept=ARMARIO,
        hints=["Son dos palabras y la primera es un artículo.", "Es un mueble donde se guarda ropa.", "La respuesta es EL ARMARIO."]),
   dict(type="text", clue=TEST,
        question="Lee con cuidado. ¿Qué escuchó el testigo a las 7:30?", pattern="D_S_U__ON", accept=["discusion", "unadiscusion", "ladiscusion"],
        hints=["La respuesta está en la segunda declaración.", "Fue algo que se oye, entre dos personas.", "Escuchó una DISCUSIÓN."]),
   dict(type="text", clue="Soy pequeña y de metal. Viajo en bolsillos y cuelgo de un aro. Si me pierdes, te quedas afuera.",
        question="¿Qué objeto debes revisar en la mesa?", pattern="L_A__", accept=LLAVE,
        hints=["Sirve para entrar a un lugar cerrado.", "Va en un llavero.", "La respuesta es LLAVE."]),
   dict(type="text", clue=DECL,
        question="Solo una coartada nombra un lugar que se puede ir a revisar. ¿Qué lugar es?", pattern="B_BL__T__A", accept=["biblioteca", "labiblioteca", "unabiblioteca"],
        hints=["Descarta las declaraciones que no mencionan ningún lugar concreto.", "Es un lugar lleno de libros.", "El lugar es la BIBLIOTECA."]),
  ]),
 estratega=dict(num=4, name="Estratega", desc="Organiza la información, resuelve acertijos y propone el orden para avanzar.", skill="Tus retos: lógica y orden.",
  mission="Tú pones orden. En cada estación recibirás un problema de lógica que solo se resuelve paso a paso.",
  task="Tu parte, estratega: decide el orden en que el equipo revisa las pistas y no dejes que se salten ninguna.",
  ch=[
   dict(type="text", clue="Arma la palabra letra por letra:\n1. La segunda letra del abecedario.\n2. La primera vocal.\n3. La letra con la que empieza NOCHE.\n4. La tercera letra del abecedario.\n5. Otra vez la primera vocal.",
        question="¿Qué palabra armaste?", pattern="_____", accept=BANCA,
        hints=["Escribe una letra por cada instrucción, en orden.", "Empieza con B y termina con A.", "La respuesta es BANCA."]),
   dict(type="text", clue="Doy vueltas todo el día sin moverme de mi sitio. Tengo doce marcas y dos agujas que nunca cosen. Si me atraso, todos llegan tarde.",
        question="¿Qué es?", pattern="R_L__", accept=RELOJ,
        hints=["Las doce marcas son horas.", "Las agujas también se llaman manecillas.", "La respuesta es RELOJ."]),
   dict(type="order", question="Toca las sílabas en el orden correcto para formar el lugar.",
        items=[dict(who="MA"), dict(who="EL"), dict(who="RIO"), dict(who="AR")],
        correct=[1, 3, 0, 2], wrong="Así no se forma ninguna palabra. Prueba otro orden.",
        hints=["Son dos palabras: un artículo y un mueble.", "Empieza con EL y termina con RIO.", "El orden es EL, AR, MA, RIO."]),
   dict(type="code", clue=TEST,
        question="¿Cuántos minutos pasaron entre la entrada de Daniel y la salida apresurada?", accept=["60"],
        hints=["Busca la primera hora y la última.", "Entró a las 7:00 y alguien salió a las 8:00.", "Pasaron 60 minutos."]),
   dict(type="choice", clue="Daniel buscaba un objeto de metal, con dientes, que abre algo.\nLa moneda es de metal, pero no abre nada.\nEl peine tiene dientes, pero no es de metal ni abre nada.\nEl anillo es de metal, pero no tiene dientes.\nEl botón no cumple ninguna condición.",
        question="¿Qué objeto queda?", items=[dict(who="Moneda"), dict(who="Peine"), dict(who="Anillo"), dict(who="Llave"), dict(who="Botón")],
        correct=[3], wrong="Ese objeto no cumple las tres condiciones. Revisa la lista.",
        hints=["Tacha los objetos uno por uno.", "Debe ser de metal, tener dientes y abrir algo.", "Queda la LLAVE."]),
   dict(type="choice", clue=DECL + "\n\nDescarta a quien no nombra ningún lugar.\nDescarta a quien habla como testigo y no de sí mismo.\nDescarta a quien dice no haberse movido.",
        question="¿Quién queda con una coartada por comprobar?", items=SUS,
        correct=[1], wrong="Esa persona queda descartada por una de las tres reglas. Vuelve a aplicarlas.",
        hints=["Aplica las reglas en orden y tacha un nombre con cada una.", "Samuel no nombra un lugar, Laura es testigo y Andrés no se movió.", "Queda MARTÍN."]),
  ]),
)

OWN = ["todos", "estratega", "criptografo", "detective", "investigador", "todos"]
SRC = ["detective", "detective", "criptografo", "detective", "detective", "detective"]
stages = []
for k, c in enumerate(common):
    s = dict(c); s.update(roles[SRC[k]]["ch"][k]); s["owner"] = OWN[k]; stages.append(s)
stages[0]["intro"] = ["Ya tienen sus tarjetas de rol, sus pulseras y el mensaje de Daniel. La primera señal es para todos."]
stages[0]["question"] = "¿Qué deben buscar en el Bloque C?"
stages[2]["intro"] = ["Sobre la mesa hay nueve letras desordenadas."]
stages[2]["pattern"] = "E_ A_M__I_"
stages[3]["intro"] = ["Un testigo dejó tres declaraciones sobre esa noche."]
stages[4]["intro"] = ["Sobre la mesa hay cinco objetos casi iguales. Antes de tocarlos, resuelve esto."]
stages[5]["intro"] = ["Cuatro sospechosos dejaron su declaración. Discútanlo entre los cuatro y respondan lo mismo en cada teléfono."]
META = dict(
 detective=("Tu estación: la 3, el testigo.", "Tu trabajo es dudar y comparar versiones. Te toca responder la estación 3. En las demás acompañas a tu equipo, y la quinta la resuelven entre todos."),
 criptografo=("Tu estación: la 2, el mensaje oculto.", "Tú lees lo que los demás no pueden leer. Te toca responder la estación 2. En las demás acompañas a tu equipo, y la quinta la resuelven entre todos."),
 investigador=("Tu estación: la 4, el objeto.", "Tú eres los ojos del equipo. Te toca responder la estación 4. En las demás acompañas a tu equipo, y la quinta la resuelven entre todos."),
 estratega=("Tu estación: la 1, la primera evidencia.", "Tú resuelves acertijos y pones orden. Te toca responder la estación 1. En las demás acompañas a tu equipo, y la quinta la resuelven entre todos."),
)
for rid, r in roles.items():
    r.pop("ch"); r["skill"], r["mission"] = META[rid]
answers = [dict(owner=s["owner"], type=s["type"], a=s.get("accept", [None])[0], c=s.get("correct")) for s in stages]

finale = dict(
 title="El camino sigue por su cuenta",
 intro="Aquí terminan tus sobres. Quedan cinco estaciones y ya no habrá nadie que les confirme las respuestas: sigan las señales de Daniel hasta encontrar al responsable y el tesoro.",
 lead="Esto es lo que sabe tu equipo hasta ahora:",
 evidence=[
  "Alguien revisó las pertenencias de Daniel antes del crimen.",
  "El testigo vio a Daniel entrar a las 7:00, oyó una discusión a las 7:30 y vio salir a alguien con prisa a las 8:00.",
  "Esa noche, una persona tenía una llave que no debía tener.",
  "La coartada de Martín sigue sin comprobarse.",
 ],
 clueLabel="La última pista",
 clue="Lo que sigue está hecho pedazos sobre una mesa del kiosco que está al lado del Bloque C. Únanlo y lean lo que dice por los dos lados. Y no olviden esto: una evidencia que ya vieron puede tener otro significado.",
 closing="Observen, comparen y confíen en su equipo. Suerte, investigadores.",
)

data = dict(stages=stages, roles=roles, order=["detective", "criptografo", "investigador", "estratega"], finale=finale)
blob = base64.b64encode(json.dumps(data, ensure_ascii=False).encode("utf-8")).decode()
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read().replace("__DATA__", blob).replace("__FONT__", base64.b64encode(open(os.path.join(HERE, "door.woff"), "rb").read()).decode())
open(os.path.join(HERE, "..", "index.html"), "w", encoding="utf-8").write(html)
print(len(html))
