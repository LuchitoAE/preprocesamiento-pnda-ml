"""
Dataset 5: Servicio de cuidado diurno a NNA en CEDIF (INABIF).
Fuente: https://www.datosabiertos.gob.pe/dataset/servicio-de-cuidado-diurno-nna-en-situacion-de-riesgo-de-desproteccion-familiar
Se descargan 5 archivos mensuales (oct 2025 a feb 2026) y se concatenan.
"""
import os
import glob
import pandas as pd

from utils import descargar, quitar_tildes, stats, imprimir_comparativa

BASE_URL = "https://www.datosabiertos.gob.pe/sites/default/files/NNA%20atendidos%20en%20CEDIF%20{mes}%20{anio}.csv"
DEST_DIR = "datasets/cuidado_diurno_nna"
OUT = "datasets_limpios/nna_cedif_limpio.csv"

MESES = [
    ("Octubre", 2025),
    ("Noviembre", 2025),
    ("Diciembre", 2025),
    ("Enero", 2026),
    ("Febrero", 2026),
]

# Esquema "estandar" centrado en el usuario (16 columnas).
# El archivo de enero 2026 trae otro esquema (datos familiares) y se descarta.
ESQUEMA = ["COD_USU", "SEX_USU", "FEC_NAC_USU", "EDAD_USU", "GRU_ET",
           "PAI_USU", "TIE_DIS", "LEN_MAT", "AUT_IDE_ET", "NOM_CEN",
           "FEC_ING", "PER_ING", "TIP_SEG_SAL", "EST_ACT", "FEC_EGR",
           "MOT_EGR"]


def cargar() -> pd.DataFrame:
    """Descarga los 5 archivos mensuales y los concatena tal cual."""
    rutas = []
    for mes, anio in MESES:
        url = BASE_URL.format(mes=mes, anio=anio)
        destino = os.path.join(DEST_DIR, f"NNA_{mes}_{anio}.csv")
        descargar(url, destino)
        rutas.append(destino)
    trozos = [pd.read_csv(r, sep=";", encoding="latin-1", low_memory=False)
              for r in rutas]
    return pd.concat(trozos, ignore_index=True)


def preprocesar(nna_concat: pd.DataFrame, rutas: list[str]) -> pd.DataFrame:
    # 1) Solo mantenemos los archivos cuyo esquema coincide con el estandar
    trozos = []
    for r in rutas:
        d = pd.read_csv(r, sep=";", encoding="latin-1", low_memory=False)
        if all(c in d.columns for c in ESQUEMA):
            d["__archivo__"] = os.path.basename(r)
            trozos.append(d[ESQUEMA + ["__archivo__"]])
    nna = pd.concat(trozos, ignore_index=True)

    # 2) Eliminar duplicados exactos
    nna = nna.drop_duplicates()

    # 3) Normalizar PAI_USU (PERU sin tilde, mayusculas)
    nna["PAI_USU"] = nna["PAI_USU"].apply(quitar_tildes)

    # 4) Fechas a datetime
    for c in ["FEC_NAC_USU", "FEC_ING", "FEC_EGR"]:
        nna[c] = pd.to_datetime(nna[c], errors="coerce")

    # 5) Codificar sexo (1=M, 2=F)
    nna["SEXO"] = nna["SEX_USU"].map({1: "MASCULINO", 2: "FEMENINO"})

    # 6) Filtrar edades validas para NNA (0 - 17)
    nna["EDAD_USU"] = pd.to_numeric(nna["EDAD_USU"], errors="coerce")
    nna = nna[nna["EDAD_USU"].between(0, 17)].copy()
    nna["EDAD_USU"] = nna["EDAD_USU"].astype("int8")

    # 7) Tipos categoricos
    for c in ["NOM_CEN", "PAI_USU", "SEXO"]:
        nna[c] = nna[c].astype("category")

    return nna


def main():
    print("[5/5] NNA CEDIF (INABIF)")
    rutas = []
    for mes, anio in MESES:
        url = BASE_URL.format(mes=mes, anio=anio)
        destino = os.path.join(DEST_DIR, f"NNA_{mes}_{anio}.csv")
        descargar(url, destino)
        rutas.append(destino)

    raw = pd.concat(
        [pd.read_csv(r, sep=";", encoding="latin-1", low_memory=False) for r in rutas],
        ignore_index=True
    )
    antes = stats(raw, "antes")
    limpio = preprocesar(raw, rutas)
    despues = stats(limpio, "despues")
    imprimir_comparativa(antes, despues, "NNA CEDIF")
    os.makedirs("datasets_limpios", exist_ok=True)
    limpio.to_csv(OUT, index=False, encoding="utf-8")
    print(f"  guardado: {OUT}")
    return antes, despues


if __name__ == "__main__":
    main()
