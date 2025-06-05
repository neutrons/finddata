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

# create the tarball
echo "building sdist..."
pixi run build-sdist || exit 127

TARBALL_SRC="finddata-$(pixi run versioningit).tar.gz" # created
TARBALL_TGT="finddata-${VERSION}.tar.gz" # what we want
# fixup the tarball if necessary
if [ "${TARBALL_SRC}" != "${TARBALL_TGT}" ]; then
    echo "cleaning up tarball"
    rm -rf "finddata-${VERSION}"
    mkdir "python-finddata-${VERSION}"

    echo "unpacking ${TARBALL_SRC}"
    tar xzf "sdist/${TARBALL_SRC}" --strip 1 -C "python-finddata-${VERSION}" || exit 127
    rm "${TARBALL_SRC}"

    # set a fixed version number
    echo "modify the pyproject.toml"
    pixi run toml unset project.dynamic --toml-path python-finddata-"${VERSION}"/pyproject.toml || exit 127
    pixi run toml set project.version "${VERSION}" --toml-path python-finddata-"${VERSION}"/pyproject.toml || exit 127
    pixi run toml unset tool.versioningit --toml-path python-finddata-"${VERSION}"/pyproject.toml || exit 127
    pixi run toml unset tool.hatch.version --toml-path python-finddata-"${VERSION}"/pyproject.toml || exit 127
    pixi run toml unset tool.hatch.build.hooks.versioningit-onbuild --toml-path python-finddata-"${VERSION}"/pyproject.toml || exit 127
    # remove dependencies since rpm will handle them
    pixi run toml unset project.dependencies --toml-path python-finddata-"${VERSION}"/pyproject.toml || exit 127

    echo "create tarball with correct name"
    tar czf "${TARBALL_TGT}" "python-finddata-${VERSION}" || exit 127
    rm -rf "python-finddata-${VERSION}"
fi

# setup rpm directories for building - renames the tarball
mkdir -p "${HOME}"/rpmbuild/SOURCES
cp "${TARBALL_TGT}" "${HOME}/rpmbuild/SOURCES/${TARBALL_TGT}" || exit 127

# build the rpm and give instructions
echo "building the rpm"
rpmbuild -ba finddata.spec || exit 127

# give people a hint on how to verify the rpm
# shellcheck disable=SC1083
DIST=$(rpm --eval %{?dist})
echo "========================================"
echo "Successfully built rpm. To manually inspect package run"
echo "rpm -qilRp ~/rpmbuild/RPMS/noarch/python3-finddata-${VERSION}-1${DIST}.noarch.rpm"
