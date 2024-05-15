<?php

namespace Statamic\Addons\SeoPro;

use Illuminate\Contracts\Http\Kernel;
use Statamic\Addons\SeoPro\Middleware\GenerateReport;
use Statamic\Extend\ServiceProvider;

class SeoProServiceProvider extends ServiceProvider
{
    public function boot()
    {
        if (version_compare(STATAMIC_VERSION, '2.10.0', '<')) {
            throw new \Exception('SEO Pro requires Statamic 2.10.0');
        }

        $this->addGlidePresets();
        $this->registerMiddleware();
    }

    protected function addGlidePresets()
    {
        $server = app(\League\Glide\Server::class);
        $server->setPresets($server->getPresets() + [
            'seo' => [
                'w' => $this->getConfig('open_graph_image_width'),
                'h' => $this->getConfig('open_graph_image_height'),
            ],
        ]);
    }

    protected function registerMiddleware()
    {
        $this->app[Kernel::class]->pushMiddleware(GenerateReport::class);
    }
}
