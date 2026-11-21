import re


def test_tokens_present(css):
    for t in ["#f5f4ed", "#0b0d0b", "#52534e", "#c2410c", "#f7591f"]:
        assert t in css.lower(), t


def test_no_shadows(css):
    assert "box-shadow" not in css


def test_focus_visible(css):
    assert ":focus-visible" in css


def test_reduced_motion(css):
    assert "prefers-reduced-motion" in css


def test_bright_accent_only_on_display_or_fill(css):
    # Bright accent as text is 2.97:1 on paper: only display-size type, or on the ink band (5.9:1).
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(r"(?<![-\w])color:\s*(#f7591f|var\(--accent\))", body, re.I):
            assert "display" in sel or "band--dark" in sel, sel


def test_classes_defined(css):
    for c in [".row__date", ".section-head__rule", ".btn", ".card", ".oss__row",
              ".status--merged", ".skip-link", ".prose", ".rail__cell", ".band--dark"]:
        assert c in css, c


def test_code_blocks_override_giallo_white(css):
    assert ".z-code" in css


def test_hero_portrait_beside_text_from_640px(css):
    # Two-column hero must start at the small breakpoint, not only on desktop.
    flat = re.sub(r"\s+", "", css)
    m = re.search(r"@media\(min-width:640px\)\{\.hero__inner\{[^}]*grid-template-columns", flat)
    assert m, "hero two-column layout not enabled at 640px"


def test_hero_short_viewport_padding(css):
    flat = re.sub(r"\s+", "", css)
    assert re.search(r"@media\(min-width:640px\)and\(max-height:500px\)\{\.hero__inner\{padding-top:40px", flat)
