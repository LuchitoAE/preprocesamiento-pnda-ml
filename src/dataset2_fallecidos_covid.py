"""
Dataset 2: Fallecidos por COVID-19 (MINSA).
Fuente: https://www.datosabiertos.gob.pe/dataset/fallecidos-por-covid-19-ministerio-de-salud-minsa
"""
import os
import pandas as pd
import numpy as np

from utils import descargar, quitar_tildes, stats, imprimir_comparativa

URL = "https://files.minsa.gob.pe/s/t9AFqRbXw3F55Ho/download"
RAW = "datasets/covid_fallecidos/fallecidos_covid.csv"
OUT = "datasets_limpios/fallecidos_covid_limpio.parquet"


def cargar() -> pd.DataFrame:
    descargar(URL, RAW)
    return pd.read_csv(RAW, sep=";", encoding="utf-8", low_memory=False)


def preprocesar(fall: pd.DataFrame) -> pd.DataFrame:
    # 1) Fechas a datetime (vienen como entero yyyymmdd)
    for c in ["FECHA_FALLECIMIENTO", "FECHA_CORTE"]:
        fall[c] = pd.to_datetime(
            fall[c].astype(str), format="%Y%m%d", errors="coerce"
        )

    # 2) UBIGEO a string de 6 digitos (preserva ceros a la izquierda)
    fall["UBIGEO"] = fall["UBIGEO"].apply(
        lambda x: str(int(x)).zfill(6) if pd.notna(x) else np.nan
    )

    # 3) Eliminar duplicados exactos
    fall = fall.drop_duplicates()

    # 4) Filtrar edades plausibles (0 - 110)
    fall = fall[fall["EDAD_DECLARADA"].between(0, 110)].copy()

    # 5) Normalizar nombres geograficos (mayusculas, sin tildes)
    for c in ["DEPARTAMENTO", "PROVINCIA", "DISTRITO"]:
        fall[c] = fall[c].apply(quitar_tildes)

    # 6) Quitar filas sin geografia
    fall = fall.dropna(subset=["DEPARTAMENTO", "PROVINCIA", "UBIGEO"])

    # 7) Tipos optimizados para reducir memoria
    fall["EDAD_DECLARADA"] = fall["EDAD_DECLARADA"].astype("int8")
    fall["SEXO"] = fall["SEXO"].astype("category")
    fall["DEPARTAMENTO"] = fall["DEPARTAMENTO"].astype("category")
    fall["CLASIFICACION_DEF"] = fall["CLASIFICACION_DEF"].astype("category")

    return fall


def main():
    print("[2/5] Fallecidos COVID-19")
    raw = cargar()
    antes = stats(raw, "antes")
    limpio = preprocesar(raw)
    despues = stats(limpio, "despues")
    imprimir_comparativa(antes, despues, "Fallecidos COVID-19")
    os.makedirs("datasets_limpios", exist_ok=True)
    limpio.to_parquet(OUT)
    print(f"  guardado: {OUT}")
    return antes, despues


if __name__ == "__main__":
    main()
