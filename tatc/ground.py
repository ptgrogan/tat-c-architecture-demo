#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for managing ground system elements including
    ground stations.
"""

import json
import itertools

from .util import Entity, CommunicationBand, QuantitativeValue, QuantitativeRange
from .agency import Agency

class Region(Entity):
    """A region or point designated by bounding latitudes and longitudes.

    Attributes:
        latitude    Latitude (decimal degrees) with respect to the WGS 84
                    geodetic model. Ranges between -90° (south) and 90° (north)
                    where 0° represents the equator.
        longitude   Longitude (decimal degrees) with respect to the WGS 84
                    geodetic model. Ranges between -180° (west) and 180° (east)
                    where 0° represents the prime meridian.
    """

    def __init__(self, latitude=None, longitude=None, _id=None):
        """Initialize a region object.
        """
        self.latitude = latitude
        self.longitude = longitude
        super(Region,self).__init__(_id, "Region")

    @staticmethod
    def from_dict(d):
        """Parses a region from a normalized JSON dictionary."""
        return Region(
                latitude = QuantitativeValue.from_json(d.get("latitude", None)),
                longitude = QuantitativeValue.from_json(d.get("longitude", None)),
                _id = d.get("@id", None)
            )

class GroundStation(Entity):
    """A surface facility providing uplink or downlink communication services
    to satellites.

    Attributes:
        name        Full name of this launch vehicle.
        acronym     Acronym, initialism, or abbreviation.
        agency      Designer, provider, or operator of this entity.
        latitude    Latitude (decimal degrees) with respect to the WGS 84
                    geodetic model. Ranges between -90° (south) and 90° (north)
                    where 0° represents the equator.
        longitude   Longitude (decimal degrees) with respect to the WGS 84
                    geodetic model. Ranges between -180° (west) and 180° (east)
                    where 0° represents the prime meridian.
        elevation   Elevation (m) above mean sea level with respect to the WGS
                    84 geodetic model.
        commBand    List of communication bands avaialble for broadcast.
                    Recognized values include: VHF, UHF, L, S, C, X, Ku, Ka.
    """

    def __init__(self, name=None, acronym=None, agency=None, latitude=None,
                 longitude=None, elevation=None, commBand=None, _id=None):
        """Initialize a ground station object.
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.agency = agency
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.commBand = commBand
        super(GroundStation,self).__init__(_id, "GroundStation")

    @staticmethod
    def from_dict(d):
        """Parses a ground station from a normalized JSON dictionary."""
        return GroundStation(
                name = d.get("name", None),
                acronym = d.get("acronym", None),
                agency = Agency.from_json(d.get("agency", None)),
                latitude = QuantitativeValue.from_json(d.get("latitude", None)),
                longitude = QuantitativeValue.from_json(d.get("longitude", None)),
                elevation = d.get("elevation", None),
                commBand = CommunicationBand.get(d.get("commBand", None)),
                _id = d.get("@id", None)
            )

class GroundNetwork(Entity):
    """A network of ground stations providing communication services.

    Attributes:
        name        Full name of this launch vehicle.
        acronym     Acronym, initialism, or abbreviation.
        agency      Designer, provider, or operator of this entity.
        numberStations    Number of ground stations participating in the network.
        groundStations    List of member ground stations in this network.
    """

    def __init__(self, name=None, acronym=None, agency=None, numberStations=None,
                 groundStations=None, _id=None):
        """Initialize a ground network object.
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.agency = agency
        self.numberStations = numberStations
        self.groundStations = groundStations
        super(GroundNetwork,self).__init__(_id, "GroundNetwork")

    def generate_networks(self, groundStations):
        """Generates networks for a given set of ground stations."""
        networks = []
        # iterate over all networks
        for network in self:
            # valid stations must have compatible agency types
            validStations = [station for station in groundStations
                    if network.agency is None or
                    (station.agency is not None and station.agency.agencyType is network.agency.agencyType)]
            # iterate over all possible combinations of valid stations
            for selectedStations in itertools.combinations(validStations, network.numberStations):
                # append a new network
                networks.append(
                    GroundNetwork(
                        name=network.name,
                        acronym=network.acronym,
                        agency=network.agency,
                        numberStations=network.numberStations,
                        groundStations=list(selectedStations)
                    )
                )
        return networks

    def __iter__(self):
        """Iterates valid ground networks."""
        # if ground stations specified, return self
        if self.groundStations is not None:
            return iter([self])

        # iterate number stations
        try:
            numberStationsIter = iter(self.numberStations)
        except TypeError:
            numberStationsIter = [self.numberStations]
        # return the Cartesian product of iterated values
        return iter([
                GroundNetwork(
                    name=self.name,
                    acronym=self.acronym,
                    agency=self.agency,
                    numberStations=numberStations
                )
                for numberStations,
                in itertools.product(numberStationsIter)
            ])

    @staticmethod
    def from_dict(d):
        """Parses a ground network from a normalized JSON dictionary."""
        return GroundNetwork(
                name = d.get("name", None),
                acronym = d.get("acronym", None),
                agency = Agency.from_json(d.get("agency", None)),
                numberStations = QuantitativeRange.from_json(d.get("numberStations", None)),
                groundStations = GroundStation.from_json(d.get("groundStations", None)),
                _id = d.get("@id", None)
            )
