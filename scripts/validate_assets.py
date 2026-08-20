#!/usr/bin/env python3
"""Validate public binary assets without third-party dependencies."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOCIAL_PREVIEW = ROOT / "assets" / "social-preview.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
FORBIDDEN_METADATA_CHUNKS = {b"eXIf", b"iTXt", b"tEXt", b"zTXt"}


def validate_png(path: Path, expected_size: tuple[int, int]) -> list[str]:
    errors: list[str] = []
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        return [f"not a valid PNG signature: {path.relative_to(ROOT)}"]

    offset = len(PNG_SIGNATURE)
    dimensions: tuple[int, int] | None = None
    saw_iend = False
    while offset < len(data):
        if offset + 12 > len(data):
            errors.append("truncated PNG chunk header")
            break
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        payload_start = offset + 8
        payload_end = payload_start + length
        crc_end = payload_end + 4
        if crc_end > len(data):
            errors.append(f"truncated PNG chunk: {chunk_type!r}")
            break

        payload = data[payload_start:payload_end]
        recorded_crc = struct.unpack(">I", data[payload_end:crc_end])[0]
        calculated_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if recorded_crc != calculated_crc:
            errors.append(f"PNG CRC mismatch: {chunk_type!r}")

        if chunk_type == b"IHDR":
            if length != 13:
                errors.append("PNG IHDR has an invalid length")
            else:
                dimensions = struct.unpack(">II", payload[:8])
        if chunk_type in FORBIDDEN_METADATA_CHUNKS:
            errors.append(f"embedded metadata chunk is not allowed: {chunk_type!r}")
        if chunk_type == b"IEND":
            saw_iend = True
            offset = crc_end
            break
        offset = crc_end

    if dimensions != expected_size:
        errors.append(
            f"expected {expected_size[0]}x{expected_size[1]}, found {dimensions}"
        )
    if not saw_iend:
        errors.append("PNG IEND chunk is missing")
    if offset != len(data):
        errors.append("unexpected bytes follow the PNG IEND chunk")
    return errors


def main() -> int:
    if not SOCIAL_PREVIEW.is_file():
        print("Asset validation failed: assets/social-preview.png is missing.")
        return 1

    errors = validate_png(SOCIAL_PREVIEW, (1280, 640))
    if errors:
        print("Asset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Asset validation passed: social preview is a metadata-free 1280x640 PNG "
        "with valid chunk checksums."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
