#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for managing space system instruments.
"""

import json
from numbers import Number

from .util import Entity, EnumEntity
from .agency import Agency

class MountType(EnumEntity):
    """Enumeration of recognized instrument mount types."""
    BODY = "BODY"
    MAST = "MAST"
    PROBE = "PROBE"

class OrientationConvention(EnumEntity):
    """Enumeration of recognized instrument orientation conventions."""
    XYZ = "XYZ"
    SIDE_LOOK = "SIDE_LOOK"

class Orientation(Entity):
    """Orientation of the instrument with respect to the satellite body frame.

    Attributes:
        convention      Convention used to specify the orientation. Recognized
                        values include:
                            XYZ (x-axis, y-axis, z-axis rotation; default)
                            SIDE_LOOK (only specify side look (y-axis) angle)
        xRotation       Rotation angle (deg) about x-axis. Default: 0.
        yRotation       Rotation angle (deg) about y-axis. Default: 0.
        zRotation       Rotation angle (deg) about z-axis. Default: 0.
        sideLookAngle   Rotation angle (deg) about spacecraft side (y-axis).
    """
    def __init__(self, convention="XYZ", xRotation=None, yRotation=None,
            zRotation=None, sideLookAngle=None, _id=None):
        """Initializes an orientation object.
        """
        self.convention = OrientationConvention.get(convention)
        self.xRotation = xRotation if xRotation is not None else (0 if convention == "XYZ" else None)
        self.yRotation = yRotation if yRotation is not None else (0 if convention == "XYZ" else None)
        self.zRotation = zRotation if zRotation is not None else (0 if convention == "XYZ" else None)
        self.sideLookAngle = sideLookAngle
        super(Orientation,self).__init__(_id, "Orientation")

    def from_dict(d):
        """Parses an orientation from a normalized JSON dictionary."""
        return Orientation(
            convention = d.get("convention", "XYZ"),
            xRotation = d.get("xRotation ", None),
            yRotation = d.get("yRotation ", None),
            zRotation = d.get("zRotation ", None),
            sideLookAngle = d.get("sideLookAngle", None),
            _id = d.get("@id", None)
        )

class SensorGeometry(EnumEntity):
    """Enumeration of recognized instrument sensor geometries."""
    CONICAL = "CONICAL",
    RECTANGULAR = "RECTANGULAR"

class FieldOfView(Entity):
    """Field of view provided by an instrument.

    Attributes:
        sensorGeometry          Specification of sensor geometry. Recongized
                                values include:
                                    CONICAL
                                    RECTANGULAR (default)
        fullConeAngle           Angle (deg) of full FoV cone (for CONE geometry).
        alongTrackFieldOfView   Angle (deg) in along-track direction.
        crossTrackFieldOfView   Angle (deg) in cross-track direction.
    """
    def __init__(self, sensorGeometry="CONICAL", fullConeAngle=30,
            alongTrackFieldOfView=None, crossTrackFieldOfView=None, _id=None):
        """Initializes a field of view object.
        """
        self.sensorGeometry = SensorGeometry.get(sensorGeometry)
        self.fullConeAngle = fullConeAngle
        self.alongTrackFieldOfView = alongTrackFieldOfView
        self.crossTrackFieldOfView = crossTrackFieldOfView
        super(FieldOfView,self).__init__(_id, "FieldOfView")

    def from_dict(d):
        """Parses a field of view from a normalized JSON dictionary."""
        if isinstance(d, Number):
            # if d is a number, interpret as conical sensor with full cone angle
            return FieldOfView(
                sensorGeometry = "CONICAL",
                fullConeAngle = d
            )
        if (isinstance(d, list) and len(d) == 2
                and isinstance(d[0], Number) and isinstance(d[1], Number)):
            # if d is a numeric list of size 2, interpret as rectangular sensor
            # with cross-track x along-track angles
            return FieldOfView(
                sensorGeometry = "RECTANGULAR",
                alongTrackFieldOfView = d[1],
                crossTrackFieldOfView = d[0],
            )
        return FieldOfView(
            sensorGeometry = d.get("sensorGeometry", "CONICAL"),
            fullConeAngle = d.get("fullConeAngle", 30),
            alongTrackFieldOfView = d.get("alongTrackFieldOfView", None),
            crossTrackFieldOfView = d.get("crossTrackFieldOfView", None),
            _id = d.get("@id", None)
        )

class Instrument(Entity):
    """A payload component that performs scientific observation functions.

    Attributes:
        name        Full name of this entity.
        acronym     Acronym, initialism, or abbreviation.
        agency      Designer, provider, or operator of this entity.
        mass        Total mass (kg) of this entity including any consumable
                    propellants or gases.
        volume      Total volume (m3) of this entity.
        power       Nominal operating power (W).
        orientation     Instrument orientation with respect to the
                        satellite body frame.
        fieldOfView     Instrument field of view.
        dataRate        Rate of data recorded (Mbps) during nominal operations.
        techReadinessLevel  Instrument technology readiness level.
        mountType           Type of mounting. Recognized values include:
                            BODY (default), MAST, PROBE.
    """

    def __init__(self, name=None, acronym=None, agency=None, mass=None,
            volume=None, power=None, orientation=Orientation(),
            fieldOfView=FieldOfView(), dataRate=None, techReadinessLevel=9,
            mountType="BODY", _id=None, _type="Instrument"):
        """Initialize an instrument object.
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.agency = agency
        self.mass = mass
        self.volume = volume
        self.power = power
        self.orientation = orientation
        self.fieldOfView = fieldOfView
        self.dataRate = dataRate
        self.techReadinessLevel = techReadinessLevel
        self.mountType = MountType.get(mountType)
        super(Instrument,self).__init__(_id, _type)

    @staticmethod
    def from_dict(d):
        """Parses an instrument from a normalized JSON dictionary."""
        type = d.get("@type", "Instrument")
        if type == "Instrument":
            return Instrument(
                    name = d.get("name", None),
                    acronym = d.get("acronym", None),
                    agency = Agency.from_json(d.get("agency", None)),
                    mass = d.get("mass", None),
                    volume = d.get("volume", None),
                    power = d.get("power", None),
                    orientation = Orientation.from_json(d.get("orientation", Orientation())),
                    fieldOfView = FieldOfView.from_json(d.get("fieldOfView", FieldOfView())),
                    dataRate = d.get("dataRate", None),
                    techReadinessLevel = d.get("techReadinessLevel", 9),
                    mountType = d.get("mountType", "BODY"),
                    _id = d.get("@id", None)
                )
        elif type == "OpticalScanner":
            return OpticalScanner(
                    name = d.get("name", None),
                    acronym = d.get("acronym", None),
                    agency = Agency.from_json(d.get("agency", None)),
                    mass = d.get("mass", None),
                    volume = d.get("volume", None),
                    power = d.get("power", None),
                    orientation = Orientation.from_json(d.get("orientation", Orientation())),
                    fieldOfView = FieldOfView.from_json(d.get("fieldOfView", FieldOfView())),
                    dataRate = d.get("dataRate", None),
                    scanTechnique = d.get("scanTechnique", None),
                    numberDetectorsAlongTrack = d.get("numberDetectorsAlongTrack", None),
                    numberDetectorsCrossTrack = d.get("numberDetectorsCrossTrack", None),
                    fNumber = d.get("fNumber", None),
                    focalLength = d.get("focalLength", None),
                    operatingWavelength = d.get("operatingWavelength", None),
                    bandwidth = d.get("bandwidth", None),
                    quantumEfficiency = d.get("quantumEfficiency", None),
                    opticalTransmissionFactor = d.get("opticalTransmissionFactor", None),
                    numberReadOutElectrons = d.get("numberReadOutElectrons", None),
                    targetBlackBodyTemp = d.get("targetBlackBodyTemp", None),
                    bitsPerPixel = d.get("bitsPerPixel", None),
                    detectorWidth = d.get("detectorWidth", None),
                    techReadinessLevel = d.get("techReadinessLevel", 9),
                    mountType = d.get("mountType", "BODY"),
                    _id = d.get("@id", None)
                )
        elif type == "SyntheticApertureRadar":
            return SyntheticApertureRadar(
                    name = d.get("name", None),
                    acronym = d.get("acronym", None),
                    agency = Agency.from_json(d.get("agency", None)),
                    mass = d.get("mass", None),
                    volume = d.get("volume", None),
                    power = d.get("power", None),
                    orientation = Orientation.from_json(d.get("orientation", Orientation())),
                    dataRate = d.get("dataRate", None),
                    pulseWidth = d.get("pulseWidth", None),
                    antennaDimensionAlongTrack = d.get("antennaDimensionAlongTrack", None),
                    antennaDimensionCrossTrack = d.get("antennaDimensionCrossTrack", None),
                    antennaApertureEfficiency = d.get("antennaApertureEfficiency", None),
                    operatingFrequency = d.get("operatingFrequency", None),
                    peakTransmitPower = d.get("peakTransmitPower", None),
                    chirpBandwidth = d.get("chirpBandwidth", None),
                    minPulseRepetitionFrequency = d.get("minPulseRepetitionFrequency", None),
                    maxPulseRepetitionFrequency = d.get("maxPulseRepetitionFrequency", None),
                    sceneNoiseTemp = d.get("sceneNoiseTemp", None),
                    systemNoiseFigure = d.get("systemNoiseFigure", None),
                    radarLosses = d.get("radarLosses", None),
                    thresholdSigmaNEZ0 = d.get("thresholdSigmaNEZ0", None),
                    techReadinessLevel = d.get("techReadinessLevel", 9),
                    mountType = d.get("mountType", "BODY"),
                    _id = d.get("@id", None)
                )

