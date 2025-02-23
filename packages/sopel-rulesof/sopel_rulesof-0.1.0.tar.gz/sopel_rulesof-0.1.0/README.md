# sopel-rulesof

"Rules of X" plugins for Sopel IRC bots.

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-rulesof
```

[**Depending on your Sopel bot's configuration**][sopel-endis-plugins], you
might need to enable or disable the specific `rules_of_x` plugins ([see
below](#available-rule-collections)) that you want your bot to use. You
can do so with [the `sopel-plugins` command][cli-sopel-plugins], e.g.:

```shell
$ sopel-plugins enable rules_of_acquisition
```

[cli-sopel-plugins]: https://sopel.chat/docs/run/cli.html#sopel-plugins
[sopel-endis-plugins]: https://sopel.chat/docs/run/plugin#enabling-or-disabling-plugins

### Available rule collections

* `rules_of_acquisition`: The Ferengi Rules of Acquisition
* `rules_of_the_internet`: The Rules of the Internet (Rule 34 & friends)

### Installation requirements

The `sopel-rulesof` package is written with Python 3 and Sopel 8.0+ in mind.
Installation on Python 2, or usage with Sopel 7.x, is not supported.

## Using

### `rules_of_acquisition`

Commands:

* `.roa`
  * Call without arguments to grab a random Rule of Acquisition
  * Call with a single number to print that specific Rule (e.g. `.roa 153`)
  * Call with a word or phrase to pick a random rule containing it (e.g. `.roa
    justification`)

### `rules_of_the_internet`

Commands:

* `.roti`
  * Call without arguments to grab a random Rule of the Internet
  * Call with a single number to print that specific Rule (e.g. `.roti 34`)
  * Call with a word or phrase to pick a random rule containing it (e.g. `.roti
    talk about`)
