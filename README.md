# Universal Patch Orchestrator

Vendor-neutral enterprise patch orchestration platform.

## Hosted development stack
Nginx is the only application entry point. It proxies the React/Vite UI and FastAPI API. PostgreSQL is the authoritative control-plane store; Redis supports workers/coordination.

Services: **nginx · web · api · worker · postgres · redis**

## Run locally
1. Copy `.env.example` to `.env` and change the database password/credentials.
2. Run `docker compose up --build`.
3. Open `http://localhost:8080`.
4. API health is available at `http://localhost:8080/health`.

## Architecture
```
Browser -> Nginx -> React UI
              \--> FastAPI -> PostgreSQL
                       |
                       +--> Redis -> Worker
                       |
                       +--> Provider interface -> BigFix REST
                                             -> future providers
```

## Campaign strategies
Standard, Rolling/Batch, Canary/Ring, Tier Based, Cluster/DB and Hybrid.

## Security
Do not store BigFix or database credentials in source control. Production will add TLS termination, OIDC/SSO, RBAC, approval separation, immutable execution snapshots and audit trails.
