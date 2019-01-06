#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TAT-C resources loaded from file.
"""

import json
import os.path

from .ground import GroundNetwork

def load_from_json(entity, resource_file):
    """Loads an entity from JSON."""
    file_path = os.path.join(os.path.dirname(__file__), "resources", resource_file)
    with open(file_path) as infile:
        return entity.from_json(infile)

DSN = load_from_json(GroundNetwork, "DSN.json")
NENcom = load_from_json(GroundNetwork, "NENcom.json")
NENgov = load_from_json(GroundNetwork, "NENgov.json")

NENall = GroundNetwork(
    name="Near Earth Network (All)",
    acronym="NENall",
    groundStations=NENcom.groundStations + NENgov.groundStations
)
