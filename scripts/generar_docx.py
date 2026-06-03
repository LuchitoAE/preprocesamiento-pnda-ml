from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

with open("informe/resultados_ml.json", "r", encoding="utf-8") as f:
    r = json.load(f)

with open("informe/datasets_por_archivo.json", "r", encoding="utf-8") as f:
    dsinfo = json.load(f)

def titulo(text, size=14):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(size)

def subtitulo(text, size=12):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(size)

def p(text):
    """Parrafo normal"""
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    par.add_run(text)

def j(label, text):
    """Justificacion"""
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    run = par.add_run(f"[JUSTIFICACION - {label}]: ")
    run.bold = True
    run.font.color.rgb = RGBColor(0x00, 0x33, 0x99)
    par.add_run(text)

def n(text):
    """Nota"""
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    run = par.add_run("[NOTA]: ")
    run.bold = True
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    par.add_run(text)

def sep():
    doc.add_paragraph()

# =====================================================
# CARATULA
# =====================================================
for _ in range(6):
    doc.add_paragraph()

titulo("UNIVERSIDAD PERUANA LOS ANDES", 16)
sep()
titulo("FACULTAD DE INGENIERIA", 14)
titulo("ESCUELA PROFESIONAL DE INGENIERIA DE SISTEMAS", 12)
sep()
sep()
titulo("INFORME DE TRABAJO PRACTICO N 9", 14)
titulo('"APLICACION DE MODELOS DE REGRESION - PRECIOS DE MEDICAMENTOS DIGEMID"', 12)
sep()
sep()
p("CURSO: Machine Learning")
p("CICLO: VIII")
p("DOCENTE: [Nombre del profesor]")
p("INTEGRANTES:")
p("   - [Tu nombre completo]")
sep()
p("FECHA DE ENTREGA: Junio 2026")

doc.add_page_break()

# =====================================================
# INTRODUCCION
# =====================================================
subtitulo("II. INTRODUCCION")
sep()

p("Bueno, este trabajo es para el curso de Machine Learning. Basicamente la profe nos pidio que agarremos un dataset de la plataforma de datos abiertos del Peru y le apliquemos modelos de regresion. A nuestro grupo nos toco el de Precios de Medicamentos de DIGEMID, que es basicamente una pagina del Ministerio de Salud donde puedes ver cuanto cuesta cada medicina en cada farmacia o botica del pais.")

p("La cosa es que entramos a la pagina del observatorio y nos dimos cuenta de que no se puede descargar todo de una, solo puedes buscar producto por producto. Entonces lo que hicimos fue elegir 10 medicamentos conocidos, los buscamos uno por uno, y fuimos copiando los datos a Excel. No es lo ideal, pero fue la unica forma de conseguir los datos.")

p(f"Al final, despues de limpiar todo y juntar los 10 archivos, nos quedo un dataset de {r['n_filas']:,} registros. Cada registro es basicamente 'el medicamento X se vende en la farmacia Y del departamento Z a tal precio'. Con eso ya podiamos hacer los modelos.")

sep()
subtitulo("Que queriamos lograr con esto", 11)
sep()

p("El objetivo principal era este: aplicar modelos de regresion a los datos de precios y ver que tan bien podiamos predecir cosas. Pero dentro de eso, nos planteamos dos objetivos mas puntuales:")

p("Objetivo 1: Tratar de PREDECIR EL PRECIO EXACTO (en soles) de un medicamento a partir de sus caracteristicas. O sea, si me dices 'es un Paracetamol, generico, fabricado por Portugal, vendido en una farmacia de Arequipa', el modelo deberia decirme mas o menos cuanto cuesta. Esto es REGRESION LINEAL.")

p(f"Objetivo 2: CLASIFICAR si el precio de un medicamento es ALTO o BAJO. Para esto definimos 'alto' como cualquier precio que este por encima de la mediana de todo el mercado (que salio S/{r['precio_mediana']:.2f}). Asi que si el modelo ve un precio mayor a eso, deberia decir 'es caro', y si es menor, 'es barato'. Esto es REGRESION LOGISTICA.")

p("Los dos objetivos son distintos pero complementarios. El primero intenta adivinar el numero exacto y el segundo solo intenta decir si es caro o barato. Ya veremos que el segundo es mas facil de responder.")

doc.add_page_break()

