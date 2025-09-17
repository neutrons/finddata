%global srcname finddata
%global summary Find data files using ONCat
%define release 1
# default python3=python3.9 on rhel9 which is too old
%define python3_pkgversion 3

Summary: %{summary}
Name: python-%{srcname}
Version: 0.11.1
Release: %{release}%{?dist}
Source: %{srcname}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Pete Peterson <petersonpf@ornl.gov>
Url: https://github.com/neutrons/finddata
Obsoletes: python3-finddata < 0.10

%description
Finddata uses ONCat to locate the full path of files on the NScD clusters.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  %{summary}
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-urllib3
Requires: bash
Requires: bash-completion
#Requires: python{python3_pkgversion}-argcomplete
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-wheel
BuildRequires: python%{python3_pkgversion}-pip

%description -n python%{python3_pkgversion}-%{srcname}
Finddata uses ONCat to locate the full path of files on the NScD clusters.

# unpack tarball and apply patchfile - add -v to see individual commands
%prep
%autosetup -p1

%build
%pyproject_wheel

%install
%pyproject_install
# automatically scan files to install
%pyproject_save_files finddata
# install bash completions
%{__mkdir} -p %{buildroot}%{_sysconfdir}/bash_completion.d/
%{__install} -m 644 finddata.bashcomplete %{buildroot}%{_sysconfdir}/bash_completion.d/

# there are no tests - check that top level module can be imported
%check
%pyproject_check_import -t

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/finddata
%{_sysconfdir}/bash_completion.d/finddata.bashcomplete
