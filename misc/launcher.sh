#!/bin/bash

# Source - https://stackoverflow.com/a/68922466
# Posted by Sandy
# Retrieved 2026-01-11, License - CC BY-SA 4.0

uv run python data_gen.py &
uv run python plotting_animation.py &
wait
