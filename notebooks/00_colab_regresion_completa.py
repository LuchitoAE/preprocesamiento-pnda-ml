# Semana 9 - Colab: Regresion completa
# Dataset: Precios de Medicamentos DIGEMID (198,351 registros)
# ============================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)

# ============================================================
# 1. CARGAR DATOS DESDE GITHUB
# ============================================================
URL = "https://raw.githubusercontent.com/LuchitoAE/preprocesamiento-pnda-ml/semana9-regresion/data/precios_digemid.csv.gz"
df = pd.read_csv(URL, compression="gzip", encoding="utf-8", low_memory=False)
print(f"Dataset cargado: {len(df):,} filas x {df.shape[1]} columnas\n")

# ============================================================
# 2. OUTLIERS (IQR)
# ============================================================
q1 = df["Precio Unit."].quantile(0.25)
q3 = df["Precio Unit."].quantile(0.75)
iqr = q3 - q1
lim_inf = q1 - 1.5*iqr
lim_sup = q3 + 1.5*iqr
df["Outlier"] = ~df["Precio Unit."].between(lim_inf, lim_sup)

print(f"Outliers - Q1={q1:.2f} | Q3={q3:.2f} | IQR={iqr:.2f}")
print(f"Limites: [{lim_inf:.2f}, {lim_sup:.2f}]")
print(f"Outliers detectados: {df['Outlier'].sum():,} ({df['Outlier'].mean()*100:.1f}%)\n")

# ============================================================
# 3. PREPROCESAMIENTO
# ============================================================
# Crear variable binaria para regresion logistica
mediana = df["Precio Unit."].median()
df["Precio_Alto"] = (df["Precio Unit."] > mediana).astype(int)
print(f"Mediana: S/{mediana:.2f}")
print(f"Altos: {df['Precio_Alto'].sum():,} | Bajos: {len(df)-df['Precio_Alto'].sum():,}\n")

# Label Encoding
features = ["Tipo", "Nombre de producto", "Fabricante", "Farmacia/Botica", "Departamento"]
X = pd.DataFrame()
for c in features:
    X[c] = LabelEncoder().fit_transform(df[c].astype(str))

y_reg = df["Precio Unit."].values
y_clf = df["Precio_Alto"].values

# ============================================================
# 4. TRAIN/TEST SPLIT
# ============================================================
X_tr, X_te, yr_tr, yr_te, yc_tr, yc_te = train_test_split(
    X, y_reg, y_clf, test_size=0.2, random_state=42
)
print(f"Train: {len(X_tr):,} | Test: {len(X_te):,}\n")

# ============================================================
# 5. REGRESION LINEAL
# ============================================================
print("=== REGRESION LINEAL ===")
lr = LinearRegression()
lr.fit(X_tr, yr_tr)
yp = lr.predict(X_te)

rmse = np.sqrt(mean_squared_error(yr_te, yp))
mae = mean_absolute_error(yr_te, yp)
r2 = r2_score(yr_te, yp)

print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"R2:   {r2:.4f} ({r2*100:.1f}%)")

# Coeficientes
coefs = sorted(zip(features, lr.coef_), key=lambda x: abs(x[1]), reverse=True)
print("Importancia (|coef|):")
for name, coef in coefs:
    print(f"  {name:25s}: {coef:+.4f}")

# ============================================================
# 6. REGRESION LOGISTICA
# ============================================================
print("\n=== REGRESION LOGISTICA ===")
log = LogisticRegression(max_iter=2000, random_state=42)
log.fit(X_tr, yc_tr)
ypc = log.predict(X_te)

acc = accuracy_score(yc_te, ypc)
prec = precision_score(yc_te, ypc, zero_division=0)
rec = recall_score(yc_te, ypc, zero_division=0)
f1 = f1_score(yc_te, ypc, zero_division=0)
cm = confusion_matrix(yc_te, ypc)

print(f"Accuracy:  {acc:.4f} ({acc*100:.1f}%)")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"Matriz de confusion:")
print(f"  VP={cm[1,1]:,}  FP={cm[0,1]:,}")
print(f"  FN={cm[1,0]:,}  VN={cm[0,0]:,}")

# ============================================================
# 7. RESUMEN
# ============================================================
print("\n" + "="*50)
print("RESUMEN FINAL")
print("="*50)
print(f"Registros: {len(df):,}")
print(f"Reg. Lineal  -> RMSE={rmse:.4f} | MAE={mae:.4f} | R2={r2:.4f}")
print(f"Reg. Logistica -> Acc={acc:.4f} | Prec={prec:.4f} | Recall={rec:.4f} | F1={f1:.4f}")
print("="*50)
