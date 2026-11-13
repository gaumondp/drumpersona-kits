# drumpersona-kits

Free, openly licensed sampled drum kits for
[DrumPersona](https://github.com/gaumondp/drumpersona), kept in one place so
they stay available. Each kit is a SoundFont 2 file (`.sf2`) that DrumPersona
imports with **Edit kit → Import .sf2…**. Any SoundFont player can play them too.

Each kit is copied here as its author published it (or, when its licence allows,
changed only to work better as a drum kit, the original kept next to it), and
keeps its author's licence. This repository is not affiliated with the authors
of the kits.

## The kits

The files are attached to the [Releases](https://github.com/gaumondp/drumpersona-kits/releases)
of this repository (one release per collection), not stored in its history.
Each collection's folder holds its author, source, licence text, checksums and
key map.

<!-- kits:begin -->
| Kit | Collection | Author | Licence | What it is | Size |
|---|---|---|---|---|---|
| Black Pearl | [AVL Drumkits](avl-drumkits/) | Glen MacArthur | CC BY-SA 3.0 | 4-piece acoustic kit | 19 MB |
| Red Zeppelin | [AVL Drumkits](avl-drumkits/) | Glen MacArthur | CC BY-SA 3.0 | 4-piece acoustic kit | 25 MB |
| Blonde Bop | [AVL Drumkits](avl-drumkits/) | Glen MacArthur | CC BY-SA 3.0 | jazz kit | 30 MB |
| Blonde Bop HR | [AVL Drumkits](avl-drumkits/) | Glen MacArthur | CC BY-SA 3.0 | jazz kit | 29 MB |
| Buskmans Holiday | [AVL Drumkits](avl-drumkits/) | Glen MacArthur | CC BY-SA 3.0 | hand percussion | 42 MB |
| MuldjordKit (General MIDI) | [MuldjordKit (FreePats)](freepats-muldjordkit/) | Lars Muldjord, FreePats | CC BY 4.0 | rock / metal acoustic kit, moved to the General MIDI keys | 209 MB |
| ColomboADK (General MIDI) | [ColomboADK (FreePats)](freepats-colombo/) | Marcos Guglielmetti, FreePats | GPL-2.0-or-later + exception | acoustic kit, moved to the General MIDI keys | 21 MB |
| World Percussion (General MIDI) | [World Percussion (FreePats)](freepats-world-percussion/) | FreePats | CC0 | hand percussion, moved to the General MIDI keys | 9 MB |
| GeneralUser GS 2.0.3 | [GeneralUser GS](generaluser-gs/) | S. Christian Collins | GeneralUser GS License v2.0 | a General MIDI bank with 13 drum kits (sample origin not guaranteed) | 31 MB |
<!-- kits:end -->

The AVL kits are close to the General MIDI key map but not identical: see their
key table. In DrumPersona, a pad whose sound is not the piece it names can be
redirected with **Edit kit**. `tools/remap_keys.py` makes the General MIDI
versions from the originals, with each collection's `gm-keys.json`.

## Adding a kit

A kit is added only when:

1. its author states an open licence on their own page (CC0, CC BY, CC BY-SA,
   MIT, Apache-2.0, GPL, or an author's own licence that allows redistribution
   and changes), not only a re-uploader or an archive;
2. the file is copied unchanged from the author's own release (extracted from
   its archive if it ships in one);
3. its source page, the file's date, its licence and its SHA-256 are recorded in
   its collection's folder, with the licence text.

A kit may also be **changed** here, only to make it work better as a drum kit
(today: moving it to the General MIDI keys), and only when its licence allows
changes (no ND licence). Then the original is kept unchanged next to it, the
change is explained in the collection's README with the reason, the script that
makes it is in the folder, and the changed file keeps the original's licence
(and the same licence again for a share-alike one).

Kits under a non-commercial (NC) or no-derivatives (ND) licence, or of unknown
origin, are not added. When an author says the origin of some samples is not
fully known, the kit is marked so in the table and its README. A new version of
a collection is a new release; a published release is never changed.

## For later

- **Salamander Drumkit** by Alexander Holm (CC BY-SA 3.0): published in SFZ only.
  It needs a conversion to SoundFont 2, which loses its random round-robins and
  its controller-driven hi-hat.

## Licence of this repository

Each kit file is under its author's licence (see its folder). The README files
of this repository are under CC BY-SA 3.0.
