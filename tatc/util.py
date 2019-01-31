#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object models and methods for base classes and other utilities.
"""

import json
import numpy as np
import math
from enum import Enum
from numbers import Number

class Entity(object):
    """An entity is an abstract class to aggregate common functionality.

    Attributes:
        _id         Unique identifier for this entity.
        _type       Class type description for this entity.
    """

    def __init__(self, _id=None, _type="Entity"):
        """Initialize an entity.

        Parameters:
            _id : str (default: None)
            _type : str (default: "Entity")
        """
        self._id = _id
        self._type = _type

    def to_dict(self):
        """Convert this entity to a JSON-formatted dictionary."""
        # extract and copy the python dictionary
        json_dict = dict(self.__dict__)

        def recursive_normalize(d):
            """Helper function to recursively remove null values and serialize
            unserializable objects from dictionary."""
            # if not a dictionary, return immediately
            if not isinstance(d, dict):
                if isinstance(d, Entity): return d.to_dict()
                else: return d
            # otherwise loop through each key/value pair
            for key, value in list(d.items()):
                # if value is None remove key
                if value is None:
                    del d[key]
                # else if non-seralizable object, manually serialize to json
                elif isinstance(value, Entity):
                    d[key] = value.to_dict()
                # else if list, recursively serialize each list element
                elif isinstance(value, list):
                    d[key] = list(map(recursive_normalize, value))
                # otherwise recursively call function
                else: recursive_normalize(value)
            return d
        recursive_normalize(json_dict)
        # translate special python to json keys: _id to @id, _type to @type
        if json_dict.get("_id"): json_dict["@id"] = json_dict.pop("_id")
        if json_dict.get("_type"): json_dict["@type"] = json_dict.pop("_type")
        return json_dict

    def to_json(self, file=None, *args, **kwargs):
        """Serializes this entity to a JSON-formatted string or file."""
        if file is None:
            # return json string
            return json.dumps(self.to_dict(), *args, **kwargs)
        else:
            # write json file
            return json.dump(self.to_dict(), file, *args, **kwargs)

    @classmethod
    def from_json(cls, json_doc):
        """Parses an entity from a JSON-formatted string, dictionary, or file."""
        # convert json string or file to dictionary (if necessary)
        if isinstance(json_doc, str):
            json_doc = json.loads(json_doc)
        elif hasattr(json_doc, 'read'):
            json_doc = json.load(json_doc)
        # if pre-formatted, return directly
        if (json_doc is None or isinstance(json_doc, Number) or isinstance(json_doc, Entity)):
            return json_doc
        # if list, recursively parse each element and return mapped list
        if isinstance(json_doc, list):
            return list(map(lambda e: cls.from_json(e), json_doc))
        # otherwise use class method to initialize from normalized dictionary
        return cls.from_dict(json_doc)

    @staticmethod
    def from_dict(d):
        """Parses an entity from a normalized JSON dictionary."""
        return Entity(_id = d.get("@id", None))

    def __eq__(self, other):
        """Overrides the default check if this entity is equal to another by
        comparing unique identifiers if available.
        """
        # if specified, perform comparison on unique identifier
        if self._id is not None:
            return self._id == other._id
        # otherwise return the default comparison using `is` operator
        else:
            return self is other

    def __ne__(self, other):
        """Overrides the default check if this entity is not equal to another
        by comparing unique identifiers if available. (n.b. required for Python 2)
        """
        return not self.__eq__(other)

    def __hash__(self):
        """Overrides the default hash function by using the unique identifiers
        if available."""
        # if specified, return the hash of the unique identifier
        if self._id is not None:
            return hash(self._id)
        # otherwise return default hash from superclass
        return super(Entity, self).__hash__()

class CommunicationBand(str, Enum):
    """Enumeration of recognized communication bands."""
    VHF = "VHF"
    UHF = "UHF"
    L = "L"
    S = "S"
    C = "C"
    X = "X"
    KU = "KU"
    KA = "KA"
    LASER = "LASER"

    @staticmethod
    def get(key):
        """Attempts to parse a communication band from a string, otherwise returns None."""
        if isinstance(key, CommunicationBand):
            return key
        elif isinstance(key, list):
            return list(map(lambda e: CommunicationBand.get(e), key))
        else:
            try: return CommunicationBand(key.upper())
            except: return None

class QuantitativeValue(Entity):
    """A quantitative value bounded by minimum and maximum values.

    Attributes:
        minValue        Minimum value.
        maxValue        Maximum value.
    """
    def __init__(self, minValue, maxValue, _id=None):
        self.minValue = minValue
        self.maxValue = maxValue
        super(QuantitativeValue,self).__init__(_id, "QuantitativeValue")

    def __iter__(self):
        """Iterates values."""
        return iter([self.minValue, self.maxValue])

    @staticmethod
    def from_dict(d):
        """Parses a quantitative value from a normalized JSON dictionary."""
        return QuantitativeValue(
                minValue = d.get("minValue", None),
                maxValue = d.get("maxValue", None),
                _id = d.get("@id", None)
            )

class QuantitativeRange(Entity):
    """A range of quantitative values bounded by minimum and maximum values.

    Attributes:
        minValue        Minimum value of the enumerated range.
        maxValue        Maximum value of the enumerated range.
        numberSteps     Number of enumerated steps inclusive of minimum and
                        maximum values.
        stepSize        Enumeration step size. Ranges from the minimum value to
                        the largest step less than / equal to the maximum value.
    """
    def __init__(self, minValue, maxValue, numberSteps=None, stepSize=None, _id=None):
        self.minValue = minValue
        self.maxValue = maxValue
        self.numberSteps = numberSteps
        self.stepSize = stepSize
        super(QuantitativeRange,self).__init__(_id, "QuantitativeRange")

    def __iter__(self):
        """Iterates values in this range."""
        # if numberSteps specified, return linear space directly
        if self.numberSteps:
            # stepSize = (self.maxValue - self.minValue) / (self.numberSteps - 1)
            return iter(np.linspace(self.minValue, self.maxValue, self.numberSteps))
        # else if stepSize specified, compute appropriate number steps
        elif self.stepSize:
            numberSteps = 1 + math.floor((self.maxValue - self.minValue) / self.stepSize)
            maxValue = self.minValue + (numberSteps - 1)*self.stepSize
            return iter(np.linspace(self.minValue, maxValue, numberSteps))
        # otherwise return the end points
        else:
            return iter([self.minValue, self.maxValue])

    @staticmethod
    def from_dict(d):
        """Parses a quantitative range from a normalized JSON dictionary."""
        return QuantitativeRange(
                minValue = d.get("minValue", None),
                maxValue = d.get("maxValue", None),
                stepSize = d.get("stepSize", None),
                numberSteps = d.get("numberSteps", None),
                _id = d.get("@id", None)
            )
