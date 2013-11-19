# vimradish
a vim plugin for running radish

**Author:** Claudio Klingler <ck@realtime-projects.com><br />
**License:** GPL<br />

## About

vimradish is a vim plugin that allows you to run radish directly
within the vim python interpreter.

Features:

+ run radish within your vim python interpreter
+ signal highlighting of passed/failed tests

## Requirements

1. radish installed
2. vim compiled with python support (2.7)
3. python installed with setuptools

## Installation

1. Ensure radish is installed in your python environment

    See [radish: Installation Manual](https://github.com/timofurrer/radish/wiki/Installation)

2. Get vimradish

    ```bash
    git clone http://www.github.com/realtimeprojects/vimradish ~/vimradish
    ```

3. Install vimradish:

    ```bash
    cd ~/vimradish
    python setup.py install
    ```

4. Place the following statement somewhere in your ~/.vimrc

    ```vim
    py import vimradish
    ```

## Usage

1. Open a feature file from the test directory (radish base directory)

    ```bash
    vim features/001.feature
    ```

2. Run radish

    ```vim
    :Rr
    ```

3. Enjoy :-)
