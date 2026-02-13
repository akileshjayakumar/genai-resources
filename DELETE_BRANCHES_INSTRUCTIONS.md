# Instructions to Delete All Branches Except Main

This document provides instructions for deleting all Git branches (both local and remote) except the `main` branch.

## Current Branch Status

As of this update:
- **Local branches**: `main`, `copilot/delete-all-branches-except-main`
- **Remote branches**: `main`, `copilot/delete-all-branches-except-main`, `copilot/sub-pr-6`

## Automated Approach

A script has been prepared to automate the branch deletion process. However, due to environment constraints, this script must be run locally with proper Git credentials.

### Steps to Use the Script

1. Download or copy the script from this repository
2. Save it as `delete_branches.sh` in your local repository
3. Make it executable: `chmod +x delete_branches.sh`
4. Run the script: `./delete_branches.sh`

### Script Content

```bash
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
```

## Manual Approach

If you prefer to delete branches manually, follow these steps:

### 1. Delete Local Branches

```bash
# Switch to main branch first
git checkout main
git pull origin main

# List all local branches
git branch

# Delete each branch individually (except main)
git branch -D <branch-name>
```

For the current repository, run:
```bash
git branch -D copilot/delete-all-branches-except-main
```

### 2. Delete Remote Branches

```bash
# List all remote branches
git ls-remote --heads origin

# Delete each remote branch individually (except main)
git push origin --delete <branch-name>
```

For the current repository, run:
```bash
git push origin --delete copilot/delete-all-branches-except-main
git push origin --delete copilot/sub-pr-6
```

## Verification

After deletion, verify the cleanup:

```bash
# Check local branches
git branch

# Check remote branches
git ls-remote --heads origin
```

You should only see `main` in both lists.

## Important Notes

- ⚠️ **This action is irreversible** - deleted branches cannot be easily recovered
- Make sure you have merged any important changes before deleting branches
- You need push access to the repository to delete remote branches
- The `main` branch is protected and will not be deleted

## Troubleshooting

If you encounter authentication issues when deleting remote branches:
- Ensure you have the correct permissions for the repository
- Verify your Git credentials are properly configured
- You may need to use SSH instead of HTTPS, or vice versa

If a branch is protected on GitHub:
- You'll need to remove branch protection rules in the repository settings
- Navigate to: Settings → Branches → Branch protection rules
