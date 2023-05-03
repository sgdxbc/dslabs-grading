#!/bin/bash -x -e
git clone https://github.com/emichael/dslabs
pushd dslabs
git checkout handout
tar -cf handout-overlay.tar.gz run-tests.py README.md Makefile lombok.config labs/*/tst jars
popd
