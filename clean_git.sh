#!/usr/bin/env bash
set -e

# Remove .env.railway from all git history
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env.railway' --prune-empty --tag-name-filter cat -- --all

# Clean up reflogs and garbage collect
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now
