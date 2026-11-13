# drumpersona-kits

Free sampled drum kits for [DrumPersona](https://github.com/gaumondp/drumpersona),
kept in one place so they stay available. Each kit is a SoundFont 2 file (`.sf2`)
that DrumPersona imports with **Edit kit → Import .sf2…**. Any SoundFont player
can play them too.

Only kits whose author published them under an open licence are kept here, each
exactly as its author published it.

## The kits

The files are attached to the [Releases](https://github.com/gaumondp/drumpersona-kits/releases)
of this repository, not stored in its history. `SHA256SUMS` lists their checksums.

| File | Size | What it is |
|---|---|---|
| `Black_Pearl_4_LV2.sf2` | 19 MB | a 4-piece acoustic kit |
| `Red_Zeppelin_4_LV2.sf2` | 25 MB | a 4-piece acoustic kit |
| `Blonde_Bop_LV2.sf2` | 30 MB | a jazz (bop) kit |
| `Blonde_Bop_HR_LV2.sf2` | 29 MB | the same kit, "HR" variant |
| `Buskmans_Holiday.sf2` | 42 MB | hand percussion, not a drum kit |

All five are the **AVL Drumkits** by Glen MacArthur, recorded with 5 to 10
velocity layers per piece.

- Source: [bandshed.net/avldrumkits](https://www.bandshed.net/avldrumkits/),
  files from [bandshed.net/sounds/AVLDrumkits_SF2](https://www.bandshed.net/sounds/AVLDrumkits_SF2/)
  (dated 2023-09-05), copied here unchanged on 2026-11-13.
- Licence: [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/), text in `LICENSE`.
  As the author puts it, music made with the kits may be shared or sold without
  attribution; attribution and the same licence apply to the samples and the
  kit files themselves, when they are shared or changed.
- The same kits exist for Hydrogen, in SFZ and as an LV2 plug-in: see the source page.

## Their keys

The AVL kits follow their own key map, close to General MIDI but not identical:
kick 36, snare 38, closed hat 42, pedal hat 44, crash 49, ride 51, ride bell 53
as in General MIDI, but 48 is a swish hat (General MIDI: a tom), 46 a semi-open
hat, and the toms sit on 41, 43, 45 and 47. The author's note-name files
([AVL-Drumkits-1.0-Midnams.zip](https://www.bandshed.net/sounds/midnams/AVL-Drumkits-1.0-Midnams.zip))
list every key. In DrumPersona, a pad whose sound is not the piece it names can
be redirected with **Edit kit**. *Buskmans Holiday* is a percussion set on its
own map.

## Adding a kit

A kit is added only when its author states an open licence (CC0, CC BY, CC BY-SA,
or equivalent) and the file is copied unchanged from the author's own page.
Record the source page, the file's date, the licence and its checksum here.

## Licence of this repository

The kit files are under the licence of their author (above). This README and
the checksum file are under CC BY-SA 3.0 as well. This repository is not
affiliated with the authors of the kits.
