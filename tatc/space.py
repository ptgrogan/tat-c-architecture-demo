#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for managing space system elements including
    satellites, orbits, and constellations.
"""

import json
import math
from numbers import Number
import isodate
import datetime
import itertools
import copy

from .util import Entity, EnumEntity, CommunicationBand, QuantitativeRange
from .instrument import Instrument
from .launch import LaunchVehicle

class PropellantType(EnumEntity):
    """Enumeration of recognized propellant types."""
    COLD_GAS = "COLD_GAS"
    SOLID = "SOLID"
    LIQUID_MONO_PROP = "LIQUID_MONO_PROP"
    LIQUID_BI_PROP = "LIQUID_BI_PROP"
    HYBRID = "HYBRID"
    ELECTROTHERMAL = "ELECTROTHERMAL"
    ELECTROSTATIC = "ELECTROSTATIC"
    MONO_PROP = "MONO_PROP"

class StabilizationType(EnumEntity):
    """Enumeration of recognized stabilization types."""
    AXIS_3 = "AXIS_3"
    SPINNING = "SPINNING"
    GRAVITY_GRADIENT = "GRAVITY_GRADIENT"

class Satellite(Entity):
    """An entity orbiting the Earth in support of mission objectives.

    Attributes:
        name        Full name of this entity.
        acronym     Acronym, initialism, or abbreviation.
        mass        Total mass (kg) including any consumable propellant or
                    gases.
        volume      Total volume (m3).
        power       Nominal operating power (W).
        commBand    List of communication bands avaialble for broadcast.
                    Recognized values include: VHF, UHF, L, S, C, X, Ku, Ka,
                    Laser.
        payload     List of instruments carried onboard this satellite.
        orbit       Orbital trajectory of this satellite.
        techReadinessLevel  Spacecraft technology readiness level (default: 9).
        isGroundCommand     Command performed by ground station (default: True).
        isSpare             Spacecraft is a spare (default: False)
        propellantType      Type of propellant. Recognized values include:
                                COLD_GAS, SOLID, LIQUID_MONO_PROP, LIQUID_BI_PROP
                                HYBRID, ELECTROTHERMAL, ELECTROSTATIC,
                                MONO_PROP (default)
        stabilizationType   Type of spacecraft stabilization. Recognized values include:
                                AXIS_3 (default), SPINNING, GRAVITY_GRADIENT
    """

    def __init__(self, name=None, acronym=None, mass=0.0, volume=0.0,
                 power=0.0, commBand=None, payload=None, orbit=None,
                 techReadinessLevel=9, isGroundCommand=True, isSpare=False,
                 propellantType="MONO_PROP", stabilizationType="AXIS_3", _id=None):
        """Initialize a satellite object.
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.mass = mass
        self.volume = volume
        self.power = power
        self.commBand = commBand
        self.payload = payload
        self.orbit = orbit
        self.techReadinessLevel = techReadinessLevel
        self.isGroundCommand = isGroundCommand
        self.isSpare = isSpare
        self.propellantType = propellantType
        self.stabilizationType = stabilizationType
        super(Satellite,self).__init__(_id, "Satellite")

    @staticmethod
    def from_dict(d):
        """Parses a satellite from a normalized JSON dictionary."""
        return Satellite(
                name = d.get("name", None),
                acronym = d.get("acronym", None),
                mass = d.get("mass", 0),
                volume = d.get("volume", 0),
                power = d.get("power", 0),
                commBand = CommunicationBand.get(d.get("commBand", None)),
                payload = Instrument.from_json(d.get("payload", None)),
                orbit = Orbit.from_json(d.get("orbit", None)),
                techReadinessLevel = d.get("techReadinessLevel", 9),
                isGroundCommand = d.get("isGroundCommand", True),
                isSpare = d.get("isSpare", False),
                propellantType = d.get("propellantType", "MONO_PROP"),
                stabilizationType = d.get("stabilizationType", "AXIS_3"),
                _id = d.get("@id", None)
            )

class OrbitType(EnumEntity):
    """Enumeration of recognized orbit types."""
    KEPLERIAN = "KEPLERIAN"
    CIRCULAR = "CIRCULAR"
    SUN_SYNCHRONOUS = "SUN_SYNCHRONOUS"

