#!/usr/bin/env python3
"""Builds privacy.html and support.html from src/*.md with pandoc.

    python3 build.py

index.html is hand-written. Edit the Markdown in src/ (or copy updated text from the
app repo's docs/store/), run this, and commit the generated .html files: the site is
served as plain static files (see .nojekyll).
"""
import pathlib
import subprocess

root = pathlib.Path(__file__).parent
template = (root / "templates" / "page.html").read_text()

pages = {
    "privacy": ("Privacy policy", "How GtW handles your data: it never leaves your Apple Health database."),
    "support": ("Support", "Help and contact for GtW, short timed sets on Apple Watch."),
}

for name, (title, description) in pages.items():
    body = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html", str(root / "src" / f"{name}.md")],
        check=True, capture_output=True, text=True,
    ).stdout
    html = (template.replace("{{title}}", title)
                    .replace("{{description}}", description)
                    .replace("{{content}}", body))
    (root / f"{name}.html").write_text(html)
    print(f"wrote {name}.html")
