# CHANGELOG


## v2.1.0 (2025-02-24)

### Chores

- Update pytest options
  ([`49f6abd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/49f6abd5d0b7b86ba5a78bc0eeefeb171348b446))

### Refactoring

- Update type hints
  ([`b454517`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/b45451706b617776bb9aefb767d142f2bc563007))


## v2.1.0-rc.1 (2024-11-26)

### Features

- Add difference method to Resources and ResourceGroup classes
  ([`60d9c3e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/60d9c3eebc57d62f0735e97af9c3839a854ef1a8))


## v2.0.1 (2024-07-04)

### Bug Fixes

- Invalid escape sequence warnings
  ([`e23c14b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/e23c14bbbe5ca404ccc4a0df9fe6662e4b310f57))


## v2.0.0 (2024-04-16)


## v2.0.0-rc.2 (2024-03-19)

### Features

- Convert to PEP420 namespace packages
  ([`bddd7c4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/bddd7c48d3f63fe6ccea60bdb9be75eb9694b1dc))

requires all other momotor.* packages to be PEP420 too

BREAKING CHANGE: convert to PEP420 namespace packages

### Refactoring

- Replace all deprecated uses from typing (PEP-0585)
  ([`5043246`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/50432464f68e9963576ec1d190657e7ee927e488))

### Breaking Changes

- Convert to PEP420 namespace packages


## v2.0.0-rc.1 (2024-02-06)

### Chores

- Add Python 3.10 and 3.11 classifiers
  ([`e6b117e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/e6b117e454fc346f1de78150d2a78fafb2f69e6e))

### Features

- Drop Python 3.8 support, test with Python 3.12
  ([`dedba4a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/dedba4a38cc392a87179179882b4ceaf9560e3e9))

BREAKING CHANGE: Requires Python 3.9+

### Refactoring

- Update type hints for Python 3.9
  ([`ab73d16`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/ab73d16c31083c42e6e8e4c04f371daaa6d70d77))

### Testing

- Update to latest Pytest
  ([`00893a9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/00893a926a3a4de885cfd00f9666c1fd83df244b))

### Breaking Changes

- Requires Python 3.9+


## v1.4.2 (2022-06-10)


## v1.4.1 (2022-04-04)

### Bug Fixes

- Correct type annotations for (async_)log_exception method
  ([`b59f5d2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/b59f5d21b48721be6954099a90ab6d44fca03462))

- Typo in dependencies
  ([`8c87f28`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/8c87f2844fed82f929d509bb43b2e30fea849ada))


## v1.4.0 (2022-01-24)

### Features

- Make caller_name argument to (Ex)LockSet optional
  ([`ffbc23e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/ffbc23e50334342d9e19b1ec4088ea8abfa92489))


## v1.3.0 (2021-12-06)

### Features

- Moved lockset module from broker
  ([`9d80d0c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/9d80d0c2450ff88c7adf4aee04fee0d7f771715e))


## v1.2.1 (2021-11-04)

### Bug Fixes

- Save exception info before submitting log message to executor
  ([`431ec1f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/431ec1f949dc83572767e8cddb1c9195a721fe3f))

### Chores

- Link to documentation with the correct version number
  ([`38c1b12`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/38c1b1237ac6ff2e2ca8795dc186900bfb9a5306))


## v1.2.0 (2021-10-01)


## v1.1.1 (2021-10-01)

### Bug Fixes

- Correctly wait on completion after log message has been sent to the Python logger; always wait on
  completion for critical messages and messages with exception info
  ([`364bb8d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/364bb8d1c10694d083da2cb2a66e8f06a354e769))

### Features

- Implement AsyncLogWrapper.handle
  ([`329c283`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/329c2830fe13f209580e329acc6841d4d7ff64ec))


## v1.1.0 (2021-10-01)

### Bug Fixes

- Remove dependency on Django
  ([`a2cdb8b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/a2cdb8b245dd32ec8c1c18aeb62fd3d825269311))

### Chores

- Update project files
  ([`88ef9df`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/88ef9dfe7247975a33d9f3c8839d98516cadfe8f))

- Update project files
  ([`267016b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/267016bb24551fad8b5fb3c2c066ee70e94c223b))

- Update project files
  ([`bdb976f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/bdb976f1959a397a9de6b02d8bb3a5ee4c40b249))

### Features

- Moved `log` module from momotor-django package, changed the way async logging is handled
  ([`7a58618`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/7a586183c1fc6d728a0ca006cfd288337ea581f5))


## v1.0.1 (2021-02-11)

### Bug Fixes

- __doc__ is not available when running Python with the -OO option
  ([`0e66a4f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/0e66a4f124776cf09fe1b4d24eab469100e85c77))

### Chores

- Added missing [docs] extra
  ([`631e714`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/631e7141617e7df62326d6b04266e01063f08b9d))

- Update Python SDK
  ([`0533760`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/0533760a47ce3c9fb3439d5f46d114761bf1f139))