class Orbit(Entity):
    """An orbital trajectory about the Earth.

    Attributes:
        orbitType       Type of orbit. Recognized values include: KEPLERIAN,
                        CIRCULAR, SUN_SYNCHRONOUS.
        altitude        Average distance (km) above mean sea level with respect
                        to the WGS 84 geodetic model (for circular orbits).
                        **Multiple values allowed for a design space.**
        inclination     Angle (decimal degrees) of an obrital trajectory with
                        respect to the equatorial plane. Ranges between 0 for
                        a prograde (with Earth's rotation) equatorial orbit to
                        180 for a retrograde (opposite of Earth's rotation)
                        equatorial orbit. Also accepts special values including:
                        SSO (sun-synchronous).
                        **Multiple values allowed for a design space.**
        semimajorAxis   Average of the distances (km) of periapsis (closest
                        approach) and apoapsis (furthest extent) between the
                        center of masses of a planetary body and a satellite.
        eccentricity    Nondimensional measure of deviation from a circular
                        orbit. Ranges from 0.0 for a circular orbit to 1.0 for
                        a parabolic escape orbit or > 1 for hyperbolic escape
                        orbits.
        periapsisArgument   Angle (decimal degrees) between the ascending node
                        (location at which the orbit crosses the equatorial
                        plane moving north) and the periapsis (point of closest
                        extent).
        rightAscensionAscendingNode     Angle (decimal degrees) between the
                        ascending node (location at which the orbit crosses the
                        equatorial plane moving north) and the frame's vernal
                        point (vector between the Sun and the Earth on the
                        vernal equinox).
        trueAnomaly     Angle (decimal degrees) between the satellite and its
                        argument of periapsis.
        epoch           The initial or reference point in time for a set of
                        Keplerian orbital elements.
        localSolarTimeAscendingNode     Local time (ISO 8601) as measured by
                        the angle of the sun when crossing the equator in the
                        northerly (ascending) direction.
        """

    def __init__(self, orbitType=None, altitude=None, inclination=None,
                 semimajorAxis=None, eccentricity=None, periapsisArgument=None,
                 rightAscensionAscendingNode=None, trueAnomaly=None, epoch=None,
                 localSolarTimeAscendingNode=None, _id=None):
        """Initialize an orbit object.
        """
        self.orbitType = OrbitType.get(orbitType)
        self.altitude = altitude
        # compute and assign special inclination for sun-synchronous orbits
        if isinstance(self.altitude, Number) and (inclination == "SSO" or self.orbitType == OrbitType.SUN_SYNCHRONOUS):
            self.inclination = Orbit.get_sso_inclination(self.altitude)
        else: self.inclination = inclination
        self.semimajorAxis = semimajorAxis
        # assign 0 eccentricity for circular orbits
        if self.orbitType == OrbitType.CIRCULAR or self.orbitType == OrbitType.SUN_SYNCHRONOUS:
            self.eccentricity = 0.0
        # assign 0 eccentricity for Keplerian orbits with missing information
        elif self.orbitType == OrbitType.KEPLERIAN and eccentricity is None:
            self.eccentricity = 0.0
        else: self.eccentricity = eccentricity
        # assign 0 periapsis arg for Keplerian orbits with missing information
        if self.orbitType == OrbitType.KEPLERIAN and periapsisArgument is None:
            self.periapsisArgument = 0.0
        else: self.periapsisArgument = periapsisArgument
        self.rightAscensionAscendingNode = rightAscensionAscendingNode
        self.trueAnomaly = trueAnomaly
        self.epoch = epoch
        self.localSolarTimeAscendingNode = localSolarTimeAscendingNode
        super(Orbit,self).__init__(_id, "Orbit")

    def __iter__(self):
        """Iterates valid orbits."""
        # iterate altitudes
        try: altitudeIter = iter(self.altitude)
        except TypeError: altitudeIter = [self.altitude]
        # iterate inclinations
        try:
            if isinstance(self.inclination, str): raise TypeError
            inclinationIter = iter(self.inclination)
        except TypeError: inclinationIter = [self.inclination]

        # return the Cartesian product of iterated values
        return iter([
                Orbit(
                    orbitType=self.orbitType,
                    altitude=altitude,
                    inclination=inclination,
                    semimajorAxis=self.semimajorAxis,
                    eccentricity=self.eccentricity,
                    periapsisArgument=self.periapsisArgument,
                    rightAscensionAscendingNode=self.rightAscensionAscendingNode,
                    trueAnomaly=self.trueAnomaly,
                    epoch=self.epoch,
                    localSolarTimeAscendingNode=self.localSolarTimeAscendingNode
                )
                for altitude, inclination
                in itertools.product(altitudeIter, inclinationIter)
            ])

    @staticmethod
    def get_orbital_period(altitude):
        """Returns the orbital period (s) for a given altitude (km)."""
        re = 6378.14 # radius of the earth (km)
        sma = re + altitude # semimajor axis (km)
        mu = 3.98600440*(10**5) # gravitational constant (km^3/s^2)
        return 2*math.pi*math.sqrt((sma**3)/mu)

    @staticmethod
    def get_semimajor_axis(altitude):
        re = 6378.14 # radius of the earth (km)
        return re + altitude

    @staticmethod
    def get_sso_inclination(altitude):
        """Returns the sun-synchronous inclination (deg) for a given altitude (km)."""
        re = 6378.14 # radius of the earth (km)
        coef = 10.10949 # calculation coefficient
        return math.degrees(math.acos((((re+altitude)/re)**3.5)/(-coef)))

    @staticmethod
    def from_dict(d):
        """Parses a satellite from a normalized JSON dictionary."""
        return Orbit(
                orbitType = d.get("orbitType", None),
                altitude = QuantitativeRange.from_json(d.get("altitude", None)),
                inclination = QuantitativeRange.from_json(d.get("inclination", None)),
                semimajorAxis = d.get("semimajorAxis", None),
                eccentricity = d.get("eccentricity", None),
                periapsisArgument = d.get("periapsisArgument", None),
                rightAscensionAscendingNode = d.get("rightAscensionAscendingNode", None),
                trueAnomaly = d.get("trueAnomaly", None),
                epoch = d.get("epoch", None),
                localSolarTimeAscendingNode = d.get("localSolarTimeAscendingNode", None),
                _id = d.get("@id", None)
            )

