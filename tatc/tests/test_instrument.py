#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for tatc.instrument module.
"""

import unittest
import json

from tatc import *

class TestInstrument(unittest.TestCase):
    def test_from_json_basic(self):
        o = Instrument.from_json('{"name": "OLI/TIRS", "agency": {"agencyType": "GOVERNMENT"}, "mass": 657, "volume": 10.016, "power": 319, "operatingWavelength": [443,482,561,655,865,1609,2201,590,1373,10900,12000], "pixelBitDepth": 12, "fieldOfView": 7.5, "numberPixels": 6250, "solarConditions": "SUNLIT"}')
        self.assertEqual(o.name, "OLI/TIRS")
        self.assertIsInstance(o.agency, Agency)
        self.assertEqual(o.agency.agencyType, AgencyType.GOVERNMENT)
        self.assertEqual(o.mass, 657)
        self.assertEqual(o.volume, 10.016)
        self.assertEqual(o.power, 319)
        self.assertItemsEqual(o.operatingWavelength, [443,482,561,655,865,1609,2201,590,1373,10900,12000])
        self.assertEqual(o.pixelBitDepth, 12)
        self.assertEqual(o.fieldOfView, 7.5)
        self.assertEqual(o.numberPixels, 6250)
        self.assertEqual(o.solarConditions, "SUNLIT")
        self.assertEqual(o._type, "Instrument")
        self.assertIsNone(o._id)
    def test_to_json_basic(self):
        d = json.loads(Instrument(name="OLI/TIRS", agency=Agency(agencyType="GOVERNMENT"), mass=657, volume=10.016, power=319, operatingWavelength=[443,482,561,655,865,1609,2201,590,1373,10900,12000], pixelBitDepth=12, fieldOfView=7.5, numberPixels=6250, solarConditions="SUNLIT").to_json())
        self.assertEqual(d.get("name"), "OLI/TIRS")
        self.assertEqual(d.get("agency").get("agencyType"), "GOVERNMENT")
        self.assertEqual(d.get("mass"), 657)
        self.assertEqual(d.get("volume"), 10.016)
        self.assertEqual(d.get("power"), 319)
        self.assertItemsEqual(d.get("operatingWavelength"), [443,482,561,655,865,1609,2201,590,1373,10900,12000])
        self.assertEqual(d.get("pixelBitDepth"), 12)
        self.assertEqual(d.get("fieldOfView"), 7.5)
        self.assertEqual(d.get("numberPixels"), 6250)
        self.assertEqual(d.get("solarConditions"), "SUNLIT")
        self.assertEqual(d.get("@type"), "Instrument")
        self.assertIsNone(d.get("@id"))
