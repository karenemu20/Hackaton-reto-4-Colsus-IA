"""Registro de fuentes de la ruta asistida. AGREGAR UNA FUENTE = 1 adapter + 1 linea.

La historia completa de este archivo es la prueba de ADR-0012/0014: cada fuente que se
sumo (foto, voz-nube) fue un adapter nuevo + una linea aqui. El grafo, el dominio,
`contracts/` y el schema NUNCA cambiaron.

  voz    -> ElevenLabs Scribe (STT en la nube). ADR-0014, con creditos de la hackaton.
  manual -> texto tecleado, pasa directo al matcher.
  foto   -> vision (OCR + YOLO). ADR-0012.

(ADR-0012 dibujaba '1 rama en nodes.py: if fuente == FOTO'. Con este registry ni esa rama
hace falta: el nodo queda ciego a la fuente. Mejora sobre el ADR; ratificarla con el equipo.)
"""
from __future__ import annotations
from contracts.events import Fuente
from .base import Resolver
from .expresion import ExpresionResolver
from .vision import VisionResolver
from ._vision_yolo_stub import DetectorStub            # <- swap por YOLO + OCR real
from .voz_elevenlabs import VozElevenLabsResolver
from ._voz_elevenlabs_stub import ElevenLabsStubSTT    # <- swap por la API real de ElevenLabs

RESOLVERS: dict[str, Resolver] = {
    Fuente.VOZ.value: VozElevenLabsResolver(ElevenLabsStubSTT()),  # ADR-0014
    Fuente.MANUAL.value: ExpresionResolver(Fuente.MANUAL.value),   # texto tecleado
    Fuente.FOTO.value: VisionResolver(DetectorStub()),             # ADR-0012
}
