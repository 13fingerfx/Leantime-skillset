<div class="tw-flex tw-flex-col tw-gap-base">
    <div class="row">
        <div class="col-sm-4">
            <strong>{{ $summary['overdue'] }}</strong><br>
            <small>{{ __('codexdashboard.widget.overdue') }}</small>
        </div>
        <div class="col-sm-4">
            <strong>{{ $summary['dueToday'] }}</strong><br>
            <small>{{ __('codexdashboard.widget.due_today') }}</small>
        </div>
        <div class="col-sm-4">
            <strong>{{ $summary['assignedToMe'] }}</strong><br>
            <small>{{ __('codexdashboard.widget.mine') }}</small>
        </div>
    </div>

    <div>
        <i class="fa fa-shield-halved"></i>
        {{ __('codexdashboard.widget.dry_run') }}:
        <strong>{{ $summary['dryRun'] ? __('codexdashboard.widget.enabled') : __('codexdashboard.widget.disabled') }}</strong>
    </div>
</div>
