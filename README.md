# Syntriq public website

A standalone commercial presentation site, separate from the product source. Plain HTML, CSS and JavaScript; no runtime dependencies, analytics cookies or build tooling.

## Local preview

Run `python3 -m http.server 8080` from this directory. Open `http://localhost:8080`.

## Validation

Run `node --check app.js` and `python3 scripts/validate.py`.

## GitHub Pages

In repository Settings → Pages, select **GitHub Actions** as the source. The `Validate and deploy website` workflow validates every push/PR and deploys pushes to `main`. Expected URL: https://syntriq-org.github.io/site/

Only index.html, style.css, app.js and assets are included in the deployment. Relative URLs support both the `/site/` project path and a future custom domain.

## Brand and content

Midnight navy `#090f1a`, teal `#20bbae`, cyan `#31c3ea`. The approved generated logo is displayed through a compact CSS frame; the hero artwork was generated for this site. The favicon is a simplified small-scale rendering of the mark. Assets are stored locally in WebP format.

The Studio interaction is explicitly an illustrative concept, not a product screenshot or live application. Temporal analytics is marked as planned/in development. Do not add unverified customer, performance, certification or production-readiness claims.

The header shrinks after 35px of scrolling. Entrance motion respects `prefers-reduced-motion`; content remains visible without JavaScript. Navigation and Studio tabs support keyboard use. No lead form is shown until a real contact destination is supplied; the CTA links to the organization.
