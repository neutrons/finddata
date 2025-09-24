#!/bin/sh
# error out at first issue
set -e
#set -o pipefail

VERSION=$(python -m versioningit)
# set the version to static value
toml set project.version "${VERSION}" --toml-path pyproject.toml
toml set tool.pixi.package.version "${VERSION}" --toml-path pyproject.toml
# remove all the things that reference dynamic versions
toml unset project.dynamic --toml-path pyproject.toml
toml set project.version "${VERSION}" --toml-path pyproject.toml
toml unset tool.versioningit --toml-path pyproject.toml
toml unset tool.hatch.version --toml-path pyproject.toml
toml unset tool.hatch.build.hooks.versioningit-onbuild --toml-path pyproject.toml
# remove dependencies since rpm will handle them
toml unset project.dependencies --toml-path pyproject.toml

# no longer error
#set +o pipefail
