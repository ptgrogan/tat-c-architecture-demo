#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for space missions.
"""

import json
import isodate
import datetime
from numbers import Number
import itertools

from .util import Entity, EnumEntity
from .agency import Agency
from .space import Satellite, Constellation
from .ground import GroundStation, GroundNetwork, Region, GLOBAL_REGION
from .launch import LaunchVehicle
from .instrument import Instrument

class MissionConcept(Entity):
    """Top-level functional description of an Earth-observing mission.

    Attributes:
        name        Full name of this entity.
        acronym     Acronym, initialism, or abbreviation.
        agency      Designer, provider, or operator of this entity.
        start       Mission start in ISO-8601 datetime format.
                    (default: today)
        duration    Mission duration in ISO-8601 duration format.
                    (default: P90D, 90 days)
        target      Target region of interest for mission objectives.
                    (default: GLOBAL_REGION)
        objectives  List of mission objectives.
    """

    def __init__(self, name=None, acronym=None, agency=None,
                start=datetime.date.today().isoformat(), duration="P90D",
                target=GLOBAL_REGION, objectives=None, _id=None):
        """Initialize a mission concept object.
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.agency = agency
        self.start = start
        if isinstance(duration, Number):
            self.duration = isodate.duration_isoformat(datetime.timedelta(days=duration))
        else: self.duration = duration
        self.target = target
        # convert objectives to list, if necessary
        if isinstance(objectives, str): self.objectives = [objectives]
        else: self.objectives = objectives
        super(MissionConcept, self).__init__(_id, "MissionConcept")

    @staticmethod
    def from_dict(d):
        """Parses a mission concept from a normalized JSON dictionary."""
        return MissionConcept(
                name = d.get("name", None),
                acronym = d.get("acronym", None),
                agency = Agency.from_json(d.get("agency", None)),
                start = d.get("start", datetime.date.today().isoformat()),
                duration = d.get("duration", "P90D"),
                target = Region.from_json(d.get("target", GLOBAL_REGION)),
                objectives = MissionObjective.from_json(d.get("objectives", None)),
                _id = d.get("@id", None)
            )

class MissionObjective(Entity):
    """A variable to be maximized or minimized to acheive mission objectives.

    Attributes:
        name        The full name of this objective.
        parent      The full name of the parent objective.
        weight      Weight or importance of this metric, ranging between 0 to inf
        type        Type of metric. Recognized case-insensitive values include:
                        MAX (maximize)
                        MIN (minimize)
                        TAR (target)
        target      Target value for the objective. Required for TAR type only.
    """

    def __init__(self, name=None, parent=None, weight=None, type=None,
            target=None, _id=None):
        """Initialize a mission objective.
        """
        self.name = name
        self.parent = parent
        self.weight = weight
        self.type = ObjectiveType.get(type)
        self.target = target
        super(MissionObjective,self).__init__(_id, "MissionObjective")

    @staticmethod
    def from_dict(d):
        """Parses a mission objective from a normalized JSON dictionary."""
        return MissionObjective(
                name = d.get("name", None),
                parent = d.get("parent", None),
                weight = d.get("weight", None),
                type = d.get("type", None),
                target = d.get("target", None),
                _id = d.get("@id", None)
        )

class ObjectiveType(EnumEntity):
    """Enumeration of recognized objective types."""
    MAX = "MAX"
    MIN = "MIN"
    TAR = "TAR"

class DesignSpace(Entity):
    """Specification of fixed and variable quantities for a space mission.

    Attributes:
        constellations  List of potential constellations to consider.
        launchers       List of available launch vehicles to consider
                        (overrides default database).
        satellites      List of available satellites.
        groundNetworks  List of potential ground networks to consider.
        groundStations  List of available ground stations.
    """

    def __init__(self, constellations=None, launchers=None, satellites=None,
                 groundNetworks=None, groundStations=None, _id=None):
        """Initialize a design space object.
        """
        # convert constellations to list, if necessary
        if isinstance(constellations, Constellation): self.constellations = [constellations]
        else: self.constellations = constellations
        # convert launchers to list, if necessary
        if isinstance(launchers, LaunchVehicle): self.launchers = [launchers]
        else: self.launchers = launchers
        # convert satellites to list, if necessary
        if isinstance(satellites, Satellite): self.satellites  = [satellites]
        else: self.satellites = satellites
        # convert ground networks to list, if necessary
        if isinstance(groundNetworks, GroundNetwork): self.groundNetworks = [groundNetworks]
        else: self.groundNetworks = groundNetworks
        # convert ground stations to list, if necessary
        if isinstance(groundStations, GroundStation): self.groundStations = [groundStations]
        else: self.groundStations = groundStations
        super(DesignSpace,self).__init__(_id, "DesignSpace")

    def generate_architectures(self):
        """Generates architectures in this design space."""
        # merge lists of iterated constellations
        constellationsList = iter(iter(i) for i in self.constellations)
        constellationsIter = iter(set().union(*constellationsList))
        # merge lists of iterated ground networks
        groundNetworksList = iter(iter(i) for i in self.groundNetworks)
        groundNetworksIter = iter(set().union(*groundNetworksList))

        return iter([
                Architecture(
                    constellation=constellation,
                    groundNetwork=groundNetwork
                )
                for constellation, groundNetwork
                in itertools.product(
                    [i.generate_constellations(self.satellites) for i in constellationsIter],
                    [i.generate_networks(self.groundStations) for i in groundNetworksIter]
                )
            ])

    @staticmethod
    def from_dict(d):
        """Parses a design space from a normalized JSON dictionary."""
        return DesignSpace(
                constellations = Constellation.from_json(d.get("constellations", None)),
                launchers = LaunchVehicle.from_json(d.get("launchers", None)),
                satellites = Satellite.from_json(d.get("satellites", None)),
                groundNetworks = GroundNetwork.from_json(d.get("groundNetworks", None)),
                groundStations = GroundStation.from_json(d.get("groundStations", None)),
                _id = d.get("@id", None)
            )

class Architecture(Entity):
    """Instantiation of a space mission including satellites and ground stations.

    Attributes:
        constellation   Constellation of member satellites.
        groundNetwork   Network of member ground stations.
    """

    def __init__(self, constellation=None, groundNetwork=None, _id=None):
        """Initialize an architecture object.
        """
        self.constellation = constellation
        self.groundNetwork = groundNetwork
        super(Architecture, self).__init__(_id, "Architecture")

    @staticmethod
    def from_dict(d):
        """Parses an architecture from a normalized JSON dictionary."""
        return Architecture(
                constellation = Constellation.from_json(d.get("constellation", None)),
                groundNetwork = GroundNetwork.from_json(d.get("groundNetwork", None)),
                _id = d.get("@id", None)
            )
