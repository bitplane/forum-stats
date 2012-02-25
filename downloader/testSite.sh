#!/bin/bash

wget --user-agent=ForumStats0.0a -qO- $1 | ./detect.py
