#!/bin/bash

# Commit and push to GitHub - don't use as this push on main :)
git add .
git commit -m "$1"  # The first argument is the commit message
git push origin main