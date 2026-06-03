# Semana 9 - Ejecucion completa con datos reales DIGEMID
# Genera los resultados que iran en el informe.

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

print("Cargando datos...")
df = pd.read_csv("../datasets_limpios/precios_digemid.csv", encoding="utf-8")
print(f"  {len(df)} filas, {df.shape[1]} columnas")

# ============================================================
# 1. IDENTIFICACION DE VARIABLES
# ============================================================
print("\n=== 1. IDENTIFICACION DE VARIABLES ===")
print("Target (regresion): Precio Unit.")
print("Target (logistica): Precio_Alto (> mediana)")
print("Features: Tipo, Nombre de producto, Fabricante, Farmacia/Botica, Departamento")
print()

# ============================================================
# 2. LIMPIEZA
# ============================================================
print("=== 2. LIMPIEZA Y DATOS FALTANTES ===")
n_antes = len(df)
df = df.drop_duplicates()
dup_elim = n_antes - len(df)

# Arreglar "P u b l i c o" -> "PUBLICO"
if "Tipo" in df.columns:
    df["Tipo"] = df["Tipo"].str.replace(" ", "", regex=False).str.upper().astype("category")

df["Precio Unit."] = pd.to_numeric(df["Precio Unit."], errors="coerce")
precio_antes = len(df)
df = df[df["Precio Unit."].notna() & (df["Precio Unit."] > 0)]
precio_filtrados = precio_antes - len(df)

nulos = df.isnull().sum().sum()
print(f"  Duplicados: {dup_elim}")
print(f"  Precios invalidos (nulos/<=0): {precio_filtrados}")
print(f"  Nulos restantes: {nulos}")
print(f"  Filas final: {len(df)}")
print()

# ============================================================
# 3. CATEGORICAS
# ============================================================
print("=== 3. TRANSFORMACION DE VARIABLES CATEGORICAS ===")
cat_cols = ["Tipo", "Nombre de producto", "Fabricante", "Farmacia/Botica", "Departamento"]
cats_info = {}
for c in cat_cols:
    if c in df.columns:
        df[c] = df[c].astype("category")
        cats_info[c] = df[c].nunique()
        print(f"  {c}: {df[c].nunique()} categorias")

# Crear target binario
mediana = float(df["Precio Unit."].median())
df["Precio_Alto"] = (df["Precio Unit."] > mediana).astype(int)
n_altos = int(df["Precio_Alto"].sum())
n_bajos = int(len(df) - n_altos)
print(f"\n  Mediana precio: S/{mediana:.2f}")
print(f"  Altos: {n_altos} | Bajos: {n_bajos}")
print()

# ============================================================
# 4. OUTLIERS
# ============================================================
print("=== 4. DETECCION DE OUTLIERS ===")
q1 = float(df["Precio Unit."].quantile(0.25))
q3 = float(df["Precio Unit."].quantile(0.75))
iqr = q3 - q1
lim_inf = q1 - 1.5 * iqr
lim_sup = q3 + 1.5 * iqr
n_outliers = int((~df["Precio Unit."].between(lim_inf, lim_sup)).sum())
print(f"  Q1={q1:.4f} | Q3={q3:.4f} | IQR={iqr:.4f}")
print(f"  Limites: [{lim_inf:.4f}, {lim_sup:.4f}]")
print(f"  Outliers: {n_outliers} de {len(df)} ({100*n_outliers/len(df):.1f}%)")
print()

# ============================================================
# 5. EDA
# ============================================================
print("=== 5. ANALISIS EXPLORATORIO (EDA) ===")
stats = df["Precio Unit."].describe()
print(f"  Media: S/{stats['mean']:.2f}")
print(f"  Mediana: S/{stats['50%']:.2f}")
print(f"  Min: S/{stats['min']:.4f} | Max: S/{stats['max']:.2f}")
print(f"  Desv. Estandar: S/{stats['std']:.2f}")

print("\n  Precio promedio por Tipo:")
for t in df["Tipo"].unique():
    grupo = df[df["Tipo"] == t]
    print(f"    {t}: media=S/{grupo['Precio Unit.'].mean():.2f}  n={len(grupo)}")

print("\n  Top 5 Departamentos con mas registros:")
deptos = df.groupby("Departamento", observed=True).agg(
    n=("Precio Unit.", "count"),
    precio_medio=("Precio Unit.", "mean")
).sort_values("n", ascending=False).head(5)
for d, row in deptos.iterrows():
    print(f"    {d}: {int(row['n'])} registros, precio medio S/{row['precio_medio']:.2f}")

print("\n  Top 5 Fabricantes:")
fabs = df.groupby("Fabricante", observed=True).agg(
    n=("Precio Unit.", "count"),
    precio_medio=("Precio Unit.", "mean")
).sort_values("n", ascending=False).head(5)
for f, row in fabs.iterrows():
    print(f"    {f}: {int(row['n'])} registros, precio medio S/{row['precio_medio']:.2f}")

