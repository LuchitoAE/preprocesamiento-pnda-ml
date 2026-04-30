# Dataset 3 - ENDES 2024 REC42 (lactancia / nutricion / IMC)
# Fuente: https://www.datosabiertos.gob.pe/dataset/encuesta-demografica-y-de-salud-familiar-endes-2024-instituto-nacional-de-estadistica-e

import pandas as pd
import numpy as np
import urllib.request

# Headers de navegador real (los servidores de la PNDA bloquean User-Agents simples)
url = "https://www.datosabiertos.gob.pe/sites/default/files/REC42_2024.csv"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=300) as r, open("REC42_2024.csv", "wb") as f:
    f.write(r.read())

# El archivo viene con BOM, por eso utf-8-sig
df = pd.read_csv("REC42_2024.csv", encoding="utf-8-sig", low_memory=False)
print("Antes del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  V445 (IMC) min/max:", df["V445"].min(), df["V445"].max())
print("  V445 media:", round(df["V445"].mean(), 1), " <- aparenta error pero es la convencion DHS (x100)")
print(df[["CASEID", "V401", "V404", "V437", "V438", "V445"]].head(3))

# Problemas detectados:
# - 169 columnas con nombres tipo V401, V404, V445. Sin diccionario no se entiende nada.
# - V445 (IMC) viene multiplicado por 100 (convencion DHS). Valores entre 1290 y 9999 lucen como datos imposibles.
# - Codigos 9998 y 9999 que en realidad significan "No sabe" / "No respondio".
#   Si se procesan como numeros distorsionan completamente la media.

# 1) Renombrar variables clave segun el diccionario DHS / INEI
df = df.rename(columns={
    "V401": "tuvo_hijos_alguna_vez",
    "V404": "lacta_actualmente",
    "V437": "peso_kg_x10",
    "V438": "talla_cm_x10",
    "V445": "imc_x100",
})

# 2) Codigos especiales DHS (9998 = NS, 9999 = NR) -> NaN
for c in ["imc_x100", "peso_kg_x10", "talla_cm_x10"]:
    df.loc[df[c].isin([9998, 9999]), c] = np.nan

# 3) Reescalar a unidades reales
df["imc"] = df["imc_x100"] / 100
df["peso_kg"] = df["peso_kg_x10"] / 10
df["talla_cm"] = df["talla_cm_x10"] / 10

# 4) Marcar outliers de IMC con IQR
q1, q3 = df["imc"].quantile([0.25, 0.75])
iqr = q3 - q1
df["imc_outlier"] = ~df["imc"].between(q1 - 1.5*iqr, q3 + 1.5*iqr)

# 5) Quedarnos con columnas relevantes para el analisis nutricional
df = df[["ID1", "CASEID", "tuvo_hijos_alguna_vez", "lacta_actualmente",
         "imc", "peso_kg", "talla_cm", "imc_outlier"]]

print("\nDespues del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  IMC media:", round(df["imc"].mean(), 2), "  <- ahora si es un IMC creible")
print("  IMC mediana:", round(df["imc"].median(), 2))
print("  outliers IMC:", int(df["imc_outlier"].sum()))
print(df.head(3))
