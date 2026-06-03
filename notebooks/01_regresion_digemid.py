# Semana 9 - Aplicacion de Modelos de Regresion
# Dataset: Precios de Medicamentos en Establecimientos de Salud (DIGEMID)
# Fuente: Observatorio de Precios de Medicamentos - https://opm-digemid.minsa.gob.pe/
#
# NOTA: Ejecuta cada bloque por separado (Ctrl+Enter en VS Code / celda en Colab).
# El archivo "precios_digemid.csv" debe estar en la misma carpeta que este script.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

sns.set_style("whitegrid")

# ============================================================
# 0. CARGA DE DATOS
# ============================================================
df = pd.read_csv("../datasets_limpios/precios_digemid.csv", encoding="utf-8")
print("Dimensiones:", df.shape)
print("Columnas:", list(df.columns))
print(df.head())

# ============================================================
# 1. IDENTIFICACION DE VARIABLES
# ============================================================
print("\n--- TIPOS DE DATOS ---")
print(df.dtypes)

print("\n--- VARIABLE OBJETIVO (TARGET) ---")
print("  Precio Unit. (cuantitativa continua) -> regresion lineal")
print("  Precio_Alto (binaria: 1 si precio > mediana) -> regresion logistica")

print("\n--- VARIABLES PREDICTORAS ---")
print("  Categoricas: Tipo, Nombre de producto, Titular, Fabricante,")
print("               Farmacia/Botica, Departamento, Provincia, Distrito")
print("  Fecha (temporal): Fecha de Actualizac.")
print("  Excluidas: Telefono, Direccion (irrelevantes para regresion)")

# ============================================================
# 2. LIMPIEZA Y DATOS FALTANTES
# ============================================================
print("\n--- VALORES NULOS ---")
print(df.isnull().sum())

# Duplicados
d_antes = len(df)
df = df.drop_duplicates()
print(f"\nDuplicados eliminados: {d_antes - len(df)}")

# Convertir Precio Unit. a numerico
df["Precio Unit."] = pd.to_numeric(df["Precio Unit."], errors="coerce")

# Filtrar precios nulos o <= 0
df = df[df["Precio Unit."].notna() & (df["Precio Unit."] > 0)]

# Convertir fecha
df["Fecha de Actualizac."] = pd.to_datetime(df["Fecha de Actualizac."], dayfirst=True, errors="coerce")

print(f"\nFilas despues de limpieza: {len(df)}")

# ============================================================
# 3. TRANSFORMACION DE VARIABLES CATEGORICAS
# ============================================================
cat_cols = ["Tipo", "Nombre de producto", "Titular", "Fabricante",
            "Farmacia/Botica", "Departamento", "Provincia", "Distrito"]

# Normalizar texto: quitar tildes, mayusculas, espacios extra
import unicodedata

def limpiar_texto(s):
    if pd.isna(s):
        return "DESCONOCIDO"
    s = str(s).strip().upper()
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

for c in cat_cols:
    df[c] = df[c].apply(limpiar_texto).astype("category")

print("\n--- CATEGORIAS POR VARIABLE ---")
for c in cat_cols:
    print(f"  {c}: {df[c].nunique()} valores unicos")

# Crear variable binaria para regresion logistica: precio alto/bajo
mediana = df["Precio Unit."].median()
df["Precio_Alto"] = (df["Precio Unit."] > mediana).astype(int)
print(f"\nMediana de precio: S/{mediana:.2f}")
print(f"Precios altos (> mediana): {df['Precio_Alto'].sum()} de {len(df)}")

# ============================================================
# 4. DETECCION DE OUTLIERS
# ============================================================
q1 = df["Precio Unit."].quantile(0.25)
q3 = df["Precio Unit."].quantile(0.75)
iqr = q3 - q1
lim_inf = q1 - 1.5 * iqr
lim_sup = q3 + 1.5 * iqr

df["Outlier"] = ~df["Precio Unit."].between(lim_inf, lim_sup)
print(f"\n--- OUTLIERS (IQR) ---")
print(f"  Q1 = {q1:.2f}, Q3 = {q3:.2f}, IQR = {iqr:.2f}")
print(f"  Limites: [{lim_inf:.2f}, {lim_sup:.2f}]")
print(f"  Outliers detectados: {df['Outlier'].sum()} de {len(df)}")

# ============================================================
# 5. ANALISIS EXPLORATORIO (EDA)
# ============================================================
print("\n--- ESTADISTICAS DESCRIPTIVAS ---")
print(df["Precio Unit."].describe())

