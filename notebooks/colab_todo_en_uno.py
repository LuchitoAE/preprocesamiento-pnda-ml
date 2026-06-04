# Semana 9 - Colab: Todo en uno (unificar desde CSV + regresion)
# Sube los 10 CSV y ejecuta celda por celda (Ctrl+Enter)

import pandas as pd
import numpy as np
import unicodedata
from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)

# ============================================================
# CELDA 1: Subir los 10 archivos CSV desde tu PC
# ============================================================
print("Sube los 10 archivos CSV (paracetamol.csv, Ibuprofeno.csv, etc.)")
uploaded = files.upload()

# ============================================================
# CELDA 2: Leer cada CSV y concatenarlos
# ============================================================
archivos = [
    "paracetamol.csv", "Ibuprofeno.csv", "Amoxicilina.csv",
    "Diclofenaco.csv", "Omeprazol.csv", "Losartan.csv",
    "Metformina.csv", "Azitromicina.csv", "Enalapril.csv",
    "Clorfenamina.csv"
]

trozos = []
total = 0
print("=== LEYENDO CADA CSV ===")
for a in archivos:
    d = pd.read_csv(a, encoding="utf-8", low_memory=False).dropna(how="all")
    n = len(d)
    total += n
    print(f"  {a}: {n:,} filas | {d['Nombre de producto'].nunique()} productos")
    trozos.append(d)

df = pd.concat(trozos, ignore_index=True)
print(f"\n  TOTAL BRUTO: {total:,} registros")

# ============================================================
# CELDA 3: Limpieza
# ============================================================
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

df["Tipo"] = df["Tipo"].str.replace(" ", "", regex=False)
print(f"  Despues de limpieza: {len(df):,} registros")

# ============================================================
# CELDA 4: Muestreo estratificado
# ============================================================
muestras = []
for p, g in df.groupby("Nombre de producto", observed=False):
    n = min(2000, len(g))
    muestras.append(g.sample(n=n, random_state=42))
df = pd.concat(muestras, ignore_index=True)
print(f"  Despues de muestreo: {len(df):,} registros")
print(f"  Productos: {df['Nombre de producto'].nunique()} | Deptos: {df['Departamento'].nunique()} | Fabricantes: {df['Fabricante'].nunique()}")

# ============================================================
# CELDA 5: Outliers + preparacion
# ============================================================
q1 = df["Precio Unit."].quantile(0.25)
q3 = df["Precio Unit."].quantile(0.75)
iqr = q3 - q1
lim_inf = q1 - 1.5*iqr
lim_sup = q3 + 1.5*iqr
n_out = (~df["Precio Unit."].between(lim_inf, lim_sup)).sum()
print(f"\n  Outliers (IQR): {n_out:,} ({100*n_out/len(df):.1f}%)")

mediana = df["Precio Unit."].median()
df["Precio_Alto"] = (df["Precio Unit."] > mediana).astype(int)

# Encoding
features = ["Tipo", "Nombre de producto", "Fabricante", "Farmacia/Botica", "Departamento"]
X = pd.DataFrame({c: LabelEncoder().fit_transform(df[c].astype(str)) for c in features})
y_reg = df["Precio Unit."].values
y_clf = df["Precio_Alto"].values

# ============================================================
# CELDA 6: Train/test split + modelos
# ============================================================
X_tr, X_te, yr_tr, yr_te, yc_tr, yc_te = train_test_split(
    X, y_reg, y_clf, test_size=0.2, random_state=42)

print(f"\n  Train: {len(X_tr):,} | Test: {len(X_te):,}")

# Regresion lineal
lr = LinearRegression()
lr.fit(X_tr, yr_tr)
yp = lr.predict(X_te)
print(f"\n  REGRESION LINEAL")
print(f"  RMSE={np.sqrt(mean_squared_error(yr_te,yp)):.4f} | MAE={mean_absolute_error(yr_te,yp):.4f} | R2={r2_score(yr_te,yp):.4f}")

# Regresion logistica
log = LogisticRegression(max_iter=2000, random_state=42)
log.fit(X_tr, yc_tr)
ypc = log.predict(X_te)
cm = confusion_matrix(yc_te, ypc)
print(f"\n  REGRESION LOGISTICA")
print(f"  Acc={accuracy_score(yc_te,ypc):.4f} | Prec={precision_score(yc_te,ypc,zero_division=0):.4f} | Rec={recall_score(yc_te,ypc,zero_division=0):.4f} | F1={f1_score(yc_te,ypc,zero_division=0):.4f}")
print(f"  VP={cm[1,1]:,} FP={cm[0,1]:,} FN={cm[1,0]:,} VN={cm[0,0]:,}")

# ============================================================
# CELDA 7 (OPCIONAL): Descargar dataset unificado
# ============================================================
# df.to_csv("precios_digemid_unificado.csv", index=False)
# files.download("precios_digemid_unificado.csv")
print("\n  === PROCESO COMPLETO ===")
