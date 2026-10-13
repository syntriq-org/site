# Syntriq Insights

## Purpose and voice

Explain the commercial product through business problems, the system's organising ideas and practical examples. Lead with reader value, then explain the mechanism in plain language. Keep API wire formats, repository milestones and build internals in engineering documentation.

Use a confident product voice without finished/unfinished, prerelease or roadmap badges. Describe architecture accurately; do not invent customer adoption, measured savings, production readiness, certification or product access. ChargeWeave is the concrete domain example. Its application definitions remain distinct from the shared foundation.

## Article structure

Each article has a specific business question, a short introduction, a rich visual explanation, substantive sections, a concise business-value takeaway and related reading. Keep article text accessible independently of the infographic. Provide a full-size PNG link and a downloadable PNG. Use page-specific titles, descriptions, canonical URLs and social preview metadata.

## Visual direction

Midnight navy #090f1a, teal #20bbae, cyan #31c3ea and white. Rich editorial isometric glass imagery occupies most of the frame. Large readable titles and short labels. Avoid dense architecture boxes, tiny prose, fabricated metrics and redrawn logos. Visuals are conceptual illustrations; exact technical contracts remain in the text and engineering documents.

The three 1536 × 1024 PNG illustrations were generated with the built-in image-generation tool. Source assets are committed in assets/insights/. Each uses a landscape conceptual product infographic brief, with navy, teal and cyan, cinematic glass structures, generous margins and no readiness or numerical claims.

### Asset briefs and final text

- `connected-business.png`: luminous central application model surrounded by business entities, workflows, analytics and AI engineering. Title: “One connected business story”. Eyebrow: “SYNTRIQ / PLATFORM”. Labels: “Model”, “Coordinate”, “Understand”, “Evolve”. Closing line: “Shared meaning. Coordinated action.”
- `ai-context.png`: browser workbench connected to a component library, cloud reasoning and an evidence journal. Title: “Give AI the context to act precisely”. Eyebrow: “SYNTRIQ / AI & CONTEXT”. Labels: “Discover”, “Understand”, “Act”, “Verify”. Closing line: “Current sources. Focused context. Visible evidence.”
- `simulation-evidence.png`: glass simulation laboratory with routine, boundary and fault scenario streams, an evidence ledger and a verification gateway. Title: “Explore change before release”. Eyebrow: “SYNTRIQ / SIMULATION & EVIDENCE”. Labels: “Generate”, “Simulate”, “Compare”, “Verify”. Closing line: “Repeatable scenarios. Traceable decisions.”

## Publishing

Articles live in insights/ and use the shared stylesheet and progressive enhancement script. Add new article links to the Insights index, homepage and related-reading sections. GitHub Actions validates cross-page links and packages insights/ together with the public assets. Run `python3 scripts/validate.py` and `node --check app.js` before publishing.

## Exact explanatory diagram system

The extended series pairs the retained rich brand artwork with exact explanatory diagrams. Source data lives in `content/articles.json`; `scripts/build_content.py` generates the HTML and SVG sources. SVGs are editable and render to 2000 × 1300 PNG plus 1000 × 650 card previews through `scripts/render_diagrams.sh` (Inkscape). Retain navy, teal, cyan, subtle grid depth and layered panels. Six large labelled areas use a serpentine reading order; dashed feedback paths are reserved for engineering loops. Labels use DejaVu Sans, at least 25px for supporting information in the full-size source. Do not put prose inside diagrams.

The original generated editorial illustrations remain available in assets/insights; no logo is recreated. Exact diagrams are authored as vectors because relationships, ordering and labels must remain controlled. Each diagram has an accessible HTML equivalent and an image description. Do not crop diagram previews.

Source changes: edit content/articles.json, run `python3 scripts/build_content.py`, then render changed diagram PNGs. Inspect the PNG output before committing. The website is buildless; GitHub only regenerates HTML/SVG to detect drift and validates the committed PNGs. Internal source/docs/scripts are excluded from the published artifact.

## Infographics within articles

Navigation thumbnails never substitute for an in-article visual. The three rich illustrated PNGs appear full-width after the opening explanation of their matching articles. All ten precise diagrams sit inside the article reading flow after the third section. Preserve full-size viewing, descriptive captions, alt text and direct PNG downloads. Keep text in a readable narrow column while figures use the wider editorial container; never crop article figures.

## Public-site links

Display infographics directly in the article. Do not offer PNG downloads, direct image-file links or GitHub/repository links on public pages. Keep calls to action within the commercial site. This supersedes earlier download and full-size-link guidance above.
