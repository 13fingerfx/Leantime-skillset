# Leantime Plugin Development

Use this reference when creating, modifying, validating, installing, or packaging Leantime plugins.

## Minimum Structure

Leantime custom plugins normally live under:

```text
app/Plugins/PluginName/
├── composer.json
├── register.php
├── bootstrap.php
├── routes.php
├── Controllers/
├── Templates/
├── Language/
└── Services/
```

`composer.json` must identify the package as a Leantime plugin:

```json
{
  "name": "vendor/pluginname",
  "description": "Plugin description",
  "version": "1.0.0",
  "type": "leantime-plugin",
  "autoload": {
    "psr-4": {
      "Leantime\\Plugins\\PluginName\\": "/"
    }
  }
}
```

Keep the folder name, namespace segment, and PSR-4 prefix aligned.

## Registration

Use `register.php` for early plugin registration: language files, menu entries, middleware, events, and common extension points. Typical plugin docs show the registration helper being created with the plugin id and then registering language files and menu items.

Common checks:

- `register.php` exists and returns no accidental output.
- Language files are registered before translation keys are used.
- Menu labels and tooltips use translation keys, not raw UI text.
- Menu URLs match controller/action naming.

## Routing

A controller with no matching route is a plugin that installs but silently does nothing — this is one of the most common failures. Register every controller action Leantime should expose in `routes.php`:

```php
<?php

use Illuminate\Support\Facades\Route;
use Leantime\Plugins\PluginName\Controllers\Show;

Route::get('/PluginName/show', [Show::class, 'get'])->name('pluginname.show');
```

- Every menu `href` added in `register.php` needs a matching route.
- Every controller action meant to be reachable over HTTP needs a matching route.
- Routes that mutate state should use `POST`/`PATCH`/`DELETE` and go through Leantime's normal auth/CSRF middleware — do not add unauthenticated `GET` routes that change data.

## Controllers And Templates

Leantime uses an MVC/front-controller pattern. Plugin controllers should live in `Controllers/`, extend the appropriate Leantime base controller when needed, and render Blade views under `Templates/`. In Leantime 3.9.x, plugin template namespaces are registered from `app/Plugins/PluginName/Templates` as `pluginname::...`.

Native view conventions matter:

- Use the app layout provided by Leantime.
- Use translation helpers for visible strings.
- Use existing wrappers such as page headers and main content containers when present in the target version.
- Avoid introducing a new mini design system inside a plugin.

## Installation

Manual installation usually means copying the extracted plugin folder into `app/Plugins/PluginName/`, fixing ownership/permissions if needed, then enabling it in Settings > Plugins or with the Leantime CLI.

Useful CLI commands in a Leantime checkout:

```bash
php ./bin/leantime plugin:list
php ./bin/leantime plugin:enable --plugin=PluginName
php ./bin/leantime plugin:disable --plugin=PluginName
php ./bin/leantime cron:run
```

## Packaging

The package should zip the plugin folder itself, not the whole Leantime app. After unzipping, the path should look like:

```text
app/Plugins/PluginName/composer.json
```

Run the validator before packaging and after installation.

## Common Failures

- Folder name and namespace do not match.
- `composer.json` omits `"type": "leantime-plugin"`.
- Templates render from a namespace/path that does not match the plugin name.
- UI strings are hard-coded instead of translated.
- Menu item or controller action has no matching entry in `routes.php`.
- Plugin calls internal Leantime services without a compatibility note.
- Plugin installs but does nothing because it was copied to the wrong directory level.
