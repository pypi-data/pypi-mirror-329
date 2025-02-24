set -euo pipefail

grep "current_version =" "$REPO_ROOT/pyproject.toml" 

while true; do
  read -rp "Is the current version flag correctly set? [y/N] " yn
  case $yn in
    [yY]* ) break;;
    [Nn]* ) exit;;
    * ) exit ;;
  esac
done

# update the caches
uv sync
touch "$REPO_ROOT/flake.nix"

# ensure that everything works as expected
mkdocs build --clean
pytest

rm -rf "$REPO_ROOT/dist"
rm -f "$REPO_ROOT/isd.x86_64-linux.AppImage"
rm -f "$REPO_ROOT/isd.aarch64-linux.AppImage"

# start building everything
uv build

echo "Building x86-64 isd-AppImage"
nix build .#isd-AppImage
cp "$(readlink -f ./result)" isd.x86_64-linux.AppImage

echo "Building aarch64 isd-AppImage"
nix build .#packages.aarch64-linux.isd-AppImage
cp "$(readlink -f ./result)" isd.aarch64-linux.AppImage

# publish latest docs
echo "Publishing docs"
mkdocs gh-deploy --no-history

echo "Remember to update PyPI!"

