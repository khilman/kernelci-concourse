#!/bin/sh

pwd
ls -alR

cd kernelci-core
./kci_build list_configs

