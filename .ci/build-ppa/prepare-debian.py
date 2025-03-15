#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from datetime import datetime

COPYRIGHT_HEADER = """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: krux-installer
Source: https://github.com/selfcustody/krux-installer
"""

def generate_copyright_content(header: str, license: str) -> str:
    return f"""{header}
Files: *
Copyright: {datetime.now().year} SelfCustody
License: {license}
"""

def generate_copyright(license_path, output_path):
    
    with open(license_path, 'r') as f:
        license_content = f.read()
    
    copyright_content = generate_copyright_content(COPYRIGHT_HEADER, license_content)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(copyright_content)

def parse_changelog(changelog_path, version):
    with open(changelog_path, 'r') as f:
        content = f.read()

    version_pattern = re.compile(
        r"## (?P<version>\d+(?:\.\d+)*[a-zA-Z-]*[\d-]*)"
        r"(?: - (?P<date>\d{4}-\d{2}-\d{2}))?\n\n"
        r"(?P<body>.*?)(?=\n## |\Z)",
        re.DOTALL
    )
    
    for match in version_pattern.finditer(content):
        if match.group('version') == version:
            date_str = match.group('date') or datetime.now().strftime("%Y-%m-%d")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            body = match.group('body').strip()
            return date, body
    
    raise ValueError(f"Version {version} not found in changelog")

def generate_changelog(changelog_path, version, output_path, maintainer_name, maintainer_email):
    try:
        date, body = parse_changelog(changelog_path, version)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    
    changelog_content = f"""krux-installer ({version}-1) focal; urgency=medium

{body}

 -- {maintainer_name} <{maintainer_email}>  {date}
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(changelog_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Debian packaging files')
    parser.add_argument('--software-version', help='Package version to build (e.g., 0.0.2-alpha)')
    parser.add_argument('--changelog', default='CHANGELOG.md', help='Path to CHANGELOG.md')
    parser.add_argument('--license', default='LICENSE.md', help='Path to LICENSE.md')
    parser.add_argument('--output-dir', default='.ci/build-ppa/debian', help='Output directory for Debian files')
    parser.add_argument('--maintainer-name')
    parser.add_argument('--maintainer-email')
    
    args = parser.parse_args()
    
    # Generate copyright file
    generate_copyright(
        Path(args.license),
        Path(args.output_dir) / 'copyright'
    )
    
    # Generate changelog file
    generate_changelog(
        Path(args.changelog),
        args.software_version,
        Path(args.output_dir) / 'changelog',
        args.maintainer_name,
        args.maintainer_email
    )
    
    print(f"Generated Debian packaging files in {args.output_dir}")
