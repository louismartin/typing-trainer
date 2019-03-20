#!/bin/bash
# Close the Terminal App: https://stackoverflow.com/questions/5560167/osx-how-to-auto-close-terminal-window-after-the-exit-command-executed
gtimeout 600 /Users/louismartin/miniconda3/bin/python3 /Users/louismartin/dev/typing-trainer/typing_trainer.py
kill -9 $PPID