print("\n  Precio promedio por medicamento:")
meds = df.groupby("Nombre de producto", observed=True).agg(
    n=("Precio Unit.", "count"),
    precio_medio=("Precio Unit.", "mean")
).sort_values("n", ascending=False).head(10)
for m, row in meds.iterrows():
    print(f"    {m}: {int(row['n'])} registros, precio medio S/{row['precio_medio']:.2f}")
print()

# ============================================================
# 6. SPLIT
# ============================================================
print("=== 6. DIVISION TRAIN/TEST ===")
feature_cols = ["Tipo", "Nombre de producto", "Fabricante", "Farmacia/Botica", "Departamento"]

# Codificar
X = pd.DataFrame()
for c in feature_cols:
    le = LabelEncoder()
    X[c] = le.fit_transform(df[c].astype(str))

y_reg = df["Precio Unit."].values
y_clf = df["Precio_Alto"].values

X_train, X_test, yr_train, yr_test, yc_train, yc_test = \
    train_test_split(X, y_reg, y_clf, test_size=0.2, random_state=42)

print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
print()

# ============================================================
# 7. REGRESION LINEAL
# ============================================================
print("=== 7. REGRESION LINEAL ===")
lr = LinearRegression()
lr.fit(X_train, yr_train)
y_pred_lr = lr.predict(X_test)

rmse = float(np.sqrt(mean_squared_error(yr_test, y_pred_lr)))
mae = float(mean_absolute_error(yr_test, y_pred_lr))
r2 = float(r2_score(yr_test, y_pred_lr))

print(f"  RMSE: {rmse:.4f}")
print(f"  MAE: {mae:.4f}")
print(f"  R2: {r2:.4f} ({(r2*100):.1f}%)")

# Coeficientes
coefs = sorted(zip(feature_cols, lr.coef_), key=lambda x: abs(x[1]), reverse=True)
print("  Importancia (|coef|):")
for nombre, coef in coefs:
    print(f"    {nombre:25s}: {coef:+.4f}")
print()

# ============================================================
# 8. REGRESION LOGISTICA
# ============================================================
print("=== 8. REGRESION LOGISTICA ===")
log = LogisticRegression(max_iter=2000, random_state=42)
log.fit(X_train, yc_train)
y_pred_log = log.predict(X_test)

acc = float(accuracy_score(yc_test, y_pred_log))
prec = float(precision_score(yc_test, y_pred_log, zero_division=0))
rec = float(recall_score(yc_test, y_pred_log, zero_division=0))
f1 = float(f1_score(yc_test, y_pred_log, zero_division=0))
cm = confusion_matrix(yc_test, y_pred_log)

print(f"  Accuracy: {acc:.4f} ({acc*100:.1f}%)")
print(f"  Precision: {prec:.4f}")
print(f"  Recall: {rec:.4f}")
print(f"  F1-Score: {f1:.4f}")
print(f"  Matriz confusion:")
print(f"    VP={cm[1,1]:6d}  FP={cm[0,1]:6d}")
print(f"    FN={cm[1,0]:6d}  VN={cm[0,0]:6d}")
print()

# ============================================================
# GUARDAR RESULTADOS PARA EL DOCX
# ============================================================
resultados = {
    "n_filas": int(len(df)),
    "n_columnas": int(df.shape[1]),
    "n_medicamentos": int(df["Nombre de producto"].nunique()),
    "n_departamentos": int(df["Departamento"].nunique()),
    "n_fabricantes": int(df["Fabricante"].nunique()),
    "precio_min": float(df["Precio Unit."].min()),
    "precio_max": float(df["Precio Unit."].max()),
    "precio_media": float(df["Precio Unit."].mean()),
    "precio_mediana": float(mediana),
    "precio_std": float(df["Precio Unit."].std()),
    "n_outliers": n_outliers,
    "pct_outliers": float(100*n_outliers/len(df)),
    "lim_inf": float(lim_inf),
    "lim_sup": float(lim_sup),
    "iqr": float(iqr),
    "n_altos": n_altos,
    "n_bajos": n_bajos,
    "rmse": rmse,
    "mae": mae,
    "r2": r2,
    "acc": acc,
    "prec": prec,
    "rec": rec,
    "f1": f1,
    "cm_vp": int(cm[1,1]),
    "cm_fp": int(cm[0,1]),
    "cm_fn": int(cm[1,0]),
    "cm_vn": int(cm[0,0]),
    "top_deptos": [(str(d), int(r['n']), float(r['precio_medio'])) for d, r in deptos.iterrows()],
    "top_fabricantes": [(str(f), int(r['n']), float(r['precio_medio'])) for f, r in fabs.iterrows()],
    "precios_por_tipo": [(str(t), float(grupo['Precio Unit.'].mean()), int(len(grupo))) for t, grupo in df.groupby("Tipo", observed=True)],
}

with open("../informe/resultados_ml.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print("=== RESULTADOS GUARDADOS EN resultados_ml.json ===")


