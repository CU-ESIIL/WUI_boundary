"""Smoke tests for the streaming real-data pilot CLI helpers."""

from pathlib import Path
import importlib.util
import unittest
from unittest import mock


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


    def test_candidate_nlcd_urls_dedupes(self) -> None:
        urls = MODULE._candidate_nlcd_urls(MODULE.DEFAULT_NLCD_URLS[0])
        self.assertEqual(urls[0], MODULE.DEFAULT_NLCD_URLS[0])
        self.assertEqual(len(urls), len(set(urls)))

    def test_series_union_prefers_union_all(self) -> None:
        class _Series:
            def union_all(self):
                return "union_all"

            @property
            def unary_union(self):
                return "unary_union"

        self.assertEqual(MODULE._series_union(_Series()), "union_all")

    def test_overpass_query_retries_and_fallback(self) -> None:
        class _Resp:
            def __init__(self, status_code: int, payload: dict | None = None):
                self.status_code = status_code
                self._payload = payload or {}

            def raise_for_status(self) -> None:
                if self.status_code >= 400:
                    raise MODULE.requests.HTTPError(f"status={self.status_code}", response=self)

            def json(self) -> dict:
                return self._payload

        calls: list[str] = []

        def _fake_post(url: str, data: str, timeout: int):
            calls.append(url)
            if url == MODULE.OVERPASS_URLS[0]:
                return _Resp(504)
            return _Resp(200, {"elements": []})

        with mock.patch.object(MODULE.requests, "post", side_effect=_fake_post):
            with mock.patch.object(MODULE.time, "sleep", return_value=None):
                payload = MODULE._query_overpass_buildings((-105.2, 40.0, -105.1, 40.1), timeout_s=5)

        self.assertEqual(payload, {"elements": []})
        self.assertEqual(calls[0], MODULE.OVERPASS_URLS[0])
        self.assertIn(MODULE.OVERPASS_URLS[1], calls)


if __name__ == "__main__":
    unittest.main()
