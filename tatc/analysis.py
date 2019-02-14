#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for tradespace search analysis.
"""

import json

from .util import Entity, EnumEntity
from .mission import MissionConcept, DesignSpace

class TradespaceSearch(Entity):
    """Set of constraints and parameters to bound and define a tradespace search.

    Attributes:
        mission        Context and objectives for mission.
        designSpace    Constraints and requirements for available architectures.
        settings       Settings specific to TAT-C analysis.
    """

    def __init__(self, mission=None, designSpace=None, settings=None, _id=None):
        """Initialize a tradespace search object.
        """
        self.mission = mission
        self.designSpace = designSpace
        self.settings = settings
        super(TradespaceSearch,self).__init__(_id, "TradespaceSearch")

    @staticmethod
    def from_dict(d):
        """Parses a tradespace search from a normalized JSON dictionary."""
        return TradespaceSearch(
                mission = MissionConcept.from_json(d.get("mission", None)),
                designSpace = DesignSpace.from_json(d.get("designSpace", None)),
                settings = AnalysisSettings.from_json(d.get("settings", None)),
                _id = d.get("@id", None)
            )

class SearchStrategy(EnumEntity):
    """Enumeration of recognized search strategies."""
    FF = "FF"
    GA = "GA"
    KDO = "KDO"

class SearchParameters(Entity):
    """Aggregates search parameters needed to set up the genetic algorithm.

    Attributes:
        maxNFE          Maximum number of function evaluations
        populationSize  Size of the initial population of solutions.
        epsilons        List of epsilons for the dominance archive (one per objective).
        sizeTournament  Size of the tournament selection.
        pCrossover      Probability of crossover.
        pMutation       Probability of mutation.
        alpha           Learning rate parameter for credit updates in adaptive operator selection.
        beta            Learning rate paraemter for probability updates in adaptive operator selection.
        pMin            Minimum probability of selection for adaptive operator selection.
        iOperators      List of domain-independent operators.
        dOperators      List of domain-dependent operators.
        nfeTriggerDM    Number of evaluations between successive rule mining algorithm applications.
        nOperRepl       Number of operators to replace after each rule mining.
    """
    def __init__(self, maxNFE=None, populationSize=None, epsilons=None,
            sizeTournament=None, pCrossover=None, pMutation=None, alpha=None,
            beta=None, pMin=None, iOperators=None, dOperators=None,
            nfeTriggerDM=None, nOperRepl=None, _id=None):
        self.maxNFE = maxNFE
        self.populationSize = populationSize
        self.epsilons = epsilons
        self.sizeTournament = sizeTournament
        self.pCrossover = pCrossover
        self.pMutation = pMutation
        self.alpha = alpha
        self.beta = beta
        self.pMin = pMin
        self.iOperators = iOperators
        self.dOperators = dOperators
        self.nfeTriggerDM = nfeTriggerDM
        self.nOperRepl = nOperRepl
        super(SearchParameters,self).__init__(_id, "SearchParameters")

    @staticmethod
    def from_dict(d):
        return SearchParameters(
            maxNFE = d.get("maxNFE", None),
            populationSize = d.get("populationSize", None),
            epsilons = d.get("epsilons", None),
            sizeTournament = d.get("sizeTournament", None),
            pCrossover = d.get("pCrossover", None),
            pMutation = d.get("pMutation", None),
            alpha = d.get("alpha", None),
            beta = d.get("beta", None),
            pMin = d.get("pMin", None),
            iOperators = d.get("iOperators", None),
            dOperators = d.get("dOperators", None),
            nfeTriggerDM = d.get("nfeTriggerDM", None),
            nOperRepl = d.get("nOperRepl", None)
        )

class AnalysisOutputs(Entity):
    """Configuration options to filter analysis outputs based on ranges of parameters.

    Attributes:
        timeAfterStart      Elapsed time (from start of simulation).
        timeToCoverage      Time required to cover point/target.
        accessTime          Time periods with access to point/ground station.
        downlinkLatency     Elapsed time from observation to downlink opportunity.
        revisitTime         Elapsed time between subsequent access blocks.
        repeatTime          ???
        crossOverlap        ??? (%)
        alongOverlap        ??? (%)
        numPasses           Total number of passes with visibility to a point.
        lunarPhase          ??? (deg)
        obsZenith           Observatory zenith angle (deg) relative to a point.
        obsAzimuth          Observatory azimuth angle (deg) relative to a point.
        sunZenith           Sun zenith angle (deg) relative to a point.
        sunAzimuth          Sun azimuth angle (deg) relative to a point.
        spatialResolution   Observatory spatial resolution (m).
        crossSwath          Observatory swath width (km) in the cross-track direction.
        alongSwath          Observatory swath width (km) in the along-track direction.
        obsLatitude         Observatory latitude (deg).
        obsLongitude        Observatory longitude (deg).
        obsAltitude         Observatory altitude (deg).
        objZenith           Object ??? zenith angle (deg) relative to a point.
        objAzimuth          Object ??? azimuth angle (deg) relative to a point.

    """
    def __init__(self, timeAfterStart=None, timeToCoverage=True, accessTime=True,
            downlinkLatency=None, revisitTime=None, repeatTime=None,
            crossOverlap=None, alongOverlap=None, numPasses=None, lunarPhase=None,
            obsZenith=None, obsAzimuth=None, sunZenith=None, sunAzimuth=None,
            spatialResolution=None, crossSwath=None, alongSwath=None,
            obsLatitude=None, obsLongitude=None, objZenith=None, objAzimuth=None,
            objRange=None, _id=None):
        self.timeAfterStart = timeAfterStart
        self.timeToCoverage = timeToCoverage
        self.accessTime = accessTime
        self.downlinkLatency = downlinkLatency
        self.revisitTime = revisitTime
        self.repeatTime = repeatTime
        self.crossOverlap = crossOverlap
        self.alongOverlap = alongOverlap
        self.numPasses = numPasses
        self.lunarPhase = lunarPhase
        self.obsZenith = obsZenith
        self.obsAzimuth = obsAzimuth
        self.sunZenith = sunZenith
        self.sunAzimuth = sunAzimuth
        self.spatialResolution = spatialResolution
        self.crossSwath = crossSwath
        self.alongSwath = alongSwath
        self.obsLatitude = obsLatitude
        self.obsLongitude = obsLongitude
        self.objZenith = objZenith
        self.objAzimuth = objAzimuth
        self.objRange = objRange
        super(AnalysisOutputs,self).__init__(_id, "AnalysisOutputs")

    @staticmethod
    def from_dict(d):
        """Parses analysis outputs from a normalized JSON dictionary."""
        return AnalysisOutputs(
            timeAfterStart = d.get("timeAfterStart", None),
            timeToCoverage = d.get("timeToCoverage", None),
            accessTime = d.get("accessTime", None),
            downlinkLatency = d.get("downlinkLatency", None),
            revisitTime = d.get("revisitTime", None),
            repeatTime = d.get("repeatTime", None),
            crossOverlap = d.get("crossOverlap", None),
            alongOverlap = d.get("alongOverlap", None),
            numPasses = d.get("numPasses", None),
            lunarPhase = d.get("lunarPhase", None),
            obsZenith = d.get("obsZenith", None),
            obsAzimuth = d.get("obsAzimuth", None),
            sunZenith = d.get("sunZenith", None),
            sunAzimuth = d.get("sunAzimuth", None),
            spatialResolution = d.get("spatialResolution", None),
            crossSwath = d.get("crossSwath", None),
            alongSwath = d.get("alongSwath", None),
            obsLatitude = d.get("obsLatitude", None),
            obsLongitude = d.get("obsLongitude", None),
            objZenith = d.get("objZenith", None),
            objAzimuth = d.get("objAzimuth", None),
            objRange = d.get("objRange", None)
        )

class AnalysisSettings(Entity):
    """Configuration options specific to TAT-C analysis tool.

    Attributes:
        propagationFidelity     Configures fidelity of the orbital propagator.
        includePropulsion       Toggles satellite propulsion on or off.
        outputs                 Set of intermediate or internal outputs to
                                toggle on or off or specify bounds.
        searchStrategy          Specifies preferences for the search.
                                Recognized case-insensitive values include:
                                    FF (full factorial, default)
                                    GA (genetic algorithm)
                                    KDO (knowledge-driven optimization)
        searchParameters        Parameters for the intelligent search strategy.
    """

    def __init__(self, propagationFidelity=None, includePropulsion=None,
            outputs=None, searchStrategy="FF", searchParameters=None, _id=None):
        """Initialize a tradespace search object.
        """
        self.propagationFidelity = propagationFidelity
        self.includePropulsion = includePropulsion
        self.outputs = outputs
        self.searchStrategy = SearchStrategy.get(searchStrategy)
        self.searchParameters = searchParameters
        super(AnalysisSettings,self).__init__(_id, "AnalysisSettings")

    @staticmethod
    def from_dict(d):
        """Parses analysis settings from a normalized JSON dictionary."""
        return AnalysisSettings(
                propagationFidelity = d.get("propagationFidelity", None),
                includePropulsion = d.get("includePropulsion", None),
                outputs = AnalysisOutputs.from_json(d.get("outputs", None)),
                searchStrategy = d.get("searchStrategy", "FF"),
                searchParameters = SearchParameters.from_json(d.get("searchParameters", None)),
                _id = d.get("@id", None)
            )
