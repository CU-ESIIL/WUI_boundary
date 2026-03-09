"""Unit tests for minimal streaming WUI module."""

from __future__ import annotations

import unittest
from unittest import mock

try:
    import numpy as np
    from rasterio.transform import from_origin
    from shapely.geometry import box
    from boundary_analytics.streaming_wui import (
        coarsen_binary_mask,
        interface_length_m,
        local_pixel_size_m,
        mask_to_union,
        query_osm_buildings_with_fallback,
    )
    STREAMING_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - environment dependent
    STREAMING_IMPORT_ERROR = exc


@unittest.skipIf(STREAMING_IMPORT_ERROR is not None, f"streaming deps unavailable: {STREAMING_IMPORT_ERROR}")
class StreamingModuleTests(unittest.TestCase):
    def test_coarsen_binary_mask_majority_rule(self) -> None:
        mask = np.array(
            [[1, 1, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1], [0, 0, 1, 1]],
            dtype=np.uint8,
        )
        coarse = coarsen_binary_mask(mask, 2)
        expected = np.array([[1, 0], [1, 1]], dtype=np.uint8)
        np.testing.assert_array_equal(coarse, expected)

    def test_local_pixel_size_estimation(self) -> None:
        transform = from_origin(-105.271, 40.021, 0.0001, 0.0001)
        px_m, epsg = local_pixel_size_m(transform, (-105.271, 40.018, -105.268, 40.021))
        self.assertGreater(px_m, 5.0)
        self.assertLess(px_m, 20.0)
        self.assertEqual(epsg, 32613)

    def test_mask_to_polygon_conversion(self) -> None:
        mask = np.array([[1, 1], [0, 0]], dtype=np.uint8)
        geom = mask_to_union(mask, from_origin(0, 2, 1, 1))
        self.assertIsNotNone(geom)
        self.assertAlmostEqual(float(geom.area), 2.0)

    def test_interface_length_calculation(self) -> None:
        settlement = box(0, 0, 10, 10)
        vegetation = box(8, 0, 20, 10)
        value = interface_length_m(settlement, vegetation, 0.0)
        self.assertAlmostEqual(value, 20.0)

    def test_overpass_fallback(self) -> None:
        class FakeResp:
            def __init__(self, ok: bool):
                self.ok = ok

            def raise_for_status(self):
                if not self.ok:
                    raise RuntimeError("bad endpoint")

            def json(self):
                return {
                    "elements": [
                        {
                            "geometry": [
                                {"lon": -105.0, "lat": 40.0},
                                {"lon": -105.0, "lat": 40.001},
                                {"lon": -105.001, "lat": 40.001},
                                {"lon": -105.001, "lat": 40.0},
                            ]
                        }
                    ]
                }

        def fake_post(url, data, headers, timeout):
            return FakeResp(ok=not url.startswith("https://bad"))

        with mock.patch("boundary_analytics.streaming_wui.time.sleep", return_value=None):
            gdf = query_osm_buildings_with_fallback(
                (-105.1, 40.0, -105.0, 40.1),
                endpoints=["https://bad.endpoint", "https://good.endpoint"],
                attempts_per_endpoint=1,
                request_post=fake_post,
            )
        self.assertEqual(len(gdf), 1)


if __name__ == "__main__":
    unittest.main()
