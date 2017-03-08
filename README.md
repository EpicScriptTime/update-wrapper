update-wrapper
==============

[![Travis](https://img.shields.io/travis/EpicScriptTime/update-wrapper.svg)](https://travis-ci.org/EpicScriptTime/update-wrapper)
[![Release](https://img.shields.io/pypi/v/update-wrapper.svg)](https://pypi.python.org/pypi/update-wrapper)
[![MIT License](https://img.shields.io/badge/license-MIT-8469ad.svg)](https://tldrlegal.com/license/mit-license)

Python script that simplify applying updates on multiple servers by wrapping the update process and logging the output.
Built with the help of various Ansible internals.

Requirements
------------

* Python3 and `pip`

Installation
------------

    pip install update-wrapper

Configuration
-------------

Create the configuration file `~/.update-wrapper.yml` and configure your hosts list.
See the sample file in the `examples` directory.

Usage
-----

    update-wrapper