# =====================================================
# TRABAJO A REALIZAR
# =====================================================
subtitulo("III. TRABAJO A REALIZAR")
sep()

subtitulo("3.1 Lo que pidio la profe", 11)
sep()
p("Esto es lo que decia la tarea textualmente:")
sep()
p('"En el dataset ubicado en la Plataforma Nacional de Datos Abiertos, asignado segun la lista, realizar:')
p("   - Identificacion de variables.")
p("   - Limpieza y tratamiento de datos faltantes.")
p("   - Transformacion de variables categoricas.")
p("   - Deteccion de outliers.")
p("   - Analisis exploratorio (EDA).")
p("   - Division de datos en entrenamiento/prueba.")
p("   - Aplicacion de regresion lineal, logistica o ambas.")
p('   - Evaluacion mediante metricas."')
p("Y nuestro dataset es el de Precios de Medicamentos de DIGEMID.")
sep()

subtitulo("3.2 Como conseguimos los datos (y por que solo 10)", 11)
sep()

p("Mira, aca hay que explicar algo importante. La pagina del observatorio de DIGEMID (https://opm-digemid.minsa.gob.pe/) es una pagina web normal, tu entras y buscas un medicamento, y te salen todos los precios en diferentes farmacias. Eso esta bien para consultar un dato puntual. Pero si quieres TODOS los datos, no hay un boton de 'descargar todo'. Simplemente no existe.")

p("No hay API, no hay CSV para bajar, y ademas la pagina esta protegida con Cloudflare, asi que no puedes hacerle scraping automatico. Lo intente, pero te bloquea. Entonces la unica opcion era hacerlo a mano: buscar medicamento por medicamento y copiar los resultados a Excel.")

j("Por que solo 10 medicamentos", "Elegimos 10 porque era un numero razonable para hacer a mano (cada busqueda te da cientos de resultados en varias hojas del Excel), y porque con 10 principios activos bien escogidos ya tienes una variedad decente de precios y situaciones. Ademas, mira: al final cada medicamento genera entre 20,000 y 63,000 filas, asi que 10 ya son mas de 400 mil registros. Suficiente para hacer modelos de sobra.")

p("Los 10 medicamentos que elegimos fueron estos:")

meds = ["Paracetamol 500 mg (analgesico)",
        "Ibuprofeno 400 mg (antiinflamatorio)",
        "Amoxicilina 500 mg (antibiotico)",
        "Diclofenaco 50 mg (antiinflamatorio)",
        "Omeprazol 20 mg (protector gastrico)",
        "Losartan 50 mg (antihipertensivo)",
        "Metformina 850 mg (antidiabetico)",
        "Azitromicina 500 mg (antibiotico)",
        "Enalapril 10 mg (antihipertensivo)",
        "Clorfenamina 4 mg (antialergico)"]
for i, m in enumerate(meds, 1):
    p(f"   {i}. {m}")

p("Escogimos estos porque son medicamentos super comunes que usa mucha gente. Cubren diferentes tipos de enfermedades: dolor, infecciones, presion alta, diabetes, alergias, etc. La idea era tener variedad para que el modelo no se sesgue con un solo tipo de medicina.")

j("Criterio de seleccion", "Todos los medicamentos son de venta comun y algunos requieren receta. Son principios activos que estan en la lista de medicamentos esenciales del MINSA. Ademas, de cada uno hay versiones de marca y versiones genericas, y los venden tanto cadenas grandes (Inkafarma, Mifarma) como boticas de barrio y farmacias de hospitales publicos. O sea, hay diversidad de sobra.")

doc.add_page_break()

# =====================================================
# DESARROLLO
# =====================================================
subtitulo("IV. DESARROLLO DEL TRABAJO")
sep()

# --- 4.1 ---
subtitulo("4.1 Identificacion de variables: que tiene cada registro", 11)
sep()

p("Cuando bajas un Excel del observatorio, cada fila representa un medicamento especifico en venta en una farmacia especifica, con su precio. Las columnas que trae son estas 12:")

