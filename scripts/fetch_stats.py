#!/usr/bin/env python3
"""Collect download + citation stats and write src/data/stats.json.

Run weekly from a GitHub Action (and manually). Sources:
  - conda-forge lifetime downloads via api.anaconda.org (no auth)
  - PyPI lifetime downloads via pepy.tech (needs PEPY_API_KEY)
  - total Google Scholar citations via the `scholarly` scraper (no key, fragile)

Everything is best-effort: on any failure the previous value from the existing
stats.json is kept, so a flaky run never regresses a number to zero.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import date, timezone, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "src" / "data" / "index.json"
OUT = ROOT / "src" / "data" / "stats.json"
SCHOLAR_ID = os.environ.get("SCHOLAR_ID", "3Pz_4wwAAAAJ")
PEPY_KEY = os.environ.get("PEPY_API_KEY")
GH_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def get_json(url: str, headers: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "braniii-stats"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def conda_downloads(name: str) -> int | None:
    try:
        d = get_json(f"https://api.anaconda.org/package/conda-forge/{name}")
        n = d.get("ndownloads")
        if n is None:
            n = sum(f.get("ndownloads", 0) for f in d.get("files", []))
        return int(n)
    except Exception as e:  # noqa: BLE001
        print(f"  conda {name}: {e}", file=sys.stderr)
        return None


def pypi_downloads(name: str) -> int | None:
    if not PEPY_KEY:
        print(f"  pypi {name}: no PEPY_API_KEY, skipping", file=sys.stderr)
        return None
    try:
        d = get_json(
            f"https://api.pepy.tech/api/v2/projects/{name}",
            headers={"X-API-Key": PEPY_KEY, "User-Agent": "braniii-stats"},
        )
        return int(d.get("total_downloads"))
    except Exception as e:  # noqa: BLE001
        print(f"  pypi {name}: {e}", file=sys.stderr)
        return None


def github_stars(repo: str) -> int | None:
    headers = {"User-Agent": "braniii-stats", "Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    try:
        d = get_json(f"https://api.github.com/repos/{repo}", headers=headers)
        return int(d.get("stargazers_count"))
    except Exception as e:  # noqa: BLE001
        print(f"  stars {repo}: {e}", file=sys.stderr)
        return None


def _norm(title: str) -> str:
    return "".join(c for c in title.lower() if c.isalnum())


def scholar_data() -> tuple[int | None, dict[str, int]]:
    """Return (total citations, {normalized_title: num_citations})."""
    try:
        from scholarly import scholarly

        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author, sections=["indices", "publications"])
        total = int(author.get("citedby"))
        pubs: dict[str, int] = {}
        for p in author.get("publications", []):
            title = p.get("bib", {}).get("title", "")
            if title:
                pubs[_norm(title)] = int(p.get("num_citations", 0) or 0)
        return total, pubs
    except Exception as e:  # noqa: BLE001
        print(f"  scholar: {e}", file=sys.stderr)
        return None, {}


def main() -> int:
    index = json.loads(INDEX.read_text())
    prev = {}
    if OUT.exists():
        try:
            prev = json.loads(OUT.read_text())
        except Exception:  # noqa: BLE001
            prev = {}
    prev_pkgs = prev.get("packages", {})
    prev_stars = prev.get("stars", {})

    packages: dict[str, dict] = {}
    stars: dict[str, int] = {}
    for section in ("projects", "research"):
        for e in index.get(section, []):
            title = e["title"]
            if "github" in e:
                n = github_stars(e["github"])
                stars[title] = n if n is not None else prev_stars.get(title)
                print(f"  stars {title}: {stars[title]}")
            if "pypi" not in e and "conda" not in e:
                continue
            old = prev_pkgs.get(title, {})
            entry: dict[str, int | None] = {}
            if "pypi" in e:
                entry["pypi"] = pypi_downloads(e["pypi"])
                if entry["pypi"] is None:
                    entry["pypi"] = old.get("pypi")
            if "conda" in e:
                entry["conda"] = conda_downloads(e["conda"])
                if entry["conda"] is None:
                    entry["conda"] = old.get("conda")
            entry["total"] = sum(v for v in (entry.get("pypi"), entry.get("conda")) if v)
            packages[title] = entry
            print(f"  {title}: {entry}")

    citations, pub_cites = scholar_data()
    if citations is None:
        citations = prev.get("totals", {}).get("citations")

    # Map each article's citation count by DOI (stable key), matched on title.
    prev_articles = prev.get("articles", {})
    articles: dict[str, int] = {}
    for a in index.get("articles", []):
        doi = a.get("doi")
        if not doi:
            continue
        n = pub_cites.get(_norm(a.get("title", "")))
        articles[doi] = n if n is not None else prev_articles.get(doi, 0)
        print(f"  cite {doi}: {articles[doi]}")

    total_downloads = sum(p.get("total", 0) for p in packages.values())
    total_stars = sum(v for v in stars.values() if v)

    out = {
        "updated": date.today().isoformat(),
        "totals": {
            "downloads": total_downloads,
            "citations": citations,
            "stars": total_stars,
        },
        "packages": packages,
        "stars": stars,
        "articles": articles,
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(
        f"wrote {OUT.relative_to(ROOT)}: downloads={total_downloads} "
        f"stars={total_stars} citations={citations}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
