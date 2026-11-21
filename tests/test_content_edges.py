from conftest import html


def test_summary_deck_not_double_escaped(scratch_site):
    deck = html(scratch_site, "/blog/").select_one(".row__deck")
    assert deck.get_text(strip=True) == "Fish & chips with code<x>."


def test_literal_template_braces_in_markdown_render(scratch_site):
    pre = html(scratch_site, "/notes/edge-cases/").select_one(".prose pre")
    assert "{{ .Values.image }}" in pre.get_text()


def test_oss_more_link_works_logged_out(site):
    a = html(site, "/").select_one(".oss__more a")
    assert a["href"].startswith("https://github.com/search?") and "type=pullrequests" in a["href"]
