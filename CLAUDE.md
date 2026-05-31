# CLAUDE.md — genehalbrooks.github.io

Personal portfolio and professional resume site for Gene Halbrooks, deployed via GitHub Pages at **genehalbrooks.com**.

## Repository Structure

```
/
├── index.html              # Primary page — current live version
├── index                   # Older HTML snapshot (no hero photo layout)
├── gene_headshot.jpg       # Profile photo used in hero section
├── GeneHalbrooks_Resume.pdf  # Downloadable resume linked from hero
└── CNAME                   # Custom domain: genehalbrooks.com
```

## Technology Stack

- **Pure HTML/CSS** — no JavaScript frameworks, no build tools, no package.json, no dependencies
- **Inline styles** — all CSS lives in a single `<style>` block inside `<head>`; no external stylesheets
- **Google Fonts** — Playfair Display (headings), IBM Plex Sans (body) loaded via CDN
- **Formspree** — contact form backend (`action="https://formspree.io/f/xdapzqvk"`)
- **GitHub Pages** — static hosting, deploys automatically from `main` branch

## Design System

All design tokens are defined as CSS custom properties at `:root`:

| Variable        | Value                    | Usage                        |
|-----------------|--------------------------|------------------------------|
| `--navy`        | `#0f2240`                | Primary brand color          |
| `--navy-mid`    | `#1a3a6b`                | Hover states on navy elements|
| `--gold`        | `#c9a84c`                | Accent / highlight color     |
| `--gold-light`  | `#e8c97a`                | Hover states on gold elements|
| `--off-white`   | `#f5f3ee`                | Page background              |
| `--text-dark`   | `#111827`                | Primary text                 |
| `--text-mid`    | `#374151`                | Secondary text               |
| `--text-muted`  | `#6b7280`                | Tertiary / metadata text     |
| `--border`      | `rgba(15,34,64,0.12)`    | Card and section borders     |
| `--font-display`| `'Playfair Display'`     | Section titles, job titles   |
| `--font-body`   | `'IBM Plex Sans'`        | All body copy                |

## Page Structure (index.html)

1. **`<nav>`** — Sticky top nav with logo and links to `#accomplishments`, `#experience`, `#skills`, `#contact`, and LinkedIn
2. **`<header class="hero">`** — Two-column layout: headshot photo left, name/title/summary/badges/CTA buttons right
3. **`<section id="accomplishments">`** — CSS grid of accomplishment cards; featured card spans full width
4. **`<section id="experience">`** — Chronological work history with `.job` entries
5. **`<section id="skills">`** — Skill cards on navy background with gold progress bars
6. **`<section id="contact">`** — Two-column: text/LinkedIn left, Formspree form right
7. **`<footer>`** — Copyright and LinkedIn link

## Key HTML Patterns

**Section template:**
```html
<section id="[id]">
  <div class="section-inner">
    <p class="section-label">Category Label</p>
    <h2 class="section-title">Section Title</h2>
    <!-- content -->
  </div>
</section>
```

**Job entry template:**
```html
<div class="job">
  <div class="job-header">
    <span class="job-title">Title</span>
    <span class="job-period">Start – End</span>
  </div>
  <p class="job-company">Company &nbsp;·&nbsp; Location</p>
  <ul class="job-bullets">
    <li>Bullet point</li>
  </ul>
</div>
```

**Skill card template:**
```html
<div class="skill-card">
  <p class="skill-name">Skill Name</p>
  <div class="skill-bar"><div class="skill-fill" style="width:XX%"></div></div>
  <p class="skill-tag">Tag · Tag · Tag</p>
</div>
```

**Accomplishment card template:**
```html
<div class="accom-card">
  <p class="accom-year">YYYY</p>
  <p>Description text.</p>
  <!-- optional: .accom-link or .video-link -->
</div>
```
Add `class="accom-card featured"` to make a card span all columns.

## Responsive Breakpoints

- **768px** — nav stacks vertically, hero becomes single-column, accom grid becomes 1 column, contact grid becomes 1 column
- **400px** — skills grid becomes 1 column, hero h1 shrinks to 2rem

## Development Workflow

**No build step required.** Edit `index.html` directly and open in a browser.

To preview locally:
```bash
# Any static server works, e.g.:
python3 -m http.server 8080
# or
npx serve .
```

**Deployment:** Push to `main` branch → GitHub Pages auto-deploys to genehalbrooks.com. Changes are live within ~30–60 seconds.

**Branch convention:** Feature work happens on descriptive branches; merge to `main` when ready to publish.

## Editing Guidelines

- **Do not extract CSS** to a separate file — the single-file approach is intentional for simplicity and portability
- **Do not add JavaScript** unless explicitly requested; the site is intentionally JS-free
- **Preserve the `index` file** as-is; it is a prior-version snapshot, not the active page
- **Keep the two HTML files in sync** if making structural changes that should apply to both
- **External links** open in `target="_blank"` — maintain this for LinkedIn, Calendly, Formspree, and OneStream resource links
- **Accessibility**: keep `alt` text on the headshot image; form inputs already have `required` attributes
- **Color tokens**: always use CSS variables (`var(--navy)`) rather than hardcoding hex values

## Static Assets

| File | Notes |
|------|-------|
| `gene_headshot.jpg` | ~23KB, used as `<img src="gene_headshot.jpg">` in the hero; `object-position: center top` |
| `GeneHalbrooks_Resume.pdf` | ~624KB, linked with `download` attribute from hero CTA |

When replacing either asset, keep the same filename to avoid updating HTML references.
