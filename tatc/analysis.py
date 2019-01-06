#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for tradespace search analysis.
"""

import json

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

class AnalysisSettings(Entity):
    """Configuration options specific to TAT-C analysis tool.

    Attributes:
        propagationFidelity     Configures fidelity of the orbital propagator.
        includePropulsion       Toggles satellite propulsion on or off.
    """

    def __init__(self, propagationFidelity=None, includePropulsion=None, _id=None):
        """Initialize a tradespace search object.
        """
        self.propagationFidelity = propagationFidelity
        self.includePropulsion = includePropulsion
        super(AnalysisSettings,self).__init__(_id, "AnalysisSettings")

    @staticmethod
    def from_dict(d):
        """Parses analysis settings from a normalized JSON dictionary."""
        return AnalysisSettings(
                propagationFidelity = d.get("propagationFidelity", None),
                includePropulsion = d.get("includePropulsion", None),
                _id = d.get("@id", None)
            )
