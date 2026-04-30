# Dataset 1 - ETES (Gasto Presupuestal Entidades Tratamiento Empresarial 2024)
# Fuente: https://www.datosabiertos.gob.pe/dataset/gasto-presupuestal-de-las-entidades-de-tratamiento-empresarial-etes
# El archivo se sirve comprimido (gzip) desde el propio repo de GitHub.

import pandas as pd

URL = "https://raw.githubusercontent.com/LuchitoAE/preprocesamiento-pnda-ml/main/data/etes_2024.csv.gz"
df = pd.read_csv(URL, compression="gzip", encoding="utf-8", low_memory=False)
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
