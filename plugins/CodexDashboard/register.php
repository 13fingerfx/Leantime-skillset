<?php

use Leantime\Core\Events\EventDispatcher;
use Leantime\Domain\Plugins\Services\Registration;
use Leantime\Domain\Tickets\Events\TicketStatusUpdated;
use Leantime\Domain\Widgets\Models\Widget;
use Leantime\Plugins\CodexDashboard\Services\CodexDashboard;

$registration = app()->makeWith(Registration::class, ['pluginId' => 'CodexDashboard']);

$registration->registerLanguageFiles(['en-US']);

$registration->addMenuItem([
    'title' => 'codexdashboard.menu.title',
    'icon' => 'fa fa-gauge-high',
    'tooltip' => 'codexdashboard.menu.tooltip',
    'href' => '/CodexDashboard/settings',
], 'personal', [10]);

EventDispatcher::add_filter_listener('leantime.domain.widgets.services.widgets.__construct.availableWidgets', function (array $widgets): array {
    $widgets['codexdashboard_overview'] = app()->make(Widget::class, [
        'id' => 'codexdashboard_overview',
        'name' => 'codexdashboard.widget.title',
        'description' => 'codexdashboard.widget.description',
        'widgetUrl' => BASE_URL.'/CodexDashboard/widget',
        'gridHeight' => 14,
        'gridWidth' => 4,
        'gridMinHeight' => 8,
        'gridMinWidth' => 3,
        'gridX' => 8,
        'gridY' => 43,
        'widgetLoadingIndicator' => 'text',
        'widgetBackground' => 'default',
        'alwaysVisible' => false,
        'noTitle' => false,
        'fixed' => false,
    ]);

    return $widgets;
}, 20);

EventDispatcher::add_event_listener(TicketStatusUpdated::class, function (TicketStatusUpdated $event): void {
    app()->make(CodexDashboard::class)->handleTicketStatusUpdated($event);
});
