#!/usr/bin/env python3
"""
Automatically update organization members in the README.md file.
"""

import os
import re
import requests

def fetch_org_members(org_name, token):
    """Fetch public members from GitHub organization."""
    url = f"https://api.github.com/orgs/{org_name}/members"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    members = response.json()
    print(f"Found {len(members)} members")
    return members

def generate_member_html(members):
    """Generate HTML table for organization members."""
    if not members:
        return '<p align="center">No public members found.</p>'

    # Calculate how many rows we need (3 members per row)
    members_per_row = 3
    rows = []

    for i in range(0, len(members), members_per_row):
        row_members = members[i:i + members_per_row]
        cells = []

        for member in row_members:
            username = member['login']
            avatar_url = member['avatar_url']
            profile_url = member['html_url']

            cell = f'''<td align="center" width="{100//members_per_row}%">
<a href="{profile_url}">
<img src="{avatar_url}" width="100px;" alt="{username}"/><br />
<sub><b>@{username}</b></sub>
</a>
</td>'''
            cells.append(cell)

        # Fill remaining cells if row is not complete
        while len(cells) < members_per_row:
            cells.append(f'<td align="center" width="{100//members_per_row}%"></td>')

        row = f'''<tr>
{chr(10).join(cells)}
</tr>'''
        rows.append(row)

    table = f'''<table>
{chr(10).join(rows)}
</table>'''

    return table

def update_readme(readme_path, member_html):
    """Update the README.md file with new member information."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the markers for the dynamic section
    start_marker = '<!-- MEMBERS_START -->'
    end_marker = '<!-- MEMBERS_END -->'

    # Check if markers exist
    if start_marker in content and end_marker in content:
        # Replace content between markers
        pattern = f'{re.escape(start_marker)}.*?{re.escape(end_marker)}'
        replacement = f'{start_marker}\n{member_html}\n{end_marker}'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        print("Warning: Member markers not found in README.md")
        return False

    # Write updated content
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated {readme_path}")
    return True

def main():
    org_name = os.environ.get('ORG_NAME', 'kendroo-limited')
    token = os.environ.get('GITHUB_TOKEN')

    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return 1

    try:
        # Fetch organization members
        members = fetch_org_members(org_name, token)

        # Generate HTML for members
        member_html = generate_member_html(members)

        # Update README
        readme_path = 'profile/README.md'
        if os.path.exists(readme_path):
            update_readme(readme_path, member_html)
        else:
            print(f"Error: {readme_path} not found")
            return 1

        print("Member update completed successfully!")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
