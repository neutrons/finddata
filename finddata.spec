Name:           finddata
Version:        0.1.0
Release:        1%{?dist}
Summary:        Find data files using ICAT

License:        The MIT License (MIT)
URL:            http://github.com/peterfpeterson/finddata/
Source:	        %{name}.tar.gz
BuildArch:      noarch

Requires:       python
Requires:       bash
Requires:       bash-completion

%description
This package uses ICAT4 at SNS to find NeXus files.

%prep
%setup -n %{name}

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}/finddata %{buildroot}%{_bindir}/finddata
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{_builddir}/%{name}/finddata.bashcomplete %{buildroot}%{_sysconfdir}/bash_completion.d/finddata.bashcomplete

%clean
exit 0

%files
%defattr(-,root,root,-)
%doc README.md
%doc LICENSE.txt
%{_bindir}/finddata
%{_sysconfdir}/bash_completion.d/finddata.bashcomplete

%changelog
