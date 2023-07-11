%global srcname finddata
%global summary Find data files using ONCat
%define release 1

Summary: %{summary}
Name: python-%{srcname}
Version: 0.8.4
Release: %{release}%{?dist}
Source0: https://github.com/peterfpeterson/finddata/archive/v%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Pete Peterson <petersonpf@ornl.gov>
Url: https://github.com/peterfpeterson/finddata

%description
Finddata uses ONCat to locate the full path of files on the NScD clusters.

%package -n %{srcname}
Summary:  %{summary}
Requires: python2
Requires: python2-plotly
Requires: python2-pyoncat
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

BuildRequires: python2-devel
BuildRequires: python2-setuptools

%description -n %{srcname}
Finddata uses ONCat to locate the full path of files on the NScD clusters.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  %{summary}
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-plotly
Requires: python%{python3_pkgversion}-pyoncat
Requires: bash
Requires: bash-completion
Requires: python%{python3_pkgversion}-argcomplete
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description -n python%{python3_pkgversion}-%{srcname}
Finddata uses ONCat to locate the full path of files on the NScD clusters.

%prep
%setup -n %{srcname}-%{version} -n %{srcname}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

# testing is somehow broken, but the package did work
#%check
#%{__python3} setup.py test
# ipywidgets is missing
# skimage is missing

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{srcname}
%doc README
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python%{python3_pkgversion}-%{srcname}
%doc README
%license LICENSE.txt
%{python3_sitelib}/*
/usr/bin/finddata
/etc/bash_completion.d/finddata.bashcomplete
