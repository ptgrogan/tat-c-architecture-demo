#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for tatc.launch module.
"""

import unittest
import json
import isodate
import datetime

from tatc import *

class TestLaunchVehicle(unittest.TestCase):
    def test_from_json_basic(self):
        o = LaunchVehicle.from_json('{"name": "Atlas V", "dryMass": 2316, "propellantMass": 20830, "specificImpulse": 450.5, "massToLEO": 9800, "reliability": 1, "cost": 130, "meanTimeBetweenLaunches": "P0Y0M133D"}')
        self.assertEqual(o.name, "Atlas V")
        self.assertIsNone(o.agency)
        self.assertEqual(o.dryMass, 2316)
        self.assertEqual(o.propellantMass, 20830)
        self.assertEqual(o.specificImpulse, 450.5)
        self.assertEqual(o.massToLEO, 9800)
        self.assertEqual(o.reliability, 1)
        self.assertEqual(o.cost, 130)
        self.assertEqual(isodate.parse_duration(o.meanTimeBetweenLaunches), isodate.parse_duration("P0Y0M133D"))
        self.assertEqual(o._type, "LaunchVehicle")
        self.assertIsNone(o._id)
    def test_from_json_agency(self):
        o = LaunchVehicle.from_json('{"name": "Atlas V", "agency": {"agencyType": "COMMERCIAL"}}')
        self.assertIsInstance(o.agency, Agency)
        self.assertEqual(o.agency.agencyType, AgencyType.COMMERCIAL)
    def test_from_json_numeric_duration(self):
        o = LaunchVehicle.from_json('{"meanTimeBetweenLaunches": 133}')
        self.assertEqual(isodate.parse_duration(o.meanTimeBetweenLaunches), datetime.timedelta(days=133))
    def test_to_json_basic(self):
        d = json.loads(LaunchVehicle(name="Atlas V", dryMass=2316, propellantMass=20830, specificImpulse=450.5, massToLEO=9800, reliability=1, cost=130, meanTimeBetweenLaunches="P0Y0M133D").to_json())
        self.assertEqual(d.get("name"), "Atlas V")
        self.assertEqual(d.get("dryMass"), 2316)
        self.assertEqual(d.get("propellantMass"), 20830)
        self.assertEqual(d.get("specificImpulse"), 450.5)
        self.assertEqual(d.get("massToLEO"), 9800)
        self.assertEqual(d.get("reliability"), 1)
        self.assertEqual(d.get("cost"), 130)
        self.assertEqual(d.get("meanTimeBetweenLaunches"), "P0Y0M133D")
        self.assertEqual(d.get("@type"), "LaunchVehicle")
        self.assertIsNone(d.get("@id"))
    def test_to_json_agency(self):
        d = json.loads(LaunchVehicle(name="Atlas V", agency=Agency(agencyType=AgencyType.COMMERCIAL)).to_json())
        self.assertEqual(d.get("agency").get("agencyType"), "COMMERCIAL")
    def test_to_json_numeric_duration(self):
        d = json.loads(LaunchVehicle(meanTimeBetweenLaunches=133).to_json())
        self.assertEqual(isodate.parse_duration(d.get("meanTimeBetweenLaunches")), datetime.timedelta(days=133))
