# Universal Patch Orchestrator (UPO)

Vendor-neutral enterprise patch orchestration platform for Standard, Rolling/Batch, Canary/Ring, Tier Based, Cluster/Database and Hybrid patching.

## Architecture

```
Users
  |
HTTPS / HTTP
  |
Nginx
  |-------------------|
React UI           FastAPI
                      |
              PostgreSQL + Redis
                      |
                    Worker
                      |
              Provider Interface
                      |
                    BigFix
                      |
               Future Providers
```

## Quick Installation

### 1. Prerequisites

Install:
- Git
- Docker Engine 27+
- Docker Compose v2

Recommended development host: Linux VM, 4 vCPU, 8 GB RAM, 30 GB free disk.

Verify:

```bash
git --version
docker --version
docker compose version
```

### 2. Clone the repository

```bash
git clone https://github.com/SRakhade/Universal_Patch_Orchestrator.git
cd Universal_Patch_Orchestrator
```

The hosted application is currently being developed in:

```bash
git checkout feat/hosted-app-foundation
```

### 3. Create the environment file

```bash
cp .env.example .env
chmod 600 .env
```

Edit it:

```bash
nano .env
```

Example:

```env
UPO_ENVIRONMENT=development
UPO_DATABASE_URL=postgresql+asyncpg://upo:changeme@postgres:5432/upo
UPO_REDIS_URL=redis://redis:6379/0

UPO_BIGFIX_BASE_URL=https://bigfix.example.internal:52311
UPO_BIGFIX_USERNAME=
UPO_BIGFIX_PASSWORD=
UPO_BIGFIX_VERIFY_TLS=true
```

Do not commit `.env` or real credentials.

### 4. Build and start UPO

```bash
docker compose up --build -d
```

Check services:

```bash
docker compose ps
```

Expected services:

```
nginx
web
api
worker
postgres
redis
```

The API container automatically runs the Alembic database migrations before starting FastAPI.

### 5. Open UPO

From the UPO server:

```
http://localhost:8080
```

From another machine:

```
http://<UPO-SERVER-IP>:8080
```

API health:

```bash
curl http://localhost:8080/health
```

Expected:

```json
{"status":"ok"}
```

### 6. Check logs

All services:

```bash
docker compose logs -f
```

API:

```bash
docker compose logs -f api
```

Worker:

```bash
docker compose logs -f worker
```

Nginx:

```bash
docker compose logs -f nginx
```

### 7. Verify PostgreSQL

```bash
docker compose exec postgres pg_isready -U upo -d upo
```

Check database migration:

```bash
docker compose exec api alembic current
```

### 8. Verify Redis / Worker

```bash
docker compose exec redis redis-cli ping
```

Expected:

```
PONG
```

Worker heartbeat:

```bash
docker compose exec redis redis-cli GET upo:worker:heartbeat
```

### 9. Stop / Start

Stop without deleting data:

```bash
docker compose stop
```

Start again:

```bash
docker compose start
```

Restart:

```bash
docker compose restart
```

Remove containers while retaining persistent volumes:

```bash
docker compose down
```

> Do not run `docker compose down -v` unless you intentionally want to delete persistent PostgreSQL and Redis volumes.

## Upgrade UPO

```bash
git pull
docker compose build
docker compose up -d
docker compose ps
```

Database migrations execute during API startup.

## PostgreSQL Backup

```bash
docker compose exec -T postgres pg_dump -U upo -Fc upo > upo-backup.dump
```

## Rebuild a service

API:

```bash
docker compose build api
docker compose up -d api
```

Web UI:

```bash
docker compose build web
docker compose up -d web
```

## Troubleshooting

Check container state:

```bash
docker compose ps
```

API failure:

```bash
docker compose logs --tail=200 api
```

UI failure:

```bash
docker compose logs --tail=200 web nginx
```

PostgreSQL failure:

```bash
docker compose logs --tail=200 postgres
docker compose exec postgres pg_isready -U upo -d upo
```

Redis failure:

```bash
docker compose logs --tail=200 redis
docker compose exec redis redis-cli ping
```

## Production Warning

The current stack is a development foundation. Before production use, configure HTTPS/TLS, enterprise SSO/OIDC, RBAC, an approved secrets manager, firewall restrictions, database backups, centralized logging/monitoring and high availability. Keep BigFix TLS verification enabled.

## Documentation

- `docs/INSTALLATION.md` — detailed installation, operations and production-hardening guide
- `docs/architecture.md` — architecture decisions
- `docs/security.md` — security baseline
- `docs/TOPOLOGY.md` — application/server classification and topology model

## Reporting and action status

UPO is designed to track patching after deployment, not only trigger it. Provider action IDs are persisted and reconciled through provider APIs. BigFix is the first implementation; endpoint results will be normalized into common UPO states for campaign reporting, compliance, failures, reboot-pending and execution history.

The same provider contract is intentionally retained for future patch-management integrations. See `docs/REPORTING.md`.

## Development status

Current focus: hosted control plane, topology-aware campaign creation and BigFix provider integration.
