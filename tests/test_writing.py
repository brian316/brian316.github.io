from conftest import html


def test_writing_index_lists_all_pages(site):
    rows = html(site, "/blog/").select("article.row")
    titles = [r.select_one(".row__title").get_text(strip=True) for r in rows]
    assert titles == ["macOS SD Card Read Only Issues", "Init Blog"]  # newest first, merged
    assert [r.select_one(".row__tags").get_text(strip=True) for r in rows] == ["NOTE", "BLOG"]


def test_notes_section_still_lists(site):
    assert len(html(site, "/notes/").select("article.row")) == 1


def test_about_prose_mode(site):
    s = html(site, "/about/")
    assert s.select_one("h1").get_text(strip=True) == "About" and s.select_one(".prose")


def test_post_page(site):
    s = html(site, "/notes/macos-sd-card-read-only/")
    assert s.select_one("h1.display-lg").get_text(strip=True) == "macOS SD Card Read Only Issues"
    assert s.select_one("time[datetime='2025-05-05']") and s.select_one(".prose pre")
    back = s.select_one('a.back-link[href$="/blog/"]')
    assert back and back.get_text(strip=True).startswith("←")


def test_rows_without_deck_render_clean(site):
    for r in html(site, "/blog/").select("article.row"):
        assert "None" not in r.get_text()
        deck = r.select_one(".row__deck")
        assert deck is None or deck.get_text(strip=True)
