"""
Dataset 3: ENDES 2024 - REC42 (lactancia, nutricion, antropometria).
Fuente: https://www.datosabiertos.gob.pe/dataset/encuesta-demografica-y-de-salud-familiar-endes-2024-instituto-nacional-de-estadistica-e
"""
import os
import pandas as pd
import numpy as np

from utils import descargar, stats, imprimir_comparativa

URL = "https://www.datosabiertos.gob.pe/sites/default/files/REC42_2024.csv"
RAW = "datasets/endes_2024/REC42_2024.csv"
OUT = "datasets_limpios/endes_2024_limpio.csv"


def cargar() -> pd.DataFrame:
    descargar(URL, RAW)
    return pd.read_csv(RAW, encoding="utf-8-sig", low_memory=False)


def preprocesar(endes: pd.DataFrame) -> pd.DataFrame:
    # 1) Renombrar variables clave segun diccionario DHS / INEI
    ren = {
        "V401": "tuvo_hijos_alguna_vez",
        "V404": "lacta_actualmente",
        "V437": "peso_kg_x10",
        "V438": "talla_cm_x10",
        "V445": "imc_x100",
    }
    endes = endes.rename(columns={k: v for k, v in ren.items() if k in endes.columns})

    # 2) Codigos especiales DHS (9998 = NS, 9999 = NR) -> NaN
    for c in ["imc_x100", "peso_kg_x10", "talla_cm_x10"]:
        if c in endes.columns:
            endes.loc[endes[c].isin([9998, 9999]), c] = np.nan

    # 3) Reescalar a unidades reales (DHS guarda x100 / x10)
    if "imc_x100" in endes.columns:
        endes["imc"] = endes["imc_x100"] / 100
    if "peso_kg_x10" in endes.columns:
        endes["peso_kg"] = endes["peso_kg_x10"] / 10
    if "talla_cm_x10" in endes.columns:
        endes["talla_cm"] = endes["talla_cm_x10"] / 10

    # 4) Marcar outliers de IMC con IQR
    if "imc" in endes.columns:
        q1, q3 = endes["imc"].quantile([0.25, 0.75])
        iqr = q3 - q1
        endes["imc_outlier"] = ~endes["imc"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

    # 5) Quedarnos con columnas relevantes para el analisis nutricional
    cols = [c for c in ["ID1", "CASEID", "tuvo_hijos_alguna_vez",
                        "lacta_actualmente", "imc", "peso_kg", "talla_cm",
                        "imc_outlier"] if c in endes.columns]
    return endes[cols]


def main():
    print("[3/5] ENDES 2024 (REC42)")
    raw = cargar()
    antes = stats(raw, "antes")
    limpio = preprocesar(raw)
    despues = stats(limpio, "despues")
    imprimir_comparativa(antes, despues, "ENDES 2024")
    os.makedirs("datasets_limpios", exist_ok=True)
    limpio.to_csv(OUT, index=False, encoding="utf-8")
    print(f"  guardado: {OUT}")
    if "imc" in limpio.columns:
        print(f"  IMC media (despues): {limpio['imc'].mean():.2f}")
    return antes, despues


if __name__ == "__main__":
    main()
