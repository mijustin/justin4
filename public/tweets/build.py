#!/usr/local/bin/python3.13
"""
Build script for justinjackson.ca/tweets/ static archive.
Run from the project root or from public/tweets/:
    python3 public/tweets/build.py

Re-running is safe: media files that already exist are skipped.
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from html import escape
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
ARCHIVE_DIR = Path(
    "/Users/jj/Documents/"
    "twitter-2024-11-13-c0ac9b4e18d6bcd6eaae0918b6a112c9c892415d7c38b9d2d5a7154c042582d5"
)
OUTPUT_DIR      = Path(__file__).parent.resolve()   # /public/tweets/
TWEETS_PER_PAGE = 100
SITE_URL        = "https://justinjackson.ca"
AVATAR_SRC      = Path(__file__).parent / "avatar-source.jpg"  # copy your preferred photo here
TWEETS_MEDIA    = ARCHIVE_DIR / "data" / "tweets_media"


# ── Data loading ───────────────────────────────────────────────────────────────
def strip_js_wrapper(text: str) -> str:
    """Remove window.YTD.tweets.partN = prefix so we get raw JSON."""
    return re.sub(r"^window\.YTD\.tweets\.part\d+\s*=\s*", "", text.strip())


def load_tweets_file(path: Path) -> list:
    print(f"  Loading {path.name} ({path.stat().st_size // 1_000_000} MB)…", flush=True)
    raw = path.read_text(encoding="utf-8")
    return json.loads(strip_js_wrapper(raw))


def load_all_tweets() -> list:
    print("Loading tweet data…", flush=True)
    part0 = load_tweets_file(ARCHIVE_DIR / "data" / "tweets.js")
    part1 = load_tweets_file(ARCHIVE_DIR / "data" / "tweets-part1.js")

    seen = {}
    for item in part0 + part1:
        t = item["tweet"]
        seen[t["id"]] = t

    tweets = list(seen.values())
    tweets.sort(key=lambda t: parse_dt(t["created_at"]), reverse=True)
    print(f"  {len(tweets):,} unique tweets loaded, sorted newest-first.", flush=True)
    return tweets


# ── Date helpers ───────────────────────────────────────────────────────────────
def parse_dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")


def fmt_date_display(date_str: str) -> str:
    dt = parse_dt(date_str)
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def fmt_date_iso(date_str: str) -> str:
    dt = parse_dt(date_str)
    return dt.strftime("%Y-%m-%dT%H:%M")


# ── Tweet classification ────────────────────────────────────────────────────────
def classify(t: dict) -> str:
    if t["full_text"].startswith("RT @"):
        return "retweet"
    if t.get("in_reply_to_status_id_str"):
        return "reply"
    return "tweet"


# ── Text formatting ─────────────────────────────────────────────────────────────
URL_PATTERN     = re.compile(r'(https?://[^\s<>"]+)')
MENTION_PATTERN = re.compile(r'@(\w+)')
HASHTAG_PATTERN = re.compile(r'#(\w+)')


def plain_text(t: dict) -> str:
    """Clean tweet text for use in <title> / <meta description> — no HTML tags."""
    text = t["full_text"]
    entities = t.get("entities", {})

    try:
        ranges = t.get("display_text_range", ["0", str(len(text))])
        text = text[int(ranges[0]) : int(ranges[1])]
    except (ValueError, IndexError):
        pass

    for u in entities.get("urls", []):
        text = text.replace(u["url"], u.get("expanded_url", u["url"]))

    for m in entities.get("media", []):
        text = text.replace(m["url"], "")

    return text.strip()


def format_text(t: dict) -> str:
    text = t["full_text"]
    entities = t.get("entities", {})

    # Trim to display range (strips leading @mention in replies, trailing media URL)
    try:
        ranges = t.get("display_text_range", ["0", str(len(text))])
        text = text[int(ranges[0]) : int(ranges[1])]
    except (ValueError, IndexError):
        pass

    # Replace t.co → expanded URL
    for u in entities.get("urls", []):
        text = text.replace(u["url"], u.get("expanded_url", u["url"]))

    # Remove inline media t.co links (we show the image/video directly)
    for m in entities.get("media", []):
        text = text.replace(m["url"], "")

    text = text.strip()

    # Escape only the characters that are dangerous in HTML element content.
    # Do NOT escape single quotes — html.escape() converts ' to &#x27;, and
    # the hashtag regex then matches #x27 inside that entity, breaking the text.
    # Single quotes are safe unescaped inside element content (only attributes need it).
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Linkify — runs after escaping so we don't accidentally escape injected tags
    text = URL_PATTERN.sub(r'<a href="\1" rel="noopener noreferrer">\1</a>', text)
    text = MENTION_PATTERN.sub(
        r'<a href="https://twitter.com/\1" rel="noopener noreferrer">@\1</a>', text
    )
    text = HASHTAG_PATTERN.sub(
        r'<a href="https://twitter.com/hashtag/\1" rel="noopener noreferrer">#\1</a>', text
    )
    text = text.replace("\n", "<br>")
    return text


# ── Media rendering ─────────────────────────────────────────────────────────────
def media_html(t: dict) -> str:
    entities = t.get("extended_entities") or t.get("entities", {})
    items = entities.get("media", [])
    if not items:
        return ""

    parts = []
    for m in items:
        raw_url = m.get("media_url_https") or m.get("media_url", "")
        original = raw_url.split("/")[-1]
        local = f"/tweets/media/{t['id']}-{original}"

        if m["type"] == "photo":
            parts.append(
                f'<img src="{local}" alt="" loading="lazy" class="tw-media-img">'
            )
        else:  # video / animated_gif
            parts.append(
                f'<div class="tw-video-wrap">'
                f'<img src="{local}" alt="" loading="lazy" class="tw-media-img">'
                f'<span class="tw-play-btn" aria-label="Video">&#9654;</span>'
                f'</div>'
            )

    n = min(len(parts), 4)
    return f'<div class="tw-media tw-media-{n}">{"".join(parts)}</div>'


# ── Tweet card ─────────────────────────────────────────────────────────────────
def tweet_card(t: dict) -> str:
    tid        = t["id"]
    kind       = classify(t)
    text       = format_text(t)
    imgs       = media_html(t)
    date_disp  = fmt_date_display(t["created_at"])
    date_iso   = fmt_date_iso(t["created_at"])
    rt_count   = t.get("retweet_count", "0")
    like_count = t.get("favorite_count", "0")
    has_media  = "1" if t.get("entities", {}).get("media") or \
                       t.get("extended_entities", {}).get("media") else "0"

    badge = ""
    if kind == "retweet":
        badge = '<span class="tw-badge tw-rt">RT</span>'
    elif kind == "reply":
        reply_to = t.get("in_reply_to_screen_name", "")
        badge = (
            f'<span class="tw-reply-ctx">'
            f'Replying to <a href="https://twitter.com/{reply_to}" '
            f'rel="noopener noreferrer">@{reply_to}</a>'
            f'</span>'
            if reply_to else ""
        )

    return f"""\
