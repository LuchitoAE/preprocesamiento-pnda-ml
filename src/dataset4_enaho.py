"""
Dataset 4: ENAHO 2024 - Modulo 01 (caracteristicas de la vivienda).
Fuente: https://www.datosabiertos.gob.pe/dataset/encuesta-nacional-de-hogares-enaho-2024-instituto-nacional-de-estadistica-e-informatica-
"""
import os
import pandas as pd

from utils import descargar, quitar_tildes, stats, imprimir_comparativa

URL = "https://www.datosabiertos.gob.pe/sites/default/files/Enaho01-2024-100.csv"
RAW = "datasets/enaho_2024/Enaho01-2024-100.csv"
OUT = "datasets_limpios/enaho_2024_limpio.csv"

DOMINIO_INEI = {
    1: "COSTA NORTE", 2: "COSTA CENTRO", 3: "COSTA SUR",
    4: "SIERRA NORTE", 5: "SIERRA CENTRO", 6: "SIERRA SUR",
    7: "SELVA", 8: "LIMA METROPOLITANA",
}


def cargar() -> pd.DataFrame:
    descargar(URL, RAW)
    # El archivo de la PNDA viene en Latin-1; con UTF-8 falla por la "AÑO".
    return pd.read_csv(RAW, encoding="latin-1", low_memory=False)


def preprocesar(enaho: pd.DataFrame) -> pd.DataFrame:
    # 1) Normalizar nombres de columnas (quitar tildes, eñes, espacios)
    enaho.columns = [quitar_tildes(c).replace(" ", "_") for c in enaho.columns]

    # 2) UBIGEO a string de 6 digitos
    enaho["UBIGEO"] = enaho["UBIGEO"].apply(lambda x: str(int(x)).zfill(6))

    # 3) DOMINIO con etiqueta legible
    enaho["DOMINIO_NOMBRE"] = enaho["DOMINIO"].map(DOMINIO_INEI)

    # 4) Quitar columnas constantes (no aportan informacion)
    nunique = enaho.nunique(dropna=True)
    enaho = enaho.loc[:, nunique > 1]

    # 5) Quitar columnas con > 80% de nulos
    umbral = int(0.2 * len(enaho))
    enaho = enaho.dropna(axis=1, thresh=umbral)

    return enaho


def main():
    print("[4/5] ENAHO 2024 - Modulo 01")
    raw = cargar()
    antes = stats(raw, "antes")
    limpio = preprocesar(raw)
    despues = stats(limpio, "despues")
    imprimir_comparativa(antes, despues, "ENAHO 2024")
    os.makedirs("datasets_limpios", exist_ok=True)
    limpio.to_csv(OUT, index=False, encoding="utf-8")
    print(f"  guardado: {OUT}")
    return antes, despues


if __name__ == "__main__":
    main()
