<?php

namespace Statamic\Addons\SeoPro\Controllers;

use Illuminate\Http\Request;
use Statamic\Addons\SeoPro\Settings;
use Statamic\Addons\SeoPro\TranslatesFieldsets;
use Statamic\API\Fieldset;
use Statamic\API\File;
use Statamic\API\YAML;

class DefaultsController extends Controller
{
    use TranslatesFieldsets;

    public function edit()
    {
        $fieldset = $this->fieldset();

        $data = $this->preProcessWithBlankFields(
            $fieldset,
            Settings::load()->get('defaults')
        );

        return $this->view('edit', [
            'title' => 'Site Defaults',
            'data' => $data,
            'fieldset' => $fieldset->toPublishArray(),
            'suggestions' => $this->getSuggestions($fieldset),
            'submitUrl' => route('seopro.defaults.update'),
        ]);
    }

    public function update(Request $request)
    {
        $data = $this->processFields($this->fieldset(), $request->fields);

        Settings::load()->put('defaults', $data)->save();

        return ['success' => true, 'message' => trans('cp.saved_success')];
    }

    protected function fieldset()
    {
        $contents = File::get($this->getDirectory().'/resources/fieldsets/defaults.yaml');
        $fieldset = Fieldset::create('defaults', YAML::parse($contents));

        return $this->translateFieldset($fieldset);
    }
}
