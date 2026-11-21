import shutil
import subprocess
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent


def html(site: Path, url_path: str) -> BeautifulSoup:
    rel = url_path.strip("/")
    f = site / rel / "index.html" if rel else site / "index.html"
    return BeautifulSoup(f.read_text(), "html.parser")


@pytest.fixture(scope="session")
def site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("build") / "public"
    res = subprocess.run(
        ["zola", "build", "--output-dir", str(out), "--force"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert "WARN" not in res.stdout + res.stderr, res.stdout + res.stderr
    yield out
    shutil.rmtree(out, ignore_errors=True)


@pytest.fixture(scope="session")
def css(site: Path) -> str:
    return (site / "theme.css").read_text()


@pytest.fixture(scope="session")
def scratch_site(tmp_path_factory) -> Path:
    """Build a copy of the site with an extra post exercising content edge cases."""
    root = tmp_path_factory.mktemp("scratch") / "site"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".superpowers", ".playwright-mcp", "themes", "tests", "public"))
    (root / "content/notes/2099-01-01-edge-cases.md").write_text(
        '+++\ntitle = "Edge cases"\n+++\n\nFish & chips with `code<x>`.\n\n<!-- more -->\n\n'
        "```yaml\nimage: {{ .Values.image }}\n```\n"
    )
    out = root / "public"
    res = subprocess.run(["zola", "build", "--output-dir", str(out), "--force"], cwd=root, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    return out
