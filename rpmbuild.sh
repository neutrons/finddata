#!/bin/sh
SPECFILE="$(dirname "$(realpath "$0")")/finddata.spec"

# get the version from the pyproject.toml file
VERSION=$(grep ^version pyproject.toml  | cut -d " " -f 3 | sed 's/\"//g')
echo "version in pyproject.toml is ${VERSION}"

# create the source tarball
if command -v pixi >/dev/null 2>&1; then
    # this runs outside of docker where pixi exists
    echo "building sdist..."
    pixi run build-sdist || exit 127
else
    # must be inside of docker
    echo "assuming sdist already exists"
fi

# setup rpm directories for building - renames the tarball
TARBALL_SRC="finddata-${VERSION}.tar.gz" # created
if [ ! -f dist/"${TARBALL_SRC}" ]; then
    echo "Failed to find source tarball: dist/${TARBALL_SRC}"
    exit 127
fi
mkdir -p "${HOME}"/rpmbuild/SOURCES
cp dist/"${TARBALL_SRC}" "${HOME}"/rpmbuild/SOURCES/"${TARBALL_SRC}" || exit 127

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba "${SPECFILE}" --define "version ${VERSION}" || exit 127

# give people a hint on how to verify the rpm
# shellcheck disable=SC1083
DIST=$(rpm --eval %{?dist})
echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3-finddata-${VERSION}-1${DIST}.noarch.rpm"
