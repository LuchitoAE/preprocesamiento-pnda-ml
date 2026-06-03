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
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    par.add_run(text)

def j(label, text):
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    run = par.add_run(f"[JUSTIFICACION - {label}]: ")
    run.bold = True
    run.font.color.rgb = RGBColor(0x00, 0x33, 0x99)
    par.add_run(text)

def n(text):
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
titulo('"APLICACION DE LOS MODELOS DE REGRESION"', 12)
sep()
sep()
p("CURSO: Machine Learning")
p("CICLO: VIII")
p("DOCENTE: Ing. Cabrera Padilla, Jowel Sigfrido")
p("INTEGRANTES:")
p("   - Aquino Espinoza, Luis Walter")
sep()
p("FECHA DE ENTREGA: Junio 2026")

doc.add_page_break()

# =====================================================
# INTRODUCCION
# =====================================================
subtitulo("II. INTRODUCCION")
sep()

p("El presente informe corresponde a la actividad de la semana 9 del curso de Machine Learning, titulada 'Aplicacion de los modelos de regresion'. Esta consiste en tomar un dataset disponible en la Plataforma Nacional de Datos Abiertos del Peru (PNDA), aplicarle un proceso completo de limpieza y preprocesamiento, y posteriormente construir modelos de regresion lineal y logistica para evaluar su capacidad predictiva.")

p("El dataset asignado segun la lista publicada por el docente en Microsoft Teams es el de 'Precios de Medicamentos en Establecimientos de Salud', elaborado por la Direccion General de Medicamentos, Insumos y Drogas (DIGEMID) del Ministerio de Salud. Sin embargo, al ingresar a la PNDA (https://www.datosabiertos.gob.pe/) en busca de este dataset, no se encontro un archivo descargable como tal. Lo unico disponible es el Observatorio de Precios de Medicamentos de DIGEMID (https://opm-digemid.minsa.gob.pe/), una aplicacion web interactiva que permite consultar precios producto por producto, pero que no ofrece una opcion de descarga masiva de todos los registros.")

p("Ante esta limitacion, se procedio a recolectar los datos de forma manual desde el propio observatorio. Se seleccionaron 10 medicamentos de alto consumo en el mercado peruano, se buscaron uno por uno en la plataforma y se exportaron los resultados en formato Excel. Posteriormente, los 10 archivos fueron concatenados y sometidos a un proceso de limpieza, normalizacion y muestreo estratificado, obteniendo como resultado un dataset unificado de 198,351 registros con precios reales de medicamentos en establecimientos de salud de los 25 departamentos del Peru.")

sep()
subtitulo("Objetivos del trabajo", 11)
sep()

p("El objetivo general de este trabajo es aplicar tecnicas de machine learning supervisado para analizar el comportamiento de los precios de medicamentos en el mercado peruano, utilizando datos reales extraidos del observatorio de DIGEMID.")

p("Objetivo especifico 1 - Regresion lineal multiple:")
p("Predecir el precio unitario de un medicamento (en soles) a partir de sus caracteristicas: tipo de producto (marca o generico), nombre del medicamento, laboratorio fabricante, establecimiento donde se vende y departamento de ubicacion. El modelo se evalua mediante las metricas RMSE, MAE y R2.")

p(f"Objetivo especifico 2 - Regresion logistica (clasificacion binaria):")
p(f"Clasificar si un medicamento tiene un precio alto o bajo, tomando como umbral la mediana de todos los precios del mercado, que resulto ser S/{r['precio_mediana']:.2f}. El modelo se evalua mediante accuracy, precision, recall, F1-score y matriz de confusion.")

doc.add_page_break()

# =====================================================
# TRABAJO A REALIZAR
# =====================================================
subtitulo("III. TRABAJO A REALIZAR")
sep()

subtitulo("3.1 Enunciado de la actividad", 11)
sep()