- Update Python version classifiers
  ([`448f909`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/448f909feacf6e31d86fc1cb1e3fa0802fb2915c))

- Update/move PyCharm module files
  ([`44a96bb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/44a96bb10c0a156c1ee5962e82067202302ab5ad))


## v1.0.0 (2020-08-17)

### Features

- Changed minimum Python requirement to 3.7
  ([`26286b0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/26286b05ad4e2c3dc44e25e729dba98e1fed2fc1))

BREAKING CHANGE: Requires Python 3.7 or higher

### Breaking Changes

- Requires Python 3.7 or higher


## v0.7.0 (2020-04-23)

### Features

- Version bump to make `annotate_docstring` available as new feature
  ([`f82c77d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/f82c77d20f877bba8d29f9b05fc1ca7569d72888))


## v0.6.5 (2020-04-14)


## v0.6.4 (2020-04-14)

### Bug Fixes

- `as_str()` methods should apply quotes and escapes so that the string can be parsed again with
  `from_str()`
  ([`e9b1e42`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/e9b1e420b2f1413667e94141df4123ae4b7ef48b))

- Correct project links in documentation, set project links for PyPi
  ([`351650e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/351650e9bf51a1d4a0a6fae8201f1f7bb603d7a7))

### Testing

- Add failing test case for resource -> string -> resource conversion
  ([`c1f5735`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/c1f57355c414f1fe52f21b5c675cdd1635806247))


## v0.6.3 (2020-04-07)

### Bug Fixes

- Document resources and make code act like the documentation
  ([`a39c69a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/a39c69a4995b50b13aa77bec3f3086af2b49ead8))

* renamed match constants to a more meaningful name * combining items should take the strongest,
  whereas combining groups should take the weakest * added test cases for the document examples


## v0.6.2 (2020-04-06)

### Bug Fixes

- Require colons to be escaped in resource key parts (closes #3)
  ([`0b1b484`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/0b1b4844d7dfce26ea80d8e4e631f5fda76f55ba))


## v0.6.1 (2019-10-29)

### Bug Fixes

- Typo
  ([`2e3c6c1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/2e3c6c131d77bbc2bc9ab04d70c0cb6a94d0a4e2))


## v0.6.0 (2019-10-29)

### Bug Fixes

- Localstate not working correctly
  ([`3cfb7d6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/3cfb7d67313d1ed917759bee6e1cea91011e347e))

- Typo
  ([`dfe6de0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/dfe6de080a3521b531d23da2719b849ae171a33d))

### Features

- Add ExLock, a very tiny wrapper around aiorwlock.RWLock
  ([`848ba86`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/848ba86a98a292d3006e13aa1060cec04cc935cd))


## v0.5.0 (2019-10-28)

### Features

- Add 'exclusive' option to LocalState locks
  ([`be37258`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/be3725884cdfbb96e6207d9e8a0b7d97ae571fd3))

### Refactoring

- Reduce debug log spam
  ([`802be15`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/802be152436b7d29edf93dda9fc21102623b8a47))

- Use contextlib.asynccontextmanager on Python>=3.7
  ([`ac60220`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/ac60220bd8aa89efcef23d54f66a8b64fdb7f252))


## v0.4.0 (2019-09-27)

### Bug Fixes

- Keep groups in order when merging Resources and ResourceGroups
  ([`1a51cf8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/1a51cf8f3d7f3ae1d794f1a20d6392cfd1425128))

### Features

- Also accept newlines as resource group separator
  ([`bf249e3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/bf249e3bdda016593125f284b0f93f86c79a764a))

- String input/output changes
  ([`5596e95`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/5596e958a5e307662ea154f8ad1faee8c77a360c))

* accept empty strings as input for Resoures.from_string() * added as_str() method to Resources


## v0.3.1 (2019-09-24)

### Bug Fixes

- Add __str__ to Resources for easy debug printing and logging
  ([`a378749`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/a37874950f0dbf52e04b72992ececd9ea8c19e1b))

### Refactoring

- Simplified splitters by adding field separator at end of string
  ([`1634ee7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/1634ee7d5711d1c418e491bfd0802f12ed2e8f2d))


## v0.3.0 (2019-09-05)

### Features

- Add base and local implementation for shared state (moved from cli package)
  ([`5b4a781`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/5b4a7818601e21c27c7238895b1ef5a36f9918b0))


## v0.2.0 (2019-09-03)


## v0.1.0 (2019-09-03)

### Features

- Better string processing
  ([`1282a69`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/1282a697589d272bf7baf025d4fd76de1f0e1b7e))

- Small changes to interface
  ([`52a008f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/52a008ff09f122f1bbcc8c25bef381a1159a7cd2))


## v0.0.0 (2019-09-02)

### Features

- Extracted Resources handling code from broker into separate package
  ([`5e6ee39`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/-/commit/5e6ee39f9fe811c3f9f04f5ec75c55296bbbc34d))
