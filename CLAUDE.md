# justinjackson.ca — CLAUDE.md

Personal website and blog of Justin Jackson. Built on Statamic 6.2.5 (Laravel 12). Flat-file CMS — no database, content lives in Markdown files.

## Tech stack

- **CMS:** Statamic 6.2.5 (flat-file mode)
- **Framework:** Laravel 12
- **Templating:** Antlers (`.antlers.html` files in `resources/views/`)
- **Build:** Vite (`package.json`)
- **Local dev URL:** http://justin4.test

## Key directories

```
content/collections/   ← All CMS-managed content (articles, pages)
resources/views/       ← Antlers templates and partials
public/                ← Web root: static assets + archived sites
routes/web.php         ← Feed routes + URL redirects
config/statamic/       ← 24 Statamic module configs
app/                   ← Minimal custom PHP (3 files)
```

## Content collections

### Articles (`content/collections/articles/`)

390+ articles spanning **2008–2026**. Files named `YYYY-MM-DD.slug.md`.

Frontmatter structure:
```yaml
---
id: [UUID]
blueprint: article
title: 'Post Title'
article_content:
  - type: paragraph
    content:
      - type: text
        text: 'Paragraph text here'
  - type: heading
    attrs:
      level: 2
    content:
      - type: text
        text: 'Section heading'
  - type: set
    attrs:
      values:
        type: html_embed
        embed_code: '<blockquote>...</blockquote>'
  - type: set
    attrs:
      values:
        type: image
        image: content/filename.png
        size: md
        brutalized: false
  - type: set
    attrs:
      values:
        type: newsletter   ← newsletter signup CTA block
author: admin
published: true
meta_title: '...'
meta_description: '...'
social_sharing_image: filename.png
---
```

The `article_content` field is a ProseMirror/Bard array. When writing new articles, the prose goes in `paragraph` nodes with `text` children; headings use `type: heading` with `attrs.level`; embeds and images use `type: set`.

### Pages (`content/collections/pages/`)

35 pages (no date prefix, just `slug.md`). Same blueprint structure. Key pages: `about.md`, `now.md`, `consulting.md`, `podcasts.md`, `newsletter.md`, `tools.md`, `speaking.md`.

## Justin's writing — voice and style

Justin writes in a **direct, conversational, first-person** voice. Key patterns:

- **Short paragraphs** — often 1–3 sentences. Rarely long walls of text.
- **Bold for emphasis** on key claims or provocative statements.
- **Stories as anchors** — articles frequently open with a personal anecdote or a vivid story from someone else's experience, then extract a lesson. (e.g., the FreshBooks/BillSpring undercover rewrite story in the Claude Code article.)
- **Honest about struggle** — openly discusses failures, uncertainty, hard times. Not a hype voice.
- **Builder perspective** — shares what he's currently building, experimenting with, thinking about.
- **External voices** — frequently embeds tweets, Bluesky posts, quotes from others to support points.
- **Ends posts** with:
  ```
  Cheers,
  Justin Jackson
  
  Connect with me on:
  🦋 Bluesky
  💼 LinkedIn
  🐘 Mastodon
  🧵 Threads
  ```
- **Annual year-in-review** tradition since 2013 (published each January).
- **Rhetorical questions** used to invite the reader in.

### Core topics (recurring across 18 years of writing)

- **Bootstrapping / indie business** — building sustainable businesses without VC funding
- **SaaS and product development** — especially for small/indie teams
- **Marketing for developers** — how builders find customers (his 2015 book, revived as community in 2026)
- **Podcasting** — co-founder of Transistor.fm; writes frequently about the podcast industry
- **Personal productivity / mindset** — motivation, decision-making, focus ("zone of genius", hustle, burnout)
- **AI and software development** — recent focus (2025–2026) on Claude Code, building with AI
- **Community building** — JFDI community, Marketing for Developers community
- **Reflection / life** — family, mental health, what matters

### Transistor.fm

