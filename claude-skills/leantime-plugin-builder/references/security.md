# Security

Use this reference for every plugin, even UI-only ones — templates that render external data and settings pages that persist input are still attack surface.

## Output Escaping

- Default to `{{ $value }}` in Blade. Only use `{!! $value !!}` for values you generate and trust (e.g. a fixed icon markup string), never for ticket titles, comments, usernames, webhook payloads, or any other user/external-controlled string.
- If a plugin must render trusted HTML fragments, keep the allowlist small and document why escaping is skipped at that specific line.

## Injection

- Never build SQL by string-concatenating request input. Use Leantime's query builder/PDO parameter binding.
- Never pass unsanitized request input to `shell_exec`, `exec`, `eval`, `include`/`require` with a dynamic path, or `unserialize`.
- Validate and type-cast route parameters and form input before using them in a query, file path, or external call.

## Secrets

- No API keys, tokens, passwords, or webhook secrets in source files, `composer.json`, `.env.example` with real values, or committed test fixtures.
- Read secrets from environment variables or Leantime's settings/service storage.
- Log method names, object ids, and outcomes — never log secrets or full tokens.

## Authentication And Authorization

- Every route that mutates state must run behind Leantime's normal auth/session middleware; do not add an unauthenticated route "just for now."
- Check the acting user has permission on the specific project/ticket/resource being mutated, not just that they are logged in.
- Webhook endpoints must verify a signature or shared secret before acting on the payload, and must not trust a `user_id`/`project_id` supplied only in the request body.

## Dependencies And Uploads

- Avoid adding new Composer/npm dependencies for something a couple dozen lines of plugin code can do; new dependencies are new supply-chain surface.
- If the plugin accepts file uploads, validate MIME type and size, and store outside any web-executable path if possible.

## Red Flags

- `{!! !!}` around anything that came from a ticket, comment, user profile, or external API response.
- A route handler with no auth check that accepts `POST`/`PATCH`/`DELETE`.
- A webhook controller that reads `request()->all()` and mutates records with no signature check.
- Hard-coded API keys or tokens anywhere in the diff.
- SQL assembled with `.` / string interpolation using request input.
