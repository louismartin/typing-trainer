#!/bin/bash
export DISPLAY=:0
pkill -f prompt_input.py
xterm -e "/home/louis/miniconda3/bin/python3 /home/louis/dev/typing-trainer/prompt_input.py"
