<?php

namespace Statamic\Addons\SeoPro\Controllers;

use Statamic\API\Collection;
use Statamic\API\Taxonomy;

class SectionController extends Controller
{
    public function index()
    {
        return $this->view('sections', [
            'title' => $this->trans('messages.section_defaults'),
            'collections' => Collection::all(),
            'taxonomies' => Taxonomy::all(),
        ]);
    }
}
