@extends($layout)

@section('content')
<x-global::pageheader :icon="'fa fa-gauge-high'">
    <h1>{{ __('codexdashboard.headline') }}</h1>
</x-global::pageheader>

<div class="maincontent">
    {!! $tpl->displayNotification() !!}

    <div class="maincontentinner">
        <p>{{ __('codexdashboard.intro') }}</p>

        <div class="row">
            <div class="col-md-4">
                <div class="projectBox">
                    <h4 class="widgettitle title-light"><i class="fa fa-list-check"></i> {{ __('codexdashboard.settings.status') }}</h4>
                    <p><strong>{{ __('codexdashboard.widget.overdue') }}:</strong> {{ $summary['overdue'] }}</p>
                    <p><strong>{{ __('codexdashboard.widget.due_today') }}:</strong> {{ $summary['dueToday'] }}</p>
                    <p><strong>{{ __('codexdashboard.widget.mine') }}:</strong> {{ $summary['assignedToMe'] }}</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="projectBox">
                    <h4 class="widgettitle title-light"><i class="fa fa-shield-halved"></i> {{ __('codexdashboard.settings.compatibility') }}</h4>
                    <p>Target Leantime version: {{ $summary['targetVersion'] }}</p>
                    <p>Routes, widget registration, language files, and ticket events are used through Leantime 3.9.8 extension points.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="projectBox">
                    <h4 class="widgettitle title-light"><i class="fa fa-rotate"></i> {{ __('codexdashboard.settings.automation') }}</h4>
                    <p>{{ __('codexdashboard.widget.dry_run') }}:
                        <strong>{{ $summary['dryRun'] ? __('codexdashboard.widget.enabled') : __('codexdashboard.widget.disabled') }}</strong>
                    </p>
                    <p>Status-change automation logs idempotency keys and does not mutate comments in v0.1.0.</p>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <div class="projectBox">
                    <h4 class="widgettitle title-light"><i class="fa fa-palette"></i> {{ __('codexdashboard.settings.native_ui') }}</h4>
                    <p>This page intentionally uses native Leantime wrappers, cards, icons, and theme classes with no custom CSS.</p>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
