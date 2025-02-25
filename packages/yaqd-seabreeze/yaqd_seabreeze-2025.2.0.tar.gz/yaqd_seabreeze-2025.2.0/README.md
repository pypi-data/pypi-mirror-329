# yaqd-seabreeze

[![PyPI version](https://badge.fury.io/py/yaqd-seabreeze.svg)](https://badge.fury.io/py/yaqd-seabreeze)
[![Conda](https://img.shields.io/conda/vn/conda-forge/yaqd-seabreeze)](https://anaconda.org/conda-forge/yaqd-seabreeze)
[![yaq](https://img.shields.io/badge/framework-yaq-orange)](https://yaq.fyi/)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![ver](https://img.shields.io/badge/calver-YYYY.M.MICRO-blue)](https://calver.org/)
[![log](https://img.shields.io/badge/change-log-informational)](https://github.com/yaq-project/yaqd-seabreeze/blob/main/CHANGELOG.md)

yaq daemons for Ocean Optics SeaBreeze spectrometers.
A simple wrapper of the excellent [python-seabreeze package](https://github.com/ap--/python-seabreeze).

This package contains the following daemon(s):
- [seabreeze](https://yaq.fyi/daemons/seabreeze/)
- [seabreeze-script](https://yaq.fyi/daemons/seabreeze-script)


## installation notes
The seabreeze dependency is not always plug-and-play; after installing (through pip or conda), be sure to run the command `seabreeze_os_setup` to run os-dependent setup steps. For more details, see [python-seabreeze documentation](https://github.com/ap--/python-seabreeze/blob/master/os_support/readme.md).
