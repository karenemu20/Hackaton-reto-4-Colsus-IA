# Hallazgos del dataset real

Extraídos de `BODEGAS_Y_STOCK.xlsx` (corte entregado por Colsubsidio).
Los datos limpios están en `context/data/`. **Cada hallazgo trae su comando de verificación — si dudas, ejecútalo. No inventes cifras.**

Cifras base:
- **1.405 filas** de stock, **936 referencias únicas**, **8 bodegas con datos**
- **48 bodegas declaradas** en la hoja `BODEGAS DISPONIBLES`
- 4 unidades de medida: `Unidad` (864), `Kilogram` (430), `Liter` (89), `Portion` (22)

---

## P-01 · El 18% del inventario no tiene código

**252 de 1.405 filas** (17,9%) tienen el campo `Nr.Artículo` vacío. No son ítems raros: `AGUA WAIRA SABORIZADA` con 2.844 unidades, `AGUARDIENTE NECTAR CLUB`, `PLATO CUADRADO` con 400.

> **Implicación de diseño:** `sku` es NULLABLE en `count_event`. Un conteo sin código **no es un error de la app** — es el evento `MISSING_SKU`, que es la salida más valiosa del sistema. Si pones `NOT NULL` en el schema, borras el diferenciador.

```bash
awk -F, 'NR>1 && $2=="" {n++} END {print n" filas sin SKU"}' context/data/stock_corte.csv
```

---

## P-02 · No existe un solo cero, pero sí 79 negativos

**Ceros en todo el dataset: 0. Negativos: 79.** Los peores: `GASEOSA KOLA SOL 330 ML` en −9.120, `COLA Y POLA` en −7.434, `ARROZ` en −720 kilos.

Que no haya ni un cero no significa que todo tenga existencia. Significa que **el ERP nunca registra el cero**: cuando algo se acaba, la línea desaparece o queda negativa por consumos sin entrada.

> **Implicación de diseño:** esto es la prueba empírica de *saltar ≠ cero*. Al cerrar una ubicación, si el ERP esperaba un ítem que el operario no contó, hay que **preguntar explícitamente si es 0 real o si se saltó**. Sin eso, el descuadre es ruido. Y los negativos van a `STALE_SYSTEM_STOCK` — evidencia de que el sistema miente, no de que el operario contó mal.

```bash
awk -F, 'NR>1 && $5+0<0 {n++} END {print n" negativos"}' context/data/stock_corte.csv
awk -F, 'NR>1 && $5+0==0 {n++} END {print n+0" ceros"}' context/data/stock_corte.csv
```

---

## P-03 · La bodega reduce el espacio de búsqueda 16x

936 referencias únicas globales. Pero `STOCK KIOSCO PISCIGIROS AYB` solo maneja **56**, y `ZOOLOGICO` **55**.

El caso canónico: `AGUA OXIGENADA GALON` vive en zoológico. `AGUA BOTELLA`, `AGUA 280 ML`, `AGUA SABORIZADA H2O`, `AGUA WAIRA` viven en AYB. `AGUARDIENTE` × 4 en almacén AYB. `AGUACATE` en restaurante y zoológico. Buscar "agua" contra el catálogo global devuelve agua, aguardiente, aguacate y agujas desechables.

> **Implicación de diseño:** **podar el catálogo por bodega ANTES de tocar embeddings.** El mayor desambiguador es gratis y está en el dato. Nunca `LIKE '%agua%'` sobre el catálogo global.

```bash
awk -F, 'NR>1 {print $1}' context/data/catalogo.csv | sort | uniq -c | sort -n
grep -i "^\w*,\w*,AGU" context/data/catalogo.csv | head -20
```

---

## P-04 · Casi-duplicados: el resolver debe preguntar, no elegir

16 familias con prefijo compartido y SKUs distintos:

| | |
|---|---|
| `ABRELATAS MARIPOSA` | `ABRELATAS MARIPOSA FB` |
| `AJONJOLI` | `AJONJOLI NEGRO` |
| `ARROZ` | `ARROZ BASMATI` · `ARROZ DONA PEPA` |
| `MANZANA` | `MANZANA ROYAL` |
| `ACEITE` | `ACEITE DE OLIVA` · `ACEITE DE AJONJOLI` |

