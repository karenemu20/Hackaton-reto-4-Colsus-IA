# ADR-0013 — Stack congelado y alcance del hackathon

**Estado:** Aceptado (decisión del lead)

## Contexto
Aparecieron propuestas de stack ("Colsus Brain IA / AIOS Core") mezclando herramientas
alineadas con otras que hay que decidir. Con 5 personas y 48 horas, el riesgo no es el
código: es que cada quien meta una herramienta distinta y a la hora 6 haya cinco
arquitecturas. Hace falta congelar el stack, como se congeló `contracts/`.

## Decisión
El stack queda congelado en:

| Capa | Herramienta |
|---|---|
| Backend / orquestación | Python + FastAPI |
| Lógica de IA (ruta asistida) | LangGraph, solo en `contexts/resolucion` (ADR-0007) |
| Visión | YOLO + OCR, como adapter (ADR-0012) |
| Voz (STT) | ElevenLabs Scribe (ADR-0014) |
| Referencia + búsqueda semántica | Postgres + pgvector (espejo ERP read-only) |
| Escritura / realtime / auth | Firebase: Firestore + Firebase Auth (ADR-0015) |
| Frontend | React PWA, mobile-first — **un solo framework** |

**Alcance:** se construye **un** agente (inventario, Reto 4) de punta a punta. La narrativa
de "plataforma reutilizable que escala a Créditos/Salud" se **cuenta en el pitch señalando
los seams que ya existen** (la regla de aislamiento + `contracts/`, el ACL del ERP de
ADR-0002, visión/voz como adapters), **no se construye** como un "AIOS Core" genérico este
fin de semana.

## Regla de gobernanza
**Toda herramienta del stack apunta a un ADR, o se convierte en uno.** Un nombre en una
lista no es una decisión. Meter algo que contradice un ADR exige escribir el ADR que lo
reemplaza y convencer a las 5 personas. Esto protege contra "lo que me dio la IA".

## Consecuencias
- "El Cerebro que decide" es metáfora de pitch, no un componente. El invariante ADR-0007
  (el dominio decide, la IA interpreta) manda sobre el nombre comercial.
- Un solo framework de front y **una responsabilidad por store** (ADR-0015): sin dos
  frameworks corriendo, sin dos fuentes de verdad del mismo dato.

## Alternativa descartada
*Construir el AIOS Core genérico ahora*: un framework a medio hacer no es creíble ante el
jurado y se come las 48h. La reusabilidad se demuestra con los seams, no con un mega-módulo.
