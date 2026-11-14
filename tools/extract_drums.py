#!/usr/bin/env python3
"""Write a SoundFont 2 file holding only the drum kits of another one.

    tools/extract_drums.py <source.sf2> <out.sf2> [--bank 128]

Keeps the presets of the drum bank (128 by default), the instruments they use and
the samples those use (with their stereo partners). Every preset, instrument,
zone, generator, modulator and sample byte is copied unchanged; only the indexes
between them and the sample offsets are renumbered. The INFO chunk (name,
copyright, credits) is copied as is. Follows the SoundFont 2.04 specification
(sections 5 to 8: the RIFF layout, the hydra records and the sample data).
Standard library only.
"""

import struct
import sys

PHDR, BAG, MOD, GEN, INST, SHDR = 38, 4, 10, 4, 22, 46
GEN_INSTRUMENT, GEN_SAMPLE_ID = 41, 53
SAMPLE_PAD = 46  # zero sample points after each sample (spec 6.1)


def chunks(data, start, end):
    """Yield (id, payload_start, size) of the RIFF chunks in data[start:end]."""
    pos = start
    while pos + 8 <= end:
        cid, size = data[pos:pos + 4], struct.unpack_from("<I", data, pos + 4)[0]
        yield cid, pos + 8, size
        pos += 8 + size + (size & 1)


def lists(data):
    """The three LIST chunks of an sfbk file: {'INFO': (start, size), 'sdta': ..., 'pdta': ...}."""
    if data[0:4] != b"RIFF" or data[8:12] != b"sfbk":
        sys.exit("not a SoundFont 2 file")
    out = {}
    for cid, start, size in chunks(data, 12, len(data)):
        if cid == b"LIST":
            out[data[start:start + 4].decode()] = (start + 4, size - 4, start - 8, size + 8)
    return out


def records(raw, size):
    return [raw[i:i + size] for i in range(0, len(raw), size)]


