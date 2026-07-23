# Recursos oficiales del reto

Carpeta compartida por Colsubsidio: https://drive.google.com/drive/folders/1VdXHqaXAW6pXc9PszMdQln0DQMGnLX0O

## Contenido

1. **`Cómo usar los recursos del reto Hotelería.docx`** — explica el alcance del dataset: inventario de la unidad de negocio más grande de hotelería + el DIB. Cada registro tiene artículo, unidad de medida (unidades, kilogramos, litros) y cantidad disponible al corte — el mismo formato que el personal digita manualmente hoy.
2. **`BODEGAS Y STOCK.xlsx`** — dataset real de inventario. Guardarlo en `data/`.

## Hallazgos clave del dataset (usar como ground truth para pruebas)

- **48 bodegas** activas: almacén general, almacenes de A&B, restaurantes, kioscos, zoológico, etc.
- **1.405 referencias** distintas contadas en cada corte.
- **4 unidades de medida** en juego: Unidad, Kilogramo, Litro, Porción — aquí es donde vive el riesgo de ambigüedad (5 kg ≠ 5 g).
- **79 registros con stock negativo** ya existen en el sistema actual — evidencia real de los descuadres que el reto describe. Ejemplos:
  - ARROZ: -720 kg
  - GASEOSA KOLA SOL 330 ML: -9.120 unidades
  - COLA Y POLA: -7.434 unidades

Estos negativos son útiles como casos de prueba reales para el detector de anomalías (no hay que inventar ejemplos sintéticos).

## Cómo usarlos en el prototipo

- El catálogo (artículo + unidad + bodega) alimenta el fuzzy-matching de producto hablado → referencia canónica.
- La columna de cantidad (`SD`) sirve como línea base histórica para la regla de anomalías (comparar conteo nuevo vs. último valor conocido).
- Los 48 nombres de bodega dan el universo real de opciones para el selector de bodega en el flujo de captura.
