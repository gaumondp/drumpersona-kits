#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Make the General MIDI version of MuldjordKit (FreePats 2020-10-18).

The FreePats SoundFont puts the kit on keys 48-66; General MIDI drums sit on
35-81 (kick 36, snare 38, closed hat 42, ...). This moves every piece to its
General MIDI key and changes nothing else: no sample, level, envelope or
velocity layer is touched, and the file keeps its size. Three things change in
the file, in place:

  * each instrument zone's key range (generator 43), from its old key to the new;
  * each sample's original pitch (sample header), by the same move, so a sample
    plays at its own pitch on its new key exactly as on its old one;
  * the preset's key range (generator 43), opened to 0-127.

Usage: make_gm.py <MuldjordKit 20201018.sf2> <MuldjordKit-20201018-GM.sf2>
The input's SHA-256 must be the FreePats file's (checked), so the output is
always the same file.
"""
import hashlib
import struct
import sys

SOURCE_SHA256 = "fec611c55b5e1c53ea3e6df1e6779c9f18502fc6455ee45edc51d5a2b4881055"

# FreePats key -> General MIDI key. Pieces with no General MIDI key move above
# the GM drum range (82-127 is free), so they never sound in place of a GM piece.
KEYS = {
    48: 36,  # kick left        -> Bass Drum 1
    49: 35,  # kick right       -> Acoustic Bass Drum (the second kick)
    50: 38,  # snare 1          -> Acoustic Snare
    51: 40,  # snare 2          -> Electric Snare (DrumPersona: the rimshot pad)
    52: 42,  # hi-hat closed    -> Closed Hi-Hat
    53: 46,  # hi-hat open      -> Open Hi-Hat
    54: 51,  # ride left        -> Ride Cymbal 1
    55: 53,  # ride bell left   -> Ride Bell
    56: 59,  # ride right       -> Ride Cymbal 2
    57: 84,  # ride bell right  -> (no GM key) 84
    58: 49,  # crash left       -> Crash Cymbal 1
    59: 57,  # crash right      -> Crash Cymbal 2
    60: 52,  # china            -> Chinese Cymbal
    61: 50,  # tom 1            -> High Tom
    62: 48,  # tom 2            -> Hi-Mid Tom
    63: 45,  # tom 3            -> Low Tom
    64: 43,  # tom 4 (floor)    -> High Floor Tom
    65: 85,  # snare rest 1     -> (no GM key) 85
    66: 86,  # snare rest 2     -> (no GM key) 86
}
GEN_KEY_RANGE = 43
GEN_SAMPLE_ID = 53


def chunks(data, start, end):
    """Yield (id, offset of its data, size) for each RIFF chunk in data[start:end]."""
    i = start
    while i + 8 <= end:
        cid = data[i:i + 4]
        size = struct.unpack_from("<I", data, i + 4)[0]
        yield cid, i + 8, size
        i += 8 + size + (size & 1)


def hydra(data):
    """The pdta sub-chunks: name -> (offset, size)."""
    for cid, off, size in chunks(data, 12, len(data)):
        if cid == b"LIST" and data[off:off + 4] == b"pdta":
            return {c.decode(): (o, s) for c, o, s in chunks(data, off + 4, off + size)}
    raise SystemExit("no pdta chunk: not a SoundFont 2 file")


def main(src, dst):
    data = bytearray(open(src, "rb").read())
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise SystemExit("not the FreePats MuldjordKit 20201018.sf2 (SHA-256 differs)")
    pd = hydra(data)

    # Instrument zones: move each one-key range, and note which sample each key plays.
    off, size = pd["igen"]
    samples_of_key = {}
    zone_key = None
    moved = 0
    for i in range(size // 4):
        at = off + 4 * i
        oper, amount = struct.unpack_from("<HH", data, at)
        if oper == GEN_KEY_RANGE:
            lo, hi = amount & 0xFF, amount >> 8
            zone_key = None
            if lo == hi and lo in KEYS:
                zone_key = lo
                new = KEYS[lo]
                struct.pack_into("<HH", data, at, oper, new | (new << 8))
                moved += 1
        elif oper == GEN_SAMPLE_ID and zone_key is not None:
            samples_of_key.setdefault(amount, set()).add(zone_key)

    # Each sample must belong to one key only, or its pitch cannot follow.
    for sample, keys in samples_of_key.items():
        if len(keys) != 1:
            raise SystemExit(f"sample {sample} is played by keys {sorted(keys)}: cannot move its pitch")

    # Sample headers: 46 bytes each; the original pitch is byte 40.
    off, size = pd["shdr"]
    for sample, keys in samples_of_key.items():
        at = off + 46 * sample + 40
        old = data[at]
        key = next(iter(keys))
        if old != key:
            raise SystemExit(f"sample {sample}: original pitch {old}, played on key {key}: not as expected")
        data[at] = KEYS[key]

    # The preset's key range: every key.
    off, size = pd["pgen"]
    for i in range(size // 4):
        at = off + 4 * i
        oper, _ = struct.unpack_from("<HH", data, at)
        if oper == GEN_KEY_RANGE:
            struct.pack_into("<HH", data, at, oper, 0 | (127 << 8))

    open(dst, "wb").write(data)
    print(f"{moved} zones and {len(samples_of_key)} samples moved; {dst}: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
