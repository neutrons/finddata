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
TARBALL="finddata-v${VERSION}.tar.gz"
echo "creating tarball ${TARBALL}"
git archive --format=tar.gz HEAD --prefix="finddata-${VERSION}/" -o "${TARBALL}"
mkdir -p "${HOME}"/rpmbuild/SOURCES
cp "${TARBALL}" "${HOME}/rpmbuild/SOURCES/v${VERSION}.tar.gz"

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba finddata.spec || exit 127

echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3-finddata-${VERSION}-1.el7.noarch.rpm"
