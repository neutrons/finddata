#!/bin/sh
# get the version from the spec file
SPECFILE="$(dirname "$(realpath "$0")")/finddata.spec"

# check that pixi is installed
if [ ! "$(command -v pixi)" ]; then
    echo "This script requires pixi to be installed"
    exit 127
fi

VERSION=$(pixi run versioningit)
echo "versioningit reports ${VERSION}"

# create the tarball
echo "building sdist..."
pixi run backup-toml || exit 127
pixi run sync-version || exit 127
pixi run build-sdist || exit 127
pixi run reset-toml || exit 127


# setup rpm directories for building - renames the tarball
echo "copying source into place for rpmbuild"
TARBALL_SRC="finddata-${VERSION}.tar.gz"
cp dist/"${TARBALL_SRC}" "${HOME}"/rpmbuild/SOURCES/ || exit 127

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba "${SPECFILE}" --define "version ${VERSION}" || exit 127

# give people a hint on how to verify the rpm
# shellcheck disable=SC1083
DIST=$(rpm --eval %{?dist})
echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3-finddata-${VERSION}-1${DIST}.noarch.rpm"
