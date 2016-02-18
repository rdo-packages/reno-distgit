%global pypi_name reno

%if 0%{?fedora}
%global with_python3 1
%endif

# Only reason to choose 24 is that that's what was in development when we made
# the switch for this package.  Fedora Policy was to have made this switch for
# Fedora 22.
%if 0%{?fedora} >= 24
%global default_python 3
%else
%global default_python 2
%endif


Name:           python-%{pypi_name}
Version:        1.5.0
Release:        1%{?dist}
Summary:        Release NOtes manager

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.python.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
Reno is a release notes manager for storing release notes in a git repository
and then building documentation from them.

Managing release notes for a complex project over a long period
of time with many releases can be time consuming and error prone. Reno
helps automate the hard parts.

%package -n     python2-%{pypi_name}
Summary:        Release Notes Manager
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-babel
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  PyYAML

Requires:  python-pbr
Requires:  python-babel
Requires:  PyYAML

%description -n python2-%{pypi_name}
Reno is a release notes manager for storing release notes in a git repository
and then building documentation from them.

Managing release notes for a complex project over a long period
of time with many releases can be time consuming and error prone. Reno
helps automate the hard parts.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Release Notes manager
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-babel
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-PyYAML

Requires:  python3-pbr
Requires:  python3-babel
Requires:  python3-PyYAML

%description -n python3-%{pypi_name}
Reno is a release notes manager for storing release notes in a git repository
and then building documentation from them.

Managing release notes for a complex project over a long period
of time with many releases can be time consuming and error prone. Reno
helps automate the hard parts.

%endif

%package -n python-%{pypi_name}-doc
Summary:        Reno documentation
%description -n python-%{pypi_name}-doc
Documentation for Reno

%prep
# FIXME: workaround required to build reno
%autosetup -n %{pypi_name}-%{version} -S git

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
mv %{buildroot}%{_bindir}/%{pypi_name} %{buildroot}%{_bindir}/python2-%{pypi_name}

%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{pypi_name} %{buildroot}%{_bindir}/python3-%{pypi_name}
%endif

%if 0%{?default_python} >= 3
ln -s %{_bindir}/python3-%{pypi_name} %{buildroot}%{_bindir}/%{pypi_name}
%else
ln -s %{_bindir}/python2-%{pypi_name} %{buildroot}%{_bindir}/%{pypi_name}
%endif

# generate html docs
%{__python2} setup.py build_sphinx
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv

%files -n python2-%{pypi_name} 
%doc doc/source/readme.rst README.rst
%license LICENSE
%if 0%{?default_python} <= 2
%{_bindir}/%{pypi_name}
%endif
%{_bindir}/python2-%{pypi_name}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name} 
%doc doc/source/readme.rst README.rst
%license LICENSE
%if 0%{?default_python} >= 3
%{_bindir}/%{pypi_name}
%endif
%{_bindir}/python3-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE 

%changelog
* Thu Feb 18 2016 Paul Belanger <pabelanger@redhat.com> - 1.5.0-1
- New upstream 1.5.0 release
- Fix rpmlint spelling-error warnings

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.3.1-2
- Simplify macros and reno CLI generation
- Fix build on EL7

* Fri Jan 22 2016 Paul Belanger <pabelanger@redhat.com> 1.3.1-1
- New upstream 1.3.1 release
- Switch to setup.py build_sphinx to keep inline with upstream documentation
  builds
- Various rpmlint fixes

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov  5 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1.0-3
- Ship the reno script against python3 to comply with the python guidelines and
  solve the issue of the python3 package depending on /usr/bin/python2

* Wed Sep 30 2015 Chandan Kumar <chkumar246@gmail.com> -0.1.0-2
- Some cosmetic changes in spec file

* Wed Sep 30 2015 Chandan Kumar <chkumar246@gmail.com> - 0.1.0-1
- Initial Package