p("A continuacion se transcribe el enunciado de la actividad tal como fue publicado en Microsoft Teams por el docente:")
sep()
p('"APLICACION DE LOS MODELOS DE REGRESION')
p("En el dataset ubicado en el portal de la Plataforma Nacional de Datos Abiertos (https://www.gob.pe/datosabiertos) asignado de acuerdo a la lista (archivo adjunto), realizar lo siguiente:")
sep()
p("   - Identificacion de variables.")
p("   - Limpieza y tratamiento de datos faltantes.")
p("   - Transformacion de variables categoricas.")
p("   - Deteccion de outliers.")
p("   - Analisis exploratorio (EDA).")
p("   - Division de datos en entrenamiento/prueba.")
p("   - Aplicacion de regresion lineal, logistica o ambas.")
p("   - Evaluacion mediante metricas.")
sep()
p("El entregable es un informe que se debe hacer escrito a mano con la siguiente estructura:")
p("   - Caratula")
p("   - Introduccion (aqui debe indicar cual es el objetivo del trabajo)")
p("   - Trabajo a realizar (Enunciado del trabajo)")
p("   - Desarrollo del trabajo (Describir todas las tareas encargadas)")
p("   - Conclusiones (Indicar si se logro los objetivos y el aprendizaje alcanzado)")
p("   - Bibliografia (Listar las fuentes consultadas en formato estilo IEEE)")
sep()
p('Solo esta permitido usar herramientas IA para consultar ideas."')
sep()
p("En la seccion 'Materiales de referencia' del Teams, el docente adjunto una lista de datasets. A cada alumno le fue asignado uno diferente. El dataset correspondiente a este trabajo es: Dataset de Precios de Medicamentos en Establecimientos de Salud (DIGEMID).")
sep()

subtitulo("3.2 Sobre la obtencion de los datos", 11)
sep()

p("El dataset asignado, 'Precios de Medicamentos en Establecimientos de Salud (DIGEMID)', no se encuentra disponible como un archivo descargable dentro de la Plataforma Nacional de Datos Abiertos. Al buscar en el portal https://www.datosabiertos.gob.pe/ no se hallo un recurso CSV, Excel o similar que contenga todos los registros. Lo que existe es un enlace al Observatorio de Precios de Medicamentos de DIGEMID (https://opm-digemid.minsa.gob.pe/), el cual es una aplicacion web interactiva que permite consultar el precio de un medicamento especifico, pero no ofrece una funcion de exportacion masiva ni una API publica.")

j("Origen de los datos", "Los datos utilizados en este trabajo provienen del Observatorio de Precios de Medicamentos de DIGEMID, perteneciente al Ministerio de Salud del Peru. Si bien la actividad indicaba descargar el dataset desde la PNDA, al no existir tal descarga, se recurrio directamente a la fuente oficial de DIGEMID, que es el organismo que produce y publica estos datos. De esta forma, los datos son igualmente oficiales, actualizados y verificables.")

p("Dado que la plataforma solo permite consultas individuales y ademas cuenta con proteccion Cloudflare que impide el scraping automatizado, la unica via factible fue la recoleccion manual. Se seleccionaron 10 medicamentos de alto consumo en el mercado peruano, se ingresaron uno por uno en el buscador del observatorio y se exportaron los resultados en archivos Excel.")

j("Criterios de seleccion de los 10 medicamentos", "Se eligieron 10 principios activos que cubren distintas categorias terapeuticas esenciales: analgesicos (Paracetamol), antiinflamatorios (Ibuprofeno, Diclofenaco), antibioticos (Amoxicilina, Azitromicina), antihipertensivos (Losartan, Enalapril), antidiabeticos (Metformina), antihistaminicos (Clorfenamina) y protectores gastricos (Omeprazol). Esta seleccion garantiza diversidad de precios, tipos de fabricantes y contextos de uso. Ademas, cada medicamento genera miles de registros al ser comercializado en farmacias y boticas de todo el pais, por lo que con 10 principios activos se obtiene una base de datos mas que suficiente para el analisis (437,133 registros en bruto, que luego del muestreo quedaron en 198,351).")

p("Los medicamentos seleccionados fueron los siguientes:")

meds = [
    "Paracetamol 500 mg (analgesico y antipiretico)",
    "Ibuprofeno 400 mg (antiinflamatorio no esteroideo)",
    "Amoxicilina 500 mg (antibiotico de amplio espectro)",
    "Diclofenaco 50 mg (antiinflamatorio)",
    "Omeprazol 20 mg (inhibidor de la bomba de protones)",
    "Losartan 50 mg (antihipertensivo)",
    "Metformina 850 mg (antidiabetico oral)",
    "Azitromicina 500 mg (antibiotico macrolido)",
    "Enalapril 10 mg (antihipertensivo IECA)",
    "Clorfenamina 4 mg (antihistaminico)",
]
for i, m in enumerate(meds, 1):
    p(f"   {i}. {m}")

doc.add_page_break()

# =====================================================
# DESARROLLO
# =====================================================
subtitulo("IV. DESARROLLO DEL TRABAJO")
sep()

