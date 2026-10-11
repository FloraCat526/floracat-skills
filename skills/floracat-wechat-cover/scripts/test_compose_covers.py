"""Contract tests for local packaging; no generation API calls are made."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from PIL import Image


SCRIPT = Path(__file__).with_name("compose_covers.py")
SPEC = importlib.util.spec_from_file_location("compose_covers", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class ComposeCoversTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.main = self.root / "main.png"
        self.thumbnail = self.root / "thumbnail.png"
        self.output = self.root / "output"
        Image.new("RGB", (213, 100), "red").save(self.main)
        Image.new("RGB", (100, 100), "blue").save(self.thumbnail)

    def compose(self, **kwargs):
        return module.compose_covers(self.main, self.thumbnail, self.output, **kwargs)

    def test_default_dimensions_and_pixel_order_without_gutter(self):
        result = self.compose()
        with Image.open(self.output / "cover-combined.png") as image:
            self.assertEqual(image.size, (3130, 1000))
            self.assertEqual(image.getpixel((0, 500)), (255, 0, 0))
            self.assertEqual(image.getpixel((2129, 500)), (255, 0, 0))
            self.assertEqual(image.getpixel((2130, 500)), (0, 0, 255))
            self.assertEqual(image.getpixel((3129, 500)), (0, 0, 255))
        self.assertEqual(result["thumbnail"]["combined_bounds"]["x"], 2130)
        self.assertEqual(result["gutter"], 0)
        manifest = json.loads((self.output / "layout.json").read_text())
        self.assertEqual(manifest["combined"]["width"], 3130)

    def test_default_contain_preserves_edges_and_full_source_geometry(self):
        image = Image.new("RGB", (100, 100), "green")
        image.paste("red", (0, 0, 10, 100))
        image.paste("blue", (90, 0, 100, 100))
        image.save(self.main)
        result = self.compose(height=100)
        geometry = result["main"]["geometry"]
        self.assertEqual(geometry["content_bounds"], {"x": 56, "y": 0, "width": 100, "height": 100})
        self.assertEqual(geometry["visible_source_bounds"], {"x": 0.0, "y": 0.0, "width": 100.0, "height": 100.0})
        self.assertFalse(geometry["cropped"])
        with Image.open(self.output / "cover-main.png") as image:
            self.assertEqual(image.getpixel((56, 50)), (255, 0, 0))
            self.assertEqual(image.getpixel((155, 50)), (0, 0, 255))
            self.assertEqual(image.getpixel((0, 50)), (255, 255, 255))

    def test_cover_crops_explicitly_and_reports_visible_source(self):
        Image.new("RGB", (300, 100), "red").save(self.main)
        result = self.compose(height=100, fit="cover")
        geometry = result["main"]["geometry"]
        self.assertTrue(geometry["cropped"])
        self.assertEqual(geometry["content_bounds"]["x"], -44)
        self.assertEqual(geometry["visible_source_bounds"]["x"], 44.0)
        self.assertEqual(geometry["visible_source_bounds"]["width"], 213.0)

    def test_actual_png_output_even_when_input_is_jpeg_with_png_name(self):
        Image.new("RGB", (213, 100), "red").save(self.main, format="JPEG")
        result = self.compose(height=100)
        self.assertEqual(result["main"]["source"]["format"], "JPEG")
        for name in module.OUTPUT_NAMES[:3]:
            self.assertTrue((self.output / name).read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
            with Image.open(self.output / name) as image:
                self.assertEqual(image.format, "PNG")
                image.verify()

    def test_transparent_source_is_composited_on_opaque_background(self):
        image = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
        image.putpixel((50, 50), (255, 0, 0, 255))
        image.save(self.thumbnail)
        result = self.compose(height=100, background="#fff4d6")
        with Image.open(self.output / "cover-thumbnail.png") as output:
            self.assertEqual(output.mode, "RGB")
            self.assertEqual(output.getpixel((0, 0)), (255, 244, 214))
            self.assertEqual(output.getpixel((50, 50)), (255, 0, 0))
        self.assertEqual(result["background"], "#fff4d6")

    def test_existing_output_is_preserved_unless_overwrite_is_explicit(self):
        self.output.mkdir()
        sentinel = self.output / "layout.json"
        sentinel.write_text("keep me")
        with self.assertRaisesRegex(module.CoverError, "already exists"):
            self.compose(height=100)
        self.assertEqual(sentinel.read_text(), "keep me")
        self.assertEqual(list(self.output.iterdir()), [sentinel])
        self.compose(height=100, overwrite=True)
        self.assertEqual(json.loads(sentinel.read_text())["schema_version"], 1)

    def test_replacement_failure_restores_entire_previous_set(self):
        self.compose(height=100)
        previous = {name: (self.output / name).read_bytes() for name in module.OUTPUT_NAMES}
        actual_link = module.os.link

        def fail_second(source, destination):
            if Path(destination).name == "cover-thumbnail.png":
                raise OSError("simulated disk failure")
            return actual_link(source, destination)

        with mock.patch.object(module.os, "link", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "disk failure"):
                self.compose(height=120, overwrite=True)
        self.assertEqual({name: (self.output / name).read_bytes() for name in module.OUTPUT_NAMES}, previous)
        self.assertEqual(sorted(p.name for p in self.output.iterdir()), sorted(module.OUTPUT_NAMES))

    def test_output_cannot_overwrite_an_input_even_with_overwrite(self):
        self.output.mkdir()
        input_path = self.output / "cover-main.png"
        Image.new("RGB", (213, 100), "red").save(input_path)
        before = input_path.read_bytes()
        with self.assertRaisesRegex(module.CoverError, "overwrite an input"):
            module.compose_covers(input_path, self.thumbnail, self.output, overwrite=True)
        self.assertEqual(input_path.read_bytes(), before)

    def test_new_install_failure_leaves_no_partial_outputs(self):
        actual_link = module.os.link

        def fail_second(source, destination):
            if Path(destination).name == "cover-thumbnail.png":
                raise OSError("simulated disk failure")
            return actual_link(source, destination)

        with mock.patch.object(module.os, "link", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "disk failure"):
                self.compose(height=100)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_output_symlink_is_rejected_and_target_is_preserved(self):
        self.output.mkdir()
        sentinel = self.root / "sentinel.json"
        sentinel.write_text("keep me")
        (self.output / "layout.json").symlink_to(sentinel)
        with self.assertRaisesRegex(module.CoverError, "symlink"):
            self.compose(height=100, overwrite=True)
        self.assertEqual(sentinel.read_text(), "keep me")

    def test_same_file_inputs_are_rejected(self):
        alias = self.root / "same-main.png"
        alias.hardlink_to(self.main)
        with self.assertRaisesRegex(module.CoverError, "different files"):
            module.compose_covers(self.main, alias, self.output)
        self.assertFalse(self.output.exists())

    def test_main_aspect_override(self):
        result = self.compose(height=100, main_aspect=2.35)
        self.assertEqual(result["main"]["width"], 235)
        self.assertEqual(result["combined"]["width"], 335)
        with Image.open(self.output / "cover-thumbnail.png") as image:
            self.assertEqual(image.size, (100, 100))

    def test_invalid_dimensions_color_and_input_do_not_create_outputs(self):
        for kwargs in ({"height": 0}, {"height": 8193}, {"main_aspect": float("nan")}, {"main_aspect": 0.5}, {"height": 8192}, {"background": "not-a-color"}, {"background": "#ffffff00"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(module.CoverError):
                self.compose(**kwargs)
        self.main.write_text("not an image")
        with self.assertRaisesRegex(module.CoverError, "cannot read image"):
            self.compose()
        self.assertFalse(self.output.exists())

    def test_cli_stdout_is_one_json_document_and_errors_use_stderr(self):
        argv = ["--main", str(self.main), "--thumbnail", str(self.thumbnail), "--output-dir", str(self.output), "--height", "100"]
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(module.main(argv), 0)
        self.assertEqual(json.loads(stdout.getvalue())["combined"]["width"], 313)
        self.assertEqual(stderr.getvalue(), "")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(module.main(argv), 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("error:", stderr.getvalue())
        self.assertIn("--overwrite", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
