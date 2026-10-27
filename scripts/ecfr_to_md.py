"""Turn an eCFR versioner XML download into one Markdown file per section, for `p2 ingest`.

Usage: python scripts/ecfr_to_md.py ../p2-raw/title-29-part-1926.xml ../p2-raw/osha1926
The XML came from https://www.ecfr.gov/api/versioner/v1/full/2026-10-14/title-29.xml?part=1926
(the endpoint needs an Accept-Encoding header, so curl --compressed).
Each section (DIV8) becomes <number>.md: "# <heading>", a blank line, its paragraphs.
History citations, authority lines and editorial notes are left out, as in the shared corpus;
appendices and empty [Reserved] sections are skipped.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SKIP = {"CITA", "AUTH", "SOURCE", "EDNOTE", "SECAUTH", "HEAD"}


def text(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def main(src, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for sec in ET.parse(src).getroot().iter("DIV8"):
        head = text(sec.find("HEAD")).removeprefix("§").strip()
        body = [text(el) for el in sec if el.tag not in SKIP]
        body = [b for b in body if b]
        if not body:
            continue
        (out / f"{sec.get('N')}.md").write_text(f"# {head}\n\n" + "\n\n".join(body) + "\n", encoding="utf-8", newline="\n")
        n += 1
    print(f"wrote {n} sections to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