# --- 4.1 ---
subtitulo("4.1 Identificacion de variables", 11)
sep()

p("Cada archivo Excel exportado desde el observatorio de DIGEMID contiene 12 columnas. Cada fila representa un medicamento especifico en venta en una farmacia o botica determinada, con su respectivo precio registrado. A continuacion se describe cada columna:")

cols = [
    ("TIPO", "Categorico (2 valores: PRIVADO, PUBLICO). Indica si el producto corresponde al sector privado (farmacias, boticas, cadenas) o al sector publico (hospitales del MINSA)."),
    ("FECHA DE ACTUALIZACION", "Fecha y hora en que se registro o actualizo el precio en el observatorio. Todos los datos recolectados corresponden a mayo-junio de 2026."),
    ("NOMBRE DE PRODUCTO", f"Categorico ({r['n_medicamentos']} valores unicos). Contiene el nombre comercial, el principio activo, la concentracion y la forma farmaceutica (ej. 'PARACETAMOL 500 mg Tableta')."),
    ("TITULAR", "Categorico. Empresa que posee el registro sanitario del producto ante DIGEMID. En muchos casos coincide con el fabricante."),
    ("FABRICANTE", f"Categorico ({r['n_fabricantes']} valores unicos). Laboratorio que fabrica el medicamento."),
    ("FARMACIA / BOTICA", "Categorico (10,078 valores unicos). Nombre del establecimiento de salud donde se comercializa el producto."),
    ("TELEFONO", "Dato de contacto del establecimiento. No se utiliza en los modelos de regresion por carecer de valor predictivo."),
    ("PRECIO UNITARIO", "Cuantitativa continua. Precio de venta al publico expresado en soles (S/). Es la variable objetivo (target) para el modelo de regresion lineal."),
    ("DEPARTAMENTO", f"Categorico ({r['n_departamentos']} valores). Departamento donde se ubica el establecimiento."),
    ("PROVINCIA", "Categorico. No se utiliza para evitar redundancia con DEPARTAMENTO."),
    ("DISTRITO", "Categorico. No se utiliza por la misma razon que PROVINCIA."),
    ("DIRECCION", "Texto. Direccion exacta del establecimiento. No aporta valor predictivo al modelo."),
]
for nombre, desc in cols:
    par = doc.add_paragraph()
    par.paragraph_format.first_line_indent = Cm(1.25)
    run = par.add_run(f"  {nombre}: ")
    run.bold = True
    par.add_run(desc)

sep()
p("De las 12 columnas, se seleccionaron 5 como variables predictoras (features) y 1 como variable objetivo (target). Las 6 restantes se descartaron por no aportar informacion relevante para la prediccion.")
sep()

p("Variables predictoras seleccionadas:")
p("   - TIPO: Influye en el precio porque los productos de marca y genericos tienen estructuras de costo diferentes.")
p("   - NOMBRE DE PRODUCTO: Cada medicamento tiene un costo de produccion distinto segun su principio activo.")
p("   - FABRICANTE: Los laboratorios grandes y pequenos manejan escalas de produccion y margenes distintos.")
p("   - FARMACIA / BOTICA: Cada establecimiento aplica su propio margen comercial sobre el precio.")
p("   - DEPARTAMENTO: La ubicacion geografica afecta los costos logisticos y, por tanto, el precio final.")
sep()

p("Variable objetivo:")
p("   - Para regresion lineal: PRECIO UNITARIO (cuantitativa continua).")
p("   - Para regresion logistica: PRECIO_ALTO (binaria: 1 si el precio supera la mediana del mercado, 0 en caso contrario).")

j("Exclusion de variables", "TELEFONO y DIRECCION son datos de contacto sin relacion causal con el precio. PROVINCIA y DISTRITO se excluyen para evitar redundancia con DEPARTAMENTO y no aumentar la dimensionalidad del modelo innecesariamente. TITULAR se excluye porque en la mayoria de casos coincide con FABRICANTE, lo que generaria colinealidad.")

sep()
# --- 4.2 ---
subtitulo("4.2 Limpieza y tratamiento de datos faltantes", 11)
sep()

p("Una vez obtenidos los 10 archivos Excel desde el observatorio, el primer paso fue inspeccionar cada uno de forma individual antes de proceder a la union. A continuacion se muestra el desglose de cada dataset:")

# table
table = doc.add_table(rows=1, cols=6)
table.style = 'Light Shading Accent 1'
hdr = table.rows[0].cells
headers = ['#', 'Medicamento', 'Registros', 'Productos\n(marcas+gen.)', 'Fabricantes', 'Rango de precios']
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

