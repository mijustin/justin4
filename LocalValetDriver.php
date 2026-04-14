<?php

/**
 * Local Valet driver for justinjackson.ca
 *
 * Extends the standard Laravel driver to also serve index.html files from
 * static subdirectories in /public (e.g. /tweets/, /jfdi/, /words.html, etc.)
 * without routing them through the Laravel front controller.
 */
class LocalValetDriver extends \Valet\Drivers\LaravelValetDriver
{
    /**
     * Determine if the incoming request is for a static file.
     * Handles both direct static files and directories containing index.html.
     */
    public function isStaticFile(string $sitePath, string $siteName, string $uri)
    {
        $publicPath = $sitePath . '/public';

        // Check for a direct static file (parent handles .html, .jpg, .css, etc.)
        $filePath = $publicPath . $uri;
        if (file_exists($filePath) && is_file($filePath)) {
            return $filePath;
        }

        // Check for index.html inside a static subdirectory
        $indexHtml = rtrim($filePath, '/') . '/index.html';
        if (file_exists($indexHtml) && is_file($indexHtml)) {
            return $indexHtml;
        }

        // Fall back to parent (handles /storage/ paths, etc.)
        return parent::isStaticFile($sitePath, $siteName, $uri);
    }
}
