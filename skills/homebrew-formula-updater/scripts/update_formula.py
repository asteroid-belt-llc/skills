#!/usr/bin/env python3
"""
update_formula.py - Fetch latest GitHub release and update Homebrew formula

Usage:
    python3 update_formula.py <github_repo> <formula_file>

Example:
    python3 update_formula.py asteroid-belt/skulto skulto.rb

Requirements:
    Python 3.8+ (uses typing.Optional and walrus operator)
"""

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


def validate_repo_format(repo: str) -> bool:
    """Validate that repo is in 'owner/repo' format."""
    pattern = r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$'
    return bool(re.match(pattern, repo))


def fetch_latest_release(repo: str) -> dict:
    """Fetch latest release info from GitHub API."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = Request(url, headers={"Accept": "application/vnd.github.v3+json"})

    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"Error fetching release: HTTP {e.code}")
        sys.exit(1)
    except URLError as e:
        print(f"Error fetching release: {e.reason}")
        sys.exit(1)


def download_and_hash(url: str) -> Optional[str]:
    """Download a file and compute its SHA256 hash."""
    try:
        req = Request(url, headers={"Accept": "application/octet-stream"})
        with urlopen(req, timeout=120) as response:
            sha256 = hashlib.sha256()
            while chunk := response.read(8192):
                sha256.update(chunk)
            return sha256.hexdigest()
    except HTTPError as e:
        print(f"  Warning: Could not download {url} (HTTP {e.code})")
        return None
    except URLError as e:
        print(f"  Warning: Could not download {url} ({e.reason})")
        return None


def extract_current_shas(content: str) -> Dict[str, str]:
    """Extract current SHA256 values from formula."""
    shas = {}
    lines = content.split('\n')

    current_platform = None
    for line in lines:
        # Detect platform from URL
        if 'darwin-amd64' in line:
            current_platform = 'darwin-amd64'
        elif 'darwin-arm64' in line:
            current_platform = 'darwin-arm64'
        elif 'linux-amd64' in line:
            current_platform = 'linux-amd64'
        elif 'linux-arm64' in line:
            current_platform = 'linux-arm64'

        # Extract SHA256 on line following URL
        if current_platform and 'sha256' in line:
            match = re.search(r'sha256\s+"([a-f0-9]{64})"', line)
            if match:
                shas[current_platform] = match.group(1)
                current_platform = None

    return shas


def main():
    parser = argparse.ArgumentParser(
        description="Update Homebrew formula with latest GitHub release"
    )
    parser.add_argument("repo", help="GitHub repo (e.g., asteroid-belt/skulto)")
    parser.add_argument("formula", help="Path to formula file (e.g., skulto.rb)")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    # Validate repo format
    if not validate_repo_format(args.repo):
        print(f"Error: Invalid repo format '{args.repo}'. Expected 'owner/repo' (e.g., 'asteroid-belt/skulto')")
        sys.exit(1)

    formula_path = Path(args.formula)
    if not formula_path.exists():
        print(f"Error: Formula file '{args.formula}' not found")
        sys.exit(1)

    # Fetch latest release
    print(f"Fetching latest release for {args.repo}...")
    release = fetch_latest_release(args.repo)
    tag = release.get("tag_name", "")
    version = tag.lstrip("v")
    print(f"Latest version: {tag} (formula version: {version})")

    # Get repo name for asset naming
    repo_name = args.repo.split("/")[-1]

    # Extract current SHAs for replacement
    original_content = formula_path.read_text()
    old_shas = extract_current_shas(original_content)
    print(f"\nCurrent SHA256 values found:")
    for platform, sha in old_shas.items():
        print(f"  {platform}: {sha[:16]}...")

    # Download assets and compute SHA256
    print(f"\nFetching SHA256 checksums for {tag}...")
    checksums = {}

    for platform in ["darwin-amd64", "darwin-arm64", "linux-amd64", "linux-arm64"]:
        asset_name = f"{repo_name}-{tag}-{platform}.tar.gz"
        asset_url = f"https://github.com/{args.repo}/releases/download/{tag}/{asset_name}"

        print(f"  Downloading {asset_name}...")
        sha = download_and_hash(asset_url)

        if sha:
            checksums[platform] = sha
            checksums[f"{platform}_url"] = asset_url
            checksums[f"{platform}_old_sha"] = old_shas.get(platform, "")
            print(f"    SHA256: {sha}")
        else:
            print(f"    Skipped (download failed)")

    if not checksums:
        print("\nError: No checksums could be fetched")
        sys.exit(1)

    # Update formula content
    print(f"\nUpdating formula...")
    new_content = original_content

    # Update version
    new_content = re.sub(
        r'version\s+"[^"]+"',
        f'version "{version}"',
        new_content
    )

    # Update URLs and SHA256s
    for platform in ["darwin-amd64", "darwin-arm64", "linux-amd64", "linux-arm64"]:
        if platform not in checksums:
            continue

        new_url = checksums[f"{platform}_url"]
        new_sha = checksums[platform]
        old_sha = checksums.get(f"{platform}_old_sha", "")

        # Update URL
        url_pattern = rf'(url\s+")[^"]*{re.escape(platform)}[^"]*(")'
        new_content = re.sub(url_pattern, rf'\g<1>{new_url}\g<2>', new_content)

        # Update SHA256 by replacing old value
        if old_sha:
            new_content = new_content.replace(old_sha, new_sha)

    if args.dry_run:
        print("\n--- Dry run: changes that would be made ---")
        print(new_content)
    else:
        # Create backup
        backup_path = formula_path.with_suffix(formula_path.suffix + ".bak")
        shutil.copy(formula_path, backup_path)
        print(f"Backup saved to: {backup_path}")

        # Write updated formula
        formula_path.write_text(new_content)
        print(f"Formula updated: {formula_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()
