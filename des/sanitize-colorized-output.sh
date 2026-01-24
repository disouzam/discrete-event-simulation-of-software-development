#!/bin/bash
# Strip ANSI escape characters used to colorize output
cat $1 | sed 's/[^[:print:]]//g' | sed 's/\[[0-9]\+;[0-9]\+;[0-9]\+;[0-9]\+;[0-9]\+m//g' | sed 's/\[[0-9]\+;[0-9]\+;[0-9]\+m//g' | sed 's/\[0m//g' | sed 's/\[1m//g' | sed 's/  / /g' > $2

# Remove original file
rm -rf $1

# Rename sanitized file
mv $2 $1