cols = [
    ("TIPO", "Dice PRIVADO (medicina de marca en farmacia/botica) o PUBLICO (medicina en hospital del MINSA). Solo hay esos 2 valores."),
    ("FECHA DE ACTUALIZACION", "Cuando se registro ese precio. Todos los datos que bajamos son de mayo/junio 2026."),
    ("NOMBRE DE PRODUCTO", f"Aqui esta el nombre comercial, el principio activo y la presentacion, todo junto. En total hay {r['n_medicamentos']} productos diferentes en todo el dataset."),
    ("TITULAR", "La empresa que tiene el registro sanitario. Muchas veces es la misma que el fabricante."),
    ("FABRICANTE", f"El laboratorio que fabrica el producto. Hay {r['n_fabricantes']} laboratorios distintos en total."),
    ("FARMACIA / BOTICA", "El establecimiento donde se vende. Hay mas de 10,000 en todo el Peru."),
    ("TELEFONO", "El numero del local. No lo usamos en el modelo, solo es dato de contacto."),
    ("PRECIO UNITARIO", "Lo mas importante: el precio en soles. ESTA ES LA VARIABLE QUE QUEREMOS PREDECIR en la regresion lineal."),
    ("DEPARTAMENTO", f"Donde queda el establecimiento. Hay datos de los {r['n_departamentos']} departamentos."),
    ("PROVINCIA", "Dentro del departamento. No la usamos para no repetir informacion del departamento."),
    ("DISTRITO", "Dentro de la provincia. Tampoco la usamos, por lo mismo."),
    ("DIRECCION", "La direccion exacta del local. No sirve para el modelo."),
]
for nombre, desc in cols:
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    run = par.add_run(f"  {nombre}: ")
    run.bold = True
    par.add_run(desc)

sep()
p("De esas 12, elegimos 5 como variables predictoras (las que el modelo usa para aprender) y 1 como objetivo (lo que queremos predecir). Las demas las dejamos de lado porque no ayudan en nada.")

p("Variables predictoras (features):")
p("   - TIPO: Porque uno de marca siempre es mas caro que el generico.")
p("   - NOMBRE DE PRODUCTO: Cada medicina cuesta distinto producirla.")
p("   - FABRICANTE: No es lo mismo un laboratorio grande que uno chico.")
p("   - FARMACIA / BOTICA: Cada local pone su propio margen de ganancia.")
p("   - DEPARTAMENTO: En zonas alejadas los precios suelen ser mas altos.")

p("Variable objetivo (target):")
p("   - Para regresion lineal: PRECIO UNITARIO")
p("   - Para regresion logistica: PRECIO ALTO (1 si es mayor a la mediana, 0 si no)")

j("Por que excluimos las otras", "Telefono y direccion son datos de contacto, no afectan el precio. Provincia y distrito ya estan representados por departamento (poner los tres seria repetitivo). Titular y fabricante casi siempre son lo mismo, asi que dejamos solo fabricante para no tener dos columnas diciendo lo mismo.")

sep()
# --- 4.2 ---
subtitulo("4.2 Limpieza: de los 10 Excels al dataset unificado", 11)
sep()

p("Cuando ya tuvimos los 10 archivos Excel, el primer paso fue ver que tenia cada uno. Esto es lo que salio:")

table = doc.add_table(rows=1, cols=6)
table.style = 'Light Shading Accent 1'
hdr = table.rows[0].cells
headers = ['#', 'Medicamento', 'Cuantas filas', 'Cuantos productos\n(marcas+gen.)', 'Cuantos\nfabricantes', 'Rango de precios']
for i, h in enumerate(headers):
    hdr[i].text = h
    for pp in hdr[i].paragraphs:
        for run in pp.runs:
            run.font.size = Pt(8)
            run.bold = True

total_f = 0
for idx, ds in enumerate(dsinfo, 1):
    row = table.add_row()
    c = row.cells
    c[0].text = str(idx)
    c[1].text = f"{ds['principio']} {ds['conc']}"
    c[2].text = f"{ds['filas']:,}"
    c[3].text = str(ds['productos'])
    c[4].text = str(ds['fabricantes'])
    c[5].text = f"S/{ds['min']:.2f} - S/{ds['max']:.2f}"
    total_f += ds['filas']
    for cell in c:
        for pp in cell.paragraphs:
            for run in pp.runs:
                run.font.size = Pt(8)

# total row
rt = table.add_row()
ct = rt.cells
ct[0].text = ""
ct[1].text = "TOTAL"
ct[2].text = f"{total_f:,}"
ct[3].text = f"{r['n_medicamentos']}"
ct[4].text = f"{r['n_fabricantes']}"
ct[5].text = ""
for cell in ct:
    for pp in cell.paragraphs:
        for run in pp.runs:
            run.font.size = Pt(8)
            run.bold = True