class ConstellationType(EnumEntity):
    """Enumeration of recognized constellation types."""
    DELTA_HOMOGENOUS = "DELTA_HOMOGENOUS"
    DELTA_HETEROGENEOUS = "DELTA_HETEROGENEOUS"
    PRECESSING = "PRECESSING"
    AD_HOC = "AD_HOC"
    TRAIN = "TRAIN"

class Constellation(Entity):
    """A set of orbital trajectories about the Earth.

    Attributes:
        constellationType   Type of constellation. Recognized values include:
                            DELTA_HOMOGENOUS, DELTA_HETEROGENEOUS, PRECESSING,
                            AD_HOC, TRAIN.
        numberSatellites    Total number of satellites.
                            **Multiple values allowed for a design space.**
        numberPlanes        Number of equally-spaced orbital planes for a
                            Walker-type constellation. Ranges from 1 to
                            (number of satellites). Defaults to 1 for Walker
                            Delta constellations.
                            **Multiple values allowed for a design space.**
        relativeSpacing     Relative spacing of satellites between plans for a
                            Walker-type constellation. Ranges from 0 for equal
                            true anomaly to (number of planes) - 1. Defaults to
                            1 for sun-synchronous multi-plane Walker Delta
                            constellations or 0 for other Walker Delta
                            constellations.
                            **Multiple values allowed for a design space.**
        satelliteInterval   The local time interval (ISO 8601 format) between
                            satellites in a train-type constellation.
                            **Multiple values allowed for a design space.**
        orbit               Orbital trajectory of member satellites.
                            **Multiple values allowed for a design space.**
        satellites          List of member satellites.
        """
    def __init__(self, constellationType=None, numberSatellites=1, numberPlanes=None,
                relativeSpacing=None, satelliteInterval=None, orbit=None,
                satellites=None, _id=None):
        """Initialize a constellation object.
        """
        self.constellationType = ConstellationType.get(constellationType)
        self.numberSatellites = numberSatellites
        # assign default value of 1 plane for delta constellations
        if numberPlanes is None and (self.constellationType == ConstellationType.DELTA_HOMOGENOUS
                or self.constellationType == ConstellationType.DELTA_HETEROGENEOUS):
            self.numberPlanes = 1
        else: self.numberPlanes = numberPlanes

        # assign default relative spacing value for delta constellations
        if relativeSpacing is None and isinstance(self.numberPlanes, Number) and (
                self.constellationType == ConstellationType.DELTA_HOMOGENOUS
                or self.constellationType == ConstellationType.DELTA_HETEROGENEOUS):
            # assign relative spacing of 1 for multi-plane sun-synchronous constellations
            if isinstance(orbit, Orbit) and self.numberPlanes > 1 and (
                    orbit.orbitType == OrbitType.SUN_SYNCHRONOUS
                    or orbit.inclination == "SSO"):
                self.relativeSpacing = 1
            # otherwise assign relative spacing of 0
            else: self.relativeSpacing = 0
        else:
            self.relativeSpacing = relativeSpacing
        if isinstance(satelliteInterval, Number):
            self.satelliteInterval = isodate.duration_isoformat(datetime.timedelta(minutes=satelliteInterval))
        else: self.satelliteInterval = satelliteInterval
        self.orbit = orbit
        self.satellites = satellites
        super(Constellation,self).__init__(_id, "Constellation")

    def generate_delta_orbits(self):
        """Generates Walker delta orbital elements for each member satellite."""
        orbits = []
        for satellite in range(self.numberSatellites):
            satellitesPerPlane = math.ceil(self.numberSatellites/self.numberPlanes)
            plane = int(satellite / satellitesPerPlane)
            orbits.append(
                Orbit(
                    orbitType="KEPLERIAN",
                    inclination=self.orbit.inclination,
                    semimajorAxis=Orbit.get_semimajor_axis(self.orbit.altitude),
                    eccentricity=self.orbit.eccentricity,
                    periapsisArgument=self.orbit.periapsisArgument,
                    rightAscensionAscendingNode=(satellite / satellitesPerPlane)*360./self.numberPlanes,
                    trueAnomaly=((satellite % satellitesPerPlane)*self.numberPlanes
                                 + self.relativeSpacing*plane)*360./(satellitesPerPlane*self.numberPlanes),
                    epoch=None
                )
            )
        return orbits

    def generate_constellations(self, satellites):
        """Generates constellations for a given set of satellites."""
        if self.constellationType == ConstellationType.DELTA_HOMOGENOUS:
            constellations = []
            # generate one constellation iteration per satellite
            for constellation in self:
                for satellite in satellites:
                    selectedSatellites = [copy.deepcopy(satellite) for i in range(constellation.numberSatellites)]
                    for i, orbit in enumerate(self.generate_delta_orbits()):
                        selectedSatellites[i].orbit = orbit
                    constellations.append(
                        Constellation(
                            constellationType=constellation.constellationType,
                            numberSatellites=constellation.numberSatellites,
                            numberPlanes=constellation.numberPlanes,
                            relativeSpacing=constellation.relativeSpacing,
                            orbit=constellation.orbit,
                            satellites=selectedSatellites
                        )
                    )
            return constellations
        elif self.constellationType == ConstellationType.DELTA_HETEROGENEOUS:
            # generate one constellation iteration per satellite combination
            constellations = []
            for constellation in self:
                for combinations in itertools.combinations_with_replacement(
                        satellites, constellation.numberSatellites):
                    selectedSatellites = [copy.deepcopy(i) for i in combinations]
                    for i, orbit in enumerate(self.generate_delta_orbits()):
                        selectedSatellites[i].orbit = orbit
                    constellations.append(
                        constellationType=constellation.constellationType,
                        numberSatellites=constellation.numberSatellites,
                        numberPlanes=constellation.numberPlanes,
                        relativeSpacing=constellation.relativeSpacing,
                        orbit=constellation.orbit,
                        satellites=list(selectedSatellites)
                    )
            return constellations
        else:
            raise NotImplementedError

    def __iter__(self):
        """Iterates valid constellations."""
        # if member satellites specified, return self
        if self.satellites is not None:
            return iter([self])
        # iterate number satellites
        try: numberSatellitesIter = iter(self.numberSatellites)
        except TypeError: numberSatellitesIter = [self.numberSatellites]
        # iterate number planes
        try: numberPlanesIter = iter(self.numberPlanes)
        except TypeError: numberPlanesIter = [self.numberPlanes]
        # iterate relative phasing
        try: relativeSpacingIter = iter(self.relativeSpacing)
        except TypeError: relativeSpacingIter = [self.relativeSpacing]
        # iterate satellite interval
        try:
            if isinstance(self.satelliteInterval, str): raise TypeError
            satelliteIntervalIter = iter(self.satelliteInterval)
        except TypeError: satelliteIntervalIter = [self.satelliteInterval]
        # iterate orbit
        try: orbitIter = iter(self.orbit)
        except TypeError: orbitIter = [self.orbit]
        # return the Cartesian product of iterated values
        return iter([
                Constellation(
                    constellationType=self.constellationType,
                    numberSatellites=numberSatellites,
                    numberPlanes=numberPlanes,
                    relativeSpacing=relativeSpacing,
                    satelliteInterval=satelliteInterval,
                    orbit=orbit
                )
                for numberSatellites, numberPlanes, relativeSpacing, satelliteInterval, orbit
                in itertools.product(numberSatellitesIter, numberPlanesIter, relativeSpacingIter, satelliteIntervalIter, orbitIter)
                if ((relativeSpacing is None or
                        numberPlanes is None or
                        relativeSpacing < numberPlanes) and
                    (numberSatellites is None or
                        numberPlanes is None or
                        numberPlanes <= numberSatellites))
            ])

    @staticmethod
    def from_dict(d):
        """Parses a constellation from a normalized JSON dictionary."""
        return Constellation(
                constellationType = d.get("constellationType", None),
                numberSatellites = QuantitativeRange.from_json(d.get("numberSatellites", 1)),
                numberPlanes = QuantitativeRange.from_json(d.get("numberPlanes", None)),
                relativeSpacing = QuantitativeRange.from_json(d.get("relativeSpacing", None)),
                satelliteInterval = d.get("satelliteInterval", None),
                orbit = Orbit.from_json(d.get("orbit", None)),
                satellites = Satellite.from_json(d.get("satellites", None)),
                _id = d.get("@id", None)
            )
