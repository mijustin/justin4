<?php

namespace Statamic\Addons\SeoPro\Reporting\Rules\Concerns;

trait WarnsWhenPagesDontPass
{
    use FailsWhenPagesDontPass;

    public function siteStatus()
    {
        return $this->failures === 0 ? 'pass' : 'warning';
    }
}
