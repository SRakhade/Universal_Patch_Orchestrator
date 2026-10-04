# Universal Patch Orchestrator — Installation Guide

## 1. Architecture
The development deployment contains six services:

- **nginx** — single HTTP entry point and reverse proxy
- **web** — React/Vite user interface
- **api** — FastAPI control plane
- **worker** — asynchronous orchestration worker
- **postgres** — authoritative application/execution database
- **redis** — worker coordination and transient state

Only Nginx should be exposed to users. PostgreSQL, Redis and the API are internal services.

## 2. Prerequisites
Recommended development host:
- Linux VM (Ubuntu 24.04 LTS or equivalent)
- 4 vCPU minimum
- 8 GB RAM minimum
- 30 GB free disk minimum
- Docker Engine 27+
- Docker Compose v2
- Git
- Network connectivity from the host to the BigFix REST API

For production, size PostgreSQL storage and worker capacity based on endpoint count, campaign concurrency and audit retention.

## 3. Clone
```bash
git clone https://github.com/SRakhade/Universal_Patch_Orchestrator.git
cd Universal_Patch_Orchestrator
```

If testing the current development PR:
```bash
git checkout feat/hosted-app-foundation
```

## 4. Configure environment
```bash
cp .env.example .env
chmod 600 .env
```

Edit `.env`. At minimum, replace the example database password and configure the BigFix URL.

Example:
```env
UPO_ENVIRONMENT=development
UPO_DATABASE_URL=postgresql+asyncpg://upo:CHANGE_ME@postgres:5432/upo
UPO_REDIS_URL=redis://redis:6379/0
UPO_BIGFIX_BASE_URL=https://bigfix.example.internal:52311
UPO_BIGFIX_USERNAME=
UPO_BIGFIX_PASSWORD=
UPO_BIGFIX_VERIFY_TLS=true
```

Do not commit `.env`.

> The Compose database credentials and UPO_DATABASE_URL must match. A dedicated secrets mechanism will replace this development pattern for production.

## 5. Start
```bash
docker compose up --build -d
docker compose ps
```

The API container automatically runs `alembic upgrade head` before FastAPI starts.

Open:
- Application: `http://SERVER_IP:8080`
- Health endpoint: `http://SERVER_IP:8080/health`

## 6. Validate
```bash
curl http://localhost:8080/health
docker compose logs --tail=100 api
docker compose logs --tail=100 worker
```

Expected health response:
```json
{"status":"ok"}
```

Check database migrations:
```bash
docker compose exec api alembic current
```

## 7. Stop / restart
```bash
docker compose stop
docker compose start
```

To remove containers while retaining database volumes:
```bash
docker compose down
```

**Do not use `docker compose down -v` on a system containing data unless you intentionally want to delete PostgreSQL and Redis volumes.**

## 8. Upgrade
```bash
git pull
docker compose build
docker compose up -d
```

Database migrations run during API startup.

## 9. Backup
PostgreSQL is authoritative. Back it up before upgrades:
```bash
docker compose exec -T postgres pg_dump -U upo -Fc upo > upo-backup.dump
```

Restore procedures should be tested in a non-production environment.

## 10. Production hardening checklist
Do not expose the current development Compose stack directly to an untrusted network. Before production:

1. Terminate HTTPS/TLS at Nginx using an enterprise certificate.
2. Integrate OIDC/SSO and enforce RBAC.
3. Store database and BigFix credentials in an approved secrets manager.
4. Use a dedicated PostgreSQL credential with a strong password.
5. Restrict firewall rules: users -> Nginx; UPO -> BigFix; internal containers only for DB/Redis.
6. Keep `UPO_BIGFIX_VERIFY_TLS=true`; install the enterprise CA rather than disabling certificate validation.
7. Configure PostgreSQL backups, retention and restore testing.
8. Centralize logs and audit events.
9. Add monitoring/alerting for API, worker, PostgreSQL, Redis and disk usage.
10. Run vulnerability/image scanning and patch the UPO host itself.
11. Configure high availability before UPO becomes a critical production patching dependency.
12. Separate operator, approver and administrator permissions.

## 11. Troubleshooting
### UI does not load
```bash
docker compose logs nginx web
```

### API unhealthy
```bash
docker compose logs api
docker compose exec api alembic current
```

### PostgreSQL
```bash
docker compose exec postgres pg_isready -U upo -d upo
```

### Redis
```bash
docker compose exec redis redis-cli ping
```

### Worker
```bash
docker compose logs worker
docker compose exec redis redis-cli GET upo:worker:heartbeat
```

## 12. BigFix connectivity
Connectivity will be exposed through the Providers administration page. Until that milestone, verify that the UPO host can resolve and reach the configured BigFix REST endpoint. Never disable TLS verification merely to bypass an untrusted certificate; install the correct CA certificate instead.
