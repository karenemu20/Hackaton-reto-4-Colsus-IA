# Diagrama de arquitectura — MVP hackathon (propuesta simplificada)

> Complementa `arquitectura-v1.md`. Este es el flujo recortado al alcance real de 3 días, con las decisiones de la fase de refinamiento ya aplicadas.

```mermaid
flowchart TD
    U[Usuario: equipo de costos] --> UI[App web mobile-first]
    UI -->|Hablar| V[Captura de voz]
    UI -->|Foto| F[Captura de foto/nota]
    UI -->|Escribir| T[Captura de texto]

    V --> STT[ElevenLabs STT]
    F --> OCR[OCR + LLM con visión]
    T --> N

    STT --> N[Normalizador: LLM salida estructurada + fuzzy match vs catálogo]
    OCR --> N

    CAT[(Catálogo y stock real - Supabase)] --> N
    CAT --> VAL

    N --> VAL[Validador: unidad válida + delta vs histórico]

    VAL -->|confianza alta, sin anomalía| SAVE[Guardar registro limpio]
    VAL -->|duda o anomalía| CONF[Pedir confirmación]
    CONF -->|ElevenLabs TTS: pregunta hablada| UI
    UI -->|usuario confirma o corrige| VAL

    SAVE --> DB[(Supabase: Postgres + Storage fotos/audio)]
    DB --> DASH[Dashboard: KPIs + tabla contado vs sistema]
```

## Diferencias vs. el diagrama de visión completa (`arquitectura-v1.md`)

| Visión completa | MVP hackathon |
|---|---|
| Detector de tipo genérico | Endpoint directo por botón (voz/foto/texto) |
| Orquestador de agentes (LangGraph) | Llamadas directas desde FastAPI |
| YOLO (detección de objetos entrenada) | OCR + LLM con visión |
| Digital Twin visual (mapa de bodega) | Tabla simple con badges Normal/Atención/Crítico |
| PWA offline-first | Conectividad asumida en el venue |
| Autenticación real | Usuario fijo para la demo |
| Postgres o Firebase | Postgres (Supabase) únicamente |
| Módulo decisor con LangChain | Reglas + llamada directa al LLM |
