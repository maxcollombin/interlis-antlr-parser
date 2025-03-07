#!/bin/sh

python3 -m venv antlr4-tools
. antlr4-tools/bin/activate
pip install antlr4-tools

export ANTLR4_TOOLS_ANTLR_VERSION=4.13.2