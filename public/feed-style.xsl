<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:content="http://purl.org/rss/1.0/modules/content/">

  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> — RSS Feed</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
        <link href="https://fonts.googleapis.com/css?family=Roboto+Mono:400,400i,700,700i|Shadows+Into+Light" rel="stylesheet"/>
        <style type="text/css">
          *, *::before, *::after {
            box-sizing: border-box;
          }

          body {
            margin: 0;
            padding: 0;
            background-color: #fff;
            color: #1a1b1c;
            font-family: 'Roboto Mono', monospace;
            font-size: 14px;
            line-height: 1.6;
          }

          /* Zine header bar */
          .zine-header {
            background-color: #1a1b1c;
            height: 2.5rem;
            width: 50%;
            clip-path: polygon(0 0, 100% 0, 0 60%, 0 0);
          }

          /* Zine footer bar */
          .zine-footer {
            background-color: #1a1b1c;
            height: 2.5rem;
            width: 66.66667%;
            clip-path: polygon(100% 100%, 100% 4%, 0 100%, 0 100%);
            margin-left: auto;
          }

          .container {
            max-width: 680px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
          }

          /* RSS explainer banner */
          .banner {
            background-color: #1a1b1c;
            color: #fff;
            padding: 16px 24px;
            margin-bottom: 2rem;
            clip-path: polygon(95% 0, 100% 8%, 100% 100%, 0 100%, 0 0);
            font-size: 13px;
          }

          .banner a {
            color: #ff0;
            font-weight: 700;
          }

          .banner a:hover {
            background-image: linear-gradient(180deg, rgba(0,0,0,0) 10%, #ff0 0);
            color: #1a1b1c;
          }

          .banner strong {
            color: #ff0;
          }

          /* Feed title */
          h1 {
            font-size: 32px;
            text-transform: uppercase;
            font-weight: 700;
            line-height: 1.25;
            margin: 0 0 0.5em 0;
          }

          @media (min-width: 768px) {
            h1 {
              font-size: 48px;
            }
          }

          .feed-description {
            font-family: 'Shadows Into Light', cursive;
            font-size: 24px;
            color: #00f;
            transform: rotate(-2deg);
            padding: 16px 0;
            margin-bottom: 1em;
          }

          .back-link {
            display: inline-block;
            margin-bottom: 2rem;
            font-weight: 700;
            color: #00f;
            text-decoration: none;
            background-image: linear-gradient(180deg, rgba(0,0,0,0) 70%, #fff5c4 0);
            background-position: 4px bottom;
            background-repeat: no-repeat;
          }

          .back-link:hover {
            background-image: linear-gradient(180deg, rgba(0,0,0,0) 10%, #ff0 0);
          }

          h2 {
            font-size: 24px;
            text-transform: uppercase;
            font-weight: 700;
            line-height: 1.25;
            margin: 0 0 1em 0;
            letter-spacing: 0.05em;
          }

          /* Article list */
          .items {
            list-style: none;
            padding: 0;
            margin: 0;
          }

          .items li {
            border-bottom: 2px solid #1a1b1c;
            padding: 1.25em 0;
          }

          .items li:last-child {
            border-bottom: none;
          }

          .item-title {
            font-size: 18px;
            font-weight: 700;
            margin: 0 0 0.25em 0;
            line-height: 1.3;
          }

          .item-title a {
            color: #00f;
            text-decoration: none;
            background-image: linear-gradient(180deg, rgba(0,0,0,0) 70%, #fff5c4 0);
            background-position: 4px bottom;
            background-repeat: no-repeat;
          }

          .item-title a:hover {
            background-image: linear-gradient(180deg, rgba(0,0,0,0) 10%, #ff0 0);
          }

          .item-date {
            font-size: 12px;
            color: #73808c;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.5em;
          }

          .item-description {
            color: #73808c;
            font-size: 13px;
            margin: 0;
          }

          /* Footer area */
          .footer-note {
            text-align: center;
            color: #73808c;
            font-size: 12px;
            padding: 1rem 0;
            font-family: 'Shadows Into Light', cursive;
            text-transform: uppercase;
          }
        </style>
      </head>
      <body>
        <div class="zine-header"></div>

        <div class="container">
          <div class="banner">
            <strong>This is a web feed,</strong> also known as an RSS feed. You can <strong>subscribe</strong> by copying the URL from the address bar into your newsreader. Visit <a href="https://aboutfeeds.com">About Feeds</a> to get started. It's free!
          </div>

          <h1>
            <xsl:value-of select="/rss/channel/title"/>
          </h1>

          <div class="feed-description">
            <xsl:value-of select="/rss/channel/description"/>
          </div>

          <a class="back-link" target="_blank">
            <xsl:attribute name="href">
              <xsl:value-of select="/rss/channel/link"/>
            </xsl:attribute>
            &#x2190; Visit justinjackson.ca
          </a>

          <h2>Recent Articles</h2>

          <ul class="items">
            <xsl:for-each select="/rss/channel/item">
              <li>
                <h3 class="item-title">
                  <a target="_blank">
                    <xsl:attribute name="href">
                      <xsl:value-of select="link"/>
                    </xsl:attribute>
                    <xsl:value-of select="title"/>
                  </a>
                </h3>
                <div class="item-date">
                  <xsl:value-of select="pubDate"/>
                </div>
                <xsl:if test="description != ''">
                  <p class="item-description">
                    <xsl:value-of select="description"/>
                  </p>
                </xsl:if>
              </li>
            </xsl:for-each>
          </ul>
        </div>

        <div class="footer-note">
          Powered by Statamic
        </div>

        <div class="zine-footer"></div>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