> **Implicación de diseño:** cuando dos candidatos empatan, el resolver **devuelve el atributo distintivo como pregunta** ("¿basmati o normal?"), no elige el top-1. Esa pregunta *es* la conversación que pide el reto. Emite `NAME_VARIANT` — candidato a merge del maestro.

```bash
cut -d, -f4 context/data/catalogo.csv | sort -u | grep -E "^(ARROZ|ACEITE|AJONJOLI|MANZANA)" 
```

---

## P-05 · Nombres sucios: 35 con espacio o NBSP inicial

`" CAZUELA 16 ONZ"`, `"\xa0BALDE PLASTICO 10 LTS"`, `" PLATO BLANCO CUADRADO"`. El `\xa0` es un non-breaking space, invisible al ojo y letal para un match exacto.

> **Implicación de diseño:** normalizar SIEMPRE antes de comparar — NFKD, quitar acentos, colapsar espacios, upper. `context/data/catalogo.csv` ya trae `nombre_norm` hecho; usa esa columna, no `nombre_raw`. `nombre_raw` se conserva para mostrarlo al operario tal cual lo ve en la estantería.

---

## P-06 · Unidades contables con decimales

16 filas con unidad `Unidad` tienen valor fraccionario: `HUEVOS DE GALLINA` 2.809,5 unidades. `PAN BAGUETT` 256,75. `AGUA BOTELLON` 109,0065.

Medio huevo no existe. Es consumo teórico descontado por receta contra un stock contable.

> **Implicación de diseño:** la validación de unidad no puede ser "si es Unidad debe ser entero" — el ERP mismo lo viola. Lo que sí debe hacer: si el **operario** captura un decimal en una unidad contable, preguntar. Y emitir `UNIT_MISMATCH` cuando la unidad dicha no coincide con la del maestro.

---

## P-07 · El 9-vs-90 tiene contexto estadístico

Mediana de stock: **12**. Percentil 75: **88**. Máximo: **41.500** (`BANDEJA EN EARTH PACT`).

La mitad del catálogo tiene menos de 12 unidades. Un 90 en un ítem cuya mediana histórica es 9 es una anomalía detectable; un 20.108 en `SALSA DE TOMATE SOBRE` es normal.

> **Implicación de diseño:** el umbral de anomalía es **por ítem y bodega**, nunca global. Con un solo corte no hay serie histórica: para el demo, la referencia es el stock del corte + el orden de magnitud, no un promedio móvil.

---

## P-08 · El maestro de bodegas ya está duplicado

48 bodegas declaradas, y el propio listado trae colisiones:

- `cafeteria acuario suministros` aparece **dos veces**
- `caf. Velas suministros` vs `caf.velas`
- `kiosco bosque suministros` vs `kiosco bosques`
- `movil fonda suministros` vs `movil fonda`
- `kiosco parqueadero piscilago` vs `kiosco pa**q**ueadero suministros piscilago` ← typo en el maestro

> **Implicación de diseño:** la bodega no se teclea ni se elige de una lista de texto libre. **Se escanea** (código de barras en la ubicación). Y el propio duplicado del maestro es un `MASTER_DATA_DUPLICATE` para el backlog.

```bash
cut -d, -f2 context/data/bodegas_declaradas.csv | sort | uniq -d
```

---

## P-09 · Escala: solo hay datos del 17% de las bodegas

8 hojas con stock, 48 bodegas declaradas.

> **Implicación de diseño:** lo que se demuestra en 8 bodegas tiene que escalar a 48+ sin cambio de arquitectura. Es el argumento de credibilidad ante el jurado: *"esto es una unidad de negocio; hay 48 bodegas solo en Piscilago"*.

---

## P-10 · Dos maestros fusionados

Los SKU de suministros son de 8 dígitos (`95026919`, `97503113`, `80031395`). Los de A&B son de 4-5 (`7290`, `5001`, `29018`). Son rangos de numeración distintos que conviven en el mismo archivo.

> **Implicación de diseño:** `sku` es **string**, no integer. No asumas formato, no valides longitud, no hagas aritmética con él.
