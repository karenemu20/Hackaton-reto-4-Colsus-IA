# 04 · Captura por voz — el operario habla, el sistema responde

**Actores:** Operario · Navegador (micrófono/speaker) · ElevenLabs (STT+TTS) · Resolver.
**Ruta asistida** (ADR-0007). La voz es **secundaria**: si falla, botones (ADR-0003).

1. El **operario** mantiene el botón grande y **dice** *"aguardiente néctar"* al **micrófono**.
2. El **navegador** graba el **audio** y lo sube (`/v1/voz/transcribir`).
3. **ElevenLabs Scribe** transcribe el **audio** a **texto**. El español de bodega es sucio:
   devuelve *"agardiente"* (ADR-0014, P-05).
4. El **resolver** poda por bodega (P-03), no encuentra el token exacto y **cae a la búsqueda
   semántica** (embeddings/pgvector; difflib en el esqueleto): recupera la familia
   **AGUARDIENTE** aunque el STT la escribió mal.
5. Hay varios (`PIONERO`, `ANTIOQUEÑO`, `NÉCTAR CLUB`): el **resolver** NO elige — devuelve la
   **pregunta** *"¿Cuál aguardiente?"* con el atributo distintivo (P-04).
6. El **sistema HABLA** la pregunta por el **speaker** (`/v1/voz/hablar`, ElevenLabs TTS) y
   muestra los candidatos como **botones grandes**.
7. El **operario** toca uno → queda el **producto**; ingresa la **cantidad** con `+/−`.
8. El comando converge en el mismo **`RegistrarConteoCmd`** que la ruta rápida y la foto:
   el dominio no se entera de que entró por voz.

**Por qué el sistema puede hablar sin romper el conteo ciego:** solo vocaliza `pregunta` y
`PolicyResult.message`, que por diseño **nunca contienen la cantidad del ERP** (ADR-0001).

**Dónde vive:** `apps/mobile/index.html` (mic/speaker) · `apps/api` (compone STT→resolver→TTS)
· `contexts/resolucion` (matcher + adapters) · `plataforma/voz` (ElevenLabs).
