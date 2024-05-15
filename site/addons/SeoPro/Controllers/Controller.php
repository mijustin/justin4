<?php

namespace Statamic\Addons\SeoPro\Controllers;

use Statamic\CP\Publish\PreloadsSuggestions;
use Statamic\CP\Publish\ProcessesFields;

abstract class Controller extends \Statamic\Extend\Controller
{
    use PreloadsSuggestions;
    use ProcessesFields;
}
