#!/bin/sh
./kernelci-concourse/tasks/monitor.py
ls -lR monitor-out
cat monitor-out/config-list.txt
