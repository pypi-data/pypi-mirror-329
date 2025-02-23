"""sopel-rulesof utility module

Copyright 2025 dgw, technobabbl.es

Licensed under the Eiffel Forum License v2.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sopel.tools import get_logger

if TYPE_CHECKING:
    from typing import Generator
    from .types import Rule


LOGGER = get_logger('rulesof.util')


def load_tsv(
    file: str,
    cls: type[Rule],
) -> Generator[Rule, None, None]:
    """Load a TSV ``file`` and yield each row as a ``cls`` object.

    :param file: The path to the TSV file to load.
    :param cls: The class to instantiate for each row. Must be a subclass of the
                :class:`~.types.AbstractRule` type.

    The idea here is to provide a generic way to load TSV files of rule data and
    let the caller specify what kind of object to create for each row. The class
    passed in is responsible for interpreting the TSV fields.
    """
    with open(file, 'r') as tsvfile:
        for line in tsvfile:
            if line.startswith('#'):
                # comment line
                continue
            try:
                yield cls.from_tsv(line)
            except Exception as e:
                LOGGER.error('Error parsing TSV entry %r: %s', line, e)
                continue