class ScanTechnique(EnumEntity):
    PUSHBROOM = "PUSHBROOM"
    WHISKBROOM = "WHISKBROOM"
    STEP_AND_STARE = "STEP_AND_STARE"

class OpticalScanner(Instrument):
    def __init__(self, name=None, acronym=None, agency=None, mass=None,
            volume=None, power=None, orientation=Orientation(),
            fieldOfView=FieldOfView(), dataRate=None, scanTechnique=None,
            numberDetectorsAlongTrack=None, numberDetectorsCrossTrack=None,
            fNumber=None, focalLength=None, operatingWavelength=None, bandwidth=None,
            quantumEfficiency=None, opticalTransmissionFactor=None,
            numberReadOutElectrons=None, targetBlackBodyTemp=None, bitsPerPixel=None,
            detectorWidth=None, techReadinessLevel=9, mountType="BODY", _id=None):
        self.scanTechnique = ScanTechnique.get(scanTechnique)
        self.numberDetectorsAlongTrack = numberDetectorsAlongTrack
        self.numberDetectorsCrossTrack = numberDetectorsCrossTrack
        self.fNumber = fNumber
        self.focalLength = focalLength
        self.operatingWavelength = operatingWavelength
        self.bandwidth = bandwidth
        self.quantumEfficiency = quantumEfficiency
        self.opticalTransmissionFactor = opticalTransmissionFactor
        self.numberReadOutElectrons = numberReadOutElectrons
        self.targetBlackBodyTemp = targetBlackBodyTemp
        self.bitsPerPixel = bitsPerPixel
        self.detectorWidth = detectorWidth
        super(OpticalScanner,self).__init__(name=name, acronym=acronym,
                agency=agency, mass=mass, volume=volume, power=power,
                orientation=orientation, fieldOfView=fieldOfView,
                dataRate=dataRate, techReadinessLevel=techReadinessLevel,
                mountType=mountType, _id=_id, _type="OpticalScanner")

