#!/usr/bin/env python3
"""Package a landscape cover and an independently designed square thumbnail.

Requires Pillow. No generation service or network access is used. All generated
files are real PNGs; layout.json records how each input was fitted.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

from PIL import Image, ImageColor, ImageOps, UnidentifiedImageError


OUTPUT_NAMES = (
    "cover-main.png",
    "cover-thumbnail.png",
    "cover-combined.png",
    "layout.json",
)
MAX_HEIGHT = 8192
MAX_CANVAS_PIXELS = 64_000_000
MAX_SOURCE_PIXELS = 64_000_000


class CoverError(ValueError):
    """A validation or packaging failure that is safe to show in the CLI."""


def _dimensions(height: int, main_aspect: float) -> tuple[int, int]:
    if isinstance(height, bool) or not isinstance(height, int):
        raise CoverError("height must be a positive integer")
    if not 1 <= height <= MAX_HEIGHT:
        raise CoverError(f"height must be between 1 and {MAX_HEIGHT}")
    if not math.isfinite(main_aspect) or not 1 <= main_aspect <= 10:
        raise CoverError("main-aspect must be a finite number between 1 and 10")
    main_width = int(math.floor(height * main_aspect + 0.5))
    if (main_width + height) * height > MAX_CANVAS_PIXELS:
        raise CoverError(f"combined canvas must not exceed {MAX_CANVAS_PIXELS:,} pixels")
    return main_width, height


def _background(value: str) -> tuple[int, int, int, int]:
    try:
        rgba = ImageColor.getcolor(value, "RGBA")
    except (TypeError, ValueError) as exc:
        raise CoverError(f"invalid background color: {value!r}") from exc
    if rgba[3] != 255:
        raise CoverError("background must be opaque; use a color such as '#ffffff'")
    return rgba


def _paths(main: Path, thumbnail: Path, output_dir: Path, overwrite: bool) -> tuple[Path, Path, Path]:
    inputs = [main.expanduser().resolve(), thumbnail.expanduser().resolve()]
    for path in inputs:
        if not path.is_file():
            raise CoverError(f"input is not a regular file: {path}")
    if inputs[0] == inputs[1] or os.path.samefile(*inputs):
        raise CoverError("main and thumbnail must be different files; design the thumbnail independently")

    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise CoverError(f"output-dir is not a directory: {output_dir}")
    for name in OUTPUT_NAMES:
        path = output_dir / name
        if path.is_symlink():
            raise CoverError(f"refusing an output symlink: {path}")
        for source in inputs:
            if path.resolve() == source or (path.exists() and os.path.samefile(path, source)):
                raise CoverError(f"output would overwrite an input: {path}")
        if path.exists():
            if not path.is_file():
                raise CoverError(f"output is not a regular file: {path}")
            if not overwrite:
                raise CoverError(f"output already exists: {path}; use --overwrite to replace the output set")
    return inputs[0], inputs[1], output_dir


def _load(path: Path) -> tuple[Image.Image, dict[str, Any]]:
    try:
        with Image.open(path) as image:
            if getattr(image, "is_animated", False):
                raise CoverError(f"input must be a still image: {path}")
            if image.width * image.height > MAX_SOURCE_PIXELS:
                raise CoverError(f"input must not exceed {MAX_SOURCE_PIXELS:,} pixels: {path}")
            source_format = image.format
            source_size = image.size
            image.load()
            normalized = ImageOps.exif_transpose(image).convert("RGBA")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, ValueError) as exc:
        if isinstance(exc, CoverError):
            raise
        raise CoverError(f"cannot read image {path}: {exc}") from exc
    return normalized, {
        "path": str(path),
        "format": source_format,
        "original_size": {"width": source_size[0], "height": source_size[1]},
        "oriented_size": {"width": normalized.width, "height": normalized.height},
    }


def _fit(
    source: Image.Image,
    width: int,
    height: int,
    fit: str,
    background: tuple[int, int, int, int],
) -> tuple[Image.Image, dict[str, Any]]:
    ratios = (width / source.width, height / source.height)
    nominal_scale = min(ratios) if fit == "contain" else max(ratios)
    resized_width = max(1, int(math.floor(source.width * nominal_scale + 0.5)))
    resized_height = max(1, int(math.floor(source.height * nominal_scale + 0.5)))
    resized = source.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    x = (width - resized_width) // 2
    y = (height - resized_height) // 2
    canvas = Image.new("RGBA", (width, height), background)
    canvas.alpha_composite(resized, (x, y))
    visible_left, visible_top = max(0, x), max(0, y)
    visible_right, visible_bottom = min(width, x + resized_width), min(height, y + resized_height)
    scale_x, scale_y = resized_width / source.width, resized_height / source.height
    geometry = {
        "fit": fit,
        "nominal_scale": nominal_scale,
        "resized_size": {"width": resized_width, "height": resized_height},
        "content_bounds": {"x": x, "y": y, "width": resized_width, "height": resized_height},
        "visible_content_bounds": {
            "x": visible_left,
            "y": visible_top,
            "width": visible_right - visible_left,
            "height": visible_bottom - visible_top,
        },
        "visible_source_bounds": {
            "x": (visible_left - x) / scale_x,
            "y": (visible_top - y) / scale_y,
            "width": (visible_right - visible_left) / scale_x,
            "height": (visible_bottom - visible_top) / scale_y,
        },
        "padding": {
            "left": max(0, x),
            "right": max(0, width - (x + resized_width)),
            "top": max(0, y),
            "bottom": max(0, height - (y + resized_height)),
        },
        "cropped": resized_width > width or resized_height > height,
    }
    return canvas.convert("RGB"), geometry


def _install(staging: Path, output_dir: Path, overwrite: bool) -> None:
    """Install the complete staged set; roll back ordinary I/O failures.

    Hard links make the no-overwrite operation race-safe for each destination.
    Replacement backs up the previous set and restores it if installation fails.
    A group of separate files cannot be atomic to external readers; each file is.
    """
    installed: list[Path] = []
    backups: list[tuple[Path, Path]] = []
    try:
        for name in OUTPUT_NAMES:
            destination = output_dir / name
            if overwrite and os.path.lexists(destination):
                if destination.is_symlink() or not destination.is_file():
                    raise CoverError(f"refusing changed or non-file output: {destination}")
                backup = staging / f"backup-{name}"
                os.replace(destination, backup)
                backups.append((destination, backup))
        for name in OUTPUT_NAMES:
            destination = output_dir / name
            os.link(staging / name, destination)
            installed.append(destination)
    except BaseException:
        for destination in reversed(installed):
            destination.unlink()
        for destination, backup in reversed(backups):
            os.replace(backup, destination)
        raise


def compose_covers(
    main: str | Path,
    thumbnail: str | Path,
    output_dir: str | Path,
    *,
    height: int = 1000,
    main_aspect: float = 2.13,
    fit: str = "contain",
    background: str = "#ffffff",
    overwrite: bool = False,
) -> dict[str, Any]:
    """Return metadata after safely writing all four output files."""
    if fit not in ("contain", "cover"):
        raise CoverError("fit must be 'contain' or 'cover'")
    main_width, height = _dimensions(height, main_aspect)
    rgba = _background(background)
    main_path, thumbnail_path, output_dir = _paths(Path(main), Path(thumbnail), Path(output_dir), overwrite)
    main_source, main_info = _load(main_path)
    thumbnail_source, thumbnail_info = _load(thumbnail_path)
    main_image, main_geometry = _fit(main_source, main_width, height, fit, rgba)
    thumbnail_image, thumbnail_geometry = _fit(thumbnail_source, height, height, fit, rgba)
    combined = Image.new("RGB", (main_width + height, height), rgba[:3])
    combined.paste(main_image, (0, 0))
    combined.paste(thumbnail_image, (main_width, 0))
    manifest = {
        "schema_version": 1,
        "layout": "landscape-left-square-right",
        "gutter": 0,
        "background": "#" + "".join(f"{v:02x}" for v in rgba[:3]),
        "main_aspect_requested": main_aspect,
        "combined": {"file": "cover-combined.png", "width": combined.width, "height": combined.height, "format": "PNG"},
        "main": {
            "file": "cover-main.png", "width": main_width, "height": height, "format": "PNG",
            "combined_bounds": {"x": 0, "y": 0, "width": main_width, "height": height},
            "source": main_info, "geometry": main_geometry,
        },
        "thumbnail": {
            "file": "cover-thumbnail.png", "width": height, "height": height, "format": "PNG",
            "combined_bounds": {"x": main_width, "y": 0, "width": height, "height": height},
            "source": thumbnail_info, "geometry": thumbnail_geometry,
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".compose-covers-", dir=output_dir) as temporary:
        staging = Path(temporary)
        main_image.save(staging / OUTPUT_NAMES[0], format="PNG")
        thumbnail_image.save(staging / OUTPUT_NAMES[1], format="PNG")
        combined.save(staging / OUTPUT_NAMES[2], format="PNG")
        (staging / "layout.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _install(staging, output_dir, overwrite)
    return {
        **manifest,
        "output_dir": str(output_dir),
        "files": {name: str(output_dir / name) for name in OUTPUT_NAMES},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--main", required=True, type=Path, help="landscape cover image")
    parser.add_argument("--thumbnail", required=True, type=Path, help="independently designed square thumbnail")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--height", type=int, default=1000, help="shared output height in pixels (default: 1000)")
    parser.add_argument("--main-aspect", type=float, default=2.13, help="left cover width/height (default: 2.13)")
    parser.add_argument("--fit", choices=("contain", "cover"), default="contain", help="contain preserves all content; cover center-crops")
    parser.add_argument("--background", default="#ffffff", help="opaque Pillow color, used behind transparency and padding")
    parser.add_argument("--overwrite", action="store_true", help="explicitly replace an existing output set")
    args = parser.parse_args(argv)
    try:
        result = compose_covers(**vars(args))
    except (CoverError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
