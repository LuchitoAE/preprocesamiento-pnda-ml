"""
Ejecuta el preprocesamiento de los 5 datasets en orden e imprime
una tabla comparativa final (antes / despues).

Uso:
    python src/main.py            # ejecuta todos
    python src/dataset1_etes.py   # ejecuta solo uno

En Google Colab:
    !git clone https://github.com/<usuario>/<repo>.git
    %cd <repo>
    !pip install -r requirements.txt
    !python src/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dataset1_etes
import dataset2_fallecidos_covid
import dataset3_endes
import dataset4_enaho
import dataset5_nna_cedif


def main():
    resultados = {}
    resultados["ETES 2024"] = dataset1_etes.main()
    resultados["Fallecidos COVID"] = dataset2_fallecidos_covid.main()
    resultados["ENDES 2024"] = dataset3_endes.main()
    resultados["ENAHO 2024"] = dataset4_enaho.main()
    resultados["NNA CEDIF"] = dataset5_nna_cedif.main()

    print("\n" + "=" * 78)
    print("TABLA COMPARATIVA FINAL")
    print("=" * 78)
    print(f"{'Dataset':<22}{'filas A':>10}{'filas D':>10}{'cols A':>9}"
          f"{'cols D':>9}{'MB A':>9}{'MB D':>9}")
    print("-" * 78)
    for nombre, (a, d) in resultados.items():
        print(f"{nombre:<22}{a['filas']:>10,}{d['filas']:>10,}"
              f"{a['columnas']:>9}{d['columnas']:>9}"
              f"{a['memoria_mb']:>9.1f}{d['memoria_mb']:>9.1f}")


if __name__ == "__main__":
    main()
