# Preprocesamiento de 5 datasets de la PNDA

Trabajo del curso de Machine Learning (8vo ciclo, UPLA). Aplica un proceso
de limpieza y transformacion sobre cinco conjuntos de datos publicos de la
**Plataforma Nacional de Datos Abiertos del Peru** (https://www.datosabiertos.gob.pe/).

## Datasets utilizados

| # | Dataset | Entidad | Fuente |
|---|---------|---------|--------|
| 1 | Gasto Presupuestal de las Entidades de Tratamiento Empresarial (ETES) 2024 | MEF | [link](https://www.datosabiertos.gob.pe/dataset/gasto-presupuestal-de-las-entidades-de-tratamiento-empresarial-etes) |
| 2 | Fallecidos por COVID-19 | MINSA | [link](https://www.datosabiertos.gob.pe/dataset/fallecidos-por-covid-19-ministerio-de-salud-minsa) |
| 3 | ENDES 2024 - REC42 (lactancia / nutricion) | INEI | [link](https://www.datosabiertos.gob.pe/dataset/encuesta-demografica-y-de-salud-familiar-endes-2024-instituto-nacional-de-estadistica-e) |
| 4 | ENAHO 2024 - Modulo 01 (vivienda) | INEI | [link](https://www.datosabiertos.gob.pe/dataset/encuesta-nacional-de-hogares-enaho-2024-instituto-nacional-de-estadistica-e-informatica-) |
| 5 | NNA atendidos en CEDIF (oct 2025 a feb 2026) | INABIF | [link](https://www.datosabiertos.gob.pe/dataset/servicio-de-cuidado-diurno-nna-en-situacion-de-riesgo-de-desproteccion-familiar) |

## Estructura

```
.
├── README.md
├── requirements.txt
├── informe_preprocesamiento_ml_final.docx   <- informe escrito
├── notebooks/
│   └── preprocesamiento_colab.ipynb         <- mismo flujo, listo para Colab
└── src/
    ├── utils.py                             <- descarga + helpers comunes
    ├── dataset1_etes.py
    ├── dataset2_fallecidos_covid.py
    ├── dataset3_endes.py
    ├── dataset4_enaho.py
    ├── dataset5_nna_cedif.py
    └── main.py                              <- ejecuta los 5
```

Cada `dataset*.py` se puede ejecutar de forma independiente (`python src/datasetN_xxx.py`)
o todo de corrido con `python src/main.py`.

Las URLs de los datasets estan codificadas dentro de cada script, asi que el
codigo descarga los archivos automaticamente. La PNDA bloquea peticiones
sin User-Agent, por eso se usa una cabecera de navegador en `utils.descargar`.

## Ejecutar localmente

```bash
git clone https://github.com/<usuario>/<repo>.git
cd <repo>
pip install -r requirements.txt
python src/main.py
```

## Ejecutar en Google Colab

Opcion A - subir el notebook:

1. Entra a https://colab.research.google.com/
2. Archivo > Subir notebook > selecciona `notebooks/preprocesamiento_colab.ipynb`
3. Ejecuta las celdas en orden.

Opcion B - clonar el repo dentro de Colab:

```python
!git clone https://github.com/<usuario>/<repo>.git
%cd <repo>
!pip install -r requirements.txt
!python src/main.py
```

## Resultados (antes / despues)

| Dataset           | Filas (A → D)        | Cols (A → D) | Memoria MB (A → D) | Reduccion |
|-------------------|----------------------|--------------|--------------------|-----------|
| ETES 2024         | 78,135 → 14,164      | 51 → 30      | 71.4 → 9.4         | -87%      |
| Fallecidos COVID  | 220,918 → 220,899    | 10 → 10      | 27.5 → 17.4        | -37%      |
| ENDES 2024        | 34,252 → 34,252      | 169 → 8      | 48.4 → 2.5         | -95%      |
| ENAHO 2024        | 100 → 100            | 338 → 244    | 0.3 → 0.2          | -25%      |
| NNA CEDIF         | 30,128 → 26,573      | 28 → 18      | 9.4 → 3.9          | -58%      |

## Notas

- Los archivos crudos descargados (`datasets/`) y los limpios (`datasets_limpios/`)
  no se versionan: el script los regenera al correr.
- El IMC en ENDES (V445) viene multiplicado por 100; tras el reescalado la media
  cae a ~26.9 (sobrepeso poblacional), valor coherente con publicaciones del INEI.
- En NNA CEDIF, el archivo de enero 2026 trae un esquema distinto (datos
  familiares en vez de datos de usuario) y se descarta para no contaminar el merge.

## Curso

- Universidad Peruana Los Andes - Facultad de Ingenieria
- Escuela Profesional de Ingenieria de Sistemas y Computacion
- Curso: Machine Learning - 8vo ciclo (2026-I)
