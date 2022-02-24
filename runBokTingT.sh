#!/bin/sh

pkill -f telegramChat.py
python3 ./telegramChat.py T >> ./log/test/$(date '+%Y-%m-%d').log
