<?php

namespace Leantime\Plugins\CodexDashboard\Services;

use Leantime\Domain\Tickets\Events\TicketStatusUpdated;
use Leantime\Domain\Tickets\Services\Tickets;

class CodexDashboard
{
    private const MUTATE_COMMENTS = false;

    private Tickets $tickets;

    public function __construct(Tickets $tickets)
    {
        $this->tickets = $tickets;
    }

    public function install(): bool
    {
        return true;
    }

    public function uninstall(): bool
    {
        return true;
    }

    public function enable(): bool
    {
        return true;
    }

    public function disable(): bool
    {
        return true;
    }

    public function getSummary(int $userId): array
    {
        $openTickets = $this->tickets->getAllOpenUserTickets($userId);
        $today = date('Y-m-d');

        $overdue = 0;
        $dueToday = 0;

        foreach ($openTickets as $ticket) {
            $due = (string) ($ticket['dateToFinish'] ?? '');
            if ($due === '' || str_starts_with($due, '0000-00-00')) {
                continue;
            }

            $dueDate = substr($due, 0, 10);
            if ($dueDate < $today) {
                $overdue++;
            } elseif ($dueDate === $today) {
                $dueToday++;
            }
        }

        return [
            'overdue' => $overdue,
            'dueToday' => $dueToday,
            'assignedToMe' => count($openTickets),
            'dryRun' => self::MUTATE_COMMENTS === false,
            'targetVersion' => '3.9.8',
        ];
    }

    public function handleTicketStatusUpdated(TicketStatusUpdated $event): void
    {
        $idempotencyKey = sprintf('ticket-status:%d:%s', $event->ticketId, (string) $event->status);

        error_log('[CodexDashboard] dry-run ticket status automation: '.$idempotencyKey);

        if (self::MUTATE_COMMENTS === false) {
            return;
        }

        // Mutating comments deliberately stays disabled until persistent processed-event storage,
        // locking, and replay/concurrency tests have been added inside the target Leantime instance.
    }

}
