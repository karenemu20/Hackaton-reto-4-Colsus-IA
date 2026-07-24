# 02 · Conteo ciego y anomalía (el 9-vs-90)

**Actores:** Operario · Dispositivo · Dominio de conteo · ERP (read-only).
**Invariante:** el operario NUNCA ve la cantidad del ERP (ADR-0001).

1. El **operario** cuenta y captura **90** unidades de `GASEOSA KOLA SOL 330 ML`.
2. El **dominio** compara contra el **stock del corte** — que existe, pero **nunca se muestra**.
   La mediana del catálogo es 12; 90 dispara la política `DetectarAnomaliaMagnitud` (P-07).
3. El **dispositivo** NO dice "el sistema esperaba 9". Dice: **"Ese número no coincide con lo
   que tenemos. ¿Cómo lo contaste?"** y ofrece **opciones sin revelar el valor**:
   - *"90 unidades sueltas"*
   - *"9 cajas × 10"* (el empaque, origen real del 9-vs-90)
   - *"Estoy seguro"* (override)
4a. El **operario** elige *"9 cajas × 10"* → se corrige el **empaque**, el conteo cuadra, listo.
4b. El **operario** toca *"Estoy seguro"* → el conteo **se acepta** (el override siempre gana),
    queda **auditado** con `operator_id`, y **dispara un segundo conteo** obligatorio
    (política `SegundoConteo`). El costo de mentir es recontar (H-03).
5. En ambos casos el **dominio** emite el evento de calidad `MAGNITUDE_ANOMALY` con su
   **evidencia** — backlog del MDM, verificable por el jurado.

**Por qué así:** mostrar el esperado destruye el dato — el operario ancla en el número y lo
confirma sin contar (ADR-0001). El mensaje jamás contiene la cantidad; por eso el sistema
**puede leerlo en voz alta** sin filtrarla (ver historia 04).

**Dónde vive:** `contexts/conteo/domain/policies/anomalia_magnitud.py` + `segundo_conteo.py`.
