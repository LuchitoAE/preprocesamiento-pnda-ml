# Script auxiliar: concatenar los 10 xlsx y generar el CSV unico + analisis completo
# Ejecutar: python preparar_datos.py

import pandas as pd
import numpy as np
import unicodedata
import os

DIR = "../datos"
OUT = "../datasets_limpios/precios_digemid.csv"
HEADER_ROW = 7

archivos = [
    "paracetamol.xlsx", "Ibuprofeno.xlsx", "Amoxicilina.xlsx", "Diclofenaco.xlsx",
    "Omeprazol.xlsx", "Losartan.xlsx", "Metformina.xlsx", "Azitromicina.xlsx",
    "Enalapril.xlsx", "Clorfenamina.xlsx"
]

trozos = []
for archivo in archivos:
    path = os.path.join(DIR, archivo)
    d = pd.read_excel(path, header=HEADER_ROW)
    d = d.dropna(how="all")
    print(f"  {archivo}: {len(d)} filas")
    trozos.append(d)

df = pd.concat(trozos, ignore_index=True)
print(f"\n  TOTAL bruto: {len(df)} filas")

# ----- Limpieza -----
df = df.drop_duplicates()

# Convertir precio a numerico
df["Precio Unit."] = pd.to_numeric(df["Precio Unit."], errors="coerce")
df = df[df["Precio Unit."].notna() & (df["Precio Unit."] > 0)]

# Normalizar texto
def limpiar(s):
    if pd.isna(s):
        return "DESCONOCIDO"
    s = str(s).strip().upper()
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

cat_cols = ["Tipo", "Nombre de producto", "Titular", "Fabricante",
            "Farmacia/Botica", "Departamento", "Provincia", "Distrito"]
for c in cat_cols:
    if c in df.columns:
        df[c] = df[c].apply(limpiar)

# Tomar muestra estratificada por medicamento (max 2000 por producto = ~20K total)
muestras = []
for prod, grupo in df.groupby("Nombre de producto", observed=False):
    n = min(2000, len(grupo))
    muestras.append(grupo.sample(n=n, random_state=42))
df = pd.concat(muestras, ignore_index=True)

print(f"  TOTAL despues de limpieza y muestreo: {len(df)} filas")
print(f"  Medicamentos: {df['Nombre de producto'].nunique()}")
print(f"  Departamentos: {df['Departamento'].nunique()}")
print(f"  Precio min: {df['Precio Unit.'].min():.4f} | max: {df['Precio Unit.'].max():.4f} | mediana: {df['Precio Unit.'].median():.4f}")

df.to_csv(OUT, index=False, encoding="utf-8")
print(f"\n  CSV guardado: {OUT}")