<article class="tw-card" data-type="{kind}" data-media="{has_media}">
  <div class="tw-card-head">
    <img src="/tweets/avatar.jpg" alt="Justin Jackson" class="tw-avatar">
    <div class="tw-identity">
      <span class="tw-name">Justin Jackson</span><span class="tw-handle">@mijustin</span>
    </div>
    <a href="/tweets/{tid}/" class="tw-date"><time datetime="{date_iso}">{date_disp}</time></a>
  </div>
  {badge}
  <div class="tw-body">{text}</div>
  {imgs}
  <div class="tw-stats">
    <span class="tw-stat" title="Retweets">&#10227; {rt_count}</span>
    <span class="tw-stat" title="Likes">&#9825; {like_count}</span>
  </div>
</article>"""


# ── Page shell ─────────────────────────────────────────────────────────────────
def page_head(title: str, canonical: str = "", description: str = "") -> str:
    esc_title = escape(title)
    esc_desc  = escape(description)
    canon_tag = f'<link rel="canonical" href="{SITE_URL}{canonical}">' if canonical else ""
    desc_tag  = f'<meta name="description" content="{esc_desc}">' if description else ""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc_title}</title>
  {desc_tag}
  {canon_tag}
  <meta property="og:title" content="{esc_title}">
  <link rel="stylesheet" href="/tweets/tweets.css">
</head>"""


SUFFIX = " – Justin Jackson (@mijustin)"


