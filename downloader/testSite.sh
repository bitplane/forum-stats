#!/bin/bash

wget --timeout=5 --user-agent=ForumStats0.0a -qO- $1 | ./detect.py
