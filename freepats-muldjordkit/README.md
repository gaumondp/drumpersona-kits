# MuldjordKit, General MIDI version

Recorded by **Lars Muldjord** in 2009-2010 (the original kit is made for
[DrumGizmo](https://www.drumgizmo.org)); its stereo SoundFont version was
assembled by Roberto (roberto@zenvoid.org) for the **FreePats** project. A rock
/ metal kit: 2 kicks, 3 hanging toms, 1 floor tom, 1 snare, 1 hi-hat, 2 crashes,
2 rides, 1 china, with velocity layers.

## Why this is not the original file

The FreePats SoundFont puts the kit on its own keys, 48 to 66 (kick on 48, snare
on 50, hi-hat on 52...), not on the General MIDI drum keys every drum program
and DrumPersona expect (kick 36, snare 38, closed hi-hat 42...). Loaded as it
is, a General MIDI drum part plays the wrong pieces, or nothing.

**`MuldjordKit-20201018-GM.sf2` is the same kit moved to the General MIDI keys,
and nothing else.** Every sample, level, envelope and velocity layer is the
original's; only which key plays each piece changed. Each moved key was checked
to play exactly the same sound as its old key (rendered note for note, 19 of 19
identical). `../tools/remap_keys.py gm-keys.json` makes it from the original,
and always gives the same file.

The original, unchanged, is kept too (`MuldjordKit-20201018.sf2`), for anyone
who wants the FreePats key map.

## Source and licence

- Source: [freepats.zenvoid.org, Acoustic Drum Kit](https://freepats.zenvoid.org/Percussion/acoustic-drum-kit.html),
  file from the FreePats release
  [`MuldjordKit-SF2-20201018.7z`](https://github.com/freepats/muldjordkit/releases/tag/2020-10-18)
  (SHA-256 of the archive: `aef4c9e0a96f9a899a7838f65ff07565f6af247bbb4ff31e24dba3331a671a96`),
  extracted on 2026-11-13.
- Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), text in `LICENSE`
  (the licence file from the archive). Credit: Lars Muldjord for the kit, the
  FreePats project for its SoundFont version. The General MIDI version is a
  change made by drumpersona-kits (this folder), under the same licence, as
  CC BY 4.0 allows with the change stated.

| File | Release | Size | SHA-256 |
|---|---|---|---|
| `MuldjordKit-20201018-GM.sf2` (General MIDI keys) | [`freepats-muldjordkit-gm-2020-10-18`](https://github.com/gaumondp/drumpersona-kits/releases/tag/freepats-muldjordkit-gm-2020-10-18) | 209 MB | `f4370c66a80dc74efd15984f98391565289ccb1a8ee2fc00ed9bb6f563edf16a` |
| `MuldjordKit-20201018.sf2` (original, FreePats keys) | [`freepats-muldjordkit-2020-10-18`](https://github.com/gaumondp/drumpersona-kits/releases/tag/freepats-muldjordkit-2020-10-18) | 209 MB | `fec611c55b5e1c53ea3e6df1e6779c9f18502fc6455ee45edc51d5a2b4881055` |

The original is the `.sf2` inside the FreePats archive, unchanged; only its name
lost its space (`MuldjordKit 20201018.sf2` became `MuldjordKit-20201018.sf2`).

## Keys

| Piece | Original key | General MIDI key (GM version) |
|---|---|---|
| kick left | 48 | 36 Bass Drum 1 |
| kick right | 49 | 35 Acoustic Bass Drum |
| snare 1 | 50 | 38 Acoustic Snare |
| snare 2 | 51 | 40 Electric Snare |
| hi-hat closed | 52 | 42 Closed Hi-Hat |
| hi-hat open | 53 | 46 Open Hi-Hat |
| ride left | 54 | 51 Ride Cymbal 1 |
| ride bell left | 55 | 53 Ride Bell |
| ride right | 56 | 59 Ride Cymbal 2 |
| crash left | 58 | 49 Crash Cymbal 1 |
| crash right | 59 | 57 Crash Cymbal 2 |
| china | 60 | 52 Chinese Cymbal |
| tom 1 | 61 | 50 High Tom |
| tom 2 | 62 | 48 Hi-Mid Tom |
| tom 3 | 63 | 45 Low Tom |
| tom 4 (floor) | 64 | 43 High Floor Tom |
| ride bell right | 57 | 84 (no General MIDI piece) |
| snare rest 1 | 65 | 85 (no General MIDI piece) |
| snare rest 2 | 66 | 86 (no General MIDI piece) |

The kit has no pedal hi-hat sample (General MIDI 44) and no low floor tom (41).
