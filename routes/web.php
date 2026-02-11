<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

// Route::statamic('example', 'example-view', [
//    'title' => 'Example'
// ]);

Route::statamic('feed', 'feeds.articles', [
    'layout' => 'feed',
    'content_type' => 'xml',
]);
Route::statamic('feed/atom', 'feeds.articles', [
    'layout' => 'feed',
    'content_type' => 'xml',
]);

Route::permanentRedirect('ladder', 'freedom');
Route::permanentRedirect('im-a-fcking-webmaster', 'webmaster');
Route::permanentRedirect('sideproject', 'bootstrap-side-project');
Route::permanentRedirect('business-lesson-go-where-the-people-are', 'customer-behavior');
Route::permanentRedirect('my-embarrassing-itunes-receipt', 'customer-journey-itunes');
Route::permanentRedirect('stop-networking', 'more-social');
Route::permanentRedirect('words', 'words.html');
Route::permanentRedirect('pull-the-market', 'beach');
Route::permanentRedirect('why-you-need-a-week-of-hustle', 'out-of-office');
Route::permanentRedirect('blog', 'articles');