Justin co-founded [Transistor.fm](https://transistor.fm) (podcast hosting). Many articles reference building and growing Transistor. This is his primary business.

## Public directory — archived/static sites

Everything in `public/` is directly web-served. Alongside `assets/`, `css/`, and `build/`, there are numerous **archived static HTML sites** from past products, courses, and events.

### Standalone HTML files (public root)

| File | Description |
|------|-------------|
| `words.html` | Famous "You're a word person" essay (translated into 60+ languages as `words_*.html`) |
| `fun.html` | Landing page |
| `jfdi.html` | JFDI community landing page |
| `jfdi-mail.html` | JFDI email signup |
| `email.html` | Email course landing page |
| `clarity.html` | Clarity/consulting landing page |
| `amazon.html` | Amazon product page |
| `selfpub.html` | Self-publishing landing page |
| `jj2.html`, `jj3.html` | Personal landing page variants |
| `lastchance.html`, `vegas.html`, `edmonton.html` | Event/sale pages |
| `wow.html` | Campaign page |
| `amp-free-chapter.html` | Book chapter giveaway |

### Archived project directories (public subdirectories)

| Directory | Description |
|-----------|-------------|
| `/audiencecourse/` | "Build an Audience" course site |
| `/bizcamp/` | BizCamp event site |
| `/marketingfordevelopers/` | Marketing for Developers book/course site |
| `/marketingforproductpeople/` | Marketing for Product People course |
| `/buildanaudience-may31/` | Build an Audience workshop (May 31) |
| `/buildanaudience-june29/` | Build an Audience workshop (June 29) |
| `/earplugs/` | Earplugs product site |
| `/firestarter/` | Firestarter event/product |
| `/focus/` | Focus course/product |
| `/jolt/` | Jolt event/workshop |
| `/indie/` | Indie business site |
| `/pm/` | Product management content |
| `/paysplit/` | PaySplit product |
| `/producthunt/` | Product Hunt campaign |
| `/jfdi/` | JFDI community site (includes `/jfdi/campfire/` membership subsite with members.html) |
| `/teach-archive/` | Teaching content archive |
| `/levelslandingpage/` | Levels landing page |
| `/onethousand/` | 1,000 customers content |
| `/blackfriday/` | Black Friday campaign |
| `/svn/`, `/svn2/` | Legacy SVN archives |
| `/email/` | Email course content |
| `/kidlet/` | Kidlet project |
| `/squirrel/` | Squirrel project |
| `/twitter/` | Twitter content |
| `/wordcamp/` | WordCamp talk |
| `/resume/` | Resume page |
| `/slides/` | Presentation slides |
| `/hls-podcast/` | HLS podcast streaming content |
| `/wp-content/` | Legacy WordPress content |

## Templates

- `layout.antlers.html` — main layout
- `article.antlers.html` — single post
- `articles.antlers.html` — post listing
- `home.antlers.html` — homepage
- `newsletter.antlers.html` — newsletter page
- `default.antlers.html` — fallback
- `feeds/articles.antlers.html` — RSS/Atom feed

Partials in `resources/views/partials/`: `head`, `nav`, `newsletter-callout`, `scripts`

Content blocks in `resources/views/partials/blocks/`: `text`, `image`, `jumbo_text`, `html_embed`, `newsletter`, `sidebar`

## Routes

`routes/web.php` contains the RSS/Atom feed routes and ~10 permanent redirects for old URLs. No complex custom controllers — this is primarily a configuration-driven Statamic site.

## Notes for writing new content

**Articles** are written and published through the Statamic CMS GUI — do not hand-edit `content/collections/articles/` files.

**New static sites/sub-sites** (landing pages, campaign pages, archived projects) are built as a self-contained folder in `public/`, following the same pattern as existing ones (e.g., `/public/jfdi/`, `/public/audiencecourse/`). Each gets its own `index.html` plus any CSS, JS, and images it needs.

When drafting copy for a new static site, match Justin's voice: short paragraphs, personal/direct, story-anchored. See the "Justin's writing" section above for details.
