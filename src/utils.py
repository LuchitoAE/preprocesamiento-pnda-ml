"""
Utilidades comunes: descarga con User-Agent (la PNDA bloquea curl/requests sin UA),
limpieza de texto y resumen estadistico de un DataFrame.
"""
import os
import urllib.request
import unicodedata
import pandas as pd

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")


def descargar(url: str, destino: str, timeout: int = 600) -> str:
    """Descarga url a destino si no existe ya. Devuelve la ruta destino."""
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    if os.path.exists(destino) and os.path.getsize(destino) > 1000:
        print(f"  ya existe: {destino}")
        return destino
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/csv,*/*",
        "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
    })
    print(f"  descargando {os.path.basename(destino)} ...")
    with urllib.request.urlopen(req, timeout=timeout) as r, open(destino, "wb") as f:
        f.write(r.read())
    mb = os.path.getsize(destino) / 1024 / 1024
    print(f"  -> {mb:.2f} MB")
    return destino


def quitar_tildes(s):
    if pd.isna(s):
        return s
    s = str(s).upper().strip()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def stats(df: pd.DataFrame, etiqueta: str = "") -> dict:
    return {
        "etiqueta": etiqueta,
        "filas": int(len(df)),
        "columnas": int(df.shape[1]),
        "duplicados": int(df.duplicated().sum()),
        "nulos_total": int(df.isna().sum().sum()),
        "memoria_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
    }


def imprimir_comparativa(antes: dict, despues: dict, nombre: str) -> None:
    print(f"\n--- {nombre} ---")
    print(f"  filas:    {antes['filas']:>10,} -> {despues['filas']:>10,}")
    print(f"  columnas: {antes['columnas']:>10} -> {despues['columnas']:>10}")
    print(f"  duplicados: {antes['duplicados']:>8,} -> {despues['duplicados']:>8,}")
    print(f"  nulos:    {antes['nulos_total']:>10,} -> {despues['nulos_total']:>10,}")
    print(f"  memoria:  {antes['memoria_mb']:>9.1f} -> {despues['memoria_mb']:>9.1f} MB")
