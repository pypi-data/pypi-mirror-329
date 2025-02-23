"""Rules of the Internet types

Part of sopel-rulesof

Copyright 2025 dgw, technobabbl.es

Licensed under the Eiffel Forum License v2.
"""
from __future__ import annotations

from ..types import Rule, RuleCollection


class RuleOfTheInternet(Rule):
    """A Rule of the Internet."""


class RulesOfTheInternet(RuleCollection):
    _missing_message = "4chan didn't invent this one yet."