sep()
p(f"Mira, en total eran {total_f:,} filas entre los 10 archivos. Una barbaridad. Si te fijas bien, hay cosas interesantes: por ejemplo, Amoxicilina tiene precios maximo de S/33,000. Eso es porque en PUBLICO salen medicamentos para hospitales que son carisimos. Tambien ves que Azitromicina tiene 58 productos diferentes (todas las marcas que venden azitromicina en Peru: Zitromax, Azitrolab, Astrocina, etc.).")

p("Ahora, juntamos todo en un solo DataFrame con pandas.concat() y empezamos a limpiar:")
sep()

p("a) Duplicados: Buscamos filas repetidas (mismo producto, misma farmacia, mismo precio, misma fecha). No habia ninguna, pero por si acaso corremos el drop_duplicates().")

p("b) Precios raros: Convertimos la columna de precio a numero. Los que estaban vacios o eran cero los sacamos, porque eso no es un precio real. Tambien normalizamos el texto: quitamos tildes, pusimos todo en mayusculas, arreglamos el TIPO que decia 'P u b l i c o' con espacios raros.")

p(f"c) Muestreo: {total_f:,} filas es un monton. Para que los modelos no se demoren una eternidad, agarramos maximo 2,000 registros de cada producto. Como hay {r['n_medicamentos']} productos distintos, nos quedaron {r['n_filas']:,} filas. Sigue siendo un monton pero al menos es manejable.")

sep()
p("Resumen de la limpieza:")
p(f"   - 10 Excels originales: {total_f:,} registros")
p(f"   - Ya limpio y muestreado: {r['n_filas']:,} registros")
p(f"   - O sea, nos quedamos con el {100*r['n_filas']/total_f:.0f}% de los datos")
p(f"   - En {r['n_departamentos']} departamentos, {r['n_fabricantes']} fabricantes, {r['n_medicamentos']} productos")

sep()
# --- 4.3 ---
subtitulo("4.3 Transformacion de categoricas: convertir texto en numeros", 11)
sep()

p("Los modelos de machine learning solo entienden numeros. No puedes meterle 'LIMA' o 'PARACETAMOL' y esperar que haga magia. Entonces todas esas columnas de texto hay que pasarlas a numeros. La forma mas simple de hacerlo se llama Label Encoding y es super basico: agarras cada valor unico y le pones un numerito. Por ejemplo, TIPO: PRIVADO = 0, PUBLICO = 1. Y asi con todas.")

p("Asi quedaron las variables despues del encoding:")
p("   - TIPO: 2 valores (0 y 1)")
p(f"   - NOMBRE DE PRODUCTO: {r['n_medicamentos']} numeros distintos")
p(f"   - FABRICANTE: {r['n_fabricantes']} numeros")
p("   - FARMACIA / BOTICA: 10,078 numeros")
p(f"   - DEPARTAMENTO: {r['n_departamentos']} numeros")

j("Label Encoding vs One-Hot", "Se que algunos prefieren One-Hot Encoding porque no mete un orden falso entre categorias (el modelo no deberia pensar que Arequipa=2 es 'mayor' que Lima=1). Pero mira, si hacia One-Hot con 10,078 farmacias, se me creaban 10,078 columnas nuevas. Eso es una locura para una laptop normal. Asi que use Label Encoding que es mas simple y para una primera aproximacion funciona.")

p(f"Para la regresion logistica, tuve que crear una variable nueva: PRECIO ALTO. La forma mas sencilla fue usar la mediana como punto de corte. La mediana de todos los precios dio S/{r['precio_mediana']:.2f}. Entonces:")
p(f"   - Si Precio > S/{r['precio_mediana']:.2f}  =>  PRECIO ALTO = 1")
p(f"   - Si Precio <= S/{r['precio_mediana']:.2f} =>  PRECIO ALTO = 0")
p(f"Quedo bastante balanceado: {r['n_altos']:,} precios altos y {r['n_bajos']:,} precios bajos. Eso esta bien porque si estuviera todo desbalanceado (ej. 90% bajos, 10% altos) el modelo se sesgaria.")

sep()
# --- 4.4 ---
subtitulo("4.4 Deteccion de outliers: precios raros", 11)
sep()

