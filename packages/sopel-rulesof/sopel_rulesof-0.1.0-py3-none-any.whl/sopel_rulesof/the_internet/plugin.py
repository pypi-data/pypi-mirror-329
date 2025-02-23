"""Rules of the Internet plugin

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
from .types import RuleOfTheInternet, RulesOfTheInternet


if TYPE_CHECKING:
    from sopel.bot import SopelWrapper


COLLECTION = 'the_rules_of_the_internet'
LOGGER = tools.get_logger('rules_of_the_internet')
OUTPUT_PREFIX = '[ROTI] '


def setup(bot):
    bot.memory[COLLECTION] = RulesOfTheInternet()
    base_path = os.path.dirname(__file__)
    rules_path = os.path.join(base_path, 'data', 'rules.tsv')
    for rule in load_tsv(rules_path, RuleOfTheInternet):
        bot.memory[COLLECTION].add(rule)


def shutdown(bot):
    try:
        del bot.memory[COLLECTION]
    except KeyError:
        pass


def say_rule(bot: SopelWrapper, rule: RuleOfTheInternet):
    message = f"Rule of the Internet #{rule.number}: {rule.text}"
    bot.say(message, truncation=' […]')


@plugin.commands('roti')
@plugin.example('.roti in the wind', user_help=True)
@plugin.example('.roti 153', user_help=True)
@plugin.example('.roti', user_help=True)
@plugin.output_prefix(OUTPUT_PREFIX)
def rule_of_the_internet(bot, trigger):
    """Look up a Rule of the Internet."""
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
            bot.reply("4chan didn't invent a rule about that yet.")
        return
