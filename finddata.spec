%global srcname finddata
%global summary Find data files using ONCat
%define release 1

Summary: %{summary}
Name: python-%{srcname}
Version: 0.10.0
Release: %{release}%{?dist}
Source: %{srcname}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch / BuildRequires: gcc
Vendor: Pete Peterson <petersonpf@ornl.gov>
Url: https://github.com/neutrons/finddata

%description
Finddata uses ONCat to locate the full path of files on the NScD clusters.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  %{summary}
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-urllib3
Requires: bash
Requires: bash-completion
Requires: python%{python3_pkgversion}-argcomplete
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

BuildRequires: python3-devel


%description -n python%{python3_pkgversion}-%{srcname}
Finddata uses ONCat to locate the full path of files on the NScD clusters.




%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires  -t

%build
%pyproject_wheel

%install
%pyproject_install


%check
%tox



%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/*
/usr/bin/finddata

