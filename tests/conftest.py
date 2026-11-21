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
