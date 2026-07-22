# API, JSON-RPC, And MCP Integration

Use this reference when a Leantime plugin or companion integration uses JSON-RPC, API keys, personal access tokens, browser-side API calls, or the Leantime MCP server.

## JSON-RPC

Leantime exposes a JSON-RPC API endpoint commonly documented as:

```text
/api/jsonrpc
```

Typical requests include:

- JSON body with `jsonrpc`, `method`, `params`, and `id`
- `x-api-key` header for API-key authentication
- methods under Leantime RPC namespaces

Do not assume browser JavaScript can call API methods as the logged-in user. Confirm the target version's auth behavior and prefer server-side calls or explicit token handling.

## Token Choice

Use personal access tokens when user-specific behavior matters, such as "my tasks." Use service API keys for service-account style operations where user identity is not required.

Never commit tokens, generated keys, or example real credentials.

## MCP

Leantime's MCP setup requires:

- Leantime 3.x or later self-hosted
- MCP Server plugin enabled in Leantime
- Node.js bridge such as `leantime-mcp`
- an MCP-compatible client

MCP-triggered mutations still need the automation safety model: idempotency, audit logs, dry-run for risky operations, and clear identity.

## Integration Guardrails

- Keep secrets in environment variables or Leantime settings, not source files.
- Validate API response shapes before mutating local state.
- Treat API/MCP calls as unreliable: timeout, retry, and partial failure paths matter.
- Log method names and object ids, not secrets.
- For UI-triggered API calls, confirm CSRF/auth expectations in the target version.
