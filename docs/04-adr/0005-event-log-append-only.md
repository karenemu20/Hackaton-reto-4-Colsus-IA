# ADR-0005 — El log de eventos es el registro de verdad

**Estado:** Aceptado
**Nota:** este ADR cubría originalmente también local-first. Esa parte se separó a **ADR-0010** para evitar la contradicción de alcance.
**Nota 2:** el log se implementa en **Firestore**, no en Postgres (ADR-0015). El invariante de este ADR —append-only, nunca update/delete— sigue intacto; solo cambió el motor de almacenamiento.

## Contexto
La opción natural es una tabla de conteos mutable: un renglón por ítem, `UPDATE` cuando se corrige.

## Decisión
El registro de verdad es la secuencia append-only de `count_event`. **Nunca `UPDATE`, nunca `DELETE`. Corregir = emitir otro evento.** `cobertura` y `reconciliacion` son proyecciones reconstruibles.

## Por qué — cuatro razones, todas del dominio real
1. **Relevo de turno**: el operario que entra hereda un log, no un estado.
2. **Override auditado**: el "estoy seguro" tiene que quedar registrado con motivo, no perderse en un UPDATE.
3. **Segundo conteo**: no sobrescribe al primero, lo acompaña. La comparación entre ambos *es* el dato.
4. **Sync**: un append-only sincroniza trivialmente; un UPDATE genera conflictos. (ver ADR-0010)

## Consecuencias
- `utterance` se guarda **en crudo siempre**, incluso cuando la resolución fue perfecta: no es re-derivable y es la única forma de auditar por qué falló el resolver.
- Auditoría completa gratis: quién contó qué, cuándo, por qué ruta, con qué confianza.
- Costo: toda lectura de "cantidad actual" es una agregación. Irrelevante a esta escala.
