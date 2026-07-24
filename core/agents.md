# AGENTS.md

## Qué se implementó

Se creó el núcleo **/core** del brain con estos archivos:

- `core/brain.py`
- `core/memory.py`
- `core/reasoning.py`
- `core/decision.py`
- `core/action.py`
- `requirements.txt` (dependencias mínimas del brain)


---

## Por qué se implementó así

## 1) `core/memory.py`

### Qué hace
- Implementa `MemoryEngine` con Redis.
- `get_history(user_id)` carga historial por usuario.
- `save(user_id, user_msg, ai_msg)` guarda interacción y recorta a las últimas 10.

### Por qué
- El requisito pedía memoria corta con Redis.
- Limitar a 10 mensajes evita crecimiento infinito y mantiene contexto reciente útil para decisión.
- Se usó `decode_responses=True` para trabajar con `str` y simplificar serialización JSON.

---

## 2) `core/reasoning.py`

### Qué hace
- Define modelo Pydantic `Decision` con:
  - `action`
  - `params`
  - `confidence`
  - `reasoning`
- Implementa `ReasoningEngine` con:
  - `ChatOpenAI(model="gpt-4o", temperature=0)`
  - `PydanticOutputParser`
  - grafo LangGraph (`StateGraph`) con nodo de razonamiento.
- Método `think(canonical_json, history)` devuelve un `Decision`.

### Por qué
- El requisito exigía **LangGraph + ChatOpenAI**.
- El parser Pydantic fuerza estructura de salida robusta y reduce respuestas ambiguas.
- El prompt restringe explícitamente las acciones a tools disponibles para que el LLM no “invente” acciones.
- `temperature=0` mejora consistencia en decisiones operativas.

---

## 3) `core/decision.py`

### Qué hace
- Implementa `DecisionEngine`.
- Regla: si `confidence > 0.8`, aprueba la decisión del LLM.
- Si no, reemplaza acción por `pedir_ayuda`.

### Por qué
- Se separó la gobernanza de decisión del razonamiento del LLM.
- Esta capa permite control de riesgo simple y explícito.
- Cumple exactamente el requisito de fallback por umbral de confianza.

---

## 4) `core/action.py`

### Qué hace
- Implementa `ActionEngine` con `TOOL_REGISTRY` (dict).
- Registra:
  - `consultar_saldo(user_id: str) -> str`
  - `responder_texto(message: str) -> str`
- `execute(action_name, params)` resuelve y ejecuta la tool.
- Maneja `pedir_ayuda` como respuesta textual segura.

### Por qué
- El registro desacopla decisión de ejecución y facilita agregar nuevas tools sin cambiar el orquestador.
- Se incluyó manejo explícito de acción desconocida para evitar fallos silenciosos.
- `consultar_saldo` simula herramienta real (como pedía el MVP de cerebro).

---

## 5) `core/brain.py`

### Qué hace
- Define `CanonicalInput` para validar el JSON canónico de entrada.
- Configura `structlog` en JSON.
- Implementa clase `Brain` y método `run(canonical_json)` con flujo:
  1. Validar input (modelo canónico)
  2. Cargar memoria
  3. Razonar (LLM + LangGraph)
  4. Revisar decisión (umbral confianza)
  5. Ejecutar acción
  6. Guardar memoria
  7. Retornar output final:
     - `response`
     - `action_executed`
     - `confidence`
     - `thought`

### Por qué
- Centraliza orquestación y deja cada engine con responsabilidad única.
- Mantiene el orden exacto pedido: **Memory -> Reasoning -> Decision -> Action -> Save Memory**.
- El output coincide con el contrato solicitado para integrarse con el resto del sistema.

---

## Logging con `structlog`

Se agregaron eventos de log por etapa (`event=...`) para trazabilidad operativa:

- `perception_done` (en brain, al validar entrada canónica)
- `memory_loaded`
- `reasoning_done`
- `decision_done`
- `action_done`
- `memory_saved`
- `brain_done`

### Por qué
- Permite auditar qué decidió el brain, con qué confianza y qué acción ejecutó.
- Facilita debugging y observabilidad sin depender todavía de infraestructura externa.

---

## Dependencias elegidas (`requirements.txt`)

- `langchain`
- `langgraph`
- `langchain-openai`
- `redis`
- `pydantic`
- `structlog`

### Por qué
- Son exactamente las librerías requeridas para este brain.
- No se agregaron frameworks extra (como FastAPI) porque se pidió explícitamente “solo /core”.

---

## Resultado final

El brain ya recibe un JSON canónico, usa historial en Redis, decide acción con LLM (restringida por tools), aplica política de confianza y devuelve una respuesta estructurada lista para consumo por un API o agente superior.