def main():
    args = sys.argv[1:]
    bank = 128
    if "--bank" in args:
        i = args.index("--bank")
        bank = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    src, dst = args
    data = open(src, "rb").read()
    L = lists(data)

    sub = {}
    for cid, start, size in chunks(data, L["pdta"][0], L["pdta"][0] + L["pdta"][1]):
        sub[cid.decode()] = data[start:start + size]
    sdta = {}
    for cid, start, size in chunks(data, L["sdta"][0], L["sdta"][0] + L["sdta"][1]):
        sdta[cid.decode()] = data[start:start + size]

    phdr = records(sub["phdr"], PHDR)
    pbag = records(sub["pbag"], BAG)
    pmod = records(sub["pmod"], MOD)
    pgen = records(sub["pgen"], GEN)
    inst = records(sub["inst"], INST)
    ibag = records(sub["ibag"], BAG)
    imod = records(sub["imod"], MOD)
    igen = records(sub["igen"], GEN)
    shdr = records(sub["shdr"], SHDR)

    bag_of = lambda r: struct.unpack_from("<HH", r)  # (gen index, mod index)
    gen_of = lambda r: struct.unpack_from("<HH", r)  # (oper, amount)

    def zones(hdrs, i, bags, idx_off):
        """The bag indexes of header i (its zones)."""
        a = struct.unpack_from("<H", hdrs[i], idx_off)[0]
        b = struct.unpack_from("<H", hdrs[i + 1], idx_off)[0]
        return range(a, b)

    keep_p = [i for i in range(len(phdr) - 1) if struct.unpack_from("<H", phdr[i], 22)[0] == bank]
    if not keep_p:
        sys.exit(f"no preset in bank {bank}")

    # Instruments used by the kept presets, then the samples they use (and stereo links).
    used_inst = set()
    for p in keep_p:
        for z in zones(phdr, p, pbag, 24):
            g0, _ = bag_of(pbag[z])
            g1, _ = bag_of(pbag[z + 1])
            for g in range(g0, g1):
                op, amt = gen_of(pgen[g])
                if op == GEN_INSTRUMENT:
                    used_inst.add(amt)
    used_inst = sorted(used_inst)
    used_smp = set()
    for n in used_inst:
        for z in zones(inst, n, ibag, 20):
            g0, _ = bag_of(ibag[z])
            g1, _ = bag_of(ibag[z + 1])
            for g in range(g0, g1):
                op, amt = gen_of(igen[g])
                if op == GEN_SAMPLE_ID:
                    used_smp.add(amt)
    changed = True
    while changed:  # a stereo sample needs its partner
        changed = False
        for s in list(used_smp):
            link = struct.unpack_from("<H", shdr[s], 42)[0]
            stype = struct.unpack_from("<H", shdr[s], 44)[0]
            if stype & 0x8000 == 0 and stype not in (1, 0) and link < len(shdr) - 1 and link not in used_smp:
                used_smp.add(link)
                changed = True
    used_smp = sorted(used_smp)
    inst_map = {old: new for new, old in enumerate(used_inst)}
    smp_map = {old: new for new, old in enumerate(used_smp)}

    def copy_zones(hdrs, keep, bags, mods, gens, idx_off, name_len, remap_oper, remap):
        """New header, bag, mod and gen records for the kept headers, indexes renumbered."""
        nh, nb, nm, ng = [], [], [], []
        for h in keep:
            rec = bytearray(hdrs[h])
            struct.pack_into("<H", rec, idx_off, len(nb))
            nh.append(bytes(rec))
            for z in zones(hdrs, h, bags, idx_off):
                g0, m0 = bag_of(bags[z])
                g1, m1 = bag_of(bags[z + 1])
                nb.append(struct.pack("<HH", len(ng), len(nm)))
                nm.extend(mods[m0:m1])
                for g in range(g0, g1):
                    op, amt = gen_of(gens[g])
                    if op == remap_oper:
                        ng.append(struct.pack("<HH", op, remap[amt]))
                    else:
                        ng.append(gens[g])
        return nh, nb, nm, ng

    nphdr, npbag, npmod, npgen = copy_zones(phdr, keep_p, pbag, pmod, pgen, 24, 20, GEN_INSTRUMENT, inst_map)
    eop = bytearray(phdr[-1])
    struct.pack_into("<H", eop, 24, len(npbag))
    nphdr.append(bytes(eop))
    npbag.append(struct.pack("<HH", len(npgen), len(npmod)))
    npmod.append(b"\0" * MOD)
    npgen.append(b"\0" * GEN)

    ninst, nibag, nimod, nigen = copy_zones(inst, used_inst, ibag, imod, igen, 20, 20, GEN_SAMPLE_ID, smp_map)
    eoi = bytearray(inst[-1])
    struct.pack_into("<H", eoi, 20, len(nibag))
    ninst.append(bytes(eoi))
    nibag.append(struct.pack("<HH", len(nigen), len(nimod)))
    nimod.append(b"\0" * MOD)
    nigen.append(b"\0" * GEN)

    smpl, sm24 = sdta["smpl"], sdta.get("sm24")
    nsmpl, nsm24, nshdr = bytearray(), bytearray(), []
    for s in used_smp:
        rec = bytearray(shdr[s])
        start, end, ls, le = struct.unpack_from("<IIII", rec, 20)
        base = len(nsmpl) // 2
        nsmpl += smpl[start * 2:end * 2] + b"\0" * (SAMPLE_PAD * 2)
        if sm24 is not None:
            nsm24 += sm24[start:end] + b"\0" * SAMPLE_PAD
        struct.pack_into("<IIII", rec, 20, base, base + (end - start), base + (ls - start), base + (le - start))
        link = struct.unpack_from("<H", rec, 42)[0]
        if link in smp_map:
            struct.pack_into("<H", rec, 42, smp_map[link])
        nshdr.append(bytes(rec))
    nshdr.append(shdr[-1])

    def chunk(cid, payload):
        return cid + struct.pack("<I", len(payload)) + payload + (b"\0" if len(payload) & 1 else b"")

    def lst(kind, body):
        return chunk(b"LIST", kind + body)

    info = data[L["INFO"][2]:L["INFO"][2] + L["INFO"][3]]
    sdta_body = chunk(b"smpl", bytes(nsmpl)) + (chunk(b"sm24", bytes(nsm24)) if sm24 is not None else b"")
    pdta_body = b"".join(chunk(c.encode(), b"".join(r)) for c, r in (
        ("phdr", nphdr), ("pbag", npbag), ("pmod", npmod), ("pgen", npgen), ("inst", ninst),
        ("ibag", nibag), ("imod", nimod), ("igen", nigen), ("shdr", nshdr)))
    body = b"sfbk" + info + lst(b"sdta", sdta_body) + lst(b"pdta", pdta_body)
    with open(dst, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", len(body)) + body)
    print(f"{len(keep_p)} presets, {len(used_inst)} instruments, {len(used_smp)} samples, "
          f"{len(nsmpl) // 2} sample points -> {dst}")


if __name__ == "__main__":
    main()
