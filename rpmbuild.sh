#!/bin/sh
# get the version from the spec file
SPECFILE="$(dirname "$(realpath "$0")")/finddata.spec"
echo "Finding version from ${SPECFILE}"

VERSION="$(grep Version "${SPECFILE}" | awk '{print $2}')"
if [ -z "${VERSION}" ]; then
    echo "Failed to determine the version from ${SPECFILE}"
    exit 127
fi
echo "Version is ${VERSION}"

# check that pixi is installed
if [ ! "$(command -v pixi)" ]; then
    echo "This script requires pixi to be installed"
    exit 127
fi

VERSION_FROM_GIT=$(pixi run versioningit)

# create the tarball
echo "building sdist..."
pixi run backup-toml || exit 127
pixi run sync-version || exit 127
pixi run build-sdist || exit 127
pixi run reset-toml || exit 127

TARBALL_SRC="finddata-${VERSION_FROM_GIT}.tar.gz" # created

# setup rpm directories for building - renames the tarball
echo "seting up rpm files"
if [ -f "${TARBALL_TGT}" ]; then
    mkdir -p "${HOME}"/rpmbuild/SOURCES
    cp "${TARBALL_TGT}" "${HOME}/rpmbuild/SOURCES/${TARBALL_TGT}" || exit 127
else
    echo "Failed to find ${TARBALL_TGT}"
    exit 127
fi

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba finddata.spec || exit 127

# give people a hint on how to verify the rpm
# shellcheck disable=SC1083
DIST=$(rpm --eval %{?dist})
echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3-finddata-${VERSION}-1${DIST}.noarch.rpm"
