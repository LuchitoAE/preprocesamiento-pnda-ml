# Semana 9 - Modelos de Regresion con Precios de Medicamentos DIGEMID

Dataset: Precios de Medicamentos en Establecimientos de Salud (DIGEMID)
Fuente: https://opm-digemid.minsa.gob.pe/

## Estructura

```
semana 9/
  README.md
  datos/                          <- Archivos xlsx originales del observatorio
    paracetamol.xlsx
    Ibuprofeno.xlsx
    Amoxicilina.xlsx
    Diclofenaco.xlsx
    Omeprazol.xlsx
    Losartan.xlsx
    Metformina.xlsx
    Azitromicina.xlsx
    Enalapril.xlsx
    Clorfenamina.xlsx
    plantilla_digemid.csv
  datasets_limpios/               <- Dataset unificado y limpio
    precios_digemid.csv           (198,351 filas, 12 columnas)
  notebooks/                      <- Script de analisis
    01_regresion_digemid.py
  scripts/                        <- Scripts auxiliares
    preparar_datos.py             (concatena xlsx -> csv)
    ejecutar_analisis.py          (regresion lineal + logistica)
    generar_docx.py               (genera el informe .docx)
  informe/                        <- Informe y resultados
    informe_semana9_regresion_digemid.docx
    informe_para_escribir.txt
    resultados_ml.json
```

## Medicamentos incluidos

| # | Principio activo | Concentracion |
|---|-----------------|---------------|
| 1 | Paracetamol | 500 mg |
| 2 | Ibuprofeno | 400 mg |
| 3 | Amoxicilina | 500 mg |
| 4 | Diclofenaco | 50 mg |
| 5 | Omeprazol | 20 mg |
| 6 | Losartan | 50 mg |
| 7 | Metformina | 850 mg |
| 8 | Azitromicina | 500 mg |
| 9 | Enalapril | 10 mg |
| 10 | Clorfenamina | 4 mg |

## Resultados principales

| Metrica | Valor |
|---------|-------|
| Total de registros | 198,351 |
| Presentaciones unicas | 303 |
| Departamentos | 25 |
| Fabricantes | 109 |
| Mediana precio | S/1.10 |
| Regresion Lineal - RMSE | 65.41 |
| Regresion Lineal - MAE | 2.36 |
| Regresion Lineal - R2 | 0.0016 |
| Regresion Logistica - Accuracy | 54.7% |
| Regresion Logistica - F1 | 0.48 |

## Como ejecutar

```bash
# Reconstruir el dataset desde los xlsx
python scripts/preparar_datos.py

# Ejecutar el analisis completo
python scripts/ejecutar_analisis.py

# Generar el informe docx
python scripts/generar_docx.py
```