# ── Individual tweet page ──────────────────────────────────────────────────────
def render_tweet_page(t: dict, all_ids: set) -> str:
    tid   = t["id"]
    plain = plain_text(t).replace("\n", " ")
    title = (plain[:80] + "…") if len(plain) > 80 else plain

    head = page_head(
        title=title + SUFFIX,
        canonical=f"/tweets/{tid}/",
        description=plain[:200],
    )
    card = tweet_card(t)

    # Parent tweet link for replies
    parent_link = ""
    parent_id = t.get("in_reply_to_status_id_str")
    if parent_id:
        if parent_id in all_ids:
            parent_link = f'<a href="/tweets/{parent_id}/">&#8593; View parent tweet</a>'
        else:
            parent_link = (
                f'<a href="https://twitter.com/i/web/status/{parent_id}" '
                f'rel="noopener noreferrer" target="_blank">&#8593; View parent tweet ↗</a>'
            )

    nav_links = '<a href="/tweets/">&#8592; All tweets</a>'
    if parent_link:
        nav_links += f'<span class="tw-nav-sep">·</span>{parent_link}'

    return f"""\
{head}
<body class="tw-single">
  <div class="tw-wrap">
    <nav class="tw-back">{nav_links}</nav>
    {card}
  </div>
</body>
</html>"""


# ── Index / paginated page ─────────────────────────────────────────────────────
def render_index_page(
    page_tweets: list,
    page_num: int,
    total_pages: int,
    total_count: int,
    view: str = "all",   # "all" or "top"
) -> str:
    cards     = "\n".join(tweet_card(t) for t in page_tweets)
    total_fmt = f"{total_count:,}"

    base      = "/tweets/top/" if view == "top" else "/tweets/"
    base_page = f"{base}page/" if view == "top" else "/tweets/page/"

    if page_num == 1:
        canonical = base
    else:
        canonical = f"{base_page}{page_num}/"

    prev_link = ""
    next_link = ""
    if page_num > 1:
        prev_url  = base if page_num == 2 else f"{base_page}{page_num - 1}/"
        prev_link = f'<a href="{prev_url}" class="tw-pager">&#8592; Prev</a>'
    if page_num < total_pages:
        next_link = f'<a href="{base_page}{page_num + 1}/" class="tw-pager">Next &#8594;</a>'

    title_suffix = " – Top tweets" if view == "top" else ""
    head = page_head(
        title=f"Tweets{title_suffix}{SUFFIX}",
        canonical=canonical,
        description="Justin Jackson's most-liked tweets, ranked by likes." if view == "top"
                    else "Justin Jackson's full tweet archive – searchable and browsable.",
    )

    tab_all      = 'class="tw-tab tw-tab-view"'
    tab_top      = 'class="tw-tab tw-tab-view"'
    tab_tweets   = 'class="tw-tab"'
    tab_replies  = 'class="tw-tab"'
    tab_retweets = 'class="tw-tab"'

    if view == "top":
        tab_top = 'class="tw-tab tw-tab-view active"'
    else:
        tab_all = 'class="tw-tab tw-tab-view active"'

    return f"""\
{head}
<body class="tw-index">
  <div class="tw-wrap">

    <header class="tw-header">
      <h1>Tweets</h1>
      <div class="tw-search-wrap">
        <input type="search" id="tw-search"
               placeholder="Search {total_fmt} tweets…"
               autocomplete="off" spellcheck="false">
      </div>
    </header>

    <div class="tw-layout">
      <main class="tw-main">

        <nav class="tw-tabs" aria-label="Filter">
          <a href="/tweets/top/" {tab_top}>Top</a>
          <a href="/tweets/" {tab_all}>All</a>
          <button {tab_tweets} data-filter="tweet">Tweets</button>
          <button {tab_replies} data-filter="reply">Replies</button>
          <button {tab_retweets} data-filter="retweet">Retweets</button>
        </nav>

        <div id="tw-search-results" class="tw-search-results" hidden></div>

        <div id="tw-list">
{cards}
        </div>

        <nav class="tw-pagination">
          {prev_link}
          <span class="tw-page-info">Page {page_num} of {total_pages:,}</span>
          {next_link}
        </nav>
      </main>

      <aside class="tw-sidebar">
        <div class="tw-filter-group">
          <strong>Show</strong>
          <label><input type="radio" name="show" value="all" checked> All Tweets</label>
          <label><input type="radio" name="show" value="media"> Media only</label>
          <label><input type="radio" name="show" value="text"> Text only</label>
        </div>
      </aside>
    </div>

  </div>
  <script src="/tweets/tweets.js"></script>
</body>
</html>"""


