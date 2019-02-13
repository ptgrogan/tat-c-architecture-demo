#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for tradespace search analysis.
"""

import json
from enum import Enum

from .util import Entity
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

class SearchStrategy(str, Enum):
    """Enumeration of recognized search strategies."""
    FF = "FF"
    GA = "GA"
    KDO = "KDO"

    @staticmethod
    def get(key):
        """Attempts to parse a search strategy from a string, otherwise returns None."""
        if isinstance(key, SearchStrategy):
            return key
        elif isinstance(key, list):
            return list(map(lambda e: SearchStrategy.get(e), key))
        else:
            try: return SearchStrategy(key.upper())
            except: return None

class SearchParameters(Entity):
    """Aggregates search parameters needed to set up the genetic algorithm.

    Attributes:
        maxNFE          Maximum number of function evaluations
        populationSize  Size of the initial population of solutions.
        epsilons        List of epsilons for the dominance archive (one per objective).
        sizeTournament  Size of the tournament selection.
        pCrossover      Probability of crossover.
        pMutation       Probability of mutation.
        alpha           Learning rate prameter for credit updates in adaptive operator selection.
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

class AnalysisSettings(Entity):
    """Configuration options specific to TAT-C analysis tool.

    Attributes:
        propagationFidelity     Configures fidelity of the orbital propagator.
        includePropulsion       Toggles satellite propulsion on or off.
        searchStrategy          Specifies presferences for the search.
                                Recognized case-insensitive values include:
                                    FF (full factorial, default)
                                    GA (genetic algorithm)
                                    KDO (knowledge-driven optimization)
    """

    def __init__(self, propagationFidelity=None, includePropulsion=None,
            searchStrategy="FF", searchParameters=None, _id=None):
        """Initialize a tradespace search object.
        """
        self.propagationFidelity = propagationFidelity
        self.includePropulsion = includePropulsion
        self.searchStrategy = SearchStrategy.get(searchStrategy)
        self.searchParameters = searchParameters
        super(AnalysisSettings,self).__init__(_id, "AnalysisSettings")

    @staticmethod
    def from_dict(d):
        """Parses analysis settings from a normalized JSON dictionary."""
        return AnalysisSettings(
                propagationFidelity = d.get("propagationFidelity", None),
                includePropulsion = d.get("includePropulsion", None),
                searchStrategy = d.get("searchStrategy", "FF"),
                searchParameters = SearchParameters.from_json(d.get("searchParameters", None)),
                _id = d.get("@id", None)
            )
