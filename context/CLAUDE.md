# context/ — El origen del problema

**Esta carpeta es de solo lectura para agentes.** No la edites; es la evidencia.

## Cuándo leer qué

| Vas a... | Lee |
|---|---|
| empezar cualquier cosa | `00-reto.md` + `03-hallazgos.md` |
| tocar el resolver o embeddings | `03-hallazgos.md` P-03, P-04, P-05 |
| tocar el schema o el modelo de datos | `03-hallazgos.md` P-01, P-02, P-10 |
| tocar validaciones o anomalías | `03-hallazgos.md` P-06, P-07 |
| discutir alcance con alguien | `01-restricciones.md` |
| nombrar algo | `04-glosario.md` |

## Regla dura sobre los datos

`data/` son los CSV reales del corte de Colsubsidio. **Cuando necesites una cifra, consúltalos — no la recuerdes.**

```bash
python3 -c "import pandas as pd; d=pd.read_csv('context/data/stock_corte.csv'); print(d.describe())"
```

Nunca inventes un ejemplo de producto. Usa uno real: `ACHIOTE MOLIDO`, `AGUA WAIRA SABORIZADA`, `GASEOSA KOLA SOL 330 ML`, `CAZUELA 16 ONZ`.
