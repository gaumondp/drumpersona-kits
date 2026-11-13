# World Percussion, General MIDI version

Hand percussion from the **FreePats** project (version 2020-09-05): cajón
flamenco, bongos, egg shakers, tambourine, hand clap, claves, castanets, congas,
maracas and darbuka. Recorded in 2019 by Xavimart (Javier), Gonzalo and Roberto
from Xavimart's collection of instruments; the claves and congas come from the
Versilian Community Sample Library (CC0). A percussion set, not a drum kit.

## Why this is not the original file

The FreePats SoundFont puts the instruments on its own keys, 48 to 71, not on
the General MIDI percussion keys (hand clap 39, tambourine 54, bongos 60-61,
congas 62-64, maracas 70, claves 75...). Loaded as it is, a General MIDI part
plays the wrong instruments, or nothing.

**`WorldPercussion-20200905-GM.sf2` is the same set moved to the General MIDI
keys, and nothing else.** Every sample, level, envelope and velocity layer is the
original's; only which key plays each instrument changed. Each moved key was
checked to play exactly the same sound as its old key (rendered note for note,
24 of 24 identical). `../tools/remap_keys.py gm-keys.json` makes it from the
original, and always gives the same file. The original, unchanged, is kept too.

## Source and licence

- Source: [FreePats](https://freepats.zenvoid.org/), release
  [`WorldPercussion-SF2-20200905.7z`](https://github.com/freepats/world-percussion/releases/tag/2020-09-05)
  of [freepats/world-percussion](https://github.com/freepats/world-percussion)
  (SHA-256 of the archive: `5d72c35572259804091657e094fb094c4ee45ffd4bc37f1708878ef6cfeeb129`),
  extracted on 2026-11-13.
- Licence: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), public
  domain dedication (text in `LICENSE`). No attribution is required; credit is
  given anyway: FreePats, Xavimart, Gonzalo and Roberto, Versilian Studios.

| File | Release | Size | SHA-256 |
|---|---|---|---|
| `WorldPercussion-20200905-GM.sf2` (General MIDI keys) | [`freepats-world-percussion-gm-2020-09-05`](https://github.com/gaumondp/drumpersona-kits/releases/tag/freepats-world-percussion-gm-2020-09-05) | 9 MB | `9c12279c647ed285f75052a53da359a61a4c4a6ee12099acfe398430608e9272` |
| `WorldPercussion-20200905.sf2` (original, FreePats keys) | [`freepats-world-percussion-2020-09-05`](https://github.com/gaumondp/drumpersona-kits/releases/tag/freepats-world-percussion-2020-09-05) | 9 MB | `0a848e8cb3df5ba9f2720093267fdc4edf9d8512a1a367f7a0365440cb629103` |

## Keys

| Instrument | Original key | General MIDI key (GM version) |
|---|---|---|
| hand clap | 59 | 39 Hand Clap |
| tambourine | 57 | 54 Tambourine |
| bongo high | 52 | 60 Hi Bongo |
| bongo low | 53 | 61 Low Bongo |
| conga muted | 65 | 62 Mute Hi Conga |
| conga high | 63 | 63 Open Hi Conga |
| conga low | 64 | 64 Low Conga |
| maracas (forward) | 67 | 70 Maracas |
| claves | 60 | 75 Claves |
| egg shaker slow | 54 | 82 Shaker (General MIDI 2) |
| castanets | 61 | 85 Castanets (General MIDI 2) |
| cajón flamenco 1, 3, 2 | 48, 49, 50 | 96, 97, 98 (no General MIDI piece) |
| bongo muted | 51 | 99 |
| egg shaker fast, soft | 55, 56 | 100, 101 |
| tambourine fast | 58 | 102 |
| conga | 62 | 103 |
| conga low muted | 66 | 104 |
| maracas (backward) | 68 | 105 |
| darbuka doom, tak, pa | 69, 70, 71 | 106, 107, 108 |
