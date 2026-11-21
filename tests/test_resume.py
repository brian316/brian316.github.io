from conftest import html


def test_resume_page(site):
    s = html(site, "/resume/")
    assert s.select_one('a.btn[href$="/resume.pdf"]').get_text(strip=True) == "Download PDF"
    text = s.get_text(" ")
    for t in ["Quantum Applications Engineer", "Research Software Engineer", "Partner Technical Specialist",
              "Cloud Engineer", "Life Elixir", "Panasonic Avionics", "Computer Engineering", "Kubernetes, OpenShift"]:
        assert t in text, t
    assert len(s.select(".skills__row")) == 5


def test_pdf_published(site):
    assert (site / "resume.pdf").stat().st_size > 50_000


def test_optional_fields_omitted(site):
    # roles without `end` render "Present"; jobs without location render no stray separator
    text = html(site, "/resume/").get_text(" ")
    assert "Present" in text and "· ·" not in text and "None" not in text


def test_no_private_contact_in_html(site):
    for f in site.rglob("*.html"):
        t = f.read_text()
        assert "909-894-8356" not in t and "9098948356" not in t and "yahoo" not in t.lower(), f
