#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Move the pieces of a SoundFont 2 drum kit to other keys (most often: to General MIDI).

A collection folder holds a key map, `gm-keys.json`:

    {
      "source_sha256": "<the original .sf2's SHA-256>",
      "keys": { "48": 36, "49": 37, ... }        old key -> new key
    }

and this script makes the moved kit from the original:

    tools/remap_keys.py <folder>/gm-keys.json <original.sf2> <moved.sf2>

It changes nothing but the keys, in place (the file keeps its size):

  * each instrument zone's key range (generator 43), for zones on one mapped key;
  * each sample's original pitch (sample header), and a zone's root-key override
    (generator 58) if it has one, moved by the same number of keys, so a sample
    plays at its own pitch on its new key exactly as on its old one;
  * each preset zone's key range, opened to 0-127.

It refuses an input whose SHA-256 is not the map's, a sample played on two keys
moved by different amounts, and a map that sends two keys to the same key. The
same input always gives the same output.
"""
import hashlib
import json
import struct
import sys

GEN_KEY_RANGE = 43
GEN_SAMPLE_ID = 53
GEN_ROOT_KEY = 58


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


def zones(data, pd):
    """Each instrument zone as the list of (byte offset, oper, amount) of its generators."""
    ibag_off, ibag_size = pd["ibag"]
    igen_off, _ = pd["igen"]
    bags = [struct.unpack_from("<HH", data, ibag_off + 4 * i)[0] for i in range(ibag_size // 4)]
    for z in range(len(bags) - 1):
        gens = []
        for g in range(bags[z], bags[z + 1]):
            at = igen_off + 4 * g
            oper, amount = struct.unpack_from("<HH", data, at)
            gens.append((at, oper, amount))
        yield gens


def main(map_path, src, dst):
    spec = json.load(open(map_path))
    keys = {int(k): int(v) for k, v in spec["keys"].items()}
    if len(set(keys.values())) != len(keys):
        raise SystemExit("two keys go to the same key")
    data = bytearray(open(src, "rb").read())
    if hashlib.sha256(data).hexdigest() != spec["source_sha256"]:
        raise SystemExit("not the original this map is for (SHA-256 differs)")
    pd = hydra(data)

    moves = {}  # sample -> how many keys it moves
    moved = 0
    for gens in zones(data, pd):
        key_range = [g for g in gens if g[1] == GEN_KEY_RANGE]
        if not key_range:
            continue
        at, _, amount = key_range[0]
        lo, hi = amount & 0xFF, amount >> 8
        if lo != hi or lo not in keys:
            continue
        new = keys[lo]
        delta = new - lo
        struct.pack_into("<HH", data, at, GEN_KEY_RANGE, new | (new << 8))
        moved += 1
        for g_at, oper, g_amount in gens:
            if oper == GEN_ROOT_KEY:
                struct.pack_into("<HH", data, g_at, GEN_ROOT_KEY, g_amount + delta)
            elif oper == GEN_SAMPLE_ID:
                if moves.get(g_amount, delta) != delta:
                    raise SystemExit(f"sample {g_amount} is played on keys moved by different amounts")
                moves[g_amount] = delta

    shdr_off, _ = pd["shdr"]
    for sample, delta in moves.items():
        at = shdr_off + 46 * sample + 40
        pitch = data[at] + delta
        if not 0 <= pitch <= 127:
            raise SystemExit(f"sample {sample}: its pitch would leave 0-127")
        data[at] = pitch

    pgen_off, pgen_size = pd["pgen"]
    for i in range(pgen_size // 4):
        at = pgen_off + 4 * i
        if struct.unpack_from("<H", data, at)[0] == GEN_KEY_RANGE:
            struct.pack_into("<HH", data, at, GEN_KEY_RANGE, 0 | (127 << 8))

    open(dst, "wb").write(data)
    print(f"{moved} zones and {len(moves)} samples moved; {dst}: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
