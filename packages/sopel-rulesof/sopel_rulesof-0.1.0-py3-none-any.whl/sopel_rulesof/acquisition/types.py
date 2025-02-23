"""Rules of Acquisition types

Part of sopel-rulesof

Copyright 2025 dgw, technobabbl.es

Licensed under the Eiffel Forum License v2.
"""
from __future__ import annotations

from ..types import Rule, RuleCollection


class RuleOfAcquisition(Rule):
    """A Ferengi Rule of Acquisition."""


class RulesOfAcquisition(RuleCollection):
    _missing_message = "The Nagus hasn't sold me this one yet."
