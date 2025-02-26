[![CI](https://github.com/DiamondLightSource/p99-bluesky/actions/workflows/ci.yml/badge.svg)](https://github.com/DiamondLightSource/p99-bluesky/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/DiamondLightSource/p99-bluesky/branch/main/graph/badge.svg)](https://codecov.io/gh/DiamondLightSource/p99-bluesky)
[![PyPI](https://img.shields.io/pypi/v/p99-bluesky.svg)](https://pypi.org/project/p99-bluesky)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# p99-bluesky

This module provides a complete offline environment for beamline p99. It includes everything you need to get started, such as Bluesky plans for defining experiments, Ophyd-asynio for controlling hardware devices, and Blueapi for interacting with Bluesky programmatically. Additionally, it comes bundled with all the necessary modules to run p99 within an IPython terminal.


Source          | <https://github.com/DiamondLightSource/p99-bluesky>
:---:           | :---:
PyPI            | `pip install p99_bluesky`
Documentation   | <https://DiamondLightSource.github.io/p99-bluesky>
Releases        | <https://github.com/DiamondLightSource/p99-bluesky/releases>

This repository can also serve as a configuration source for a p99 instance of BlueAPI. It offers both planFunctions and deviceFunctions, streamlining the setup process.

``` yaml
    env:
      sources:
        - kind: planFunctions
          module: p99_bluesky.plans
        - kind: deviceFunctions
          module: p99_bluesky.beamlines.p99 
```

<!-- README only content. Anything below this line won't be included in index.md -->

See https://DiamondLightSource.github.io/p99_bluesky for more detailed documentation.
