#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the kit table of README.md (between its kits:begin and kits:end markers)
from drumpersona-kits-index.xml, so the two never differ.

    tools/write_readme.py           rewrite the table
    tools/write_readme.py --check   exit 1 if the table is not what the index gives
"""
import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- kits:begin -->", "<!-- kits:end -->"
LICENCE_NAMES = {"CC0-1.0": "CC0", "CC-BY-3.0": "CC BY 3.0", "CC-BY-4.0": "CC BY 4.0", "CC-BY-SA-3.0": "CC BY-SA 3.0",
                 "CC-BY-SA-4.0": "CC BY-SA 4.0", "MIT": "MIT", "Apache-2.0": "Apache-2.0",
                 "GPL-2.0-or-later": "GPL-2.0-or-later", "GPL-3.0-or-later": "GPL-3.0-or-later",
                 "LicenseRef-GeneralUser-GS-2.0": "GeneralUser GS License v2.0"}


def table():
    root = ET.parse(os.path.join(ROOT, "drumpersona-kits-index.xml")).getroot()
    lines = ["| Kit | Collection | Author | Licence | What it is | Size | File |", "|---|---|---|---|---|---|---|"]
    for col in root.findall("Collection"):
        licence = LICENCE_NAMES.get(col.get("licence"), col.get("licence"))
        if col.get("originNotGuaranteed") == "true":
            licence += " (sample origin not guaranteed)"
        for kit in col.findall("Kit"):
            mb = round(int(kit.get("size")) / 1048576)
            url = kit.get("url")
            what = "drum kit" if kit.get("nature") == "drums" else "percussion"
            lines.append(f"| {kit.get('name')} | [{col.get('name')}]({col.get('id')}/) | {col.get('author')} | {licence} "
                         f"| {what} | {mb} MB | [{url.rsplit('/', 1)[1]}]({url}) |")
    return "\n".join(lines)


def main(argv):
    path = os.path.join(ROOT, "README.md")
    text = open(path).read()
    a, b = text.index(BEGIN) + len(BEGIN), text.index(END)
    new = text[:a] + "\n" + table() + "\n" + text[b:]
    if "--check" in argv:
        if new != text:
            print("README.md's table is not the index's: run tools/write_readme.py")
            return 1
        return 0
    open(path, "w").write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
