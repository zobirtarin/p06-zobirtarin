# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerFringeTestCase(FilterTestCase):
    @gen_test
    async def test_transparent_round_corner_has_no_dark_ring(self):
        # Issue #2: edge pixels of a transparent round corner must keep the
        # source color. The bug scales them toward black, which shows as a
        # dark ring. Compare the corner with the untouched source.
        image = await self.get_filtered(
            "source.jpg",
            "thumbor.filters.round_corner",
            "round_corner(60,255,255,255,1)",
            mode="RGBA",
        )
        source = self.get_fixture("source.jpg", mode="RGB")

        darkened = 0
        for x in range(60):
            for y in range(60):
                r, g, b, a = image.getpixel((x, y))
                if a == 0:
                    continue
                sr, sg, sb = source.getpixel((x, y))
                diff = (sr - r) + (sg - g) + (sb - b)
                if diff > 150:
                    darkened += 1

        assert darkened == 0, (
            f"{darkened} corner pixels are darker than the source (dark ring)"
        )
