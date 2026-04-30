# Dataset 2 - Fallecidos por COVID-19 (MINSA)
# Fuente: https://www.datosabiertos.gob.pe/dataset/fallecidos-por-covid-19-ministerio-de-salud-minsa
# El archivo se sirve comprimido (gzip) desde el propio repo de GitHub.

import pandas as pd
import numpy as np
import unicodedata

URL = "https://raw.githubusercontent.com/LuchitoAE/preprocesamiento-pnda-ml/main/data/fallecidos_covid.csv.gz"
df = pd.read_csv(URL, sep=";", compression="gzip", encoding="utf-8", low_memory=False)
print("Antes del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  duplicados:", df.duplicated().sum())
print("  edad min/max:", df["EDAD_DECLARADA"].min(), df["EDAD_DECLARADA"].max())
print(df.head(3))

# Problemas detectados:
# - FECHA_FALLECIMIENTO y FECHA_CORTE son enteros (yyyymmdd), no datetime.
# - UBIGEO se carga como float64, perdiendo el cero a la izquierda (010101 -> 10101.0).
# - 11 duplicados exactos.
# - 5 filas con departamento, provincia, distrito o ubigeo en blanco.
# - Edades imposibles (mayores a 110).
# - Texto geografico con tildes y mayusculas inconsistentes.

# 1) Fechas a datetime
for c in ["FECHA_FALLECIMIENTO", "FECHA_CORTE"]:
    df[c] = pd.to_datetime(df[c].astype(str), format="%Y%m%d", errors="coerce")

# 2) UBIGEO a string de 6 digitos (preserva ceros a la izquierda)
df["UBIGEO"] = df["UBIGEO"].apply(lambda x: str(int(x)).zfill(6) if pd.notna(x) else np.nan)

# 3) Duplicados exactos fuera
df = df.drop_duplicates()

# 4) Edades plausibles (0 a 110)
df = df[df["EDAD_DECLARADA"].between(0, 110)]

# 5) Normalizar nombres geograficos (mayusculas, sin tildes)
def quitar_tildes(s):
    if pd.isna(s):
        return s
    s = str(s).upper().strip()
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

for c in ["DEPARTAMENTO", "PROVINCIA", "DISTRITO"]:
    df[c] = df[c].apply(quitar_tildes)

# 6) Filas sin geografia fuera
df = df.dropna(subset=["DEPARTAMENTO", "PROVINCIA", "UBIGEO"])

# 7) Tipos optimizados para reducir memoria
df["EDAD_DECLARADA"] = df["EDAD_DECLARADA"].astype("int8")
df["SEXO"] = df["SEXO"].astype("category")
df["DEPARTAMENTO"] = df["DEPARTAMENTO"].astype("category")
df["CLASIFICACION_DEF"] = df["CLASIFICACION_DEF"].astype("category")

print("\nDespues del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  duplicados:", df.duplicated().sum())
print("  memoria MB:", round(df.memory_usage(deep=True).sum()/1024/1024, 1))
print(df.head(3))

# Fallecidos por departamento (top 10)
print("\nFallecidos por departamento (top 10):")
print(df["DEPARTAMENTO"].value_counts().head(10))
