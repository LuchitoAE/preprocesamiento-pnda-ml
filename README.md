# Preprocesamiento de 5 datasets de la PNDA

Trabajo del curso de Machine Learning. Cada script descarga un dataset
de la Plataforma Nacional de Datos Abiertos del Peru y aplica su preprocesamiento.

| # | Script | Dataset |
|---|--------|---------|
| 1 | `notebooks/01_etes.py` | Gasto Presupuestal ETES 2024 (MEF) |
| 2 | `notebooks/02_fallecidos_covid.py` | Fallecidos por COVID-19 (MINSA) |
| 3 | `notebooks/03_endes.py` | ENDES 2024 - REC42 (INEI) |
| 4 | `notebooks/04_enaho.py` | ENAHO 2024 - Modulo 01 (INEI) |
| 5 | `notebooks/05_nna_cedif.py` | NNA atendidos en CEDIF (INABIF) |

Los datasets crudos estan en `data/` comprimidos con gzip (~7 MB total contra
~97 MB sin comprimir). Cada script los descarga directo desde el `raw` de
GitHub via `pd.read_csv(URL, compression="gzip")`, asi no depende de los
servidores de la PNDA y corre sin problemas en Colab.

Cada script se ejecuta por separado, son independientes entre si.
