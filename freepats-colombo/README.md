# ColomboADK, General MIDI version

The **Colombo Hydrogen Drumkit 1.0** by **Marcos Guglielmetti** (2006), assembled
as a SoundFont by Roberto (roberto@zenvoid.org) for the **FreePats** project
(version 2020-05-30). An acoustic kit: a bass drum, two side sticks, three
snares, three toms (and their double strokes), four hi-hats (closed, open,
semi-open, long open), two crashes, two rides and their cups.

## Why this is not the original file

The FreePats SoundFont puts the kit on its own keys, 48 to 69, not on the
General MIDI drum keys every drum program and DrumPersona expect. Loaded as it
is, a General MIDI drum part plays the wrong pieces, or nothing.

**`ColomboADK-FreePats-20200530-GM.sf2` is the same kit moved to the General
MIDI keys, and nothing else.** Every sample, level, envelope and velocity layer
is the original's; only which key plays each piece changed. Each moved key was
checked to play exactly the same sound as its old key (rendered note for note,
22 of 22 identical). `../tools/remap_keys.py gm-keys.json` makes it from the
original, and always gives the same file.

The original, unchanged, is kept too, for anyone who wants the FreePats key map.

## Source and licence

- Source: [FreePats](https://freepats.zenvoid.org/), release
  [`ColomboADK-FreePats-SF2-20200530.7z`](https://github.com/freepats/colomboADK/releases/tag/2020-05-30)
  of [freepats/colomboADK](https://github.com/freepats/colomboADK)
  (SHA-256 of the archive: `e28bfa57271d04c1a496ce82333d05fff300b59ffd39cf0904dd6dbec54fb2e1`),
  extracted on 2026-11-13.
- Licence: **GNU GPL version 2 or later, with an exception** (text of the GPL in
  `LICENSE`). The author's notice, as it ships with the kit:

  > As a special exception, if you create a composition which uses these sound
  > samples and/or the hydrogen drumkit, and mix these sound samples and/or the
  > hydrogen drumkit or unaltered portions of these sound samples and/or the
  > hydrogen drumkit into the composition, these sound samples and/or the
  > hydrogen drumkit do not by themselves cause the resulting composition to be
  > covered by the GNU General Public License.

  In short: music made with the kit is yours, under any licence. The kit itself,
  shared or changed, stays under the GPL. The General MIDI version is such a
  change, made by drumpersona-kits; it keeps the GPL and the exception (the
  author lets a changed version extend it), and its source is the original plus
  `gm-keys.json` and `../tools/remap_keys.py`.
- Credit: Marcos Guglielmetti (marcospcmusica@gmail.com) for the samples and the
  Hydrogen kit; the FreePats project for the SoundFont version.

| File | Release | Size | SHA-256 |
|---|---|---|---|
| `ColomboADK-FreePats-20200530-GM.sf2` (General MIDI keys) | [`freepats-colombo-gm-2020-05-30`](https://github.com/gaumondp/drumpersona-kits/releases/tag/freepats-colombo-gm-2020-05-30) | 21 MB | `2e0af482b75076fd58ff79db270ed1a305f24978037f4d01e6e024b1b0d7735e` |
| `ColomboADK-FreePats-20200530.sf2` (original, FreePats keys) | [`freepats-colombo-2020-05-30`](https://github.com/gaumondp/drumpersona-kits/releases/tag/freepats-colombo-2020-05-30) | 21 MB | `68604bc9327bf9d5fb9ca848419185655891201d42f6b1d97d471d7f9a959e48` |

The original is the `.sf2` inside the FreePats archive, unchanged; only its name
lost its spaces (`ColomboADK FreePats 20200530.sf2`).

## Keys

| Piece | Original key | General MIDI key (GM version) |
|---|---|---|
| bass drum | 48 | 36 Bass Drum 1 |
| side stick | 49 | 37 Side Stick |
| snare drum | 51 | 38 Acoustic Snare |
| snare drum 2 | 52 | 40 Electric Snare |
| closed hi-hat | 57 | 42 Closed Hi-Hat |
| open hi-hat | 58 | 46 Open Hi-Hat |
| high tom | 56 | 48 Hi-Mid Tom |
| mid tom | 55 | 45 Low Tom |
| low tom | 54 | 43 High Floor Tom |
| crash (16") | 61 | 49 Crash Cymbal 1 |
| ride (16") | 62 | 51 Ride Cymbal 1 |
| cup (16") | 63 | 53 Ride Bell |
| crash (20") | 64 | 57 Crash Cymbal 2 |
| ride (20") | 65 | 59 Ride Cymbal 2 |
| side stick 2 | 50 | 110 (no General MIDI piece) |
| snare drum dry | 53 | 111 (no General MIDI piece) |
| semi-open hi-hat | 59 | 112 (no General MIDI piece) |
| long open hi-hat | 60 | 113 (no General MIDI piece) |
| cup (20") | 66 | 114 (no General MIDI piece) |
| low, mid, high tom double strokes | 67, 68, 69 | 115, 116, 117 (no General MIDI piece) |

The three toms sit on the keys of DrumPersona's three tom pads (48, 45, 43). The
kit has no pedal hi-hat sample (General MIDI 44).
