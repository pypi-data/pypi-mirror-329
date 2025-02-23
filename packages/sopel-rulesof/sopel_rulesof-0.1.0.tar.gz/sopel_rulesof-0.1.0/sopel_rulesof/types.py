"""Common rulesof types

Part of sopel-rulesof

Copyright 2025 dgw, technobabbl.es

Licensed under the Eiffel Forum License v2.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Generator, Iterable


class Rule:
    """Interface definition of a Rule object.

    Defines properties that are expected to be common across all supported
    "Rules of X" lists.
    """
    def __init__(
        self,
        number: int,
        text: str,
        source: str | None = None,
    ):
        self._number = number
        self._text = text
        self._source = source

    @classmethod
    def from_tsv(cls, line: str) -> Rule:
        """Create and return a new Rule object using a line of TSV ``data``."""
        if not (line := line.strip()):
            raise ValueError('Empty TSV line cannot be used to create a Rule')
        elif line.startswith('#'):
            raise ValueError('Comment line cannot be used to create a Rule')

        return cls(*line.strip().split('\t'))

    @property
    def number(self) -> int:
        """Rule number, according to the rule list."""
        return self._number

    @property
    def text(self) -> str:
        """The text of the rule."""
        return self._text

    @property
    def source(self) -> str | None:
        """The source of the rule, if known, or ``None``."""
        return self._source


class RuleCollection:
    """A collection of Rule objects.

    This class is a simple container for Rule objects, with some convenience
    methods for working with them.
    """
    _missing_message = "This rule does not exist."

    def __init__(self, rules: Iterable[Rule] | None = None):
        self._rules = {}
        if rules:
            self._rules = {rule.number: rule for rule in rules}

    def add(self, rule: Rule):
        """Add a Rule object to the collection."""
        self._rules[rule.number] = rule

    def remove(self, rule: Rule):
        """Remove a Rule object from the collection."""
        try:
            del self._rules[rule.number]
        except KeyError:
            # someone probably tried to delete the result of `missing`
            # just ignore it
            pass

    def missing(self, number: int) -> Rule:
        """Return a placeholder Rule object for a missing number.

        Not all rule lists are canonically complete. This method provides a
        fallback for gaps in the canon list.

        Subclasses can override the ``_missing_message`` attribute to provide a
        more specific message that blends with the rule list's theme.
        """
        return Rule(number, self._missing_message, None)

    def search(self, query: str) -> Generator[Rule]:
        """Search for a Rule object by text or source."""
        query = query.lower()
        for rule in self._rules.values():
            if (
                query in rule.text.lower() or
                (rule.source and query in rule.source.lower())
            ):
                yield rule

    def random(self) -> Rule:
        """Return a random Rule object from the collection."""
        return random.choice(list(self._rules.values()))

    def __len__(self) -> int:
        return len(self._rules)

    def __getitem__(self, number: int) -> Rule:
        try:
            return self._rules[number]
        except KeyError:
            return self.missing(number)

    def __iter__(self):
        return iter(self._rules)

    def __contains__(self, number: int) -> bool:
        return number in self._rules

    def __str__(self) -> str:
        return f'{len(self)} rules'

    def __repr__(self) -> str:
        return f'<RuleCollection: {self}>'
