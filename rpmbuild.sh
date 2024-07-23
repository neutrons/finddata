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


# create the tarball
echo "building sdist..."
python -m build --sdist --outdir . --no-isolation || exit 127
TARBALL="finddata-${VERSION}*.tar.gz"

# setup rpm directories for building - renames the tarball
mkdir -p "${HOME}"/rpmbuild/SOURCES
cp "${TARBALL}" "${HOME}/rpmbuild/SOURCES/finddata-${VERSION}.tar.gz"

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba finddata.spec || exit 127

# give people a hint on how to verify the rpm
DIST=$(rpm --eval %{?dist})
echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3-finddata-${VERSION}-1${DIST}.noarch.rpm"
