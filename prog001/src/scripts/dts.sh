#!/bin/bash

export PATH=$PATH:/root/.local/bin
dts --set-version daffy
dts version

cp /src/dts/code/devel/run/command.py ~/.dt-shell/commands-multi/daffy/devel/run/command.py
