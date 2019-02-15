#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for tradespace search analysis.
"""

import json

from .util import Entity, EnumEntity
from .mission import MissionConcept, DesignSpace

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
            nOperRepl = d.get("nOperRepl", None),
            _id = d.get("@id", None)
        )

class AnalysisOutputs(Entity):
    """Configuration options to filter analysis outputs based on ranges of parameters.

    Attributes:
        obsTimeStep         Desired time step to record spacecraft state
                            observations. True uses minimum simulation time
                            step. False toggles outputs off.
                            (default: True)
    """
    def __init__(self, obsTimeStep=True, _id=None):
        self.obsTimeStep = obsTimeStep
        super(AnalysisOutputs,self).__init__(_id, "AnalysisOutputs")

    @staticmethod
    def from_dict(d):
        """Parses analysis outputs from a normalized JSON dictionary."""
        return AnalysisOutputs(
            obsTimeStep = d.get("obsTimeStep", True),
            _id = d.get("@id", None)
        )

class AnalysisSettings(Entity):
    """Configuration options specific to TAT-C analysis tool.

    Attributes:
        includePropulsion       Toggles satellite propulsion. True mitigates
                                effects of drag. False triggers drag effects.
                                (default: True)
        outputs                 Set of intermediate or internal outputs to
                                toggle on or off or specify bounds.
        searchStrategy          Specifies preferences for the search.
                                Recognized case-insensitive values include:
                                    FF (full factorial)
                                    GA (genetic algorithm)
                                    KDO (knowledge-driven optimization)
                                (default: FF)
        searchParameters        Parameters for the intelligent search strategy.
    """

    def __init__(self, includePropulsion=True, outputs=AnalysisOutputs(), searchStrategy="FF",
            searchParameters=None, _id=None):
        """Initialize a tradespace search object.
        """
        self.includePropulsion = includePropulsion
        self.outputs = outputs
        self.searchStrategy = SearchStrategy.get(searchStrategy)
        self.searchParameters = searchParameters
        super(AnalysisSettings,self).__init__(_id, "AnalysisSettings")

    @staticmethod
    def from_dict(d):
        """Parses analysis settings from a normalized JSON dictionary."""
        return AnalysisSettings(
                includePropulsion = d.get("includePropulsion", True),
                outputs = AnalysisOutputs.from_json(d.get("outputs", AnalysisOutputs())),
                searchStrategy = d.get("searchStrategy", "FF"),
                searchParameters = SearchParameters.from_json(d.get("searchParameters", None)),
                _id = d.get("@id", None)
            )

class TradespaceSearch(Entity):
    """Set of constraints and parameters to bound and define a tradespace search.

    Attributes:
        mission        Context and objectives for mission.
        designSpace    Constraints and requirements for available architectures.
        settings       Settings specific to TAT-C analysis.
    """

    def __init__(self, mission=MissionConcept(), designSpace=DesignSpace(), settings=AnalysisSettings(), _id=None):
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
                mission = MissionConcept.from_json(d.get("mission", MissionConcept())),
                designSpace = DesignSpace.from_json(d.get("designSpace", DesignSpace())),
                settings = AnalysisSettings.from_json(d.get("settings", AnalysisSettings())),
                _id = d.get("@id", None)
            )