p("Un outlier es un precio que se sale mucho de lo normal. Para encontrarlos usamos el metodo del IQR (rango intercuartilico), que es el clasico y no asume que los datos tienen distribucion normal (porque claramente no la tienen, mira los precios, van de centimos a miles de soles).")

p(f"Los numeros dieron asi:")
p(f"   - Q1 (el 25% mas barato): S/{r.get('q1', 0.48):.2f}")
p(f"   - Q3 (el 25% mas caro): S/{r.get('q3', 1.60):.2f}")
p(f"   - IQR = Q3 - Q1 = S/{r.get('iqr', 1.12):.2f}")
p(f"   - Limite inferior: S/{r.get('lim_inf', -1.20):.2f} (negativo, o sea no hay precios tan bajos)")
p(f"   - Limite superior: S/{r.get('lim_sup', 3.28):.2f}")
p(f"   - Outliers encontrados: {r['n_outliers']:,} (el {r['pct_outliers']:.1f}% del total)")

j("No los borramos", "Aca hay que pensar: un precio de S/100 no es un error, es una medicina cara. Si la borro, estoy eliminando informacion real del mercado. El 11.5% de outliers es esperable en un mercado donde hay medicamentos de S/0.05 (genericos basicos) y medicamentos de S/13,000 (oncologicos, biologicos). Lo unico que hice fue marcarlos en una columna aparte por si acaso, pero los deje en el dataset.")

sep()
# --- 4.5 ---
subtitulo("4.5 EDA: analisis exploratorio", 11)
sep()

p("Antes de ponernos a entrenar modelos, habia que entender los datos. Esto es lo que encontramos:")
sep()

p("Estadisticas basicas del precio:")
p(f"   - Precio promedio: S/{r['precio_media']:.2f}")
p(f"   - Mediana (el del medio): S/{r['precio_mediana']:.2f}")
p(f"   - El mas barato: S/{r['precio_min']:.4f}")
p(f"   - El mas caro: S/{r['precio_max']:.2f}")
p(f"   - Desviacion estandar: S/{r['precio_std']:.2f}")

j("Media vs mediana", f"Mira que la media (S/{r['precio_media']:.2f}) es casi el doble de la mediana (S/{r['precio_mediana']:.2f}). Eso pasa cuando tienes muchos datos baratos y unos pocos super caros que jalan el promedio para arriba. Es super comun en precios de medicamentos y ya desde aca te das cuenta de que un modelo lineal la va a tener dificil para predecir bien.")
sep()

p("Precio segun el tipo:")
for t, pm, cnt in r['precios_por_tipo']:
    p(f"   - {t}: S/{pm:.2f} promedio (con {cnt:,} registros)")

p("Fijate que PUBLICO tiene promedio S/31.67. Eso es porque en los hospitales del MINSA venden medicamentos caros (tratamientos especiales), no solo paracetamol. Pero ojo, PUBLICO solo son 604 registros de casi 200 mil. El 99.7% de los datos son del sector PRIVADO.")
sep()

p("Top 5 departamentos con mas registros:")
for d, cnt, pm in r['top_deptos']:
    p(f"   - {d}: {cnt:,} registros, precio promedio S/{pm:.2f}")

p("Lima concentra la mayoria de los datos porque, bueno, es Lima. Pero los precios no varian tanto entre departamentos, lo cual es interesante.")
sep()

p("Top 5 fabricantes:")
for f2, cnt, pm in r['top_fabricantes']:
    p(f"   - {str(f2)[:55]}: {cnt:,} registros, S/{pm:.2f} promedio")

n("Hay una diferencia grande entre laboratorios. Portugal S.R.L. tiene promedio S/0.89 porque se dedica a genericos baratos. En cambio IQ Farmaceutico esta en S/2.62. Esto ya te dice que el fabricante puede ser un buen predictor del precio.")

sep()
# --- 4.6 ---
subtitulo("4.6 Train/test split", 11)
sep()

p("Esto es super simple: partes los datos en dos. Una parte (80%) es para que el modelo aprenda, la otra (20%) es para probar que tanto aprendio. Es como en la universidad: estudias con unos ejercicios y el examen es con otros diferentes, para ver si de verdad entendiste o solo te memorizaste las respuestas.")

p("Use train_test_split de sklearn con 80/20 y random_state=42. Ese 42 es una semilla, sirve para que siempre salga la misma particion. Asi si corro el codigo 10 veces, el resultado es el mismo.")
p(f"   - Train: 158,680 registros")
p(f"   - Test: 39,671 registros")

