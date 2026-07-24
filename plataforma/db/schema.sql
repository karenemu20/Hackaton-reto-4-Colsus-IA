-- Modelo de datos. Ver ADR-0005 (append-only) y context/03-hallazgos.md.
CREATE EXTENSION IF NOT EXISTS vector;

-- ============ ESPEJO DEL ERP — READ ONLY, nunca escribimos aqui (ADR-0002) ============
CREATE TABLE bodega (
    bodega_id       TEXT PRIMARY KEY,
    nombre          TEXT NOT NULL,
    nombre_norm     TEXT NOT NULL
);

CREATE TABLE catalogo (
    bodega_id       TEXT NOT NULL REFERENCES bodega,
    sku             TEXT,              -- NULLABLE: 18% del maestro no tiene codigo (P-01)
    nombre_raw      TEXT NOT NULL,     -- como se ve en la estanteria
    nombre_norm     TEXT NOT NULL,     -- para comparar (P-05: NBSP y espacios sucios)
    unidad          TEXT NOT NULL,
    embedding       vector(384),
    PRIMARY KEY (bodega_id, nombre_norm)
);
CREATE INDEX ON catalogo (bodega_id);   -- la poda por bodega es 16x (P-03)

CREATE TABLE stock_corte (
    bodega_id       TEXT NOT NULL REFERENCES bodega,
    nombre_norm     TEXT NOT NULL,
    sku             TEXT,
    unidad          TEXT NOT NULL,
    cantidad        NUMERIC NOT NULL,  -- puede ser NEGATIVA (79 casos, P-02)
    fecha_corte     DATE NOT NULL,
    PRIMARY KEY (bodega_id, nombre_norm)
);
COMMENT ON TABLE stock_corte IS 'NUNCA se expone al operario. Conteo ciego, ADR-0001.';

-- ============ COLUMNA VERTEBRAL ============
CREATE TABLE conteo_sesion (
    session_id      UUID PRIMARY KEY,
    bodega_id       TEXT NOT NULL REFERENCES bodega,
    abierta_por     TEXT NOT NULL,
    estado          TEXT NOT NULL,      -- abierta | pausada | cerrada
    abierta_at      TIMESTAMPTZ NOT NULL,
    cerrada_at      TIMESTAMPTZ
);

CREATE TABLE count_event (
    event_id        UUID PRIMARY KEY,   -- generado en el DISPOSITIVO -> sync idempotente
    session_id      UUID NOT NULL REFERENCES conteo_sesion,
    ts              TIMESTAMPTZ NOT NULL,
    operator_id     TEXT NOT NULL,
    bodega_id       TEXT NOT NULL,
    ubicacion       TEXT,
    sku             TEXT,               -- NULL = evento MISSING_SKU, no es error
    utterance       TEXT,               -- EN CRUDO, siempre. No re-derivable
    nombre_resuelto TEXT,
    cantidad        NUMERIC NOT NULL,
    unidad          TEXT NOT NULL,
    packaging       TEXT,
    fuente          TEXT NOT NULL,      -- scan | manual | voz | foto
    confianza       REAL,
    override_motivo TEXT,
    device_id       TEXT NOT NULL,
    sync_state      TEXT NOT NULL DEFAULT 'local'
);
COMMENT ON TABLE count_event IS 'APPEND ONLY. Nunca UPDATE, nunca DELETE. Corregir = nuevo evento.';
CREATE INDEX ON count_event (session_id, ts);

CREATE TABLE data_quality_event (
    event_id        UUID PRIMARY KEY,
    origen_event_id UUID REFERENCES count_event,
    ts              TIMESTAMPTZ NOT NULL,
    tipo            TEXT NOT NULL,
    severidad       TEXT NOT NULL,
    bodega_id       TEXT NOT NULL,
    sku             TEXT,
    evidencia       JSONB NOT NULL DEFAULT '{}',
    accion_sugerida TEXT
);
CREATE INDEX ON data_quality_event (tipo, bodega_id);

-- ============ PROYECCIONES (derivadas, se pueden reconstruir del log) ============
-- INVARIANTE DE ESCRITURA: `count_event.nombre_resuelto` guarda SIEMPRE `nombre_norm`
-- (normalizado), NUNCA `nombre_raw`. Estas dos vistas unen por nombre_resuelto = nombre_norm.
-- Si el conteo guarda el raw, el JOIN falla y la reconciliacion devuelve NULL EN SILENCIO
-- (no da error, da un descuadre falso). Ver contexts/conteo/CLAUDE.md y domain/conteo_ctx.py.
CREATE VIEW cobertura AS
SELECT s.bodega_id, c.nombre_norm, c.sku,
       EXISTS (SELECT 1 FROM count_event e
               WHERE e.bodega_id = s.bodega_id AND e.nombre_resuelto = c.nombre_norm) AS contado
FROM catalogo c JOIN conteo_sesion s ON s.bodega_id = c.bodega_id;

CREATE VIEW reconciliacion AS
SELECT e.bodega_id, e.nombre_resuelto, e.unidad,
       SUM(e.cantidad) AS contado,
       sc.cantidad     AS erp_corte,
       SUM(e.cantidad) - sc.cantidad AS descuadre
FROM count_event e
LEFT JOIN stock_corte sc ON sc.bodega_id = e.bodega_id AND sc.nombre_norm = e.nombre_resuelto
GROUP BY e.bodega_id, e.nombre_resuelto, e.unidad, sc.cantidad;
