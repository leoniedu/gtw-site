#!/usr/bin/env python3
"""Builds privacy.html and support.html from src/*.md, and the Brazilian Portuguese
pt/privacy.html and pt/support.html from src/pt/*.md, with pandoc.

    python3 build.py

index.html is hand-written. Edit the Markdown in src/ (or copy updated text from the
app repo's docs/store/), run this, and commit the generated .html files: the site is
served as plain static files (see .nojekyll).
"""
import pathlib
import subprocess

root = pathlib.Path(__file__).parent
languages = {
    # code: (template, source dir, output dir, page titles/descriptions)
    "en": ("page.html", "src", ".", {
        "privacy": ("Privacy policy", "How GtW handles your data: it never leaves your Apple Health database."),
        "support": ("Support", "Help and contact for GtW, short timed sets on Apple Watch."),
    }),
    "pt-BR": ("page.pt-BR.html", "src/pt", "pt", {
        "privacy": ("Política de privacidade", "Como o GtW trata seus dados: eles nunca saem do app Saúde."),
        "support": ("Suporte", "Ajuda e contato do GtW, séries curtas cronometradas no Apple Watch."),
    }),
}

for code, (template_name, src, out, pages) in languages.items():
    template = (root / "templates" / template_name).read_text()
    for name, (title, description) in pages.items():
        body = subprocess.run(
            ["pandoc", "-f", "gfm", "-t", "html", str(root / src / f"{name}.md")],
            check=True, capture_output=True, text=True,
        ).stdout
        html = (template.replace("{{title}}", title)
                        .replace("{{description}}", description)
                        .replace("{{name}}", name)
                        .replace("{{content}}", body))
        (root / out / f"{name}.html").write_text(html)
        print(f"wrote {out}/{name}.html")
