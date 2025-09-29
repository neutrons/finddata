FROM registry.access.redhat.com/ubi9/ubi

USER root

RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
RUN dnf install -y make rpm-build python3 python-unversioned-command
RUN dnf install -y bash bash-completion
RUN dnf install -y pyproject-rpm-macros python3-build python3-pip python3-hatchling python3-devel
RUN dnf install -y python3-argcomplete python3-urllib3

RUN useradd builder
USER builder
WORKDIR /home/builder

COPY finddata.spec /home/builder
COPY pyproject.toml /home/builder
COPY rpmbuild.sh /home/builder
RUN mkdir -p /home/builder/dist/
COPY dist/finddata*.tar.gz /home/builder/dist

# make the rpm
RUN /home/builder/rpmbuild.sh || exit 1

# install it
USER root
RUN dnf install -y /home/builder/rpmbuild/RPMS/noarch/python3-finddata*.noarch.rpm || exit 1

# get the version number from it
USER builder
