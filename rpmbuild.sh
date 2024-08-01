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

TARBALL_SRC="finddata-$(versioningit).tar.gz" # created
TARBALL_TGT="finddata-${VERSION}.tar.gz" # what we want
# fixup the tarball if necessary
if [ "${TARBALL_SRC}" != "${TARBALL_TGT}" ]; then
    echo "cleaning up tarball"
    rm -rf "finddata-${VERSION}"
    mkdir "python-finddata-${VERSION}"
    tar xzf "${TARBALL_SRC}" --strip 1 -C "python-finddata-${VERSION}" || exit 127
    rm "${TARBALL_SRC}"
    tar czf "${TARBALL_TGT}" "python-finddata-${VERSION}" || exit 127
    rm -rf "python-finddata-${VERSION}"
fi

# setup rpm directories for building - renames the tarball
mkdir -p "${HOME}"/rpmbuild/SOURCES
cp "${TARBALL_TGT}" "${HOME}/rpmbuild/SOURCES/${TARBALL_TGT}" || exit 127
# move the patchfile into position
# it can be created by editing pyproject.toml then having git create it
# git diff -P pyproject.toml > pyproject.patch && git checkout pyproject.toml
cp pyproject.patch "${HOME}/rpmbuild/SOURCES/finddata-pyproject.patch" || exit 127

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba finddata.spec || exit 127

# give people a hint on how to verify the rpm
# shellcheck disable=SC1083
DIST=$(rpm --eval %{?dist})
echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3.11-finddata-${VERSION}-1${DIST}.noarch.rpm"
