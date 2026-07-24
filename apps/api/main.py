"""FastAPI: routing y composición. Cero lógica de negocio (apps/api/CLAUDE.md).

Compone el bucle de voz de la ruta asistida:
  micrófono -> /v1/voz/transcribir (ElevenLabs STT) -> texto
  texto     -> /v1/resolver        (dominio resolucion)   -> candidatos/pregunta
  pregunta  -> /v1/voz/hablar       (ElevenLabs TTS)       -> audio al speaker

Invariante ADR-0001: ninguna respuesta contiene la cantidad del ERP. Los candidatos ya
vienen sin stock (Candidato no lo tiene), y solo se vocalizan mensajes seguros.
"""
from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from contexts.resolucion.use_cases.resolver_expresion import (
    ResolverExpresionCmd, resolver_expresion,
)
from plataforma.config import settings
from plataforma.voz import elevenlabs

app = FastAPI(title="Colsus Inventory — captura por voz")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "elevenlabs": settings.tiene_elevenlabs()}


@app.post("/v1/voz/transcribir")
async def transcribir(file: UploadFile = File(...)) -> dict:
    audio = await file.read()
    try:
        texto = elevenlabs.transcribir(audio, file.filename or "audio.webm")
    except Exception as exc:  # noqa: BLE001 - la API traduce el fallo del proveedor
        raise HTTPException(status_code=502, detail=f"STT: {exc}")
    return {"texto": texto}


class ResolverIn(BaseModel):
    bodega_id: str
    texto: str
    fuente: str = "manual"


@app.post("/v1/resolver")
def resolver(inp: ResolverIn) -> dict:
    r = resolver_expresion(ResolverExpresionCmd(inp.bodega_id, inp.fuente, inp.texto))
    return {
        "requiere_desambiguacion": r.requiere_desambiguacion,
        "pregunta": r.pregunta,
        "candidatos": [vars(c) for c in r.candidatos],  # Candidato nunca trae stock (ADR-0001)
    }


class HablarIn(BaseModel):
    texto: str


@app.post("/v1/voz/hablar")
def hablar(inp: HablarIn) -> Response:
    try:
        audio = elevenlabs.sintetizar(inp.texto)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"TTS: {exc}")
    return Response(content=audio, media_type="audio/mpeg")
