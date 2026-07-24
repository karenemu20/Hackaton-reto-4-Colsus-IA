# ADR-0008 — PolicyResult con acciones requeridas, no booleano

**Estado:** Aceptado

## Contexto
Las "reglas" del sistema son de dos especies que se estaban mezclando:
- **Validan**: `ValidarCantidad`, `ValidarUnidad`, `ValidarUbicacion`.
- **Cambian la conversación**: `RequierePhoto`, `SegundoConteo`, `AprobacionSupervisor`, `ConfirmarEmpaque`.

Las segundas no devuelven válido/inválido: devuelven *algo que el frontend tiene que hacer*.

## Decisión
```python
PolicyResult = {ok, policy, severity, message, required_actions[], evidence}
```
LangGraph y la UI solo **ejecutan** las `required_actions` que devuelve el dominio.

## Consecuencias
- Agregar `ValidarTemperatura` mañana no toca el grafo, ni FastAPI, ni el frontend.
- `evidence` alimenta directo el evento de calidad de dato.
- `message` nunca puede contener la cantidad del ERP (ADR-0001).

## Por qué no un Rules Engine
Con 48 horas y ~6 políticas, un motor de reglas es infraestructura que no se amortiza. Specification + Policy simples, evaluadas por el agregado. El punto de extensión que importa es el **tipo de retorno**, no el motor.

> Si `PolicyResult` fuera `bool`, la segunda especie de regla no cabe y la lógica termina infiltrándose en el grafo. Ese es el fallo que este ADR previene.
