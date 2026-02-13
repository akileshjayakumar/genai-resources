#!/bin/bash

# Script to delete all branches except main, both locally and remotely
# Run this script from the root of your repository

echo "Deleting all branches except main..."
echo ""

# Ensure we're on the main branch
echo "Switching to main branch..."
git checkout main
git pull origin main

echo ""
echo "Deleting local branches (except main)..."
# Get all local branches except main and delete them
git branch | grep -v "^[* ]*main$" | xargs -r git branch -D

echo ""
echo "Fetching remote branch list..."
# Get all remote branches except main
remote_branches=$(git ls-remote --heads origin | grep -v "refs/heads/main$" | awk '{print $2}' | sed 's|refs/heads/||')

if [ -z "$remote_branches" ]; then
    echo "No remote branches to delete (only main exists)."
else
    echo "Deleting remote branches..."
    echo "$remote_branches" | while read branch; do
        echo "  Deleting remote branch: $branch"
        git push origin --delete "$branch"
    done
fi

echo ""
echo "Cleanup complete!"
echo ""
echo "Remaining local branches:"
git branch
echo ""
echo "Remaining remote branches:"
git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||'
