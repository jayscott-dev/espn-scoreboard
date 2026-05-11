#!/bin/zsh

branch="$(git symbolic-ref --short HEAD)"

if [ "$branch" = "main" ]; then
    echo "Direct commits to main are blocked. Please use feature branches." >&2
    exit 1
fi
