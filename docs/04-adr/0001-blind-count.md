# ADR-0001 — Conteo ciego

**Estado:** Aceptado

## Contexto
Mostrar al operario lo que el sistema espera parece útil ("valida más rápido"), pero destruye el valor del conteo: el operario ancla en el número mostrado y lo confirma sin contar. El descuadre desaparece de los datos sin haber desaparecido de la bodega.

## Decisión
La cantidad del ERP **nunca** se muestra al operario. Ni antes, ni durante, ni como sugerencia, ni como placeholder, ni en un tooltip.

Cuando hay discrepancia, se ofrecen **opciones sin revelar el valor**: "¿90 unidades sueltas o 9 cajas de 10?", "Estoy seguro".

## Consecuencias
- `stock_corte` se usa solo dentro del dominio para evaluar políticas. Nunca cruza a la respuesta HTTP.
- `PolicyResult.message` no puede contener la cantidad esperada — revisar en cada política nueva.
- La verificación es mecánica: ninguna respuesta de `apps/api` puede contener `stock_corte.cantidad`.

## Alternativa descartada
*Mostrar el esperado en modo "supervisor"*: el rol se presta y el anclaje vuelve.
