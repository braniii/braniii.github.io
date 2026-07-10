# personal webpage :-)

This repository generates a static webpage with:

- [Astro](https://astro.build) v7
- [TailwindCSS](https://tailwindcss.com) v4

### Development

```sh
$ npm install    # Install dependencies.
$ npm run dev    # Start the dev server at localhost:4321.
```

### Building

```sh
$ npm run build      # Build the static site into dist/.
$ npm run preview    # Preview the production build locally.
```

Deployment happens automatically via GitHub Actions on pushes to `main`,
publishing `dist/` to the `gh-pages` branch.

### Content

The page content (publications, software) lives in `src/data/index.json`.
Packages are tagged with optional `pypi` / `conda` names, which drive the
download statistics below.

### Download & citation stats

The header totals, per-package download badges and per-paper citation counts are
read from `src/data/stats.json`, refreshed weekly by the `Update stats` workflow
(`.github/workflows/stats.yml`; also runnable on demand from the Actions tab). It
runs `scripts/fetch_stats.py`, commits the updated JSON, and redeploys. Sources:

- **conda-forge downloads** — `api.anaconda.org`, no credentials needed.
- **GitHub stars** — GitHub REST API; uses the workflow's built-in `GITHUB_TOKEN`
  for a higher rate limit, driven by the `github` (`owner/repo`) key per entry.
- **Google Scholar citations** — scraped via `scholarly`, no credentials.
- **PyPI downloads** — [pepy.tech](https://pepy.tech), which needs a free API key
  (PyPI has no lifetime-download API). Without it, download totals fall back to
  conda-forge only.

Every source is best-effort: if one fails, the previous value is kept, so a flaky
run never resets a number to zero.

#### Setting up the pepy.tech API key

1. Sign in at [pepy.tech](https://pepy.tech) and copy your API key (see
   <https://pepy.tech/pepy-api>).
2. In the repository, go to **Settings → Secrets and variables → Actions → New
   repository secret**.
3. Name it `PEPY_API_KEY` and paste the key as the value.
4. Trigger **Actions → Update stats → Run workflow** (or wait for the weekly run).
   PyPI lifetime downloads are then folded into every package total.

Run the collector locally with:

```sh
$ pip install scholarly
$ PEPY_API_KEY=<your-key> python scripts/fetch_stats.py
```

### Assets

Some external assets are included.

- GitHub Icon from GitHub.
- Icons from HeroIcons (MIT).
