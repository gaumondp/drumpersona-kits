# MuseScore General

The General MIDI SoundFont of MuseScore, version 0.2 (13 May 2020): a whole
General MIDI bank with 37 drum kits in bank 128 (Standard, Room, Power,
Electronic, TR-808, Jazz, Brush, Orchestra Kit and their variants, and marching
snare, bass, tenor and cymbals). It is built on FluidR3 by Frank Wen (mono
version by Michael Cowgill), adapted by **S. Christian Collins**, with the Temple
Blocks of Ethan Winer and the Drumline Cymbals of Michael Schorsch.

- Source: [ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/](https://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/),
  `MuseScore_General.sf2` and `MuseScore_General_License.md`, copied here
  unchanged on 2026-11-14.
- Licence: **MIT** (text in `LICENSE`, the author's file as published). Its
  acknowledgements and copyright notices must be kept in any derivative work:
  they are in `LICENSE`, and in the INFO chunk of the drum-kit file, copied as is.
- **Origin of the samples not guaranteed.** FluidR3 was made in part from
  samples found in the public domain, which its author edited, and largely from
  his own recordings; which sample is which is not documented.

## Why a drum-kit file

The whole bank is 216 MB, of which DrumPersona plays only the drum kits.
`MuseScore_General-Drums-0.2.sf2` holds the 37 presets of bank 128, the 46
instruments they use and their 207 samples: 21 MB. Nothing in it is changed:
every preset, instrument, zone, generator, modulator and sample point is copied
from the original, only the indexes between them and the sample offsets are
renumbered (SoundFont 2.04 specification, sections 5 to 8). The MIT licence
allows it. The original stays here next to it.

It is made with `../tools/extract_drums.py MuseScore_General.sf2 MuseScore_General-Drums-0.2.sf2`.
Each of its 1996 key hits (every drum preset, every key, four velocities) was
rendered and compared with the same hit of the original: 1981 match within 2 in
32767 (the renderer itself differs by that much between two loads of one same
file), and the 15 others differ only in where the decaying tail of a long
cymbal falls under the cut-off, by at most 120 samples (2.5 ms).

| File | Release | Size | SHA-256 |
|---|---|---|---|
| `MuseScore_General-Drums-0.2.sf2` (drum kits only) | [`musescore-general-drums-0.2`](https://github.com/gaumondp/drumpersona-kits/releases/tag/musescore-general-drums-0.2) | 21 MB | `68b108ac7d919e8d01681a42da383fbdf34a97224a98d754a27775b19422fefc` |
| `MuseScore_General.sf2` (original) | [`musescore-general-0.2`](https://github.com/gaumondp/drumpersona-kits/releases/tag/musescore-general-0.2) | 216 MB | `ee51d2c4b1525e70f19a45909c4fd7a2e26d91d115fa89dbf5a6bc413d8b9bf3` |
