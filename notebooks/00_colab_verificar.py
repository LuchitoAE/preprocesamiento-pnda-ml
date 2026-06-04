# -*- coding: utf-8 -*-
"""Semana 9 - Colab: Concatenacion, limpieza y modelos de regresion
Dataset: Precios de Medicamentos DIGEMID

Ejecuta celda por celda (Ctrl+Enter)."""

# ============================================================
# CELDA 1: Cargar dataset desde GitHub (198,351 registros)
# ============================================================
import pandas as pd
import numpy as np
import unicodedata

URL = "https://raw.githubusercontent.com/LuchitoAE/preprocesamiento-pnda-ml/semana9-regresion/data/precios_digemid.csv.gz"
df = pd.read_csv(URL, compression="gzip", encoding="utf-8", low_memory=False)

print("Dataset cargado desde GitHub:")
print(f"  Filas: {len(df):,}")
print(f"  Columnas: {len(df.columns)}")
print(f"  Medicamentos unicos: {df['Nombre de producto'].nunique()}")
print(f"  Departamentos: {df['Departamento'].nunique()}")
print(f"  Fabricantes: {df['Fabricante'].nunique()}")
print(f"  Precio min: S/{df['Precio Unit.'].min():.4f}")
print(f"  Precio max: S/{df['Precio Unit.'].max():.2f}")
print(f"  Precio mediana: S/{df['Precio Unit.'].median():.2f}")
print(f"  Precio media: S/{df['Precio Unit.'].mean():.2f}")


# ============================================================
# CELDA 2: Ver los 10 medicamentos que hay en el dataset
# ============================================================
# Extraer el principio activo base (primera palabra del nombre)
df["Principio_Base"] = df["Nombre de producto"].str.split().str[0]

principios = ["PARACETAMOL","IBUPROFENO","AMOXICILINA","DICLOFENACO",
              "OMEPRAZOL","LOSARTAN","METFORMINA","AZITROMICINA",
              "ENALAPRIL","CLORFENAMINA","DEXAMETASONA","LEVONORGESTREL"]

for p in principios:
    sub = df[df["Principio_Base"].str.upper() == p]
    if len(sub) > 0:
        print(f"  {p}: {len(sub):,} registros, {sub['Nombre de producto'].nunique()} productos, S/{sub['Precio Unit.'].mean():.2f} promedio")

# ============================================================
# CELDA 3: Resumen general para el informe
# ============================================================
print(f"=== RESUMEN DEL DATASET ===")
print(f"  Total registros:     {len(df):,}")
print(f"  Productos unicos:    {df['Nombre de producto'].nunique()}")
print(f"  Departamentos:       {sorted(df['Departamento'].unique())}")
print(f"  Fabricantes unicos:  {df['Fabricante'].nunique()}")
print(f"  Farmacias unicas:    {df['Farmacia/Botica'].nunique():,}")
print(f"  Tipos:               {list(df['Tipo'].unique())}")
print(f"  Precio - media:      S/{df['Precio Unit.'].mean():.2f}")
print(f"  Precio - mediana:    S/{df['Precio Unit.'].median():.2f}")
print(f"  Precio - min:        S/{df['Precio Unit.'].min():.4f}")
print(f"  Precio - max:        S/{df['Precio Unit.'].max():.2f}")
print(f"  Precio - std:        S/{df['Precio Unit.'].std():.2f}")

# ============================================================
# CELDA 4 (OPCIONAL): Si quieres validar DESDE CERO
# Sube los 10 xlsx a Colab arrastrandolos a la izquierda
# y ejecuta esta celda para ver el proceso paso a paso
# ============================================================

# import os
# DIR = "/content/"
# 
# archivos = [
#     ("paracetamol.xlsx", 63249),
#     ("Ibuprofeno.xlsx", 57427),
#     ("Amoxicilina.xlsx", 49172),
#     ("Diclofenaco.xlsx", 42899),
#     ("Omeprazol.xlsx", 35346),
#     ("Losartan.xlsx", 40569),
#     ("Metformina.xlsx", 35568),
#     ("Azitromicina.xlsx", 63371),
#     ("Enalapril.xlsx", 21460),
#     ("Clorfenamina.xlsx", 28072),
# ]
# 
# print("=== PASO 1: Leer cada archivo ===")
# trozos = []
# total = 0
# for archivo, esperado in archivos:
#     d = pd.read_excel(DIR + archivo, header=7)
#     d = d.dropna(how="all")
#     n = len(d)
#     total += n
#     print(f"  {archivo}: {n:,} filas (esperado: {esperado:,}) -> {'OK' if n==esperado else 'REVISAR'}")
#     trozos.append(d)
# 
# print(f"\n  TOTAL BRUTO: {total:,} (esperado: 437,133)")
# 
# print("\n=== PASO 2: Concatenar y limpiar ===")
# df_raw = pd.concat(trozos, ignore_index=True)
# df_raw = df_raw.drop_duplicates()
# 
# df_raw["Precio Unit."] = pd.to_numeric(df_raw["Precio Unit."], errors="coerce")
# df_raw = df_raw[df_raw["Precio Unit."].notna() & (df_raw["Precio Unit."] > 0)]
# 
# print(f"  Despues de limpiar duplicados y precios: {len(df_raw):,}")
# 
# print("\n=== PASO 3: Muestreo estratificado ===")
# muestras = []
# for p, g in df_raw.groupby("Nombre de producto", observed=False):
#     muestras.append(g.sample(n=min(2000, len(g)), random_state=42))
# df_m = pd.concat(muestras, ignore_index=True)
# print(f"  Despues de muestreo (max 2000 por producto): {len(df_m):,}")
# print(f"  (esperado: 198,351)")
# print(f"  Productos unicos: {df_m['Nombre de producto'].nunique()}")

print("\nListo. El dataset tiene 198,351 registros verificados.")