rt = table.add_row()
ct = rt.cells
ct[0].text = ""
ct[1].text = "TOTAL BRUTO"
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
p(f"Como se observa en la tabla, los 10 archivos suman un total de {total_f:,} registros en bruto. Se aprecia que cada medicamento incluye todas sus variantes comerciales (marcas y genericos de distintos laboratorios), lo que explica que, por ejemplo, Azitromicina tenga 58 presentaciones diferentes en el mercado. Los {r['n_departamentos']} departamentos del Peru estan representados en todos los archivos, garantizando cobertura nacional. En cuanto a los precios, se observa una dispersion considerable: desde S/0.01 (medicamentos genericos basicos) hasta S/33,000.00 (medicamentos de alto costo del sector publico).")

p("Posteriormente, los 10 archivos se concatenaron en un unico DataFrame utilizando pandas.concat(). Sobre este dataset unificado se aplico el siguiente proceso de limpieza:")
sep()

p("a) Eliminacion de duplicados. Se verifico la existencia de filas identicas (mismo producto, mismo establecimiento, mismo precio en la misma fecha). No se encontraron registros duplicados, pero se ejecuto drop_duplicates() como medida preventiva.")
sep()

p("b) Conversion y filtrado del precio. La columna PRECIO UNITARIO se convirtio de texto a tipo numerico (float). Los registros con precio nulo, igual a cero o negativo fueron eliminados, ya que no representan un valor de mercado valido.")
sep()

p("c) Normalizacion de texto. Se eliminaron tildes, se unificaron mayusculas y se removieron espacios sobrantes en todos los campos de texto. Ademas, se corrigio la columna TIPO que presentaba caracteres con espaciado irregular (ej. 'P u b l i c o' fue corregido a 'PUBLICO').")

j("Importancia de la normalizacion", "Sin este paso, variantes como 'LIMA', 'Lima' y 'lima' serian tratadas como categorias distintas por el modelo, fragmentando artificialmente los datos y debilitando la capacidad predictiva. La normalizacion asegura que cada entidad geografica, fabricante o producto tenga una representacion unica y consistente.")
sep()

p(f"d) Muestreo estratificado. El dataset bruto de {total_f:,} registros resultaba excesivo para el entrenamiento de los modelos, sin que un mayor volumen aportara necesariamente un beneficio predictivo proporcional. Se aplico un muestreo estratificado, limitando a un maximo de 2,000 registros por cada una de las {r['n_medicamentos']} presentaciones de medicamento. Este procedimiento preserva la diversidad de la muestra (todas las presentaciones estan representadas) mientras mantiene un tamano manejable para los algoritmos de regresion.")
sep()

p("Resultado del proceso de limpieza:")
p(f"   - Datos brutos (10 archivos): {total_f:,} registros")
p(f"   - Datos limpios y muestreados: {r['n_filas']:,} registros")
p(f"   - Porcentaje conservado: {100*r['n_filas']/total_f:.0f}%")
p(f"   - Cobertura: {r['n_departamentos']} departamentos, {r['n_fabricantes']} fabricantes, {r['n_medicamentos']} productos")

sep()
# --- 4.3 ---
subtitulo("4.3 Transformacion de variables categoricas", 11)
sep()

p("Los modelos de regresion, tanto lineal como logistica, operan exclusivamente con valores numericos. Dado que la mayoria de las variables del dataset son de tipo texto (categoricas), fue necesario transformarlas a formato numerico antes de entrenar los modelos.")
sep()

p("a) Label Encoding. A cada valor unico dentro de una columna categorica se le asigna un numero entero consecutivo. Este metodo se aplico a las cinco variables predictoras:")
p(f"   - TIPO: 2 categorias")
p(f"   - NOMBRE DE PRODUCTO: {r['n_medicamentos']} categorias")
p(f"   - FABRICANTE: {r['n_fabricantes']} categorias")
p("   - FARMACIA / BOTICA: 10,078 categorias")
p(f"   - DEPARTAMENTO: {r['n_departamentos']} categorias")

j("Eleccion de Label Encoding sobre One-Hot Encoding", "La alternativa mas comun a Label Encoding es One-Hot Encoding, que crea una columna binaria por cada categoria. Sin embargo, con 10,078 farmacias distintas, este metodo habria generado mas de 10,000 columnas adicionales, resultando en una matriz extremadamente dispersa y computacionalmente costosa. Para este analisis exploratorio, Label Encoding representa una simplificacion razonable, aunque se reconoce que introduce un orden artificial entre categorias que no existe en la realidad.")
sep()

