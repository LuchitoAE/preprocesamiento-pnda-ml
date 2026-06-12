from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

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

def sep():
    doc.add_paragraph()

def code(text):
    par = doc.add_paragraph()
    par.paragraph_format.left_indent = Cm(1.25)
    run = par.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def result(text):
    par = doc.add_paragraph()
    par.paragraph_format.left_indent = Cm(1.25)
    run = par.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x00, 0x66, 0x00)
    run.italic = True

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
titulo("INFORME DE PRACTICA DE CLUSTERING", 14)
titulo('"WINE DATASET - K-MEANS Y AGNES"', 12)
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

p("En esta practica se aplicaron algoritmos de clustering al dataset Wine de scikit-learn. El dataset tiene 178 muestras de vinos con 13 caracteristicas quimicas y 3 tipos diferentes.")

p("Se usaron dos algoritmos: K-Means y AGNES. Primero se determino el numero optimo de clusters con el metodo del codo y el coeficiente de silueta, luego se aplicaron ambos algoritmos con ese K y se compararon los resultados usando PCA para visualizar.")

doc.add_page_break()

# =====================================================
# PROBLEMA PLANTEADO
# =====================================================
subtitulo("III. PROBLEMA PLANTEADO")
sep()

p("Usar el dataset Wine de sklearn para:")
p("   1. Encontrar el K optimo con metodo del codo y silueta.")
p("   2. Aplicar K-Means con el K encontrado.")
p("   3. Aplicar AGNES con enlace Ward.")
p("   4. Visualizar todo con PCA.")
p("   5. Generar el dendrograma.")
p("   6. Comparar resultados de ambos algoritmos.")

doc.add_page_break()

# =====================================================
# SOLUCION
# =====================================================
subtitulo("IV. SOLUCION")
sep()

subtitulo("4.1 Dataset y preparacion", 11)
sep()

p("Se cargo el dataset, se escalaron los datos y se aplico PCA para visualizar en 2D.")
sep()

code("from sklearn.datasets import load_wine")
code("from sklearn.preprocessing import StandardScaler")
code("from sklearn.decomposition import PCA")
code("")
code("wine = load_wine()")
code("X, y_real = wine.data, wine.target")
code("X_scaled = StandardScaler().fit_transform(X)")
code("X_pca = PCA(n_components=2).fit_transform(X_scaled)")
sep()

result("178 muestras, 13 caracteristicas, 3 clases")
result("Varianza PCA 2D: 55.4%")
sep()

subtitulo("4.2 Metodo del Codo", 11)
sep()

code("from sklearn.cluster import KMeans")
code("")
code("inercias = []")
code("for k in range(1, 11):")
code("    km = KMeans(n_clusters=k, random_state=42, n_init='auto')")
code("    km.fit(X_scaled)")
code("    inercias.append(km.inertia_)")
sep()

result("K= 1 -> 2314.00")
result("K= 2 -> 1661.68")
result("K= 3 -> 1277.93  <-- CODO")
result("K= 4 -> 1211.75")
result("K= 5 -> 1123.16")
result("K=10 ->  879.43")
sep()

p("El codo esta en K=3. Ahi la inercia baja fuerte y despues se estanca. K=3 coincide con las 3 clases reales del dataset.")
sep()

subtitulo("4.3 Coeficiente de Silueta", 11)
sep()

code("from sklearn.metrics import silhouette_score")
code("")
code("for k in range(2, 11):")
code("    labels = KMeans(n_clusters=k, random_state=42,")
code("                    n_init='auto').fit_predict(X_scaled)")
code("    score = silhouette_score(X_scaled, labels)")
sep()

result("K=2 -> 0.2650")
result("K=3 -> 0.2849  <-- MEJOR")
result("K=4 -> 0.2542")
result("K=5 -> 0.1836")
result("")
result("K optimo: 3")
sep()

p("El mejor puntaje de silueta es 0.2849 en K=3. Ambos metodos coinciden en K=3.")
sep()

subtitulo("4.4 K-Means", 11)
sep()

code("kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')")
code("labels_kmeans = kmeans.fit_predict(X_scaled)")
sep()

result("Clusters: [65, 51, 62]")
result("Inercia: 1277.93 | Iteraciones: 7")
result("")
result("Matriz confusion (Real vs K-Means):")
result("  [[ 0  0 59]")
result("   [65  3  3]")
result("   [ 0 48  0]]")
sep()

