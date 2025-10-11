# Personal Access Token Setup Guide

This guide will help you create a Personal Access Token (PAT) with the necessary permissions to fetch all organization members (both public and private).

## Why is this needed?

The default `GITHUB_TOKEN` provided by GitHub Actions has limited permissions and can only see **public members** of an organization. To fetch all members including those with private membership, we need a PAT with `read:org` permissions.

## Step-by-Step Instructions

### 1. Create a Personal Access Token

1. Go to GitHub Settings:
   - Click your profile picture (top-right corner)
   - Select **Settings**
   - Scroll down and click **Developer settings** (left sidebar)
   - Click **Personal access tokens** → **Tokens (classic)**

2. Generate new token:
   - Click **Generate new token** → **Generate new token (classic)**
   - Give it a descriptive name, e.g., `kendroo-org-members-read`
   - Set expiration (recommended: 90 days or No expiration for automated workflows)

3. Select permissions:
   - Check **`read:org`** (Read org and team membership, read org projects)
   - This is the minimum required permission

4. Click **Generate token** at the bottom

5. **IMPORTANT**: Copy the token immediately! You won't be able to see it again.

### 2. Add Token as Repository Secret

1. Go to your repository:
   - Navigate to https://github.com/kendroo-limited/.github

2. Open Settings:
   - Click the **Settings** tab
   - Click **Secrets and variables** → **Actions** (left sidebar)

3. Create new secret:
   - Click **New repository secret**
   - Name: `ORG_MEMBERS_PAT`
   - Value: Paste the token you copied
   - Click **Add secret**

### 3. Verify the Setup

After adding the secret, the workflow will automatically use it. You can:

1. Manually trigger the workflow:
   - Go to **Actions** tab
   - Click **Update Organization Members** workflow
   - Click **Run workflow** → **Run workflow**

2. Check the results:
   - Wait for the workflow to complete
   - Check the workflow logs to see how many members were found
   - Verify that `profile/README.md` was updated with all 4 members

## Security Notes

- The PAT should be stored as a repository secret (never commit it to code)
- Consider using a bot account or organization owner account for creating the PAT
- Set an expiration date and create calendar reminders to renew it
- If the token is compromised, immediately revoke it from GitHub settings

## Troubleshooting

### Still showing only 2 members?

1. Verify the secret name is exactly `ORG_MEMBERS_PAT`
2. Check that the token has `read:org` permission
3. Ensure the token was created by an organization member/owner
4. Check workflow logs for any API errors

### Token expired?

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click on the token name
3. Click **Regenerate token**
4. Update the `ORG_MEMBERS_PAT` secret with the new value

## Need Help?

If you encounter any issues, check the GitHub Actions workflow logs or contact the repository maintainer.
