#!/usr/bin/env python3
"""Fetch download counts from CurseForge and Modrinth, update README badges."""

import json
import os
import re
import sys
import urllib.request

USER_AGENT = "Madgique-Profile-Updater/1.0"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode()


def get_modrinth_downloads():
    data = fetch_json("https://api.modrinth.com/v2/user/Madgique/projects")
    return sum(p["downloads"] for p in data)


def get_curseforge_downloads():
    html = fetch_text("https://www.curseforge.com/members/madgique/projects")
    match = re.search(r'([\d.]+[KMk]?)\s*Downloads', html)
    if match:
        return parse_number(match.group(1))
    raise ValueError("Could not find CurseForge download total on profile page")


def parse_number(s):
    s = s.strip().upper()
    if s.endswith("K"):
        return int(float(s[:-1]) * 1000)
    if s.endswith("M"):
        return int(float(s[:-1]) * 1_000_000)
    return int(s.replace(",", ""))


def format_number(n):
    if n >= 1_000_000:
        v = n / 1_000_000
        return f"{v:.1f}M" if v < 10 else f"{int(v)}M"
    if n >= 100_000:
        return f"{int(n / 1000)}k"
    if n >= 1000:
        v = n / 1000
        return f"{v:.1f}k" if v != int(v) else f"{int(v)}k"
    return str(n)


def update_readme(cf_total, mr_total):
    path = "README.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    cf_fmt = format_number(cf_total)
    mr_fmt = format_number(mr_total)

    content = re.sub(
        r'CurseForge-[\d.]+[KMk]?_downloads',
        f"CurseForge-{cf_fmt}_downloads",
        content,
    )
    content = re.sub(
        r'Modrinth-[\d.]+[KMk]?_downloads',
        f"Modrinth-{mr_fmt}_downloads",
        content,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated: CurseForge={cf_fmt}, Modrinth={mr_fmt}")


def main():
    cf_total = None
    mr_total = None

    try:
        mr_total = get_modrinth_downloads()
        print(f"Modrinth: {mr_total}")
    except Exception as e:
        print(f"Modrinth failed: {e}", file=sys.stderr)

    try:
        cf_total = get_curseforge_downloads()
        print(f"CurseForge: {cf_total}")
    except Exception as e:
        print(f"CurseForge failed: {e}", file=sys.stderr)

    if cf_total is None and mr_total is None:
        sys.exit(1)

    update_readme(cf_total or 0, mr_total or 0)

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"cf_downloads={format_number(cf_total or 0)}\n")
            f.write(f"mr_downloads={format_number(mr_total or 0)}\n")


if __name__ == "__main__":
    main()
