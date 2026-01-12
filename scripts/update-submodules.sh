#!/bin/sh -e

echo "Updating submodules to latest branch commits..."
git submodule update --remote --merge
echo "✅ Submodules updated successfully"
