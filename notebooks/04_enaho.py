# Dataset 4 - ENAHO 2024 modulo 01 (caracteristicas de la vivienda)
# Fuente: https://www.datosabiertos.gob.pe/dataset/encuesta-nacional-de-hogares-enaho-2024-instituto-nacional-de-estadistica-e-informatica-

import pandas as pd
import unicodedata
import urllib.request

# Headers de navegador real (los servidores de la PNDA bloquean User-Agents simples)
url = "https://www.datosabiertos.gob.pe/sites/default/files/Enaho01-2024-100.csv"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=300) as r, open("Enaho01-2024-100.csv", "wb") as f:
    f.write(r.read())

# El archivo viene en Latin-1 (con utf-8 falla por la "ANO" del header)
df = pd.read_csv("Enaho01-2024-100.csv", encoding="latin-1", low_memory=False)
print("Antes del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  primer header:", repr(df.columns[0]), "<- tilde y enie rompen referencias")
print("  UBIGEO ejemplo:", df["UBIGEO"].iloc[0], "<- entero, perdio el cero a la izquierda")
print(df[[df.columns[0], "MES", "UBIGEO", "DOMINIO"]].head(3))

# Problemas detectados:
# - Encoding Latin-1: con utf-8 sale UnicodeDecodeError.
# - Header "ANO" con enie y tilde, que rompe referencias en SQL u otros entornos.
# - UBIGEO viene como entero, asi que 010101 queda como 10101.
# - 338 columnas, muchas con casi solo NaN o constantes (no aportan).
# - DOMINIO esta codificado de 1 a 8 sin etiqueta legible.

# 1) Limpiar nombres de columnas (sin tildes ni eñes)
def quitar_tildes(s):
    s = str(s).upper().strip()
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

df.columns = [quitar_tildes(c).replace(" ", "_") for c in df.columns]

# 2) UBIGEO a string de 6 digitos
df["UBIGEO"] = df["UBIGEO"].apply(lambda x: str(int(x)).zfill(6))

# 3) DOMINIO con etiqueta INEI
df["DOMINIO_NOMBRE"] = df["DOMINIO"].map({
    1: "COSTA NORTE", 2: "COSTA CENTRO", 3: "COSTA SUR",
    4: "SIERRA NORTE", 5: "SIERRA CENTRO", 6: "SIERRA SUR",
    7: "SELVA", 8: "LIMA METROPOLITANA",
})

# 4) Descartar columnas constantes (no aportan informacion)
df = df.loc[:, df.nunique(dropna=True) > 1]

# 5) Descartar columnas con > 80% de nulos
df = df.dropna(axis=1, thresh=int(0.2 * len(df)))

print("\nDespues del preprocesamiento:")
print("  filas:", len(df), "  columnas:", df.shape[1])
print("  primer header:", repr(df.columns[0]))
print("  UBIGEO ejemplo:", df["UBIGEO"].iloc[0])
print(df[["ANO", "MES", "UBIGEO", "DOMINIO", "DOMINIO_NOMBRE"]].head(5))
