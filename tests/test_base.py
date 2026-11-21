from conftest import ROOT, html

URLS = ["/", "/about/", "/blog/", "/notes/", "/blog/init-blog/", "/notes/macos-sd-card-read-only/"]


def test_all_urls_build(site):
    for u in URLS:
        rel = u.strip("/")
        assert (site / rel / "index.html" if rel else site / "index.html").exists(), u


def test_theme_detached():
    top = (ROOT / "config.toml").read_text().split("[markdown")[0]
    assert "theme =" not in top


def test_nav_order_and_labels(site):
    nav = html(site, "/").select_one('nav[aria-label="Primary"]')
    assert [a.get_text(strip=True) for a in nav.select("a.nav__link")] == ["Work", "Writing", "Resume", "About"]


def test_skip_link_and_main(site):
    s = html(site, "/")
    assert s.select_one('a.skip-link[href="#main"]') and s.select_one("main#main")


def test_icon_links_have_aria(site):
    links = html(site, "/").select("header a.icon-link")
    assert links
    for a in links:
        assert a.get("aria-label")


def test_fonts_and_css_linked(site):
    hrefs = [l["href"] for l in html(site, "/").select("link[rel=stylesheet]")]
    assert any("fonts.googleapis.com/css2" in h and "Instrument+Serif" in h and "Geist+Mono" in h and "Lora" in h for h in hrefs)
    assert any(h.endswith("/theme.css") for h in hrefs) and any(h.endswith("/giallo.css") for h in hrefs)


def test_author_typo_fixed(site):
    assert "ßrian" not in (site / "index.html").read_text()
    assert "Brian Duenas" in html(site, "/").select_one("footer").get_text()


def test_404(site):
    assert "Page not found" in (site / "404.html").read_text()
