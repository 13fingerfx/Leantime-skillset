# Compatibility And Upgrade Safety

Use this reference before touching Leantime internals, routing, assets, event hooks, services, or APIs.

## Version First

Determine the target version before editing:

- `git describe --tags --always` in a source checkout
- release tag or image tag in deployment files
- Settings/About screen if the user is working from an installed instance
- user-provided target version when no checkout is available

If the version is unknown, write the plugin for the current checkout and say so.

## Extension Surface Ranking

Prefer in this order:

1. Documented plugin registration, event hooks, filters, controllers, views, language files, services, CLI, JSON-RPC, or MCP surfaces.
2. Patterns used by bundled or marketplace-style plugins in `app/Plugins`.
3. Stable domain services with clear public methods.
4. Internal classes, private conventions, or copied core code.

Levels 3 and 4 need explicit compatibility notes.

## Compatibility Notes

When using undocumented or internal Leantime surfaces, record:

- target Leantime version or commit
- file/class/function used
- why no safer extension point was used
- how to retest after upgrade

Put the note in the final answer and, for generated plugins, in a short plugin doc or comment near the coupling.

## Upgrade Tests

For non-trivial plugins, create or recommend checks that answer:

- Does `php ./bin/leantime plugin:list` still see the plugin?
- Does enabling/disabling the plugin work?
- Do registered menu items and routes still resolve?
- Do views render without missing layout/template errors?
- Do JSON-RPC or MCP calls still authenticate and return expected shapes?
- Do automation hooks still fire exactly once for the same event?

## Red Flags

- Importing from `app/Core` or deep `app/Domain` namespaces without checking docs/examples.
- Hard-coding route paths discovered from one version.
- Depending on asset build internals instead of existing plugin asset patterns.
- Using API calls from browser JavaScript without confirming current auth behavior.
- Treating a plugin that installs as proof that it is upgrade-safe.