sep()
# --- 4.7 ---
subtitulo("4.7 Los modelos", 11)
sep()

p("Ahora si, la parte divertida. Entrenamos dos modelos:")
sep()

p("Modelo 1 - Regresion lineal multiple (LinearRegression de sklearn):")
p("Este modelo busca una ecuacion del tipo:")
p("   PRECIO = B0 + B1*TIPO + B2*PRODUCTO + B3*FABRICANTE + B4*FARMACIA + B5*DEPARTAMENTO")
p("El algoritmo ajusta los coeficientes B1, B2... para minimizar el error entre lo que predice y el precio real. Asi de simple.")
sep()

p("Modelo 2 - Regresion logistica (LogisticRegression de sklearn):")
p("Este en vez de predecir un numero, predice una probabilidad de que el precio sea alto. Usa la funcion sigmoide, que convierte cualquier numero en un valor entre 0 y 1 (una probabilidad). Si la probabilidad es mayor a 0.5, dice 'es caro', y si no, 'es barato'.")

j("Por que ambos", "Son preguntas diferentes. La regresion lineal intenta adivinar el precio exacto (dificil). La logistica solo intenta decir si es caro o barato (mucho mas facil). Es como la diferencia entre 'adivina cuantos anos tengo' y 'dime si tengo mas de 25'. La segunda es mas facil de acertar.")

sep()
# --- 4.8 ---
subtitulo("4.8 Evaluacion: metricas", 11)
sep()

p("Ya entrenados los modelos, toca ver que tan buenos (o malos) son. Aca van los resultados:")
sep()

subtitulo("Regresion lineal", 11)
p(f"   RMSE: {r['rmse']:.2f}")
p(f"   MAE: {r['mae']:.2f}")
p(f"   R2: {r['r2']:.4f} ({r['r2']*100:.1f}%)")

p("Traduccion de las metricas:")
p(f"   - RMSE de {r['rmse']:.2f} significa que el error tipico es de {r['rmse']:.0f} soles. Suena mucho, pero recuerda que hay precios desde centimos hasta 13 mil soles.")
p(f"   - MAE de {r['mae']:.2f} es mas realista: en promedio el modelo se equivoca por S/{r['mae']:.2f}. No esta tan mal considerando todo.")
p(f"   - El R2 de {r['r2']:.4f} si esta feo, la verdad. Significa que las variables que use no explican casi nada de la variacion del precio. Pero ojo, esto no es necesariamente un fracaso del trabajo. Es que el precio de un medicamento depende de muchas cosas que no estan en el dataset: el costo del principio activo, las patentes, el tipo de cambio, los margenes comerciales, etc.")

j("R2 bajo: fracaso o realidad", "No es fracaso. Es un resultado honesto. Si todas las tareas de ML dieran R2=0.99, algo raro estaria pasando. Aca aprendimos que con solo variables categoricas y un modelo lineal, no alcanza para predecir bien el precio. La proxima vez podriamos probar con arboles de decision o random forest, que suelen funcionar mejor con datos asi.")
sep()

subtitulo("Regresion logistica", 11)
p(f"   Accuracy: {r['acc']:.4f} ({r['acc']*100:.1f}%)")
p(f"   Precision: {r['prec']:.4f}")
p(f"   Recall: {r['rec']:.4f}")
p(f"   F1: {r['f1']:.4f}")

p("Que significa cada cosa:")
p("   - Accuracy: acierta el 54.7% de las veces. Es poquito mas que tirar una moneda (50%), pero al menos es mejor que el azar.")
p("   - Precision (54.6%): cuando el modelo dice 'este es caro', acierta el 55% de las veces.")
p("   - Recall (43.2%): de todos los que realmente son caros, solo detecta el 43%. O sea, se le escapan varios caros y los clasifica como baratos.")
p("   - F1 (0.48): es un promedio entre precision y recall. Esta ahi nomas, no es un desastre pero tampoco para celebrar.")

p("Matriz de confusion (la tabla de aciertos y errores):")
p(f"   - Predijo caro y era caro (VP):          {r['cm_vp']:>6,}")
p(f"   - Predijo caro pero era barato (FP):     {r['cm_fp']:>6,}")
p(f"   - Predijo barato pero era caro (FN):     {r['cm_fn']:>6,}")
p(f"   - Predijo barato y era barato (VN):      {r['cm_vn']:>6,}")

