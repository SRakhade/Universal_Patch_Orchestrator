# Security baseline

- Never commit provider credentials.
- Secrets are injected from environment variables in development and a secrets manager in production.
- TLS verification defaults to enabled.
- SSO/OIDC and RBAC will protect the control plane.
- Production execution requires explicit authorization and supports separation of duties.
- Campaign definitions become immutable execution snapshots after approval.
- Every mutation and provider operation emits an audit event with actor and correlation ID.
- Provider accounts use least privilege.
- Logs must redact credentials, authorization headers and sensitive payload fields.
- API inputs are schema validated; provider XML generation must not concatenate untrusted input.
