#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check drumpersona-kits-index.xml by the rules DrumPersona holds it to.

    tools/check_index.py              the index alone (offline)
    tools/check_index.py --remote     also: every file is a release asset of this
                                      repository, of the size the index says
    tools/check_index.py --sha DIR    also: the files in DIR (by name) have the
                                      index's SHA-256

Exit 1 on any finding. DrumPersona's own tests apply the same rules to the copy
it embeds; keep the two lists of licences the same.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "drumpersona-kits-index.xml")
REPO = "gaumondp/drumpersona-kits"
URL_PREFIX = f"https://github.com/{REPO}/releases/download/"
LICENCES = {"CC0-1.0", "CC-BY-3.0", "CC-BY-4.0", "CC-BY-SA-3.0", "CC-BY-SA-4.0", "MIT", "Apache-2.0",
            "GPL-2.0-or-later", "GPL-3.0-or-later", "LicenseRef-GeneralUser-GS-2.0"}
ID = re.compile(r"^[0-9abcdefghjkmnpqrstvwxyz]{8}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
MAX_SIZE = 1 << 30
PIECES = {"Kick", "Kick2", "Snare", "SnareRimshot", "SideStick", "ClosedHat", "PedalHat", "OpenHat", "HighTom",
          "HighMidTom", "LowMidTom", "LowTom", "FloorTom", "LowFloorTom", "Ride", "RideBell", "Crash1", "Crash2",
          "China", "Splash", "Cowbell", "Tambourine", "Triangle", "CongaHigh", "CongaLow", "Bongo", "Timbale",
          "Maracas", "Cabasa", "Claves", "Guiro", "Agogo", "WoodBlock", "HandClap", "Sticks", "Snare2"}


def check(root):
    findings, kits, ids = [], [], set()
    if root.tag != "KitIndex" or root.get("schemaVersion") != "1":
        return ["the root must be <KitIndex schemaVersion=\"1\">"], kits
    if not (root.get("revision") or "").isdigit():
        findings.append("revision must be a whole number")
    for col in root.findall("Collection"):
        cid = col.get("id", "?")
        for attr in ("id", "name", "author", "licence", "source"):
            if not col.get(attr):
                findings.append(f"collection {cid}: no {attr}")
        if col.get("licence") not in LICENCES:
            findings.append(f"collection {cid}: licence {col.get('licence')} is not in the accepted list")
        if not (col.get("source") or "").startswith("https://"):
            findings.append(f"collection {cid}: source is not https")
        if not os.path.isdir(os.path.join(ROOT, cid)):
            findings.append(f"collection {cid}: no folder of that name")
        for kit in col.findall("Kit"):
            kid = kit.get("id", "?")
            where = f"kit {kid} ({kit.get('name')})"
            if not ID.match(kid):
                findings.append(f"{where}: id is not 8 Crockford base32 characters")
            if kid in ids:
                findings.append(f"{where}: id used twice")
            ids.add(kid)
            if not kit.get("name"):
                findings.append(f"{where}: no name")
            if kit.get("nature") not in ("drums", "percussion"):
                findings.append(f"{where}: nature must be drums or percussion")
            if not (kit.get("url") or "").startswith(URL_PREFIX):
                findings.append(f"{where}: url is not a release asset of {REPO}")
            if not SHA.match(kit.get("sha256") or ""):
                findings.append(f"{where}: sha256 is not 64 lowercase hex digits")
            size = kit.get("size") or ""
            if not size.isdigit() or not 0 < int(size) <= MAX_SIZE:
                findings.append(f"{where}: size must be 1 byte to 1 GB")
            for key in kit.findall("Key"):
                if key.get("piece") not in PIECES:
                    findings.append(f"{where}: unknown piece {key.get('piece')}")
                if key.get("none") != "true" and not (key.get("key") or "").isdigit():
                    findings.append(f"{where}: a Key needs key=\"0..127\" or none=\"true\"")
                elif key.get("none") != "true" and int(key.get("key")) > 127:
                    findings.append(f"{where}: key above 127")
            kits.append(kit)
    return findings, kits


def remote(kits):
    findings = []
    assets = {}
    with urllib.request.urlopen(f"https://api.github.com/repos/{REPO}/releases?per_page=100", timeout=30) as r:
        for rel in json.load(r):
            for a in rel["assets"]:
                assets[a["browser_download_url"]] = a["size"]
    for kit in kits:
        url = kit.get("url")
        if url not in assets:
            findings.append(f"kit {kit.get('id')}: no such release asset: {url}")
        elif str(assets[url]) != kit.get("size"):
            findings.append(f"kit {kit.get('id')}: the asset is {assets[url]} bytes, the index says {kit.get('size')}")
    return findings


def local_sha(kits, folder):
    findings = []
    for kit in kits:
        path = os.path.join(folder, kit.get("url").rsplit("/", 1)[1])
        if not os.path.isfile(path):
            findings.append(f"kit {kit.get('id')}: {path} not found")
            continue
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                h.update(block)
        if h.hexdigest() != kit.get("sha256"):
            findings.append(f"kit {kit.get('id')}: {path} has SHA-256 {h.hexdigest()}")
    return findings


def main(argv):
    findings, kits = check(ET.parse(INDEX).getroot())
    if "--remote" in argv:
        findings += remote(kits)
    if "--sha" in argv:
        findings += local_sha(kits, argv[argv.index("--sha") + 1])
    for f in findings:
        print(f)
    print(f"{len(kits)} kits, {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
