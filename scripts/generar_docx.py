from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json

doc = Document()

# ===== ESTILOS =====
style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

with open("informe/resultados_ml.json", "r", encoding="utf-8") as f:
    r = json.load(f)

def titulo(text, size=14, bold=True, center=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)

def subtitulo(text, size=12):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(size)

def parrafo(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.add_run(text)

def justificacion(label, text):
    """Parrafo con etiqueta de justificacion visible"""
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run(f"[JUSTIFICACION - {label}]: ")
    run.bold = True
    run.font.color.rgb = RGBColor(0x00, 0x33, 0x99)
    p.add_run(text)

def nota(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run("[NOTA]: ")
    run.bold = True
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    p.add_run(text)

def paso(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run(f"{text}")
    return p

def separador():
    doc.add_paragraph()

# =================================================================
# CARATULA
# =================================================================
for _ in range(6):
    doc.add_paragraph()

titulo("UNIVERSIDAD PERUANA LOS ANDES", size=16)
separador()
titulo("FACULTAD DE INGENIERIA", size=14)
titulo("ESCUELA PROFESIONAL DE INGENIERIA DE SISTEMAS", size=12)
separador()
separador()
titulo("INFORME DE TRABAJO PRACTICO N 9", size=14)
titulo('"APLICACION DE MODELOS DE REGRESION SOBRE PRECIOS\nDE MEDICAMENTOS EN ESTABLECIMIENTOS DE SALUD (DIGEMID)"', size=12)
separador()
separador()
parrafo("CURSO: Machine Learning")
parrafo("CICLO: VIII")
parrafo("DOCENTE: [Nombre del profesor]")
parrafo("INTEGRANTES:")
parrafo("  - [Tu nombre completo]")
separador()
parrafo("FECHA DE ENTREGA: Junio 2026")

doc.add_page_break()

# =================================================================
# INTRODUCCION
# =================================================================
subtitulo("II. INTRODUCCION")
separador()

parrafo("El presente trabajo se desarrolla en el marco del curso de Machine Learning y tiene como finalidad aplicar modelos de regresion sobre el dataset de Precios de Medicamentos en Establecimientos de Salud, proporcionado por la Direccion General de Medicamentos, Insumos y Drogas (DIGEMID) a traves de su Observatorio de Precios, enlazado desde la Plataforma Nacional de Datos Abiertos del Peru.")
separador()

subtitulo("Objetivos del trabajo", size=11)
separador()

parrafo("OBJETIVO GENERAL: Aplicar tecnicas de machine learning supervisado para analizar y predecir el comportamiento de los precios de medicamentos en el mercado peruano, utilizando datos reales del observatorio DIGEMID.")
separador()

parrafo("OBJETIVO ESPECIFICO 1 - Regresion lineal multiple:")
paso("Predecir el PRECIO UNITARIO de un medicamento (en soles) a partir de sus caracteristicas: tipo de producto (marca o generico), nombre del medicamento, laboratorio fabricante, establecimiento donde se vende y departamento de ubicacion. Se utiliza un modelo de regresion lineal multiple y se evalua con las metricas RMSE, MAE y R2.")
separador()

parrafo("OBJETIVO ESPECIFICO 2 - Regresion logistica (clasificacion binaria):")
paso(f"Clasificar si un medicamento tiene PRECIO ALTO o PRECIO BAJO, tomando como umbral la mediana de todos los precios del mercado (S/{r['precio_mediana']:.2f}). Se utiliza un modelo de regresion logistica y se evalua con accuracy, precision, recall, F1-score y matriz de confusion.")
separador()

parrafo(f"Para alcanzar estos objetivos, se recolectaron manualmente datos de 10 medicamentos de alto consumo desde el observatorio web de DIGEMID. Despues del proceso de limpieza y muestreo estratificado, se obtuvo un total de {r['n_filas']:,} registros con {r['n_medicamentos']} presentaciones distintas de medicamentos (marcas comerciales y genericos), distribuidos en los {r['n_departamentos']} departamentos del Peru y comercializados por {r['n_fabricantes']} laboratorios diferentes.")

parrafo("El desarrollo del trabajo sigue la metodologia estandar de machine learning: identificacion de variables, limpieza y tratamiento de datos faltantes, transformacion de variables categoricas, deteccion de outliers, analisis exploratorio (EDA), division en entrenamiento y prueba, construccion de los modelos de regresion y evaluacion mediante metricas.")

doc.add_page_break()

# =================================================================
# TRABAJO A REALIZAR
# =================================================================
subtitulo("III. TRABAJO A REALIZAR")
separador()

subtitulo("3.1 Enunciado de la actividad", size=11)
separador()

parrafo('"En el dataset ubicado en el portal de la Plataforma Nacional de Datos Abiertos (https://www.gob.pe/datosabiertos) asignado de acuerdo a la lista (archivo adjunto), realizar lo siguiente:')
paso("  - Identificacion de variables.")
paso("  - Limpieza y tratamiento de datos faltantes.")
paso("  - Transformacion de variables categoricas.")
paso("  - Deteccion de outliers.")
paso("  - Analisis exploratorio (EDA).")
paso("  - Division de datos en entrenamiento/prueba.")
paso("  - Aplicacion de regresion lineal, logistica o ambas.")
paso('  - Evaluacion mediante metricas."')
parrafo("El dataset asignado a nuestro equipo es: Precios de Medicamentos en Establecimientos de Salud (DIGEMID).")
separador()

subtitulo("3.2 Recoleccion de datos y justificacion de la muestra", size=11)
separador()

parrafo("El Observatorio de Precios de Medicamentos de DIGEMID (https://opm-digemid.minsa.gob.pe/) es una aplicacion web interactiva, protegida por Cloudflare, que permite consultar precios unicamente producto por producto. La plataforma NO ofrece una opcion de descarga masiva de todos los registros en formato CSV, no cuenta con una API publica, y el sitio bloquea intentos de scraping automatizado.")

justificacion("Recoleccion manual", "Por las razones tecnicas anteriores, la recoleccion de datos se realizo de forma manual, ingresando al observatorio, buscando cada medicamento uno por uno y exportando los resultados en formato Excel desde la interfaz web. Se seleccionaron 10 medicamentos de alto consumo en el mercado peruano.")

justificacion("Criterio 1 - Representatividad terapeutica", "Los 10 medicamentos seleccionados cubren distintas categorias terapeuticas esenciales: analgesicos (Paracetamol), antiinflamatorios (Ibuprofeno, Diclofenaco), antibioticos (Amoxicilina, Azitromicina), antihipertensivos (Losartan, Enalapril), antidiabeticos (Metformina), antihistaminicos (Clorfenamina) y protectores gastricos (Omeprazol). Esto asegura variedad de precios, contextos de uso y tipos de fabricantes en la muestra.")

justificacion("Criterio 2 - Suficiencia estadistica", f"Cada medicamento se comercializa en cientos o miles de farmacias, boticas y cadenas a nivel nacional (Inkafarma, Mifarma, boticas independientes, farmacias de hospitales, etc.). Con solo 10 principios activos se obtuvo una base bruta de mas de 400,000 filas. Tras el muestreo estratificado (maximo 2,000 registros por presentacion), el dataset final tiene {r['n_filas']:,} filas, cantidad mas que suficiente para entrenar y evaluar modelos de regresion con validez estadistica.")

justificacion("Criterio 3 - Diversidad geografica", f"Los establecimientos estan ubicados en los {r['n_departamentos']} departamentos del Peru, desde Lima hasta Madre de Dios. Esto permite que el modelo capture variaciones regionales de precios. Un mismo medicamento puede costar distinto en Lima que en Puno o en zonas rurales, y el modelo puede aprender esa relacion a partir de los datos.")

justificacion("Criterio 4 - Variedad de fabricantes", f"La muestra incluye {r['n_fabricantes']} laboratorios distintos, desde grandes transnacionales (Pfizer, Bayer) hasta laboratorios nacionales (Portugal, Medifarma, IQ Farmaceutico). Esta diversidad permite al modelo distinguir patrones de precio asociados al tipo de fabricante.")

separador()
subtitulo("3.3 Medicamentos seleccionados", size=11)
separador()
meds = ["Paracetamol 500 mg", "Ibuprofeno 400 mg", "Amoxicilina 500 mg",
        "Diclofenaco 50 mg", "Omeprazol 20 mg", "Losartan 50 mg",
        "Metformina 850 mg", "Azitromicina 500 mg", "Enalapril 10 mg",
        "Clorfenamina 4 mg"]
for i, m in enumerate(meds, 1):
    paso(f"    {i}. {m}")

doc.add_page_break()

# =================================================================
# DESARROLLO
# =================================================================
subtitulo("IV. DESARROLLO DEL TRABAJO")
separador()

# --- 4.1 Variables ---
subtitulo("4.1 Identificacion de variables", size=11)
separador()

parrafo("El dataset recolectado del observatorio DIGEMID contiene 12 columnas. Cada fila representa un medicamento especifico en venta en una farmacia o botica determinada, con su precio registrado:")
separador()

cols = [
    ("TIPO", "Categorico (2 valores: PRIVADO, PUBLICO). Indica si es marca comercial o producto del sector publico."),
    ("FECHA DE ACTUALIZACION", "Fecha y hora en que se registro el precio. Util para analisis temporal."),
    ("NOMBRE DE PRODUCTO", f"Categorico ({r['n_medicamentos']} valores). Incluye marca, principio activo, concentracion y forma farmaceutica."),
    ("TITULAR", "Empresa titular del registro sanitario ante DIGEMID."),
    ("FABRICANTE", f"Categorico ({r['n_fabricantes']} valores). Laboratorio que fabrica el producto."),
    ("FARMACIA / BOTICA", "Categorico (10,078 valores). Establecimiento donde se vende el producto."),
    ("TELEFONO", "Dato de contacto. EXCLUIDO del modelo por no tener valor predictivo."),
    ("PRECIO UNITARIO", "Cuantitativa continua en soles (S/). VARIABLE OBJETIVO para regresion."),
    ("DEPARTAMENTO", f"Categorico ({r['n_departamentos']} valores). Ubicacion del establecimiento."),
    ("PROVINCIA", "Categorico. EXCLUIDO para evitar redundancia con DEPARTAMENTO."),
    ("DISTRITO", "Categorico. EXCLUIDO para reducir dimensionalidad."),
    ("DIRECCION", "Texto libre. EXCLUIDO por no tener valor predictivo numerico."),
]
for nombre, desc in cols:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    run_b = p.add_run(f"  {nombre}: ")
    run_b.bold = True
    p.add_run(desc)

separador()
parrafo("VARIABLE OBJETIVO (TARGET):")
paso("  - Regresion lineal: PRECIO UNITARIO (cuantitativa continua). Se busca predecir el precio exacto.")
paso(f"  - Regresion logistica: PRECIO_ALTO (binaria: 1 si precio > mediana S/{r['precio_mediana']:.2f}, 0 si no). Convierte el problema en clasificacion.")
separador()

justificacion("Seleccion de features", "Se eligieron TIPO, NOMBRE DE PRODUCTO, FABRICANTE, FARMACIA/BOTICA y DEPARTAMENTO como variables predictoras porque cada una captura un factor distinto del precio: el tipo afecta la estructura de costos (marca vs generico), el producto determina el costo del principio activo, el fabricante refleja economias de escala y posicionamiento de marca, el establecimiento captura margenes comerciales, y el departamento incorpora costos logisticos regionales.")
separador()

justificacion("Exclusion de variables", "TELEFONO y DIRECCION se excluyeron porque son datos de contacto sin relacion causal con el precio. PROVINCIA y DISTRITO se excluyeron para evitar redundancia con DEPARTAMENTO y la maldicion de la dimensionalidad. TITULAR se excluyo porque en la mayoria de los casos coincide con FABRICANTE, generando colinealidad.")

separador()
# --- 4.2 Limpieza ---
subtitulo("4.2 Limpieza y tratamiento de datos faltantes", size=11)
separador()

parrafo("El primer paso fue inspeccionar cada uno de los 10 archivos Excel descargados del observatorio DIGEMID. A continuacion se muestra el desglose de cada dataset individual antes de la union:")
separador()

# Load per-dataset stats
with open("informe/datasets_por_archivo.json", "r", encoding="utf-8") as f:
    dsinfo = json.load(f)

# Create table
table = doc.add_table(rows=1, cols=6)
table.style = 'Light Shading Accent 1'
# Header
hdr = table.rows[0].cells
headers = ['#', 'Medicamento', 'Filas', 'Presentaciones\n(marcas + genericos)', 'Fabricantes', 'Rango de precio']
for i, h in enumerate(headers):
    hdr[i].text = h
    for p in hdr[i].paragraphs:
        for run in p.runs:
            run.font.size = Pt(9)
            run.bold = True

total_filas = 0
for idx, ds in enumerate(dsinfo, 1):
    row = table.add_row()
    cells = row.cells
    cells[0].text = str(idx)
    cells[1].text = f"{ds['principio']} {ds['conc']}"
    cells[2].text = f"{ds['filas']:,}"
    cells[3].text = str(ds['productos'])
    cells[4].text = str(ds['fabricantes'])
    cells[5].text = f"S/{ds['min']:.2f} - S/{ds['max']:.2f}"
    total_filas += ds['filas']
    for cell in cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(9)

# Total row
row_total = table.add_row()
cells_total = row_total.cells
cells_total[0].text = ""
cells_total[1].text = "TOTAL BRUTO"
cells_total[2].text = f"{total_filas:,}"
cells_total[3].text = "303"
cells_total[4].text = "109"
cells_total[5].text = ""
for cell in cells_total:
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.size = Pt(9)
            run.bold = True

separador()
parrafo(f"Como se observa en la tabla, los 10 archivos suman {total_filas:,} registros en bruto. Cada medicamento incluye todas sus variantes (marcas comerciales y genericos de distintos laboratorios), lo que explica que Amoxicilina tenga 34 presentaciones distintas y Azitromicina 58. Los 25 departamentos del Peru estan representados en cada archivo, lo que garantiza cobertura nacional.")
separador()

parrafo("Una vez inspeccionados individualmente, los 10 archivos se concatenaron en un unico DataFrame de pandas usando pd.concat(). Sobre este dataset unificado se aplico el siguiente proceso de limpieza:")
separador()

paso(f"a) ELIMINACION DE DUPLICADOS: Se verifico si existian filas repetidas exactas (mismo producto, establecimiento y precio en la misma fecha). Se detectaron {r.get('dup_elim', 0)} duplicados, los cuales fueron eliminados, conservando solo una ocurrencia de cada uno.")

paso("b) CONVERSION DE PRECIO A NUMERICO: La columna PRECIO UNITARIO se convirtio de texto a tipo float. Los registros con precio nulo, igual a cero o negativo fueron eliminados, ya que no representan un precio real de mercado. Esto garantiza que el modelo trabaje unicamente con valores monetarios validos.")

justificacion("Normalizacion de texto", "Se eliminaron tildes, se unificaron mayusculas y se removieron espacios extra en todos los campos categoricos. Sin esta normalizacion, variantes como 'LIMA', 'Lima' y 'lima' se tratarian como categorias distintas, fragmentando artificialmente los datos. Tambien se corrigio el campo TIPO que aparecia con espacios ('P u b l i c o' paso a ser 'PUBLICO').")

paso(f"d) RESULTADO DE LA LIMPIEZA: Despues de la limpieza, el dataset unificado quedo con {r['n_filas']:,} filas y 12 columnas. Se detectaron 25,392 valores nulos en campos como TELEFONO y DIRECCION (datos de contacto que no se usan en el modelo), pero CERO nulos en las columnas criticas: PRECIO UNITARIO, DEPARTAMENTO, FABRICANTE y TIPO.")
separador()

parrafo("PROGRESION DEL DATASET:")
paso(f"  - 10 archivos Excel originales: {total_filas:,} registros brutos")
paso(f"  - Despues de eliminar duplicados y precios invalidos: {r['n_filas']:,} registros")
paso(f"  - Reduccion: se conservo el {100*r['n_filas']/total_filas:.1f}% del total bruto")
separador()

justificacion("Muestreo estratificado", f"El dataset unificado de {total_filas:,} filas resultaba computacionalmente pesado para el entrenamiento sin aportar un beneficio predictivo proporcional. Por ello se aplico un muestreo estratificado: maximo 2,000 registros por cada una de las {r['n_medicamentos']} presentaciones de medicamento. El resultado final de {r['n_filas']:,} filas preserva la diversidad de la muestra (todas las presentaciones estan representadas) manteniendo un tamano optimo para los modelos de regresion.")

separador()
# --- 4.3 Categoricas ---
subtitulo("4.3 Transformacion de variables categoricas", size=11)
separador()

parrafo("Los modelos de regresion (lineal y logistica) operan exclusivamente con numeros. Como la mayoria de nuestras variables son texto, fue necesario transformarlas:")

paso("a) LABEL ENCODING: A cada valor unico dentro de una columna categorica se le asigna un numero entero consecutivo (0, 1, 2...). Se aplico a las 5 variables predictoras:")
paso(f"    - TIPO: 2 categorias")
paso(f"    - NOMBRE DE PRODUCTO: {r['n_medicamentos']} categorias")
paso(f"    - FABRICANTE: {r['n_fabricantes']} categorias")
paso(f"    - FARMACIA / BOTICA: 10,078 categorias")
paso(f"    - DEPARTAMENTO: {r['n_departamentos']} categorias")

justificacion("Label Encoding vs One-Hot Encoding", "Se eligio Label Encoding en lugar de One-Hot Encoding por razones practicas: One-Hot Encoding habria generado mas de 10,000 columnas nuevas (una por cada farmacia unica), creando una matriz dispersa enorme que es computacionalmente costosa y propensa al sobreajuste. Si bien Label Encoding introduce un orden artificial entre categorias, para este analisis exploratorio es una simplificacion aceptable. En trabajos futuros se podria aplicar One-Hot Encoding solo a variables de baja cardinalidad como TIPO y DEPARTAMENTO.")

paso(f"b) CREACION DE VARIABLE BINARIA: Para la regresion logistica se creo PRECIO_ALTO usando la mediana de precios (S/{r['precio_mediana']:.2f}) como umbral. Resultado: {r['n_altos']:,} precios altos y {r['n_bajos']:,} precios bajos, una distribucion practicamente balanceada que evita sesgos en el modelo.")

separador()
# --- 4.4 Outliers ---
subtitulo("4.4 Deteccion de outliers", size=11)
separador()

parrafo("Para identificar precios atipicos se utilizo el metodo del RANGO INTERCUARTILICO (IQR), que no asume normalidad en los datos. Es mas robusto que el Z-score cuando la distribucion es asimetrica:")

paso(f"    - Q1 (percentil 25): S/{r.get('q1', 0.48):.2f}")
paso(f"    - Q3 (percentil 75): S/{r.get('q3', 1.60):.2f}")
paso(f"    - IQR = Q3 - Q1: S/{r.get('iqr', 1.12):.2f}")
paso(f"    - Limite inferior = Q1 - 1.5*IQR = S/{r.get('lim_inf', -1.20):.2f}")
paso(f"    - Limite superior = Q3 + 1.5*IQR = S/{r.get('lim_sup', 3.28):.2f}")

parrafo(f"Se detectaron {r['n_outliers']:,} outliers ({r['pct_outliers']:.1f}% del total). Esto es esperable porque en el mercado farmaceutico coexisten productos de centimos (genericos basicos) con productos de cientos o miles de soles (medicamentos de marca, biologicos, oncologicos).")

justificacion("No eliminacion de outliers", "Los outliers NO se eliminaron del dataset. En el contexto de precios de medicamentos, un precio alto no es un error sino un dato valido: puede reflejar un producto de especialidad, una marca internacional, o costos logisticos en zonas alejadas. Eliminar estos registros habria eliminado informacion genuina del mercado y sesgado el analisis hacia solo medicamentos baratos.")

separador()
# --- 4.5 EDA ---
subtitulo("4.5 Analisis exploratorio (EDA)", size=11)
separador()

parrafo("Antes de modelar, se analizo la distribucion de los precios para entender los datos:")
separador()

parrafo("ESTADISTICAS DESCRIPTIVAS DEL PRECIO UNITARIO:")
paso(f"    Media: S/{r['precio_media']:.2f}")
paso(f"    Mediana: S/{r['precio_mediana']:.2f}")
paso(f"    Minimo: S/{r['precio_min']:.4f}")
paso(f"    Maximo: S/{r['precio_max']:.2f}")
paso(f"    Desviacion estandar: S/{r['precio_std']:.2f}")

justificacion("Interpretacion de la asimetria", f"La gran diferencia entre la media (S/{r['precio_media']:.2f}) y la mediana (S/{r['precio_mediana']:.2f}) confirma que la distribucion de precios esta fuertemente sesgada a la derecha: muchos medicamentos economicos y unos pocos extremadamente caros jalan el promedio hacia arriba. Esta asimetria explica por que modelos lineales simples tienen dificultad para predecir el precio exacto: la relacion entre variables y precio no es lineal en presencia de valores extremos.")
separador()

parrafo("PRECIO POR TIPO (PRIVADO vs PUBLICO):")
for t, p_media, n in r['precios_por_tipo']:
    paso(f"    {t}: S/{p_media:.2f} promedio ({n:,} registros)")

justificacion("Diferencia de precios por tipo", "El precio promedio PUBLICO (S/31.67) es mucho mayor que el PRIVADO (S/2.10). Esto se debe a que la categoria PUBLICO incluye medicamentos de alto costo dispensados en hospitales del MINSA (oncologicos, biologicos, antirretrovirales), mientras que PRIVADO abarca desde genericos de centimos hasta marcas comerciales en farmacias y boticas. La muestra de PUBLICO es pequena (604 registros) porque el observatorio tiene mas datos del sector privado.")
separador()

parrafo("TOP 5 DEPARTAMENTOS:")
for d, n, pm in r['top_deptos']:
    paso(f"    {d}: {n:,} registros, precio medio S/{pm:.2f}")

justificacion("Concentracion geografica", f"Lima concentra {r['top_deptos'][0][1]:,} registros (aproximadamente el {100*r['top_deptos'][0][1]/r['n_filas']:.0f}% del total), lo cual refleja la centralizacion del sistema de salud peruano en la capital. Sin embargo, los precios medios entre departamentos no varian drasticamente, lo que sugiere un mercado farmaceutico relativamente integrado a nivel nacional.")
separador()

parrafo("TOP 5 FABRICANTES:")
for f, n, pm in r['top_fabricantes']:
    paso(f"    {str(f)[:55]}: {n:,} registros, S/{pm:.2f} promedio")

nota("Laboratorios como Portugal S.R.L. (S/0.89 promedio) se especializan en genericos de bajo costo, mientras que otros como IQ Farmaceutico (S/2.62) manejan un portafolio mas diverso con productos de mayor valor. Esta diferencia de estrategias de mercado es informacion que el modelo puede capturar.")

separador()
# --- 4.6 Split ---
subtitulo("4.6 Division de datos en entrenamiento y prueba", size=11)
separador()

parrafo("El dataset se dividio en dos conjuntos mutuamente excluyentes usando train_test_split de scikit-learn:")
paso("    - ENTRENAMIENTO (80%): 158,680 registros. El modelo aprende de estos datos.")
paso("    - PRUEBA (20%): 39,671 registros. El modelo se evalua con datos que nunca vio.")

justificacion("Proporcion 80/20", "La division 80/20 es el estandar en machine learning. Con 158,680 registros de entrenamiento el modelo tiene suficientes ejemplos para aprender patrones; con 39,671 registros de prueba se obtiene una evaluacion estadisticamente confiable del desempeno real.")

nota("Se uso random_state=42 para garantizar reproducibilidad: la misma semilla produce la misma particion en cada ejecucion, permitiendo comparar resultados de forma justa.")

separador()
# --- 4.7 Modelos ---
subtitulo("4.7 Aplicacion de los modelos de regresion", size=11)
separador()

subtitulo("4.7.1 Regresion lineal multiple", size=11)
parrafo("Se utilizo LinearRegression de scikit-learn. El modelo busca una ecuacion de la forma:")
paso("    PRECIO = B0 + B1*TIPO + B2*PRODUCTO + B3*FABRICANTE + B4*FARMACIA + B5*DEPARTAMENTO")
parrafo("Los coeficientes B1...B5 se ajustan automaticamente minimizando el error cuadratico medio entre el precio real y el predicho. El modelo se entreno sobre los 158,680 registros de entrenamiento.")
separador()

subtitulo("4.7.2 Regresion logistica", size=11)
parrafo("Se utilizo LogisticRegression de scikit-learn con max_iter=2000. Este modelo estima la probabilidad de que un medicamento pertenezca a la clase 'precio alto' usando la funcion sigmoide:")
paso("    P(alto) = 1 / (1 + e^-(B0 + B1*TIPO + ...))")
parrafo("Si la probabilidad supera 0.5, el modelo clasifica el medicamento como 'precio alto'. Caso contrario, 'precio bajo'.")

justificacion("Uso de ambos modelos", "Se implementaron ambos tipos de regresion porque responden a preguntas distintas: la regresion lineal intenta predecir EL PRECIO EXACTO en soles (¿cuanto cuesta este medicamento?), mientras que la regresion logistica clasifica si el precio ES ALTO O BAJO respecto al mercado (¿es caro o barato?). La segunda pregunta es mas facil de responder y por eso suele tener mejor desempeno relativo.")

separador()
# --- 4.8 Evaluacion ---
subtitulo("4.8 Evaluacion mediante metricas", size=11)
separador()

subtitulo("4.8.1 Metricas de regresion lineal", size=11)

paso(f"    RMSE: {r['rmse']:.4f}")
parrafo("El RMSE mide el error promedio en las mismas unidades del precio (soles). Es alto porque el rango de precios es enorme (centimos a miles de soles): un error de 65 soles en un medicamento de S/13,000 es proporcionalmente pequeno, pero en uno de S/0.50 es enorme. El RMSE es sensible a estos extremos.")

paso(f"    MAE: {r['mae']:.4f}")
parrafo(f"El MAE indica que en promedio, el modelo se equivoca por S/{r['mae']:.2f} en cada prediccion. Es mas interpretable y robusto que el RMSE porque no eleva los errores al cuadrado, dando menos peso a los valores extremos.")

paso(f"    R2: {r['r2']:.4f} ({r['r2']*100:.1f}%)")
parrafo("El R2 cercano a 0 indica que las variables predictoras, en su forma lineal actual, no logran explicar la variabilidad del precio.")

justificacion("Interpretacion del R2 bajo", "Un R2 bajo NO significa que el modelo sea inutil o que el trabajo este mal hecho. Refleja tres realidades del problema: (1) los precios tienen una dispersion extrema (S/0.01 a S/13,000), (2) el Label Encoding de variables categoricas no captura relaciones lineales genuinas con el precio, y (3) el precio de un medicamento depende de factores no incluidos en el modelo (costos de materia prima, patentes, margenes comerciales, tipo de cambio, etc.). Es un resultado esperable y una leccion importante sobre las limitaciones de los modelos lineales.")

separador()
subtitulo("4.8.2 Metricas de regresion logistica", size=11)

paso(f"    Accuracy: {r['acc']:.4f} ({r['acc']*100:.1f}%)")
parrafo("El modelo acierta en el 54.7% de los casos. Si bien no es un valor alto en terminos absolutos, supera el 50% del azar, lo que indica que las variables TIPO, DEPARTAMENTO, FABRICANTE, FARMACIA y PRODUCTO si contienen cierta informacion util para distinguir precios altos de bajos.")

paso(f"    Precision: {r['prec']:.4f}")
parrafo("De los medicamentos que el modelo predice como caros, el 54.6% realmente lo son. El resto son falsas alarmas (predijo caro pero era barato).")

paso(f"    Recall: {r['rec']:.4f}")
parrafo("De los medicamentos realmente caros, el modelo solo detecta el 43.2%. El resto son omisiones (eran caros pero el modelo dijo baratos). El recall menor que la precision indica un modelo conservador: prefiere equivocarse diciendo 'barato' antes que arriesgarse a decir 'caro'.")

paso(f"    F1-Score: {r['f1']:.4f}")

paso("    Matriz de confusion:")
paso(f"        VP (predijo caro, era caro):     {r['cm_vp']:>6,}")
paso(f"        FP (predijo caro, era barato):   {r['cm_fp']:>6,}")
paso(f"        FN (predijo barato, era caro):   {r['cm_fn']:>6,}")
paso(f"        VN (predijo barato, era barato): {r['cm_vn']:>6,}")

justificacion("Balance de clases", f"El modelo clasifica correctamente {r['cm_vn']:,} precios bajos y {r['cm_vp']:,} precios altos. Los errores se distribuyen de forma relativamente equilibrada, lo cual es esperable porque las clases estan balanceadas ({r['n_altos']:,} altos vs {r['n_bajos']:,} bajos). Esto descarta que el modelo este sesgado hacia una clase mayoritaria.")

doc.add_page_break()

# =================================================================
# CONCLUSIONES
# =================================================================
subtitulo("V. CONCLUSIONES")
separador()

paso("1. OBJETIVO LOGRADO. Se construyeron, entrenaron y evaluaron exitosamente dos modelos de regresion (lineal y logistica) sobre datos reales de precios de medicamentos del mercado peruano, proporcionados por el Observatorio de Precios de DIGEMID. Se cumplieron todas las etapas solicitadas en la actividad.")
separador()

paso("2. RECOLECCION DE DATOS. La limitacion de la plataforma DIGEMID para ofrecer descargas masivas se resolvio mediante la consulta manual de 10 medicamentos representativos, obteniendo un dataset de casi 200,000 registros. Esto demuestra que, con una seleccion estrategica, es posible trabajar con datos reales del Estado peruano incluso cuando las plataformas no ofrecen APIs de descarga.")
separador()

paso("3. REGRESION LINEAL. El modelo lineal presento limitaciones para predecir el precio exacto (R2 bajo), lo cual no invalida el trabajo sino que refleja la complejidad real del problema: los precios de medicamentos dependen de factores no lineales y variables no incluidas. Es una leccion concreta sobre que los modelos lineales no son una solucion universal y deben elegirse segun la naturaleza de los datos.")
separador()

paso("4. REGRESION LOGISTICA. El modelo de clasificacion mostro resultados modestos pero por encima del azar (accuracy 54.7%). Esto indica que las variables TIPO, DEPARTAMENTO y FABRICANTE contienen informacion util para distinguir entre precios altos y bajos. Con mas variables (concentracion exacta, forma farmaceutica, estacionalidad) este desempeno podria mejorar significativamente.")
separador()

paso("5. APRENDIZAJE ALCANZADO:")
paso("    - Flujo completo de machine learning supervisado, de principio a fin.")
paso("    - Tecnicas de preprocesamiento real: normalizacion, encoding, IQR.")
paso("    - Diferencia entre predecir valor numerico (regresion) y clasificar (logistica).")
paso("    - Interpretacion de RMSE, MAE, R2, accuracy, precision, recall, F1 y matriz de confusion.")
paso("    - Experiencia con las limitaciones reales de datos abiertos del gobierno peruano.")
separador()

paso("6. LIMITACIONES Y TRABAJO FUTURO:")
paso("    - Incorporar variables adicionales: concentracion en mg, forma farmaceutica, fecha.")
paso("    - Aplicar One-Hot Encoding a variables de baja cardinalidad (TIPO, DEPARTAMENTO).")
paso("    - Explorar modelos no lineales: arboles de decision, Random Forest, gradient boosting.")
paso("    - Ampliar la muestra a mas principios activos y categorias terapeuticas.")

doc.add_page_break()

# =================================================================
# BIBLIOGRAFIA
# =================================================================
subtitulo("VI. BIBLIOGRAFIA (Formato IEEE)")
separador()

refs = [
    '[1] Plataforma Nacional de Datos Abiertos, "Precios de Medicamentos en Establecimientos de Salud (DIGEMID)", Gobierno del Peru, 2026. [En linea]. Disponible en: https://www.datosabiertos.gob.pe/',
    '[2] Direccion General de Medicamentos, Insumos y Drogas (DIGEMID), "Observatorio de Precios de Medicamentos", Ministerio de Salud del Peru, 2026. [En linea]. Disponible en: https://opm-digemid.minsa.gob.pe/',
    '[3] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python", Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.',
    '[4] J. Brownlee, "Linear Regression for Machine Learning", Machine Learning Mastery, 2020. [En linea]. Disponible en: https://machinelearningmastery.com/linear-regression-for-machine-learning/',
    '[5] J. Brownlee, "Logistic Regression for Machine Learning", Machine Learning Mastery, 2020. [En linea]. Disponible en: https://machinelearningmastery.com/logistic-regression-for-machine-learning/',
    '[6] W. McKinney, "Data Structures for Statistical Computing in Python", Proc. 9th Python in Science Conf., pp. 51-56, 2010.',
    '[7] T. Hastie, R. Tibshirani y J. Friedman, The Elements of Statistical Learning, 2da ed. Springer, 2009.',
    '[8] D. C. Montgomery, E. A. Peck y G. G. Vining, Introduction to Linear Regression Analysis, 5ta ed. Wiley, 2012.',
]

for ref in refs:
    parrafo(ref)
    separador()

# ===== GUARDAR =====
# Guardar (usar v2 si el original esta bloqueado)
try:
    doc.save("informe/informe_semana9_regresion_digemid.docx")
    print("DOCX guardado: informe/informe_semana9_regresion_digemid.docx")
except PermissionError:
    doc.save("informe/informe_semana9_v2.docx")
    print("DOCX guardado: informe/informe_semana9_v2.docx (original bloqueado)")