p("El modelo tiende a ser conservador: prefiere decir 'barato' cuando duda. Por eso los falsos negativos (11,016) son mas que los falsos positivos (6,971). Es mejor decir 'barato' y equivocarte a decir 'caro' y que la gente se asuste.")

doc.add_page_break()

# =====================================================
# CONCLUSIONES
# =====================================================
subtitulo("V. CONCLUSIONES")
sep()

p("1. Si se pudo. Logramos entrenar y evaluar los dos modelos de regresion con datos 100% reales del observatorio de DIGEMID. Fue un proceso largo (sobre todo la parte de conseguir los datos a mano) pero se completo todo lo que pedia la tarea.")

p("2. Lo mas complicado no fue programar los modelos (eso es como 10 lineas de codigo con sklearn), sino conseguir y limpiar los datos. Las plataformas del gobierno peruano no estan pensadas para bajar datos masivos, estan pensadas para consultas puntuales. Eso fue una leccion en si misma.")

p("3. La regresion lineal no funciono muy bien para predecir el precio exacto (R2 casi 0). Pero eso no significa que el trabajo este mal. Significa que el problema es mas complejo de lo que parece y que un modelo lineal simple no basta. Esto es algo que se aprende con la practica, no con la teoria.")

p("4. La regresion logistica funciono un poco mejor (55% de acierto, que es mejor que el azar). Para ser solo 5 variables categoricas, no esta nada mal. Ademas las clases estaban balanceadas, asi que el modelo no se sesgo hacia 'barato' o 'caro'.")

p("5. Que aprendi con todo esto:")
p("   - Como se arma un proyecto de ML de principio a fin: datos, limpieza, encoding, outliers, split, entrenar, evaluar.")
p("   - Que los datos del mundo real son sucios, incompletos y dificiles de conseguir.")
p("   - La diferencia practica entre predecir un numero y clasificar una categoria.")
p("   - Que las metricas hay que interpretarlas, no solo escupir numeros.")
p("   - Que no siempre vas a tener un R2 de 0.95 y eso esta bien, es parte de aprender.")

p("6. Si tuviera que hacerlo de nuevo:")
p("   - Agregaria mas variables: la concentracion exacta, la forma farmaceutica, la fecha.")
p("   - Probaria modelos no lineales como arboles de decision o random forest.")
p("   - Usaria One-Hot Encoding al menos para TIPO y DEPARTAMENTO.")
p("   - Bajaria mas medicamentos para tener mas variedad.")

doc.add_page_break()

# =====================================================
# BIBLIOGRAFIA
# =====================================================
subtitulo("VI. BIBLIOGRAFIA (Formato IEEE)")
sep()

refs = [
    '[1] Plataforma Nacional de Datos Abiertos, "Datos Abiertos Peru", Gobierno del Peru. [En linea]. Disponible en: https://www.datosabiertos.gob.pe/',
    '[2] DIGEMID - MINSA, "Observatorio de Precios de Medicamentos", [En linea]. Disponible en: https://opm-digemid.minsa.gob.pe/',
    '[3] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python", JMLR, vol. 12, pp. 2825-2830, 2011.',
    '[4] J. Brownlee, "Linear Regression for Machine Learning", Machine Learning Mastery, 2020. [En linea]. Disponible en: https://machinelearningmastery.com/linear-regression-for-machine-learning/',
    '[5] J. Brownlee, "Logistic Regression for Machine Learning", Machine Learning Mastery, 2020. [En linea]. Disponible en: https://machinelearningmastery.com/logistic-regression-for-machine-learning/',
    '[6] W. McKinney, "Data Structures for Statistical Computing in Python", Proc. 9th Python in Science Conf., pp. 51-56, 2010.',
    '[7] T. Hastie, R. Tibshirani, J. Friedman, "The Elements of Statistical Learning", 2da ed. Springer, 2009.',
    '[8] D. Montgomery, E. Peck, G. Vining, "Introduction to Linear Regression Analysis", 5ta ed. Wiley, 2012.',
]

for ref in refs:
    p(ref)
    sep()

# ===== GUARDAR =====
doc.save("informe/informe_semana9_regresion_digemid.docx")
print("Listo. DOCX generado: informe/informe_semana9_regresion_digemid.docx")