# ── Search index ───────────────────────────────────────────────────────────────
def build_search_index(tweets: list) -> list:
    index = []
    for t in tweets:
        text = plain_text(t)
        index.append([
            t["id"],
            text[:200],
            fmt_date_display(t["created_at"]),
            classify(t),
            1 if (t.get("entities", {}).get("media") or
                  t.get("extended_entities", {}).get("media")) else 0,
        ])
    return index


# ── Media copy ─────────────────────────────────────────────────────────────────
def copy_media(output_media: Path) -> None:
    print("Copying media files…", flush=True)
    output_media.mkdir(parents=True, exist_ok=True)
    copied = skipped = 0
    for src in TWEETS_MEDIA.iterdir():
        dst = output_media / src.name
        if dst.exists():
            skipped += 1
        else:
            shutil.copy2(src, dst)
            copied += 1
    print(f"  {copied:,} copied, {skipped:,} already present.", flush=True)


# ── Main ────────────────────────────────────────────────────────────────────────
def main() -> None:
    tweets       = load_all_tweets()
    total        = len(tweets)
    total_pages  = (total + TWEETS_PER_PAGE - 1) // TWEETS_PER_PAGE
    output_media = OUTPUT_DIR / "media"

    # Avatar
    print("Copying avatar…", flush=True)
    shutil.copy2(AVATAR_SRC, OUTPUT_DIR / "avatar.jpg")

    # Media
    copy_media(output_media)

    # Build ID set for parent tweet lookups
    all_ids = {t["id"] for t in tweets}

    # Individual tweet pages
    print(f"Generating {total:,} individual tweet pages…", flush=True)
    for i, t in enumerate(tweets, 1):
        out_dir = OUTPUT_DIR / t["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(render_tweet_page(t, all_ids), encoding="utf-8")
        if i % 5_000 == 0:
            print(f"  {i:,}/{total:,}…", flush=True)
    print("  Done.", flush=True)

    # Paginated index pages (chronological)
    print(f"Generating {total_pages:,} index pages…", flush=True)
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * TWEETS_PER_PAGE
        chunk = tweets[start : start + TWEETS_PER_PAGE]
        html  = render_index_page(chunk, page_num, total_pages, total, view="all")

        if page_num == 1:
            (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")
        else:
            page_dir = OUTPUT_DIR / "page" / str(page_num)
            page_dir.mkdir(parents=True, exist_ok=True)
            (page_dir / "index.html").write_text(html, encoding="utf-8")

        if page_num % 100 == 0:
            print(f"  Page {page_num:,}/{total_pages:,}…", flush=True)
    print("  Done.", flush=True)

    # Top pages (sorted by likes descending)
    top_tweets = sorted(tweets, key=lambda t: int(t.get("favorite_count", 0)), reverse=True)
    top_pages  = (total + TWEETS_PER_PAGE - 1) // TWEETS_PER_PAGE
    print(f"Generating {top_pages:,} Top pages…", flush=True)
    for page_num in range(1, top_pages + 1):
        start = (page_num - 1) * TWEETS_PER_PAGE
        chunk = top_tweets[start : start + TWEETS_PER_PAGE]
        html  = render_index_page(chunk, page_num, top_pages, total, view="top")

        if page_num == 1:
            top_dir = OUTPUT_DIR / "top"
            top_dir.mkdir(parents=True, exist_ok=True)
            (top_dir / "index.html").write_text(html, encoding="utf-8")
        else:
            page_dir = OUTPUT_DIR / "top" / "page" / str(page_num)
            page_dir.mkdir(parents=True, exist_ok=True)
            (page_dir / "index.html").write_text(html, encoding="utf-8")

        if page_num % 100 == 0:
            print(f"  Page {page_num:,}/{top_pages:,}…", flush=True)
    print("  Done.", flush=True)

    # Search index
    print("Building search index…", flush=True)
    index = build_search_index(tweets)
    (OUTPUT_DIR / "search-index.json").write_text(
        json.dumps(index, separators=(",", ":")),
        encoding="utf-8",
    )
    size_mb = (OUTPUT_DIR / "search-index.json").stat().st_size / 1_000_000
    print(f"  {len(index):,} entries, {size_mb:.1f} MB.", flush=True)

    print(f"\nBuild complete. Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
