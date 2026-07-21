<?php

use Illuminate\Support\Facades\Route;
use Leantime\Plugins\CodexDashboard\Controllers\Settings;
use Leantime\Plugins\CodexDashboard\Controllers\Widget;

Route::get('/CodexDashboard/settings', [Settings::class, 'get'])->name('codexdashboard.settings');
Route::get('/CodexDashboard/widget', [Widget::class, 'get'])->name('codexdashboard.widget');
