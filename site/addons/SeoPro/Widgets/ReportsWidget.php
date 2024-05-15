<?php

namespace Statamic\Addons\SeoPro\Widgets;

use Statamic\Addons\SeoPro\Reporting\Report;
use Statamic\Extend\Widget;

class ReportsWidget extends Widget
{
    public function html()
    {
        return $this->view('widget', [
            'report' => Report::latest(),
        ]);
    }
}