p(f"b) Creacion de la variable objetivo binaria. Para la regresion logistica se genero la columna PRECIO_ALTO, tomando como umbral la mediana de todos los precios, que resulto ser S/{r['precio_mediana']:.2f}. Los valores se asignaron de la siguiente forma:")
p(f"   - PRECIO_ALTO = 1 si Precio > S/{r['precio_mediana']:.2f}")
p(f"   - PRECIO_ALTO = 0 si Precio <= S/{r['precio_mediana']:.2f}")
p(f"La distribucion resultante fue: {r['n_altos']:,} precios altos y {r['n_bajos']:,} precios bajos. Esta proporcion es practicamente balanceada, lo cual es deseable porque evita que el modelo de clasificacion se sesgue hacia la clase mayoritaria.")

sep()
# --- 4.4 ---
subtitulo("4.4 Deteccion de outliers", 11)
sep()

p("Se entiende por outlier un valor que se aleja significativamente del resto de las observaciones. Para identificarlos se utilizo el metodo del Rango Intercuartilico (IQR), que es robusto frente a distribuciones asimetricas y no asume normalidad en los datos.")

p(f"Los resultados del calculo fueron los siguientes:")
p(f"   - Q1 (percentil 25): S/{r.get('q1', 0.48):.2f}")
p(f"   - Q3 (percentil 75): S/{r.get('q3', 1.60):.2f}")
p(f"   - IQR = Q3 - Q1: S/{r.get('iqr', 1.12):.2f}")
p(f"   - Limite inferior = Q1 - 1.5 * IQR: S/{r.get('lim_inf', -1.20):.2f}")
p(f"   - Limite superior = Q3 + 1.5 * IQR: S/{r.get('lim_sup', 3.28):.2f}")
p(f"   - Outliers detectados: {r['n_outliers']:,} registros ({r['pct_outliers']:.1f}% del total)")

j("Decision de no eliminar los outliers", "En el contexto de precios de medicamentos, un valor alejado no constituye necesariamente un error. Un precio de S/100 o S/1,000 puede corresponder a un medicamento de marca, un producto biologico o un tratamiento oncologico. Eliminar estos registros implicaria descartar informacion genuina del mercado y sesgar el analisis hacia unicamente medicamentos de bajo costo. Por esta razon, los outliers fueron identificados y marcados en una columna adicional, pero no fueron removidos del dataset.")

sep()
# --- 4.5 ---
subtitulo("4.5 Analisis exploratorio de datos (EDA)", 11)
sep()

p("Previo al entrenamiento de los modelos, se realizo un analisis descriptivo para comprender la distribucion de los precios y las relaciones entre las variables.")
sep()

p("Estadisticas descriptivas del precio unitario:")
p(f"   - Media: S/{r['precio_media']:.2f}")
p(f"   - Mediana: S/{r['precio_mediana']:.2f}")
p(f"   - Minimo: S/{r['precio_min']:.4f}")
p(f"   - Maximo: S/{r['precio_max']:.2f}")
p(f"   - Desviacion estandar: S/{r['precio_std']:.2f}")

p(f"Se observa una diferencia notable entre la media (S/{r['precio_media']:.2f}) y la mediana (S/{r['precio_mediana']:.2f}). Esto indica que la distribucion de precios presenta un sesgo positivo (cola derecha), donde una gran cantidad de medicamentos tienen precios bajos y unos pocos alcanzan precios muy elevados. Esta asimetria es caracteristica del mercado farmaceutico y representa un desafio para los modelos lineales, que asumen relaciones mas uniformes entre las variables.")
sep()

p("Precio segun el tipo de producto:")
for t, pm, cnt in r['precios_por_tipo']:
    p(f"   - {t}: promedio S/{pm:.2f} ({cnt:,} registros)")

p("El precio promedio del sector PUBLICO es significativamente mayor (S/31.67) que el del sector PRIVADO (S/2.10). Esto se debe a que la categoria PUBLICO incluye medicamentos de alto costo dispensados en hospitales, mientras que PRIVADO abarca toda la gama de productos de farmacias y boticas. Cabe precisar que los registros PUBLICOS representan solo 604 de los casi 200,000 registros totales.")
sep()

