"""This module handle out.
"""
import copy


def convert_objectname(object_name: str):
    out = copy.copy(object_name)
    out = out.lower()
    out = out.replace(" ", "_")
    out = out.replace("+", "p")
    out = out.replace("-", "m")
    out = out.replace(".", "d")
    return out


def convert_satelitename(satelite_name: str):
    out = copy.copy(satelite_name)
    out = out.lower()
    out = out.replace(" ", "_")
    return out
