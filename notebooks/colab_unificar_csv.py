# -*- coding: utf-8 -*-
"""Colab: Concatenar los 10 CSV y hacer todo el proceso desde cero"""

import pandas as pd
import numpy as np
import unicodedata
from google.colab import files

# ============================================================
# CELDA 1: Subir los 10 archivos CSV
# ============================================================
print("Selecciona los 10 archivos CSV (paracetamol.csv, Ibuprofeno.csv, etc.)")
uploaded = files.upload()

archivos = [
    "paracetamol.csv", "Ibuprofeno.csv", "Amoxicilina.csv",
    "Diclofenaco.csv", "Omeprazol.csv", "Losartan.csv",
    "Metformina.csv", "Azitromicina.csv", "Enalapril.csv",
    "Clorfenamina.csv"
]

# ============================================================
# CELDA 2: Leer y mostrar cada archivo
# ============================================================
print("=== LEYENDO CADA CSV ===")
trozos = []
total_bruto = 0
for archivo in archivos:
    d = pd.read_csv(archivo, encoding="utf-8", low_memory=False)
    d = d.dropna(how="all")
    n = len(d)
    total_bruto += n
    print(f"  {archivo}: {n:,} filas | {d['Nombre de producto'].nunique()} productos | {d['Departamento'].nunique()} deptos")
    trozos.append(d)

print(f"\n  TOTAL BRUTO: {total_bruto:,} registros")

# ============================================================
# CELDA 3: Concatenar y limpiar
# ============================================================
df = pd.concat(trozos, ignore_index=True)
df = df.drop_duplicates()

df["Precio Unit."] = pd.to_numeric(df["Precio Unit."], errors="coerce")
df = df[df["Precio Unit."].notna() & (df["Precio Unit."] > 0)]

def limpiar(s):
    if pd.isna(s): return "DESCONOCIDO"
    s = str(s).strip().upper()
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

for c in ["Tipo", "Nombre de producto", "Titular", "Fabricante",
          "Farmacia/Botica", "Departamento", "Provincia", "Distrito"]:
    df[c] = df[c].apply(limpiar)

# Arreglar espacios raros en TIPO
df["Tipo"] = df["Tipo"].str.replace(" ", "", regex=False)

print(f"\n  Despues de limpieza (sin muestreo): {len(df):,} registros")

# ============================================================
# CELDA 4: Muestreo estratificado (max 2000 por producto)
# ============================================================
muestras = []
for prod, grupo in df.groupby("Nombre de producto", observed=False):
    n = min(2000, len(grupo))
    muestras.append(grupo.sample(n=n, random_state=42))

df = pd.concat(muestras, ignore_index=True)
print(f"\n  FINAL: {len(df):,} registros")
print(f"  Medicamentos unicos: {df['Nombre de producto'].nunique()}")
print(f"  Deptos: {df['Departamento'].nunique()}")
print(f"  Fabricantes: {df['Fabricante'].nunique()}")
print(f"  Precio medio: S/{df['Precio Unit.'].mean():.2f}")
print(f"  Precio mediana: S/{df['Precio Unit.'].median():.2f}")

# ============================================================
# CELDA 5: Guardar resultado
# ============================================================
df.to_csv("precios_digemid_unificado.csv", index=False)
print("\n  Guardado: precios_digemid_unificado.csv")
files.download("precios_digemid_unificado.csv")
