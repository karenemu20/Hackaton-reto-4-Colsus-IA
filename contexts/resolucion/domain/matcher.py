"""El nucleo de resolucion: poda por bodega + match en capas + empate.

CLAVE ARQUITECTONICA: este archivo recibe TEXTO y no sabe de que fuente vino. Voz (STT de
ElevenLabs), texto tecleado y OCR de una foto entran aqui como un string. De este punto en
adelante la fuente es irrelevante -> por eso agregar voz o vision no lo toca (ADR-0012/0014).

Estrategia en CAPAS (todas DESPUES de podar por bodega, P-03):
  1. token exacto   -> el operario dijo el nombre tal cual. Rapido, sin costo.
  2. fuzzy/semantico -> el STT o el tecleo trajo un error ('agardiente' por 'aguardiente').
                        En este esqueleto es difflib (stdlib). EN PRODUCCION es pgvector:
                        embeddings del nombre, busqueda por similitud coseno sobre el catalogo
                        YA PODADO por bodega. El seam es este mismo punto (ver _semantico()).
  3. empate (P-04)  -> si quedan 2+ candidatos parejos, NO elegir: devolver la pregunta.
"""
from __future__ import annotations
import csv
import pathlib
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher

from contracts.dtos import Candidato, ResolucionResult

DATA = pathlib.Path(__file__).resolve().parents[3] / "context" / "data"
TOP_K = 3
_MARGEN_EMPATE = 0.15    # 2do candidato a <15% del 1ro -> empate -> preguntar (P-04)
_UMBRAL_SEMANTICO = 0.78  # similitud minima para aceptar un match difuso (proxy de coseno)


def norm(s: str) -> str:
    """NFKD, sin acentos, espacios colapsados, upper. Igual que plataforma/erp/seed.py (P-05)."""
    s = unicodedata.normalize("NFKD", str(s)).replace("\xa0", " ")
    s = s.encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().upper()


def _tokens(s: str) -> list[str]:
    return [t for t in norm(s).split(" ") if t]


@dataclass(frozen=True)
class _Ref:
    sku: str | None
    nombre_raw: str
    nombre_norm: str
    unidad: str


_CACHE: dict[str, list[_Ref]] = {}


def _catalogo_de(bodega_id: str) -> list[_Ref]:
    """PODA POR BODEGA, antes de cualquier match. Reduccion hasta 16x (P-03, ADR-0004):
    936 refs globales -> 56 en un kiosco. Gratis, sin un token de LLM. En produccion la
    busqueda pgvector tambien filtra `WHERE bodega_id = %s` ANTES de comparar embeddings."""
    if bodega_id not in _CACHE:
        with open(DATA / "catalogo.csv", encoding="utf-8") as f:
            _CACHE[bodega_id] = [
                _Ref(r["sku"] or None, r["nombre_raw"], r["nombre_norm"], r["unidad"])
                for r in csv.DictReader(f) if r["bodega_id"] == bodega_id
            ]
    return _CACHE[bodega_id]


def _distintivo(ref: _Ref, q: set[str]) -> str | None:
    return " ".join(t for t in _tokens(ref.nombre_norm) if t not in q).lower() or None


def _por_token(refs: list[_Ref], q: set[str]) -> list[tuple[float, _Ref, str | None]]:
    """Capa 1. Match por TOKEN, no por substring: 'agua' pega con el token AGUA, NUNCA con
    AGUARDIENTE ni AGUACATE. Es el 'nunca LIKE %agua%' de P-03, hecho regla."""
    out = []
    for r in refs:
        comunes = q & set(_tokens(r.nombre_norm))
        if comunes:
            out.append((len(comunes) / len(q), r, _distintivo(r, q)))
    return out


def _semantico(refs: list[_Ref], q: set[str]) -> list[tuple[float, _Ref, str | None]]:
    """Capa 2. Cuando el token exacto no pega (typo del STT, variante), caemos a similitud.
    SEAM DE PRODUCCION: reemplazar este difflib por pgvector — embeddings del `nombre_norm`,
    coseno sobre el catalogo YA PODADO. La firma y el retorno NO cambian: el resto del sistema
    no se entera de si la similitud vino de difflib o de un vector de 384 dimensiones."""
    out = []
    for r in refs:
        rt = _tokens(r.nombre_norm)
        best = max((SequenceMatcher(None, a, b).ratio() for a in q for b in rt), default=0.0)
        if best >= _UMBRAL_SEMANTICO:
            out.append((round(best, 2), r, _distintivo(r, q)))
    return out


def resolver(bodega_id: str, expresion: str) -> ResolucionResult:
    refs = _catalogo_de(bodega_id)
    q = set(_tokens(expresion))
    if not q:
        return ResolucionResult(candidatos=[], requiere_desambiguacion=False)

    puntuados = _por_token(refs, q) or _semantico(refs, q)   # capa 1, si falla capa 2
    puntuados.sort(key=lambda x: x[0], reverse=True)
    top = puntuados[:TOP_K]
    if not top:
        return ResolucionResult(candidatos=[], requiere_desambiguacion=False)

    candidatos = [
        Candidato(sku=r.sku, nombre=r.nombre_raw, unidad_esperada=r.unidad,
                  confianza=round(score, 2), atributo_distintivo=dist)
        for score, r, dist in top
    ]

    # Empate (P-04): 2+ candidatos parejos -> NO elegir el top-1. Devolver la pregunta con el
    # atributo distintivo. Esa pregunta ES la conversacion que pide el reto.
    hay_empate = len(top) >= 2 and (top[0][0] - top[1][0]) < _MARGEN_EMPATE
    if hay_empate:
        cabeza = norm(candidatos[0].nombre).split(" ")[0].lower()
        return ResolucionResult(candidatos=candidatos, requiere_desambiguacion=True,
                                pregunta=f"¿Cuál {cabeza}?")
    return ResolucionResult(candidatos=candidatos, requiere_desambiguacion=False)