p("K-Means acierta 172 de 178 muestras. Pureza del 96.6%.")
sep()

subtitulo("4.5 AGNES", 11)
sep()

code("from sklearn.cluster import AgglomerativeClustering")
code("")
code("agg = AgglomerativeClustering(n_clusters=3, linkage='ward')")
code("labels_agg = agg.fit_predict(X_scaled)")
sep()

result("Clusters: [58, 56, 64]")
result("")
result("Matriz confusion (Real vs AGNES):")
result("  [[ 0  0 59]")
result("   [58  8  5]")
result("   [ 0 48  0]]")
sep()

p("AGNES acierta 165 de 178. Pureza del 92.7%. Un poco mas de error que K-Means.")
sep()

subtitulo("4.6 Dendrograma", 11)
sep()

code("from scipy.cluster.hierarchy import dendrogram, linkage")
code("")
code("linked = linkage(X_scaled, method='ward')")
code("dendrogram(linked, leaf_rotation=90)")
sep()

p("El dendrograma muestra como se van juntando las 178 muestras hasta formar los 3 grupos. La linea de corte en K=3 separa claramente tres ramas grandes.")
sep()

subtitulo("4.7 Comparacion final", 11)
sep()

result("Silhouette K-Means:  0.2849")
result("Silhouette AGNES:    0.2774")
result("Pureza K-Means:      96.6%")
result("Pureza AGNES:        92.7%")
sep()

p("K-Means gana por poco en ambas metricas. Pero AGNES da el dendrograma, que ayuda a entender la estructura de los datos.")

doc.add_page_break()

# =====================================================
# ANALISIS
# =====================================================
subtitulo("V. ANALISIS DE RESULTADOS")
sep()

p("El K optimo salio 3 con ambos metodos. Esto tiene sentido porque el dataset realmente tiene 3 tipos de vino. El codo se nota claramente en K=3 y la silueta llega a su pico ahi mismo.")

p("K-Means salio mejor (96.6% de pureza). Solo fallo en 6 muestras de las 178. AGNES tambien funciona bien (92.7%) pero cometio 13 errores. La diferencia esta en que K-Means puede reajustar los centroides varias veces, mientras que AGNES toma decisiones de fusion que despues no puede corregir.")

p("La reduccion con PCA capturo el 55.4% de la varianza. No es mucho, pero fue suficiente para que los clusters se vean separados en 2D. Los tres grupos se distinguen bien en las graficas.")

p("En conclusion, ambos algoritmos encontraron correctamente los 3 tipos de vino. K-Means fue un poco mas preciso, pero AGNES dio informacion extra con el dendrograma.") 

doc.add_page_break()

# =====================================================
# CONCLUSIONES
# =====================================================
subtitulo("VI. CONCLUSIONES")
sep()

p("Se aplicaron K-Means y AGNES al dataset Wine, encontrando K=3 como el numero optimo de clusters con los metodos del codo y silueta. Ambos algoritmos lograron separar correctamente los tres tipos de vino.")

p("K-Means obtuvo 96.6% de pureza contra 92.7% de AGNES. La diferencia es pequena y ambos resultados son buenos. La practica permitio entender la diferencia entre clustering particional y jerarquico, y como evaluar la calidad del agrupamiento con el coeficiente de silueta.")

doc.add_page_break()

# =====================================================
# BIBLIOGRAFIA
# =====================================================
subtitulo("VII. BIBLIOGRAFIA")
sep()

refs = [
    '[1] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python", JMLR, vol. 12, pp. 2825-2830, 2011.',
    '[2] P. Virtanen et al., "SciPy 1.0", Nature Methods, vol. 17, pp. 261-272, 2020.',
    '[3] P. J. Rousseeuw, "Silhouettes", Journal of Computational and Applied Mathematics, vol. 20, pp. 53-65, 1987.',
    '[4] T. Hastie, R. Tibshirani, J. Friedman, "The Elements of Statistical Learning", 2da ed. Springer, 2009.',
]

for ref in refs:
    p(ref)
    sep()

# ===== GUARDAR =====
doc.save("informe/informe_clustering_wine.docx")
print("OK")