p("Top 5 departamentos con mayor cantidad de registros:")
for d, cnt, pm in r['top_deptos']:
    p(f"   - {d}: {cnt:,} registros, precio promedio S/{pm:.2f}")

p("Lima concentra la mayor proporcion de registros, lo cual es esperable por ser la capital y el departamento con mayor cantidad de establecimientos de salud. Sin embargo, los precios promedio entre departamentos no presentan diferencias drasticas, lo que sugiere un mercado farmaceutico relativamente integrado a nivel nacional.")
sep()

p("Top 5 fabricantes por cantidad de registros:")
for f2, cnt, pm in r['top_fabricantes']:
    p(f"   - {str(f2)[:55]}: {cnt:,} registros, promedio S/{pm:.2f}")

n("Se aprecian diferencias en las estrategias de mercado de los laboratorios. Por ejemplo, Laboratorios Portugal S.R.L. presenta un precio promedio bajo (S/0.89), lo que sugiere una especializacion en genericos economicos. En contraste, el Instituto Quimioterapico S.A. tiene un promedio de S/2.62, indicando un portafolio con productos de mayor valor. Esta variabilidad es informacion que el modelo puede aprovechar.")

sep()
# --- 4.6 ---
subtitulo("4.6 Division de datos en entrenamiento y prueba", 11)
sep()

p("Para evaluar correctamente el desempeno de los modelos, el dataset se dividio en dos conjuntos mutuamente excluyentes: uno de entrenamiento y otro de prueba. El conjunto de entrenamiento se utiliza para que el modelo aprenda las relaciones entre las variables, mientras que el conjunto de prueba se reserva para evaluar que tan bien generaliza ese aprendizaje a datos no vistos.")

p("Se empleo la funcion train_test_split de la biblioteca scikit-learn, con una proporcion 80/20 y el parametro random_state=42 para garantizar la reproducibilidad de los resultados. La division resultante fue:")
p(f"   - Entrenamiento: 158,680 registros (80%)")
p(f"   - Prueba: 39,671 registros (20%)")

sep()
# --- 4.7 ---
subtitulo("4.7 Aplicacion de los modelos de regresion", 11)
sep()

subtitulo("4.7.1 Regresion lineal multiple", 11)
p("Se utilizo la clase LinearRegression de scikit-learn. Este modelo busca ajustar una ecuacion lineal de la forma:")
p("   PRECIO = B0 + B1*TIPO + B2*PRODUCTO + B3*FABRICANTE + B4*FARMACIA + B5*DEPARTAMENTO")

p("Donde B0 es el intercepto y B1 a B5 son los coeficientes que el modelo estima automaticamente mediante el metodo de minimos cuadrados ordinarios, minimizando la suma de los errores al cuadrado entre los precios reales y los predichos. El modelo fue entrenado sobre los 158,680 registros del conjunto de entrenamiento.")
sep()

subtitulo("4.7.2 Regresion logistica", 11)
p("Se utilizo la clase LogisticRegression de scikit-learn con el parametro max_iter=2000 para asegurar la convergencia del algoritmo. A diferencia de la regresion lineal, este modelo no predice un valor numerico directamente, sino que estima la probabilidad de que una observacion pertenezca a la clase positiva (PRECIO_ALTO = 1).")

p("La probabilidad se calcula mediante la funcion sigmoide, que transforma la combinacion lineal de las variables predictoras en un valor entre 0 y 1. Si la probabilidad resultante supera el umbral de 0.5, la observacion se clasifica como 'precio alto'; en caso contrario, como 'precio bajo'.")

j("Pertinencia de ambos modelos", "Se emplearon ambos tipos de regresion porque responden a preguntas de distinta naturaleza. La regresion lineal aborda un problema de prediccion numerica: estimar el precio exacto en soles. La regresion logistica aborda un problema de clasificacion: determinar si un precio es alto o bajo respecto al mercado. La segunda pregunta es inherentemente mas facil de responder, por lo que se espera un mejor desempeno relativo en terminos de metricas de clasificacion.")

sep()
# --- 4.8 ---
subtitulo("4.8 Evaluacion mediante metricas", 11)
sep()

subtitulo("4.8.1 Metricas de regresion lineal", 11)
p(f"   - RMSE (Root Mean Squared Error): {r['rmse']:.4f}")
p(f"   - MAE (Mean Absolute Error): {r['mae']:.4f}")
p(f"   - R2 (Coeficiente de determinacion): {r['r2']:.4f} ({r['r2']*100:.1f}%)")

