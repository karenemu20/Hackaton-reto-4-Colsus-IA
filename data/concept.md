### Usar Docker para poderlo mover y usar en cualquier dispositivo
* Descargar e instala **Docker Desktop** desde su sitio web oficial.
* Revisar que esté corriendo en segundo plano (verás una ballena verde).

### Crear y arrancar la base de datos
Usar PowerShell u otra terminal, y ejecutar:

```bash
docker run --name mi-postgres-mvp -e POSTGRES_PASSWORD=mi_clave_secreta -p 5432:5432 -d postgres
```

**¿Qué hace este comando?**
* `--name mi-postgres-mvp`: Nombra tu contenedor.
* `-e POSTGRES_PASSWORD=...`: Define la contraseña maestra.
* `-p 5432:5432`: Conecta el puerto con tu computadora.
* `-d postgres`: Arranca Postgres en segundo plano.

### Conectarte visualmente con pgAdmin
* Descarga e instala **pgAdmin 4** desde su página oficial.
* Abre la aplicación.
* Haz clic derecho en **Servers** > **Register** > **Server...**
* En la pestaña **General**, escribe un nombre (ej. `MVP Local`).
* En la pestaña **Connection**, llena estos campos:

| Campo | Valor |
| :--- | :--- |
| **Host name/address** | `localhost` |
| **Port** | `5432` |
| **Maintenance database** | `postgres` |
| **Username** | `postgres` |
| **Password** | `mi_clave_secreta` |

