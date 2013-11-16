# vimradish - vim plugin for running raidh

**Author:** Claudio Klingler <ck@realtime-projects.com><br />
**License:** GPL<br />

## About

vimradish is a vim plugin that allows yo to run radish directly
within the vim python interpreter.

Features:
    - run radish within your vim python interpreter
    - signal highlighting of passed/failed tests

## Requirements

1. Radish insalled
2. vim compiled with python support (2.7)
3. python installed with setuptools

## Installation

0. Ensure radish is installed in your python environment

1. Get vimradish
    git clone http://www.github.com/realtimeprojects/vimradish ~/vimradish

2. Install vimradish:
        cd ~/vimradish
        python setup.py install

3. Place the following statement somewhere in your ~/.vimrc
    :py import vimradish

## Usage

1. Open a feature file from the test directory (radish base directory)
    vim features/001.feature
2. Run radish
    :Rr
3. Enjoy :-)
