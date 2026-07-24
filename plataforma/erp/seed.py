"""Siembra el ERP mock con los CSV reales del corte de Colsubsidio.

Esto es lo que hace la evidencia EJECUTABLE en vez de narrativa:
el agente no recuerda que hay 79 negativos, los consulta.
"""
import csv, pathlib, unicodedata, re

DATA = pathlib.Path(__file__).resolve().parents[2] / "context" / "data"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).replace("\xa0", " ")
    s = s.encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().upper()


def load(name: str) -> list[dict]:
    with open(DATA / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seed(conn):
    cat, stock = load("catalogo.csv"), load("stock_corte.csv")
    bodegas = {(r["bodega_id"], r["bodega_id"]) for r in cat}
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO bodega (bodega_id, nombre, nombre_norm) VALUES (%s,%s,%s) "
            "ON CONFLICT DO NOTHING",
            [(b, b, norm(b)) for b, _ in bodegas],
        )
        cur.executemany(
            "INSERT INTO catalogo (bodega_id, sku, nombre_raw, nombre_norm, unidad) "
            "VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            [(r["bodega_id"], r["sku"] or None, r["nombre_raw"], r["nombre_norm"], r["unidad"])
             for r in cat],
        )
        cur.executemany(
            "INSERT INTO stock_corte (bodega_id, nombre_norm, sku, unidad, cantidad, fecha_corte) "
            "VALUES (%s,%s,%s,%s,%s,'2026-07-01') ON CONFLICT DO NOTHING",
            [(r["bodega_id"], r["nombre_norm"], r["sku"] or None, r["unidad"], float(r["stock"]))
             for r in stock if r["stock"]],
        )
    conn.commit()
    print(f"sembrado: {len(cat)} catalogo, {len(stock)} stock")


if __name__ == "__main__":
    c, s = load("catalogo.csv"), load("stock_corte.csv")
    neg = [r for r in s if r["stock"] and float(r["stock"]) < 0]
    nosku = [r for r in s if not r["sku"]]
    print(f"catalogo={len(c)} stock={len(s)} negativos={len(neg)} sin_sku={len(nosku)}")
    print(f"refs unicas={len({r['nombre_norm'] for r in s})} bodegas={len({r['bodega_id'] for r in s})}")
