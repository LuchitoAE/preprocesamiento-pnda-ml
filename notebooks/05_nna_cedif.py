# Dataset 5 - NNA atendidos en CEDIF (INABIF)
# Fuente: https://www.datosabiertos.gob.pe/dataset/servicio-de-cuidado-diurno-nna-en-situacion-de-riesgo-de-desproteccion-familiar
# Se descargan 5 archivos mensuales (oct 2025 a feb 2026) y se concatenan.

import pandas as pd
import unicodedata
import urllib.request

# Headers de navegador real (los servidores de la PNDA bloquean User-Agents simples)
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}

meses = [
    ("Octubre", 2025),
    ("Noviembre", 2025),
    ("Diciembre", 2025),
    ("Enero", 2026),
    ("Febrero", 2026),
]

rutas = []
for mes, anio in meses:
    url = f"https://www.datosabiertos.gob.pe/sites/default/files/NNA%20atendidos%20en%20CEDIF%20{mes}%20{anio}.csv"
    destino = f"NNA_{mes}_{anio}.csv"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as r, open(destino, "wb") as f:
        f.write(r.read())
    rutas.append(destino)
    print("  descargado:", destino)

# Concatenar bruto (sin filtrar) para ver el problema
df_raw = pd.concat([pd.read_csv(r, sep=";", encoding="latin-1", low_memory=False) for r in rutas],
                   ignore_index=True)
print("\nAntes del preprocesamiento:")
print("  filas:", len(df_raw), "  columnas:", df_raw.shape[1])
print("  duplicados:", df_raw.duplicated().sum())
print("  PAI_USU valores:", df_raw["PAI_USU"].value_counts(dropna=False).head().to_dict())

# Problemas detectados:
# - El archivo de enero 2026 tiene esquema distinto (datos familiares en vez de datos del usuario).
#   Si se concatena tal cual, pandas mete NaN en casi todo.
# - Encoding Latin-1: "PERU" aparece roto si se abre como utf-8.
# - PAI_USU mezcla "PERU" y "Peru" (mayusculas y tildes inconsistentes).
# - 2,606 filas duplicadas exactas.
# - SEX_USU codificado con 1/2 sin etiqueta.

# 1) Solo conservamos archivos con esquema estandar (16 columnas centradas en el usuario)
esquema = ["COD_USU", "SEX_USU", "FEC_NAC_USU", "EDAD_USU", "GRU_ET",
           "PAI_USU", "TIE_DIS", "LEN_MAT", "AUT_IDE_ET", "NOM_CEN",
           "FEC_ING", "PER_ING", "TIP_SEG_SAL", "EST_ACT", "FEC_EGR", "MOT_EGR"]

trozos = []
for r in rutas:
    d = pd.read_csv(r, sep=";", encoding="latin-1", low_memory=False)
    if all(c in d.columns for c in esquema):
        d["__archivo__"] = r
        trozos.append(d[esquema + ["__archivo__"]])
df = pd.concat(trozos, ignore_index=True)

# 2) Quitar duplicados exactos
df = df.drop_duplicates()

# 3) Normalizar PAI_USU (PERU sin tilde)
def quitar_tildes(s):
    if pd.isna(s):
        return s
    s = str(s).upper().strip()
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

df["PAI_USU"] = df["PAI_USU"].apply(quitar_tildes)

# 4) Fechas a datetime
for c in ["FEC_NAC_USU", "FEC_ING", "FEC_EGR"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")

# 5) Codificar sexo (1=Masculino, 2=Femenino)
df["SEXO"] = df["SEX_USU"].map({1: "MASCULINO", 2: "FEMENINO"})

# 6) Filtrar edades validas para NNA (0 a 17)
df["EDAD_USU"] = pd.to_numeric(df["EDAD_USU"], errors="coerce")
df = df[df["EDAD_USU"].between(0, 17)].copy()
df["EDAD_USU"] = df["EDAD_USU"].astype("int8")

# 7) Tipos categoricos
for c in ["NOM_CEN", "PAI_USU", "SEXO"]:
    df[c] = df[c].astype("category")

print("\nDespues del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  duplicados:", df.duplicated().sum())
print("  PAI_USU valores:", df["PAI_USU"].value_counts(dropna=False).head().to_dict())
print(df[["COD_USU", "SEXO", "EDAD_USU", "PAI_USU", "NOM_CEN", "FEC_ING"]].head(3))

# Distribucion por edad y sexo
print("\nDistribucion por edad y sexo:")
print(df.groupby("SEXO", observed=True)["EDAD_USU"].describe().round(2))
