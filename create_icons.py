"""Generate self-contained PNG icons without third-party packages."""
from pathlib import Path
import math
import struct
import zlib

out = Path(__file__).resolve().parent / 'public' / 'icons'
out.mkdir(exist_ok=True)


def chunk(kind, payload):
    return struct.pack('!I', len(payload)) + kind + payload + struct.pack('!I', zlib.crc32(kind + payload) & 0xffffffff)


def icon(size):
    data = bytearray()
    for y in range(size):
        data.append(0)
        for x in range(size):
            u, v = x / size, y / size
            inside = .12 < u < .88 and .12 < v < .88
            rounded = inside and all((u-cx)**2 + (v-cy)**2 > .07**2 for cx, cy in [(.12,.12),(.88,.12),(.12,.88),(.88,.88)] if abs(u-cx)<.07 and abs(v-cy)<.07)
            # Extruded stylized S with two curved strokes and a diagonal connector.
            upper = .34 < v < .43 and .34 < u < .68
            lower = .58 < v < .67 and .32 < u < .66
            left = .29 < u < .39 and .36 < v < .53
            right = .61 < u < .71 and .48 < v < .64
            diagonal = abs((u-.5) + (v-.5)*.8) < .06 and .42 < v < .59
            mark = upper or lower or left or right or diagonal
            if rounded and mark:
                color = (17, 43, 40, 255)
            elif rounded:
                color = (198, 238-int(v*20), 98+int(u*35), 255)
            else:
                color = (8, 19, 28, 255)
            data.extend(color)
    raw = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', size, size, 8, 6, 0, 0, 0))
    raw += chunk(b'IDAT', zlib.compress(bytes(data), 9)) + chunk(b'IEND', b'')
    (out / f'icon-{size}.png').write_bytes(raw)


for size in (192, 512):
    icon(size)
