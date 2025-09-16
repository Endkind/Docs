#!/usr/bin/env python3
"""
Render GitHub releases into per-release markdown files using a simple {{ var }} template
and update an index.md with links from newest to oldest.

Template placeholders:
  {{ tag }}          -> release tag (required)
  {{ body }}         -> release body/notes (required)
  {{ deb_url }}      -> URL to a .deb asset if present (optional)
  {{ msi_url }}      -> URL to a .msi asset if present (optional)
  {{ order }}        -> ascending integer by publish time (oldest=1, newest=N)
  {{ release_date }} -> if possible 'yyyy-mm-ddThh:mm' (UTC), otherwise 'yyyy-mm-dd' (UTC)

Index management:
  - We maintain a managed block in index.md delimited by:
        <!-- releases:start -->
        <!-- releases:end -->
    If markers exist, the block is replaced; otherwise it's appended once.
  - List items are '- [tag](sanitized-tag)' ordered newest → oldest.
  - The newest item is suffixed with ' (latest)'.

Usage:
  python fetch_release_notes.py <repo> <output_dir>

Examples:
  python fetch_release_notes.py Endkind/FastAPIBase ./releases
  python fetch_release_notes.py https://github.com/Endkind/FastAPIBase ./releases

Notes:
  - Place 'template.md' inside <output_dir>. If missing, defaults to '{{ body }}'.
  - Set GITHUB_TOKEN env var to increase GitHub API rate limits (recommended).
  - Draft releases are skipped; prereleases are included.
  - Per-release files are overwritten.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

GITHUB_API = "https://api.github.com"
RELEASES_START = "<!-- releases:start -->"
RELEASES_END = "<!-- releases:end -->"


@dataclass
class ReleaseItem:
    rid: int
    tag: str
    safe_tag: str
    body: str
    assets: List[Dict]
    published_at: Optional[datetime]  # None if unknown


def parse_repo_arg(repo_arg: str) -> Tuple[str, str]:
    s = repo_arg.strip()

    if s.startswith("git@github.com:"):
        s2 = s[len("git@github.com:") :]
        if s2.endswith(".git"):
            s2 = s2[:-4]
        parts = s2.split("/")
        if len(parts) == 2 and all(parts):
            return parts[0], parts[1]

    if s.startswith("http://") or s.startswith("https://"):
        p = urlparse(s)
        parts = [x for x in p.path.split("/") if x]
        if len(parts) >= 2:
            owner, repo = parts[0], parts[1]
            if repo.endswith(".git"):
                repo = repo[:-4]
            return owner, repo

    if "/" in s and not s.endswith("/"):
        owner, repo = s.split("/", 1)
        if owner and repo:
            return owner, repo

    raise ValueError(f"Could not parse repository identifier: {repo_arg!r}")


def gh_request(url: str, token: Optional[str] = None) -> List[Dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "fetch-release-notes-script",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8")
        except Exception:
            body = ""
        raise SystemExit(f"GitHub API error {e.code} for {url}\n{body}")
    except URLError as e:
        raise SystemExit(f"Network error calling GitHub API: {e.reason}")


def iter_all_releases(owner: str, repo: str, token: Optional[str]) -> Iterable[Dict]:
    page = 1
    per_page = 100
    while True:
        url = f"{GITHUB_API}/repos/{owner}/{repo}/releases?per_page={per_page}&page={page}"
        releases = gh_request(url, token)
        if not releases:
            break
        for rel in releases:
            yield rel
        page += 1


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "_", name)   # Windows reserved chars
    name = name.rstrip(" .")                    # trailing spaces/dots
    return name or "untagged"


def parse_iso8601(dt: Optional[str]) -> Optional[datetime]:
    if not dt:
        return None
    if dt.endswith("Z"):
        dt = dt[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(dt)
    except ValueError:
        return None


def find_asset_url(assets: List[Dict], ext: str) -> str:
    if not assets:
        return ""
    candidates = []
    for a in assets:
        url = (a.get("browser_download_url") or "").strip()
        name = (a.get("name") or url).strip()
        if url.lower().endswith(ext.lower()):
            score = 0
            lname = name.lower()
            if any(k in lname for k in ("amd64", "x86_64", "x64")):
                score += 10
            candidates.append((score, url))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    # fallback: first asset whose name contains ext
    for a in assets:
        url = (a.get("browser_download_url") or "").strip()
        name = (a.get("name") or url).strip()
        if ext.lower() in name.lower():
            return url
    return ""


_token_pattern = re.compile(r"{{\s*(\w+)\s*}}")

def render_template(template: str, values: Dict[str, str]) -> str:
    def _sub(m: re.Match) -> str:
        return str(values.get(m.group(1), ""))
    return _token_pattern.sub(_sub, template)


def build_index_block(releases_new_to_old: List[ReleaseItem]) -> str:
    lines = [RELEASES_START]
    for i, r in enumerate(releases_new_to_old):
        suffix = " (latest)" if i == 0 else ""
        lines.append(f"- [{r.tag}]({r.safe_tag}){suffix}")
    lines.append(RELEASES_END)
    return "\n".join(lines) + "\n"


def update_index_file(index_path: Path, releases_new_to_old: List[ReleaseItem]) -> None:
    block = build_index_block(releases_new_to_old)

    if index_path.exists():
        original = index_path.read_text(encoding="utf-8")
        if RELEASES_START in original and RELEASES_END in original:
            pattern = re.compile(
                re.escape(RELEASES_START) + r".*?" + re.escape(RELEASES_END),
                flags=re.DOTALL,
            )
            updated = pattern.sub(block.strip(), original)
            index_path.write_text(updated, encoding="utf-8", newline="\n")
            return
        else:
            with index_path.open("a", encoding="utf-8", newline="\n") as f:
                if not original.endswith("\n"):
                    f.write("\n")
                f.write("\n" + block)
            return
    else:
        index_path.write_text(block, encoding="utf-8", newline="\n")


def format_release_date_value(dt: Optional[datetime]) -> str:
    """
    Returns 'yyyy-mm-ddThh:mm' (UTC) if possible, otherwise 'yyyy-mm-dd' (UTC).
    If dt is None, returns ''.
    """
    if not dt:
        return ""
    dt_utc = dt.astimezone(timezone.utc) if dt.tzinfo else dt
    # Prefer full datetime; if that somehow fails, fall back to date only
    try:
        return dt_utc.strftime("%Y-%m-%dT%H:%M")
    except Exception:
        return dt_utc.strftime("%Y-%m-%d")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump GitHub release notes using a {{ var }} template and update index.md.")
    parser.add_argument("repo", help="GitHub repo (e.g., 'owner/name' or a GitHub URL).")
    parser.add_argument("output_dir", help="Directory to write {tag}.md files into (also where 'template.md' and 'index.md' live).")
    args = parser.parse_args()

    try:
        owner, repo = parse_repo_arg(args.repo)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    template_path = out_dir / "template.md"
    template = template_path.read_text(encoding="utf-8") if template_path.exists() else "{{ body }}"

    token = os.getenv("GITHUB_TOKEN")

    # 1) Collect releases (skip drafts)
    items: List[ReleaseItem] = []
    for rel in iter_all_releases(owner, repo, token):
        if rel.get("draft"):
            continue
        tag = rel.get("tag_name") or rel.get("name") or "untagged"
        body = rel.get("body") or ""
        assets = rel.get("assets") or []
        published = parse_iso8601(rel.get("published_at")) or parse_iso8601(rel.get("created_at"))
        rid_raw = rel.get("id")
        try:
            rid = int(rid_raw)
        except Exception:
            # Extremely unlikely, but keep stable ordering by hashing string id
            rid = abs(hash(str(rid_raw))) % (10**9)
        items.append(
            ReleaseItem(
                rid=rid,
                tag=tag,
                safe_tag=sanitize_filename(tag),
                body=body,
                assets=assets,
                published_at=published,
            )
        )

    # Ensure index exists (even if empty result)
    if not items:
        update_index_file(out_dir / "index.md", [])
        print("No releases found (or no access to releases).")
        return

    # 2) Compute order: oldest -> newest as 1..N
    items_old_to_new = sorted(items, key=lambda r: r.published_at or datetime.min)
    order_by_id = {r.rid: i + 1 for i, r in enumerate(items_old_to_new)}

    # 3) Build index order: newest -> oldest
    items_new_to_old = sorted(items, key=lambda r: r.published_at or datetime.min, reverse=True)

    # 4) Write per-release files (newest -> oldest)
    for r in items_new_to_old:
        deb_url = find_asset_url(r.assets, ".deb")
        msi_url = find_asset_url(r.assets, ".msi")
        release_date_value = format_release_date_value(r.published_at)

        rendered = render_template(
            template,
            {
                "tag": r.tag,
                "body": r.body,
                "deb_url": deb_url,
                "msi_url": msi_url,
                "order": str(order_by_id.get(r.rid, "")),
                "release_date": release_date_value,
            },
        )
        (out_dir / f"{r.safe_tag}.md").write_text(rendered, encoding="utf-8", newline="\n")
        print(f"Wrote: {out_dir / f'{r.safe_tag}.md'}")

    # 5) Update index.md
    update_index_file(out_dir / "index.md", items_new_to_old)

    print(f"Done. {len(items)} file(s) written to: {out_dir}")
    print("index.md updated.")


if __name__ == "__main__":
    main()
