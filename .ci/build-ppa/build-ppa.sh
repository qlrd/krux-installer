#!/bin/bash
set -e  # Exit on error

# Check if VERSION is set
if [ -z "${VERSION}" ]; then
  echo "Error: VERSION environment variable is not set."
  exit 1
fi

# Generate Debian packaging files
prepare-debian --software-version "${VERSION}" \
  --changelog /source/CHANGELOG.md \
  --license /source/LICENSE \
  --output-dir /output/debian

# Clone the repository and checkout the specific version
git config --global --add safe.directory /source/.git
git clone /source /build/krux-installer
cd /build/krux-installer
git checkout "v${VERSION}"

# Install vendored dependencies
pip install --no-index --find-links /vendor -r <(poetry export -f requirements.txt --without-hashes)

# Build the package
cp -r /output/debian .
dpkg-buildpackage -S

# Move artifacts to output directory
mkdir -p "${OUTPUT_DIR}"
mv ../krux-installer_* "${OUTPUT_DIR}/"

echo "Build complete! Artifacts are in ${OUTPUT_DIR}"
