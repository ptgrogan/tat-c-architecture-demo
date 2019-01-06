#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for managing launch vehicle elements.
"""

import json
import isodate
import datetime
from numbers import Number

from .util import Entity
from .agency import Agency

class LaunchVehicle(Entity):
    """An entity delivering satellites to orbit.

    Attributes:
        name        Full name of this launch vehicle.
        acronym     Acronym, initialism, or abbreviation.
        agency      Designer, provider, or operator of this entity.
        payloadMass     Maximum total mass (kg) available for payload.
        payloadVolume   Maximum total volume (m3) available for payload.
        dryMass     Mass of the entity (kg) without any consumable propellant.
        propellantMass  Maximum total mass (kg) available for propellantself.
        specificImpulse Measure of efficiency computed as the total impulse per
                    unit of propellant (s).
    """

    def __init__(self, name=None, acronym=None, agency=None, payloadMass=None,
                 payloadVolume=None, dryMass=None, propellantMass=None,
                 specificImpulse=None, massToLEO=None, reliability=None, cost=None,
                 meanTimeBetweenLaunches=None, _id=None):
        """Initialize a launch vehicle object.
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.agency = agency
        self.payloadMass = payloadMass
        self.payloadVolume = payloadVolume
        self.dryMass = dryMass
        self.propellantMass = propellantMass
        self.specificImpulse = specificImpulse
        self.massToLEO = massToLEO
        self.reliability = reliability
        self.cost = cost
        if isinstance(meanTimeBetweenLaunches, Number):
            self.meanTimeBetweenLaunches = isodate.duration_isoformat(datetime.timedelta(days=meanTimeBetweenLaunches))
        else:
            self.meanTimeBetweenLaunches = meanTimeBetweenLaunches
        super(LaunchVehicle,self).__init__(_id, "LaunchVehicle")

    @staticmethod
    def from_dict(d):
        """Parses a launch vehicle from a normalized JSON dictionary."""
        return LaunchVehicle(
                name = d.get("name", None),
                acronym = d.get("acronym", None),
                agency = Agency.from_json(d.get("agency", None)),
                payloadMass = d.get("payloadMass", None),
                payloadVolume = d.get("payloadVolume", None),
                dryMass = d.get("dryMass", None),
                propellantMass = d.get("propellantMass", None),
                specificImpulse = d.get("specificImpulse", None),
                massToLEO = d.get("massToLEO", None),
                reliability = d.get("reliability", None),
                cost = d.get("cost", None),
                meanTimeBetweenLaunches = d.get("meanTimeBetweenLaunches", None),
                _id = d.get("@id", None)
            )
