#!/usr/bin/env bash

title='HomeLog Parallel Run'
echo -n -e "\033]0;$title\007"

# Run parallel
echo "running parallel..."
uwsgi --http :5500 -w main -p 16