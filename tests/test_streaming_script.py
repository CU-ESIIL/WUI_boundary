"""Smoke tests for the streaming real-data pilot CLI helpers."""

from pathlib import Path
import importlib.util
import unittest


SPEC = importlib.util.spec_from_file_location(
    "run_streaming_wui_scaling", Path(__file__).resolve().parents[1] / "scripts" / "run_streaming_wui_scaling.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class StreamingScriptHelperTests(unittest.TestCase):
    def test_bbox_parser(self) -> None:
        bbox = MODULE._parse_bbox("-105.1,39.9,-105.0,40.0")
        self.assertEqual(len(bbox), 4)
        self.assertLess(bbox[0], bbox[2])

    def test_number_parsers(self) -> None:
        self.assertEqual(MODULE._parse_int_list("41,42,52"), [41, 42, 52])
        self.assertEqual(MODULE._parse_float_list("5,10,20"), [5.0, 10.0, 20.0])

    def test_fit_loglog(self) -> None:
        fit = MODULE._fit_loglog([1.0, 2.0, 4.0], [100.0, 70.0, 50.0])
        self.assertEqual(fit["status"], "ok_fitted")
        self.assertIsNotNone(fit["slope"])


if __name__ == "__main__":
    unittest.main()
