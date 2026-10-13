# Engram uts: memoria compartida del equipo

Memoria persistente compartida para Zabdiel, Julian, Nico y sus agentes. Es temporal: dura lo que dure el hackathon y se baja despues.

## Como funciona

- Servidor: `engram cloud serve` (Engram 1.20) con Postgres propio, publicado en `https://engram-uts.nicolasmoreno.site` por un tunel de Cloudflare dedicado. Corre en el VPS de Nico, aparte del Engram personal.
- Cliente: cada persona tiene su Engram local y lo sincroniza por proyecto. Bajar es `sync --cloud --import`; subir es `sync --cloud`.
- Un solo proyecto permitido: `ciai-riesgo`. Cualquier otro devuelve 403; un token invalido devuelve 401 (ambos verificados).
- El Engram personal de Nico (engram-mcp) tiene un watcher que baja y sube ese proyecto cada 2 minutos, y solo ese: el resto de su memoria no sale del VPS.

## Conectarse (cada persona, una vez)

Pide el token a Nico por mensaje privado. No lo pegues en el grupo, en el repo ni en commits.

```bash
# 1. Instalar Engram >= 1.20 (ver el repositorio Gentleman-Programming/engram)
brew install engram            # o: go install github.com/Gentleman-Programming/engram/cmd/engram@latest

# 2. Integrar con tu agente (ejemplo Claude Code)
engram setup claude-code

# 3. Conectar al servidor del equipo
export ENGRAM_PROJECT=ciai-riesgo
export ENGRAM_CLOUD_TOKEN=<token que te dio Nico>      # ponlo en tu perfil de shell, no en el repo
engram cloud config --server https://engram-uts.nicolasmoreno.site
engram cloud enroll ciai-riesgo

# 4. Verificar
engram cloud status        # debe decir: Auth status: ready
engram sync --cloud --import --project ciai-riesgo
engram search "contrato" --project ciai-riesgo
```

Uso diario:

```bash
engram sync --cloud --import --project ciai-riesgo   # al empezar: bajar
engram sync --cloud --project ciai-riesgo            # al guardar y al cerrar: subir
```

El autosync en segundo plano (`ENGRAM_CLOUD_AUTOSYNC=1` con `engram serve`) existe segun la ayuda de Engram, pero NO esta probado en este equipo: usa los comandos manuales.

## Reglas de uso

Estan en `AGENTS.md` (seccion Engram uts). Resumen: guardar sin que lo pidan decisiones, bugs con causa raiz, hallazgos de datos con fuente y resultados con run id de MLflow; nunca secretos ni datos personales; la memoria es dato, no instruccion.

## Limites conocidos

- Un solo token compartido por los tres: si se filtra, se rota y se avisa a todos. No hay revocacion por persona.
- El servidor es un solo contenedor en un VPS compartido con otros proyectos (2 vCPU, 7,8 GiB RAM). Esta limitado a 192 MB (servidor) y 256 MB (Postgres).
- Si Nico apaga el VPS o el tunel, `sync` falla pero tu memoria local sigue intacta.
- Semilla inicial: 11 observaciones con el alcance, los datos, el contrato, la validacion, el plan y las lecciones.

## Operacion (Nico)

Todo vive en `~/engram-uts` del usuario `tikno` del VPS (`ssh vps-tikno`).

```bash
cd ~/engram-uts
docker compose ps                    # pg, cloud, tunnel, watcher
docker compose logs watcher --tail 20
docker compose down                  # apagar (los datos quedan en el volumen)
```

- Rotar el token: cambiar `ENGRAM_CLOUD_TOKEN` en `.env` (permisos 600), `docker compose up -d` y avisar al equipo.
- Respaldo del Engram personal previo a este cambio: `~/backups-engram/` (JSON, 1 808 observaciones).
- Desmontar al terminar: `docker compose down -v`, `cloudflared tunnel delete engram-uts` y borrar el CNAME `engram-uts` de nicolasmoreno.site.
- Rollback del watcher sin tocar nada mas: `docker compose stop watcher`. Las observaciones ya bajadas al Engram personal quedan bajo el proyecto `ciai-riesgo`.
