#!/bin/bash

# Script to delete all branches except main, both locally and remotely
# Run this script from the root of your repository

set -e  # Exit on error

echo "Deleting all branches except main..."
echo ""

# Ensure we're on the main branch
echo "Switching to main branch..."
git checkout main || { echo "Error: Failed to checkout main branch. Please ensure you have no uncommitted changes."; exit 1; }
git pull origin main || { echo "Error: Failed to pull latest changes from main. Please check your network connection."; exit 1; }

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
    failed_deletions=()
    echo "$remote_branches" | while read branch; do
        echo "  Deleting remote branch: $branch"
        if ! git push origin --delete "$branch" 2>/dev/null; then
            echo "    Warning: Failed to delete remote branch: $branch"
            failed_deletions+=("$branch")
        fi
    done
    
    if [ ${#failed_deletions[@]} -gt 0 ]; then
        echo ""
        echo "Warning: The following remote branches could not be deleted:"
        printf '  - %s\n' "${failed_deletions[@]}"
    fi
fi

echo ""
echo "Cleanup complete!"
echo ""
echo "Remaining local branches:"
git branch
echo ""
echo "Remaining remote branches:"
git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||'
