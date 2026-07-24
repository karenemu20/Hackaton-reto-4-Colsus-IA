# Despliegue — Docker en un VPS (sin instalar nada local)

Todo corre en contenedores. En tu máquina solo necesitas Docker; no se instala Python,
FastAPI ni nada más. Un solo frente (Caddy) sirve la PWA y proxya la API, con **HTTPS
automático**.

## Local (prueba rápida)

```bash
cp .env.example .env          # pon ELEVENLABS_API_KEY; deja DOMAIN=localhost
docker compose up -d --build
# PWA:  https://localhost      (Caddy usa su CA interna; el micro funciona en localhost)
# API:  https://localhost/health
```

## VPS (demo real)

1. Apunta un dominio (o subdominio) al IP del VPS: un registro `A`, p. ej.
   `inventario.tudominio.com → <IP>`.
2. En el VPS: instala Docker, clona el repo, y:

```bash
cp .env.example .env
# edita .env:
#   ELEVENLABS_API_KEY=...          (tus créditos)
#   DOMAIN=inventario.tudominio.com
docker compose up -d --build
```

3. Abre `https://inventario.tudominio.com` en el **celular**. Caddy saca el certificado
   Let's Encrypt solo. Da permiso de micrófono y habla.

## ⚠️ El micrófono EXIGE HTTPS

`navigator.mediaDevices.getUserMedia` (el micrófono) **solo funciona en contexto seguro**:
`https://` o `http://localhost`. En un VPS con IP pelada (`http://12.34.56.78`) el navegador
**bloquea el micro sin avisar claro**. Por eso el `DOMAIN` + Caddy no es opcional para el
demo con voz: es la única forma de tener HTTPS rápido. (Nada de esto aplica a los botones y
el escaneo, que funcionan sin voz — ADR-0003.)

## Qué levanta cada servicio

| Servicio | Qué hace | Puerto |
|---|---|---|
| `caddy` | sirve la PWA (`apps/mobile`) y proxya `/v1/*` a la API. HTTPS automático | 80, 443 |
| `api` | FastAPI: STT/TTS (ElevenLabs) + resolver. Lee `context/data/*.csv` | interno 8000 |
| `db` *(opcional)* | Postgres + pgvector. **No hace falta para el demo de voz** | 5432 |

El `db` solo se necesita cuando se conecte la búsqueda semántica real (pgvector) y la
escritura. Arráncalo aparte: `docker compose --profile datos up -d`.

## Secretos
`ELEVENLABS_API_KEY` vive solo en `.env` (que **no** se sube: está en `.gitignore`). En
producción, mejor un gestor de secretos del VPS. La key nunca llega al navegador — el cliente
habla con nuestra API, y la API con ElevenLabs.

## Comprobación rápida
```bash
curl -k https://localhost/health      # {"ok":true,"elevenlabs":true}  si la key está puesta
docker compose logs -f api            # ver STT/TTS en vivo
```
