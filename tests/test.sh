#!/bin/bash

# core-helpers https://github.com/gh0st42/core-helpers needed

cea servald config del interfaces.0.match
cea dd if=/dev/urandom of=5m bs=5M count=1
cea "supervisord -c /root/shared/sv.conf"
cea rhizome put 5m
