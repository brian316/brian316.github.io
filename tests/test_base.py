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


def test_internal_section_links_keep_trailing_slash(site):
    # /blog, /resume, /about without a slash cost a redirect on GitHub Pages
    hrefs = [a["href"] for a in html(site, "/").select("a[href]")]
    for h in hrefs:
        if h.startswith("https://bduenas.com/") and "." not in h.rsplit("/", 1)[-1] and "#" not in h:
            assert h.endswith("/"), h


def test_favicon_from_initials(site):
    head = html(site, "/").select_one("head")
    assert head.select_one('link[rel="icon"][href$="/favicon.ico"]')
    assert head.select_one('link[rel="icon"][type="image/png"][href$="/favicon-32.png"]')
    assert head.select_one('link[rel="apple-touch-icon"][href$="/apple-touch-icon.png"]')
    ico = (site / "favicon.ico").read_bytes()
    assert ico[:4] == b"\x00\x00\x01\x00" and int.from_bytes(ico[4:6], "little") >= 3  # 16/32/48
    for name in ["favicon-32.png", "apple-touch-icon.png"]:
        assert (site / name).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", name


def test_no_em_dashes_in_rendered_pages(site):
    for u in ["/", "/resume/", "/blog/", "/about/"]:
        assert "\u2014" not in (site / u.strip("/") / "index.html" if u != "/" else site / "index.html").read_text(), u


def test_no_theme_submodule():
    assert not (ROOT / "themes").exists()
    assert not (ROOT / ".gitmodules").exists()
