# apps/api/

FastAPI. **Routing, auth, serialización. Nada más.**

## Invariantes
- **Cero lógica de negocio.** Si un handler tiene un `if` sobre cantidades, unidades o reglas, está en el lugar equivocado.
- Un handler = validar entrada → llamar un caso de uso → serializar. Tres líneas.
- Nunca importar de `contexts/*/domain/`. Solo `use_cases/` y `contracts/`.
- Ninguna respuesta puede contener `stock_corte.cantidad`. Revísalo antes de commitear. (ADR-0001)
