#!/bin/bash
for mf in */Makefile
do
    make -C $(dirname $mf) all
done