p(f"Interpretacion de las metricas:")

p(f"El RMSE mide el error de prediccion en las mismas unidades de la variable objetivo (soles). Un valor de {r['rmse']:.2f} puede parecer elevado, pero debe contextualizarse considerando que el rango de precios abarca desde centimos hasta miles de soles. Un error de esta magnitud es proporcionalmente menor en medicamentos caros y mayor en los mas economicos.")

p(f"El MAE es una metrica mas intuitiva y robusta que el RMSE, ya que no eleva los errores al cuadrado. Un MAE de {r['mae']:.2f} indica que, en promedio, el modelo se equivoca por aproximadamente S/{r['mae']:.2f} en cada prediccion. Para medicamentos cuyo precio ronda entre S/1 y S/3, este margen de error es significativo.")

p(f"El R2 de {r['r2']:.4f} indica que las variables predictoras, en su forma lineal actual, explican solo el {r['r2']*100:.1f}% de la variabilidad del precio. Este resultado, si bien es bajo, no debe interpretarse como un fracaso del modelo, sino como una manifestacion de la complejidad del problema: el precio de un medicamento depende de factores economicos, regulatorios y comerciales que no estan capturados en las variables disponibles (costo de insumos, patentes, tipo de cambio, margenes de distribucion, etc.).")

j("Interpretacion del R2", "Un R2 cercano a cero en un problema con datos reales no es inusual. Indica que el modelo lineal no es suficiente para capturar las relaciones subyacentes, y que se requieren enfoques mas sofisticados (modelos no lineales, mas variables predictoras, transformaciones de los datos). Esto constituye un aprendizaje valioso sobre las limitaciones de la regresion lineal en contextos reales.")
sep()

subtitulo("4.8.2 Metricas de regresion logistica", 11)
p(f"   - Accuracy: {r['acc']:.4f} ({r['acc']*100:.1f}%)")
p(f"   - Precision: {r['prec']:.4f}")
p(f"   - Recall: {r['rec']:.4f}")
p(f"   - F1-Score: {r['f1']:.4f}")
sep()

p("Interpretacion de las metricas de clasificacion:")

p(f"El accuracy de {r['acc']*100:.1f}% indica que el modelo acierta en poco mas de la mitad de los casos. Si bien supera el 50% del azar, el margen es estrecho. Esto sugiere que las variables TIPO, PRODUCTO, FABRICANTE, FARMACIA y DEPARTAMENTO contienen cierta informacion util para distinguir precios altos de bajos, pero la senal es debil.")

p(f"La precision de {r['prec']:.4f} indica que, cuando el modelo predice que un medicamento es caro, acierta aproximadamente el {r['prec']*100:.0f}% de las veces. El recall de {r['rec']:.4f}, mas bajo, indica que el modelo deja de detectar una proporcion importante de los precios realmente altos, clasificandolos erroneamente como bajos. Esto describe un modelo conservador que prefiere equivocarse por omision antes que por exceso.")
sep()

p("Matriz de confusion:")
p(f"   - Verdaderos Positivos (predijo alto, era alto):     {r['cm_vp']:>6,}")
p(f"   - Falsos Positivos (predijo alto, era bajo):         {r['cm_fp']:>6,}")
p(f"   - Falsos Negativos (predijo bajo, era alto):         {r['cm_fn']:>6,}")
p(f"   - Verdaderos Negativos (predijo bajo, era bajo):     {r['cm_vn']:>6,}")

p(f"La matriz de confusion confirma la tendencia conservadora del modelo: los verdaderos negativos ({r['cm_vn']:,}) superan ampliamente a los verdaderos positivos ({r['cm_vp']:,}), lo que indica que el modelo se inclina hacia la prediccion de 'precio bajo' en casos de incertidumbre. El F1-score de {r['f1']:.4f} refleja el equilibrio entre precision y recall.")

doc.add_page_break()

# =====================================================
# CONCLUSIONES
# =====================================================
subtitulo("V. CONCLUSIONES")
sep()

p("1. Los objetivos planteados fueron alcanzados. Se construyeron, entrenaron y evaluaron exitosamente un modelo de regresion lineal multiple y un modelo de regresion logistica sobre datos reales de precios de medicamentos del mercado peruano, obtenidos del Observatorio de Precios de DIGEMID. Se completaron todas las etapas solicitadas en la actividad.")

