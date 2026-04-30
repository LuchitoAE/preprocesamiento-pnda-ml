"""
Dataset 1: ETES - Gasto Presupuestal de las Entidades de Tratamiento Empresarial 2024.
Fuente: https://www.datosabiertos.gob.pe/dataset/gasto-presupuestal-de-las-entidades-de-tratamiento-empresarial-etes
"""
import os
import pandas as pd

from utils import descargar, stats, imprimir_comparativa

URL = "https://fs.datosabiertos.mef.gob.pe/datastorefiles/2024-Gastos-ETES.csv"
RAW = "datasets/etes/2024-Gastos-ETES.csv"
OUT = "datasets_limpios/etes_2024_limpio.csv"


def cargar() -> pd.DataFrame:
    descargar(URL, RAW)
    return pd.read_csv(RAW, encoding="utf-8", low_memory=False)


def preprocesar(etes: pd.DataFrame) -> pd.DataFrame:
    # 1) Eliminar columnas redundantes (CODIGO + _NOMBRE)
    cols_codigo = [c for c in etes.columns if (c + "_NOMBRE") in etes.columns]
    etes = etes.drop(columns=cols_codigo)

    # 2) Estructura del archivo: MES_EJE = 0 trae presupuesto (PIA/PIM),
    #    MES_EJE 1..12 trae la ejecucion mensual. Se agrega ejecucion del ano
    #    por meta y se une con su PIM para tener una fila por meta.
    key = [c for c in ["SEC_EJEC", "SEC_FUNC", "META", "FINALIDAD"]
           if c in etes.columns]
    ejec_anual = (etes[etes["MES_EJE"].between(1, 12)]
                  .groupby(key, observed=True, dropna=False)["MONTO_EJECUCION"]
                  .sum()
                  .reset_index()
                  .rename(columns={"MONTO_EJECUCION": "EJEC_ANUAL"}))
    presupuesto = etes[(etes["MES_EJE"] == 0) & (etes["MONTO_PIM"] > 0)].copy()
    etes = presupuesto.merge(ejec_anual, on=key, how="left")
    etes["EJEC_ANUAL"] = etes["EJEC_ANUAL"].fillna(0)

    # 3) Calcular porcentaje de ejecucion (metrica clave en analisis presupuestal)
    etes["PCT_EJECUCION"] = (etes["EJEC_ANUAL"] / etes["MONTO_PIM"] * 100).round(2)

    # 4) Quitar columnas auxiliares que ya no aplican
    etes = etes.drop(columns=["MES_EJE", "MONTO_EJECUCION"], errors="ignore")

    # 5) Variables categoricas de baja cardinalidad
    for c in ["GRUPO_ENTIDAD_NOMBRE", "DEPARTAMENTO_EJECUTORA_NOMBRE",
              "FUNCION_NOMBRE", "TIPO_ACT_PROY_NOMBRE"]:
        if c in etes.columns:
            etes[c] = etes[c].astype("category")

    return etes


def main():
    print("[1/5] ETES 2024")
    raw = cargar()
    antes = stats(raw, "antes")
    limpio = preprocesar(raw)
    despues = stats(limpio, "despues")
    imprimir_comparativa(antes, despues, "ETES 2024")
    os.makedirs("datasets_limpios", exist_ok=True)
    limpio.to_csv(OUT, index=False, encoding="utf-8")
    print(f"  guardado: {OUT}")
    return antes, despues


if __name__ == "__main__":
    main()
