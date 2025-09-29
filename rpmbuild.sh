#!/bin/sh
SPECFILE="$(dirname "$(realpath "$0")")/finddata.spec"

# get the version from the pyproject.toml file
VERSION=$(pixi run python -c "from importlib import metadata;print(metadata.version('finddata'))")
echo "version in pyproject.toml is ${VERSION}"

# create the tarball
echo "building sdist..."
pixi run build-sdist || exit 127


# setup rpm directories for building - renames the tarball
TARBALL_SRC="finddata-${VERSION}.tar.gz" # created
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
