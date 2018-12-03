#!/bin/bash
pkill -f typing_trainer.py  # Kill previous prompt
/Users/louismartin/miniconda3/bin/python3 /Users/louismartin/dev/typing-trainer/typing_trainer.py
exit  # Close terminal (on mac you must tell it to exit in the preferences: https://superuser.com/questions/160473/avoiding-process-completed-prompt-after-terminal-script-ends-on-mac-os-x)
