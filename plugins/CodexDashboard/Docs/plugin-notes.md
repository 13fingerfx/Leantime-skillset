# CodexDashboard

## Compatibility

- Target Leantime version: 3.9.8.
- Documented/stable surfaces used:
  - `Leantime\Domain\Plugins\Services\Registration`
  - `Leantime\Core\Events\EventDispatcher`
  - `Leantime\Domain\Widgets\Models\Widget`
  - `Leantime\Domain\Tickets\Events\TicketStatusUpdated`
  - plugin `routes.php`
- Internal or version-sensitive surface used:
  - None intended for v0.1.0. Widget counts call the documented `Tickets::getAllOpenUserTickets()` service and ticket automation listens to the documented `TicketStatusUpdated` event class.
- Retest after upgrade:
  - `php ./bin/leantime plugin:list`
  - enable/disable `CodexDashboard`
  - `/CodexDashboard/settings`
  - `/CodexDashboard/widget`
  - My Dashboard widget manager shows `Codex Overview`
  - ticket status update emits only dry-run audit logs unless mutation is explicitly enabled

## Native UI Checks

- Nearby Leantime views inspected:
  - `app/Domain/Dashboard/Templates/home.blade.php`
  - `app/Domain/Widgets/Templates/partials/welcome.blade.php`
  - `app/Domain/Widgets/Templates/widgetManager.blade.php`
  - `app/Domain/Dashboard/Templates/show.blade.php`
- Existing patterns reused:
  - `x-global::pageheader`
  - `maincontent` / `maincontentinner`
  - `row` / `col-md-*`
  - `projectBox`
  - `widgettitle`
  - Font Awesome icon classes
  - translation keys for visible text
- Custom CSS: none.
- Mobile/contrast validation: templates use native Leantime classes and theme tokens; visual browser validation still required after installation.

## Automation Safety

- Trigger source: `TicketStatusUpdated`.
- Idempotency key: `ticket-status:{ticketId}:{status}`.
- Processed-event storage: intentionally not persisted in v0.1.0 because mutation is disabled by default.
- Lock/transaction scope: not applicable while dry-run only.
- Dry-run/audit behavior:
  - `CODEX_DASHBOARD_MUTATE` defaults to `false`.
  - listener logs the computed idempotency key and intended action through PHP `error_log`.
- Replay/retry/concurrency tests before enabling mutation:
  - same status event twice logs same idempotency key and creates no comments
  - concurrent status events create no comments
  - plugin disable/re-enable does not replay old mutations
  - if mutation is later enabled, add persistent processed-event storage before writing comments
