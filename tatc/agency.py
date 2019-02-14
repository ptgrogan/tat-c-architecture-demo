#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for managing space system agencies.
"""

import json

from .util import Entity, EnumEntity

class AgencyType(EnumEntity):
    """Enumeration of recognized agency types."""
    ACADEMIC = "ACADEMIC"
    GOVERNMENT = "GOVERNMENT"
    COMMERCIAL = "COMMERCIAL"

class Agency(Entity):
    """An organizational entity responsible for operating a space mission or asset.

    Attributes:
        agencyType  Type of agency. Recognized values include: ACADEMIC,
                    COMMERCIAL, GOVERNMENT.
        name        Full name of this agencyself.
        acronym     Acronym, initialism, or abbreviation.
    """

    def __init__(self, agencyType=None, name=None, acronym=None, _id=None):
        """Initialize an agency object.

        Parameters:
            agencyType : AgencyType (default: None)
            name : str (default: None)
            acronym : str (default: name)
        """
        self.name = name
        self.acronym = acronym if acronym else name
        self.agencyType = AgencyType.get(agencyType)
        super(Agency, self).__init__(_id, "Agency")

    @staticmethod
    def from_dict(d):
        """Parses an agency from a normalized JSON dictionary."""
        return Agency(
                    agencyType = d.get("agencyType", None),
                    name = d.get("name", None),
                    acronym = d.get("acronym", None),
                    _id = d.get("@id", None)
                )
