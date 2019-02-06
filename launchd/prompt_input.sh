#!/bin/bash
pkill -f typing_trainer.py  # Kill previous prompt
/Users/louismartin/miniconda3/bin/python3 /Users/louismartin/dev/typing-trainer/typing_trainer.py
kill -9 $(ps -p $(ps -p $PPID -o ppid=) -o ppid=)  # Close the Terminal App: https://stackoverflow.com/questions/5560167/osx-how-to-auto-close-terminal-window-after-the-exit-command-executed
