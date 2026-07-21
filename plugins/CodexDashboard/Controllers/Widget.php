<?php

namespace Leantime\Plugins\CodexDashboard\Controllers;

use Leantime\Core\Controller\Controller;
use Leantime\Plugins\CodexDashboard\Services\CodexDashboard;
use Symfony\Component\HttpFoundation\Response;

class Widget extends Controller
{
    private CodexDashboard $service;

    public function init(CodexDashboard $service): void
    {
        $this->service = $service;
    }

    public function get(): Response
    {
        $this->tpl->assign('summary', $this->service->getSummary((int) session('userdata.id')));
        $this->response = $this->tpl->display('codexdashboard::widget', 'blank');

        return $this->response;
    }
}