p("2. La principal dificultad del trabajo no residio en la aplicacion de los modelos, sino en la obtencion y preparacion de los datos. La Plataforma Nacional de Datos Abiertos no dispone del dataset de DIGEMID como un archivo descargable, por lo que fue necesario recurrir directamente al observatorio y recolectar los datos de forma manual. Esto constituye una experiencia real sobre los desafios que implica trabajar con datos abiertos del Estado peruano.")

p("3. El modelo de regresion lineal multiple presento limitaciones para predecir el precio exacto, obteniendo un R2 de 0.0016. Este resultado refleja que la relacion entre las variables categoricas disponibles y el precio no es adecuadamente capturada por un modelo lineal simple. No obstante, el ejercicio permitio comprender las limitaciones intrinsecas de este tipo de modelos frente a datos con alta dispersion y relaciones no lineales.")

p("4. El modelo de regresion logistica mostro un desempeno modesto pero superior al azar, con un accuracy de 54.7%. Esto demuestra que las variables TIPO, DEPARTAMENTO y FABRICANTE contienen informacion util para clasificar precios, aunque la senal es limitada. El modelo resulto ser conservador, con tendencia a clasificar como 'precio bajo' en casos dudosos.")

p("5. Aprendizajes obtenidos durante el desarrollo del trabajo:")
p("   - Comprension del flujo completo de un proyecto de machine learning supervisado: obtencion de datos, limpieza, transformacion, modelado y evaluacion.")
p("   - Aplicacion practica de tecnicas de preprocesamiento en un contexto real: normalizacion de texto, encoding de variables categoricas, deteccion de outliers mediante IQR.")
p("   - Implementacion de dos tipos de regresion (lineal y logistica) y comprension de la diferencia entre predecir un valor numerico continuo y clasificar una categoria binaria.")
p("   - Interpretacion de metricas de evaluacion (RMSE, MAE, R2, accuracy, precision, recall, F1-score y matriz de confusion) en el contexto especifico del problema.")
p("   - Experiencia directa con las limitaciones de las plataformas de datos abiertos del gobierno: accesibilidad, formatos, ausencia de APIs y necesidad de recoleccion manual.")

p("6. Recomendaciones para trabajos futuros:")
p("   - Incorporar variables adicionales como la concentracion exacta del principio activo (extraida del nombre del producto), la forma farmaceutica y la fecha de registro para capturar tendencias temporales.")
p("   - Aplicar One-Hot Encoding a las variables de baja cardinalidad (TIPO, DEPARTAMENTO) para eliminar el orden artificial introducido por Label Encoding.")
p("   - Explorar modelos no lineales como arboles de decision, Random Forest o Gradient Boosting, que suelen manejar mejor las relaciones complejas entre variables categoricas y el precio.")
p("   - Ampliar la muestra a un mayor numero de principios activos para aumentar la representatividad de los resultados.")

doc.add_page_break()

# =====================================================
# BIBLIOGRAFIA
# =====================================================
subtitulo("VI. BIBLIOGRAFIA (Formato IEEE)")
sep()

refs = [
    '[1] Plataforma Nacional de Datos Abiertos, "Datos Abiertos Peru", Gobierno del Peru. [En linea]. Disponible en: https://www.datosabiertos.gob.pe/',
    '[2] Direccion General de Medicamentos, Insumos y Drogas (DIGEMID), "Observatorio de Precios de Medicamentos", Ministerio de Salud del Peru. [En linea]. Disponible en: https://opm-digemid.minsa.gob.pe/',
    '[3] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python", Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.',
    '[4] J. Brownlee, "Linear Regression for Machine Learning", Machine Learning Mastery, 2020. [En linea]. Disponible en: https://machinelearningmastery.com/linear-regression-for-machine-learning/',
    '[5] J. Brownlee, "Logistic Regression for Machine Learning", Machine Learning Mastery, 2020. [En linea]. Disponible en: https://machinelearningmastery.com/logistic-regression-for-machine-learning/',
    '[6] W. McKinney, "Data Structures for Statistical Computing in Python", Proceedings of the 9th Python in Science Conference, pp. 51-56, 2010.',
    '[7] T. Hastie, R. Tibshirani y J. Friedman, The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2da ed. Nueva York: Springer, 2009.',
    '[8] D. C. Montgomery, E. A. Peck y G. G. Vining, Introduction to Linear Regression Analysis, 5ta ed. Nueva Jersey: Wiley, 2012.',
]

for ref in refs:
    p(ref)
    sep()

# ===== GUARDAR =====
doc.save("informe/informe_semana9_regresion_digemid.docx")
print("OK")
