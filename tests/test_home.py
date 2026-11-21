from conftest import html


def test_hero(site):
    s = html(site, "/")
    h1 = s.select_one("h1.display-xl")
    assert "I build the tools" in h1.get_text()
    assert h1.select_one("em").get_text(strip=True) == "teams actually use."
    body = s.select_one(".hero__body").get_text()
    assert "7+ years" in body and "—" not in body
    assert s.select_one(".hero .eyebrow").get_text(" ", strip=True).upper().startswith("BRIAN DUENAS")
    cta = s.select_one(".hero a.btn")
    assert cta["href"].endswith("/resume/") and "Resume" in cta.get_text()
    assert s.select_one('.hero a[href="mailto:hello@bduenas.com"]')


def test_section_order(site):
    ids = [x.get("data-section") for x in html(site, "/").select("main [data-section]")]
    assert ids == ["hero", "rail", "experience", "founder", "work", "oss", "writing"]


def test_rail_and_experience(site):
    s = html(site, "/")
    assert len(s.select(".rail__cell")) == 3
    rows = s.select("[data-section=experience] article.row")
    exp = [r.select_one(".row__title").get_text(" ", strip=True) for r in rows]
    assert exp[0] == "Founder · Gathrly" and exp[1].startswith("Quantum Applications Engineer") and len(exp) == 8
    assert [r.select_one(".row__date").get_text(strip=True) for r in rows[:3]] == ["Now", "Now", "2024"]


def test_work_cards(site):
    names = [c.select_one(".card__title").get_text(strip=True) for c in html(site, "/").select("#work .card")]
    assert names == ["finetune-controller", "openad_service_utils", "openad-model-helm-template"]


def test_oss_band(site):
    s = html(site, "/").select_one("[data-section=oss]")
    assert s.select_one("h2").get_text(" ", strip=True) == "Small fixes, out in the open."
    assert s.select_one("h2 em").get_text(strip=True) == "out in the open."
    assert "band--dark" in s["class"] and "$ git log --author=brian316" in s.get_text(" ", strip=True).replace("$  ", "$ ")
    rows = s.select(".oss__row")
    assert len(rows) == 6 and rows[0].select_one(".status--merged") and s.select_one(".status--open")
    # thenewboston has no stars: no stray star glyph
    assert "★" not in rows[-1].get_text()


def test_recent_writing(site):
    s = html(site, "/").select_one("#writing")
    assert len(s.select("article.row")) == 2 and s.select_one('a[href$="/blog/"]')


def test_hero_portrait(site):
    img = html(site, "/").select_one(".hero img.hero__portrait")
    assert img and "Brian Duenas" in img["alt"]
    assert img["width"] == "800" and img["height"] == "800"  # reserves space, no layout shift
    assert "profile-480.jpg 480w" in img["srcset"] and "profile.jpg 800w" in img["srcset"]
    assert (site / "images/profile.jpg").exists() and (site / "images/profile-480.jpg").exists()


def test_share_preview_image_on_every_page(site):
    for u in ["/", "/resume/", "/blog/", "/notes/macos-sd-card-read-only/"]:
        meta = html(site, u).select_one('meta[property="og:image"]')
        assert meta and meta["content"] == "https://bduenas.com/images/profile.jpg", u


def test_founder_section(site):
    s = html(site, "/").select_one("[data-section=founder]")
    assert s.get("id") == "gathrly"
    text = s.get_text(" ", strip=True)
    assert "Gathrly" in text and "2018" in text and "2025" in text
    link = s.select_one('a[href="https://gathrlyapp.com/"]')
    assert link and link.get("rel") == ["noopener"]
    # kept non-technical on purpose
    for word in ["Capacitor", "Kubernetes", "API", "TypeScript", "Swift"]:
        assert word not in text, word
    assert "\u2014" not in text


def test_capacitor_pr_tagged_gathrly(site):
    row = next(r for r in html(site, "/").select(".oss__row") if "capacitor-calendar" in r.get_text())
    assert row.select_one(".oss__context").get_text(strip=True) == "While building Gathrly"