# Precio promedio por departamento
print("\n--- PRECIO PROMEDIO POR DEPARTAMENTO (top 10) ---")
print(df.groupby("Departamento", observed=True)["Precio Unit."]
        .agg(["count", "mean", "median", "min", "max"])
        .sort_values("count", ascending=False).head(10))

# Precio promedio por tipo (Marca vs Generico)
print("\n--- PRECIO POR TIPO ---")
print(df.groupby("Tipo", observed=True)["Precio Unit."]
        .agg(["count", "mean", "median"]).round(2))

# Top fabricantes
print("\n--- TOP FABRICANTES ---")
print(df.groupby("Fabricante", observed=True)["Precio Unit."]
        .agg(["count", "mean"]).round(2)
        .sort_values("count", ascending=False).head(10))

# ============================================================
# 6. DIVISION ENTRENAMIENTO / PRUEBA
# ============================================================
# Seleccionar features para regresion
feature_cols = ["Tipo", "Nombre de producto", "Fabricante",
                "Farmacia/Botica", "Departamento"]

# Codificar variables categoricas con Label Encoding
le_dict = {}
X_encoded = pd.DataFrame()
for c in feature_cols:
    le = LabelEncoder()
    X_encoded[c] = le.fit_transform(df[c].astype(str))
    le_dict[c] = le

y_reg = df["Precio Unit."].values
y_clf = df["Precio_Alto"].values

# Split 80/20
X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = \
    train_test_split(X_encoded, y_reg, y_clf, test_size=0.2, random_state=42)

print(f"\n--- DIVISION TRAIN/TEST ---")
print(f"  Train: {len(X_train)} filas, Test: {len(X_test)} filas")

# ============================================================
# 7. REGRESION LINEAL
# ============================================================
print("\n========== REGRESION LINEAL ==========")

modelo_lr = LinearRegression()
modelo_lr.fit(X_train, y_reg_train)
y_pred_lr = modelo_lr.predict(X_test)

# Metricas regresion lineal
rmse = np.sqrt(mean_squared_error(y_reg_test, y_pred_lr))
mae = mean_absolute_error(y_reg_test, y_pred_lr)
r2 = r2_score(y_reg_test, y_pred_lr)

print(f"  RMSE:  {rmse:.4f}")
print(f"  MAE:   {mae:.4f}")
print(f"  R2:    {r2:.4f} ({(r2*100):.1f}% de varianza explicada)")

# Importancia de coeficientes
coef_df = pd.DataFrame({
    "Variable": feature_cols,
    "Coeficiente": modelo_lr.coef_
}).sort_values("Coeficiente", key=abs, ascending=False)
print("\n  Importancia de variables (|coeficiente|):")
for _, row in coef_df.iterrows():
    print(f"    {row['Variable']:25s}: {row['Coeficiente']:+.4f}")

# ============================================================
# 8. REGRESION LOGISTICA
# ============================================================
print("\n========== REGRESION LOGISTICA ==========")

modelo_log = LogisticRegression(max_iter=1000, random_state=42)
modelo_log.fit(X_train, y_clf_train)
y_pred_log = modelo_log.predict(X_test)

# Metricas regresion logistica
acc = accuracy_score(y_clf_test, y_pred_log)
prec = precision_score(y_clf_test, y_pred_log, zero_division=0)
rec = recall_score(y_clf_test, y_pred_log, zero_division=0)
f1 = f1_score(y_clf_test, y_pred_log, zero_division=0)
cm = confusion_matrix(y_clf_test, y_pred_log)

print(f"  Accuracy:  {acc:.4f}")
print(f"  Precision: {prec:.4f}")
print(f"  Recall:    {rec:.4f}")
print(f"  F1-Score:  {f1:.4f}")
print(f"\n  Matriz de confusion:")
print(f"    VP: {cm[1,1]:3d}  FP: {cm[0,1]:3d}")
print(f"    FN: {cm[1,0]:3d}  VN: {cm[0,0]:3d}")

# ============================================================
# 9. RESUMEN FINAL
# ============================================================
print("\n" + "="*60)
print("  RESUMEN DE METRICAS")
print("="*60)
print(f"  Regresion Lineal -> RMSE={rmse:.4f} | MAE={mae:.4f} | R2={r2:.4f}")
print(f"  Regresion Logistica -> Accuracy={acc:.4f} | Precision={prec:.4f} | F1={f1:.4f}")
print(f"\n  Filas totales: {len(df)}")
print(f"  Outliers: {df['Outlier'].sum()}")
print(f"  Mediana precio: S/{mediana:.2f}")
print("="*60)

