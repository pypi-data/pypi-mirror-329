"""Rules of Acquisition plugin

Part of sopel-rulesof

Copyright 2025 dgw, technobabbl.es

Licensed under the Eiffel Forum License v2.
"""
from __future__ import annotations

import os.path
import random
from typing import TYPE_CHECKING

from sopel import plugin, tools

from ..util import load_tsv
from .types import RuleOfAcquisition, RulesOfAcquisition


if TYPE_CHECKING:
    from sopel.bot import SopelWrapper


COLLECTION = 'the_rules_of_acquisition'
LOGGER = tools.get_logger('rules_of_acquisition')
OUTPUT_PREFIX = '[ROA] '


def setup(bot):
    bot.memory[COLLECTION] = RulesOfAcquisition()
    base_path = os.path.dirname(__file__)
    rules_path = os.path.join(base_path, 'data', 'rules.tsv')
    for rule in load_tsv(rules_path, RuleOfAcquisition):
        bot.memory[COLLECTION].add(rule)


def shutdown(bot):
    try:
        del bot.memory[COLLECTION]
    except KeyError:
        pass


def say_rule(bot: SopelWrapper, rule: RuleOfAcquisition):
    message = f"Rule of Acquisition #{rule.number}: {rule.text}"
    if rule.source:
        message += f" | Defined in {rule.source}"

    bot.say(message, truncation=' […]')


@plugin.commands('roa')
@plugin.example('.roa in the wind', user_help=True)
@plugin.example('.roa 153', user_help=True)
@plugin.example('.roa', user_help=True)
@plugin.output_prefix(OUTPUT_PREFIX)
def rule_of_acquisition(bot, trigger):
    """Look up a Rule of Acquisition."""
    rules = bot.memory[COLLECTION]

    if (query := trigger.group(2)) is None:
        rule = rules.random()
        say_rule(bot, rule)
        return
    elif query.isdigit():
        # numeric lookup
        say_rule(bot, rules[query])
        return
    else:
        # text search
        query = query.strip().lower()
        if results := tuple(rules.search(query)):
            say_rule(bot, random.choice(results))
        else:
            bot.reply(
                "The Nagus hasn't considered a rule about that yet. "
                "If you suggest one, you might be entitled to a finder's fee."
            )
        return