class SyntheticApertureRadar(Instrument):
    def __init__(self, name=None, acronym=None, agency=None, mass=None,
            volume=None, power=None, orientation=Orientation(),
            dataRate=None, pulseWidth=None, antennaDimensionAlongTrack=None,
            antennaDimensionCrossTrack=None, antennaApertureEfficiency=None,
            operatingFrequency=None, peakTransmitPower=None, chirpBandwidth=None,
            minPulseRepetitionFrequency=None, maxPulseRepetitionFrequency=None,
            sceneNoiseTemp=None, systemNoiseFigure=None, radarLosses=None,
            thresholdSigmaNEZ0=None, techReadinessLevel=9, mountType="BODY", _id=None):
        self.pulseWidth = pulseWidth
        self.antennaDimensionAlongTrack = antennaDimensionAlongTrack
        self.antennaDimensionCrossTrack = antennaDimensionCrossTrack
        self.antennaApertureEfficiency = antennaApertureEfficiency
        self.operatingFrequency = operatingFrequency
        self.peakTransmitPower = peakTransmitPower
        self.chirpBandwidth = chirpBandwidth
        self.minPulseRepetitionFrequency = minPulseRepetitionFrequency
        self.maxPulseRepetitionFrequency = maxPulseRepetitionFrequency
        self.sceneNoiseTemp = sceneNoiseTemp
        self.systemNoiseFigure = systemNoiseFigure
        self.radarLosses = radarLosses
        self.thresholdSigmaNEZ0 = thresholdSigmaNEZ0
        super(SyntheticApertureRadar,self).__init__(name=name, acronym=acronym,
                agency=agency, mass=mass, volume=volume, power=power,
                orientation=orientation, fieldOfView=None,
                dataRate=dataRate, techReadinessLevel=techReadinessLevel,
                mountType=mountType, _id=_id, _type="SyntheticApertureRadar")
