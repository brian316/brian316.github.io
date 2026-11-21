# AGENTS.md

Personal portfolio and blog for bduenas.com. It's a Zola static site with its own templates and Sass, and no theme.

## Commands
- Preview: `zola serve`, which serves http://127.0.0.1:1111 with live reload. `zola build` writes to `public/`, which is gitignored.
- Tests: `uv run --with pytest --with beautifulsoup4 pytest tests -q`. There's no project venv; `uv run --with` supplies the dependencies.
- Single test: same command with a test ID, e.g. `uv run --with pytest --with beautifulsoup4 pytest tests/test_home.py::test_hero -q`.
- Link check: `zola check --skip-external-links`.
- The test fixture (`tests/conftest.py`) builds the site into a temp dir and **fails on any Zola `WARN`**. `scratch_site` builds a copy of the repo with an extra edge-case post.

## Deploy
- Every push to `main` deploys to production. `.github/workflows/build.yaml` runs `shalzz/zola-deploy-action`, which builds to the `gh-pages` branch; `static/CNAME` holds the domain, bduenas.com. Don't push without being asked.
- The deploy action pins **Zola 0.23.6**, so keep local Zola on the same version.

## Zola 0.23 / Tera 2 gotchas (old Zola/Tera habits break the build)
- There are no macros, shortcodes, `concat` or `slice`. Use components (`templates/components/ui.html`), spread (`[...a.pages, ...b.pages]`) and slicing (`list[:6]`).
- Components can't see template context. Pass data in explicitly, e.g. `{{<ui.icon_links extra={config.extra} />}}`.
- Undefined variables are errors. For optional data fields, use `x?.field` or `x?.field or "default"`.
- You can't read a property off a function call (`get_section(...).pages`). Assign the result to a variable first.
- Internal links: use `get_url(path="@/blog/_index.md")`. `get_url(path="blog/")` drops the trailing slash, which causes a redirect, and a test checks for this.
- `skip_content_templating = ["**/*.md"]`: Markdown isn't run through Tera, so literal `{{ }}` (e.g. Helm snippets) is safe. This also means `templates/shortcodes/` is dead code.
- Syntax highlighting is giallo in class mode, emitted as `/giallo.css`. `sass/_prose.scss` overrides its white `.z-code` background.

## Where content lives
- Homepage and `/resume/` are rendered from `data/resume.toml` and `data/work.toml`, loaded with `load_data`. Hero copy and contact details are `[extra]` in `config.toml`. Edit the data, not the templates.
- `data/resume.toml` mirrors `static/resume.pdf`, so keep them in sync. The PDF may contain Brian's phone number and Yahoo email; rendered HTML must not (`test_no_private_contact_in_html`).
- `/blog/` is a merged Writing index of blog and notes (`templates/writing.html`). Nav links are hard-coded in `templates/base.html`; they don't loop over sections.
- Posts get their date from the `YYYY-MM-DD-` filename prefix. A page without a date is silently dropped from the lists.

## Design rules (tests enforce most of these)
- Tokens are in `sass/_tokens.scss` and come from littlemight.com.
- Bright accent `#f7591f` is only for display-size text, button fills, and text on the dark `.band--dark`. Small accent text on paper uses `--accent-text` (`#c2410c`).
- No `box-shadow`, and no em dashes (—) in rendered pages.
- The Gathrly founder section and resume entry stay non-technical: no stack or tool names. Technical Gathrly context goes only in the OSS `context` tag.
- Tests assert exact copy, e.g. the hero headline, OSS blurb, and experience row count. Update `tests/test_home.py` when you change copy.
- Favicons are generated: `uv run --with pillow python scripts/make_favicon.py <InstrumentSerif-Regular.ttf>`.

## Local-only files
- `docs/superpowers/` (specs and plans) and `.superpowers/` (scratch, screenshots) are gitignored on purpose. **Never commit them or `git add -f` them.**
- Git worktrees don't contain ignored files. When working in a worktree, refer to specs and plans by absolute path in this checkout.

## Machine quirk
- The macOS firewall silently drops LAN connections to Homebrew's unsigned `zola` binary. For phone or LAN previews, run `zola build --base-url http://<lan-ip>:<port>` and serve `public/` with `/usr/bin/python3 -m http.server <port> --bind 0.0.0.0`.
