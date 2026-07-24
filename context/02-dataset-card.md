# Dataset card — BODEGAS_Y_STOCK.xlsx

Entregado por Colsubsidio. Corte único, sin serie histórica.

## Origen
9 hojas: `BODEGAS DISPONIBLES` (48 nombres de bodega) + 8 hojas de stock.

## Estructura por registro
| Columna original | Significado |
|---|---|
| `CANTIDAD` | índice de fila, **no** es cantidad. Trampa de nombre |
| `Nr.Artículo` | SKU. Vacío en el 18% de las filas |
| `Artículo` | nombre libre. Sucio (espacios, NBSP) |
| `Unidad` | `Unidad` · `Kilogram` · `Liter` · `Portion` |
| `SD` | **la cantidad real** al corte |

> `CANTIDAD` es el índice y `SD` es la cantidad. Si los inviertes, todo el sistema queda mal.

## Derivados en `data/`
- **`catalogo.csv`** — `bodega_id, sku, nombre_raw, nombre_norm, unidad`. El scope por bodega. Usa `nombre_norm` para comparar, `nombre_raw` para mostrar.
- **`stock_corte.csv`** — `bodega_id, sku, nombre_norm, unidad, stock`. **Esto es lo que NUNCA se muestra al operario** (conteo ciego).
- **`bodegas_declaradas.csv`** — las 48, con sus duplicados intactos a propósito.

## Cómo se siembra
`plataforma/erp/seed.py` carga estos CSV en Postgres. El ERP mock los sirve. Es la única fuente de datos del sistema.
