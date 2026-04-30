# Dataset 1 - ETES (Gasto Presupuestal Entidades Tratamiento Empresarial 2024)
# Fuente: https://www.datosabiertos.gob.pe/dataset/gasto-presupuestal-de-las-entidades-de-tratamiento-empresarial-etes

import pandas as pd
import urllib.request

# Headers de navegador real (los servidores de la PNDA bloquean User-Agents simples)
url = "https://fs.datosabiertos.mef.gob.pe/datastorefiles/2024-Gastos-ETES.csv"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=600) as r, open("2024-Gastos-ETES.csv", "wb") as f:
    f.write(r.read())

df = pd.read_csv("2024-Gastos-ETES.csv", encoding="utf-8", low_memory=False)
print("Antes del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  memoria MB:", round(df.memory_usage(deep=True).sum()/1024/1024, 1))
print(df.head(3))

# Problemas detectados:
# - Estructura mixta: MES_EJE = 0 trae el presupuesto (PIA y PIM), MES_EJE 1 a 12 trae la ejecucion mensual.
# - 21 columnas redundantes (cada dimension viene como codigo y como _NOMBRE).
# - No existe columna PCT_EJECUCION (la metrica mas usada en analisis presupuestal).
# - Variables categoricas de baja cardinalidad guardadas como object.

# 1) Eliminar columnas redundantes (CODIGO + _NOMBRE)
cols_codigo = [c for c in df.columns if (c + "_NOMBRE") in df.columns]
df = df.drop(columns=cols_codigo)

# 2) Separar presupuesto (MES=0) de ejecucion (MES 1..12) y unir por meta
key = ["SEC_EJEC", "SEC_FUNC", "META", "FINALIDAD"]
ejec_anual = (df[df["MES_EJE"].between(1, 12)]
              .groupby(key, dropna=False)["MONTO_EJECUCION"].sum()
              .reset_index().rename(columns={"MONTO_EJECUCION": "EJEC_ANUAL"}))
presupuesto = df[(df["MES_EJE"] == 0) & (df["MONTO_PIM"] > 0)].copy()
df = presupuesto.merge(ejec_anual, on=key, how="left").fillna({"EJEC_ANUAL": 0})

# 3) Calcular % de ejecucion
df["PCT_EJECUCION"] = (df["EJEC_ANUAL"] / df["MONTO_PIM"] * 100).round(2)

# 4) Quitar columnas auxiliares que ya no aplican
df = df.drop(columns=["MES_EJE", "MONTO_EJECUCION"], errors="ignore")

# 5) Categorizar variables de baja cardinalidad
for c in ["GRUPO_ENTIDAD_NOMBRE", "DEPARTAMENTO_EJECUTORA_NOMBRE", "FUNCION_NOMBRE"]:
    if c in df.columns:
        df[c] = df[c].astype("category")

print("\nDespues del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  memoria MB:", round(df.memory_usage(deep=True).sum()/1024/1024, 1))
print(df.head(3))

# Top 10 ejecutoras con mayor ejecucion presupuestal
print("\nTop 10 ejecutoras por ejecucion anual:")
print(df.groupby("EJECUTORA_NOMBRE", observed=True)[["MONTO_PIM", "EJEC_ANUAL", "PCT_EJECUCION"]]
        .sum().sort_values("EJEC_ANUAL", ascending=False).head(10))
