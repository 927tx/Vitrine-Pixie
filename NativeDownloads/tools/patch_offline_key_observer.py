"""Observe the native offline-key completion in the guarded Spotify 9.1.88 image.

The original completion remains responsible for all Spotify state changes. This
patch passes its two arguments to the already loaded companion library first.
"""
import struct

from patch_native_restrictions import layout, branch

UUID = bytes.fromhex("f51dbd933b8f3a12943196c606e3afc2")
ORIGINAL = 0x106adce10
CAVE = 0x100023e00
DLSYM_STUB = 0x10a16f0cc
EXPECTED = bytes.fromhex("ff4301d1f44f03a9fd7b04a9fd030191")
SYMBOL = b"SpotifyAudioProbeObserveOfflineKey\0"


def adrp(register, source, target):
    delta = (target >> 12) - (source >> 12)
    if not -(1 << 20) <= delta < (1 << 20):
        raise ValueError("ADRP out of range")
    bits = delta & 0x1fffff
    return 0x90000000 | ((bits & 3) << 29) | ((bits >> 2) << 5) | register


def add_imm(register, base, amount):
    if amount >= 4096:
        raise ValueError("ADD offset out of range")
    return 0x91000000 | (amount << 10) | (base << 5) | register


def trampoline():
    # The first 18 instructions were assembled and checked against llvm-objdump.
    # It preserves the callback arguments, LR and stack alignment around both
    # external calls, then replays the four displaced original instructions.
    words = [
        0xa9be07e0, 0xf9000bfe, 0x92800020, 0x10000201,
        adrp(16, CAVE + 0x10, DLSYM_STUB),
        add_imm(16, 16, DLSYM_STUB & 0xfff),
        0xd63f0200, 0xb4000080, 0xaa0003f0, 0xa94007e0,
        0xd63f0200, 0xa94007e0, 0xf9400bfe, 0x910083ff,
    ]
    words.extend(struct.unpack("<4I", EXPECTED))
    words.append(branch(CAVE + 4 * len(words), ORIGINAL + len(EXPECTED)))
    code = struct.pack("<" + "I" * len(words), *words) + SYMBOL
    if len(code) > 0x100:
        raise ValueError("No room in guarded cave")
    return code


def patch(data):
    commands_end, first_section, segments, uuid = layout(data)
    if uuid != UUID:
        raise ValueError("Unsupported Spotify UUID")
    text = next(s for s in segments if s[0] == b"__TEXT")
    _, vm, _, fileoff, filesize, protection = text

    def offset(address, count):
        if not vm <= address or address + count > vm + filesize:
            raise ValueError("Patch outside __TEXT")
        return fileoff + address - vm

    stub = trampoline()
    target = offset(CAVE, len(stub))
    source = offset(ORIGINAL, len(EXPECTED))
    if protection & 5 != 5 or not commands_end <= target or target + len(stub) > first_section:
        raise ValueError("No executable header padding")
    if any(data[target:target + len(stub)]):
        raise ValueError("Key-observer code cave is occupied")
    if data[source:source + len(EXPECTED)] != EXPECTED:
        raise ValueError("Offline-key callback bytes differ")
    result = bytearray(data)
    result[target:target + len(stub)] = stub
    struct.pack_into("<I", result, source, branch(ORIGINAL, CAVE))
    return bytes(result), {"callback": hex(ORIGINAL), "cave": hex(CAVE),
                            "size": len(stub), "original_replayed": True}
