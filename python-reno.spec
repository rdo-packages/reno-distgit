%global pypi_name reno

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        0.1.0
Release:        2%{?dist}
Summary:        Release NOtes manager

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.python.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
Reno is a release notes manager for storing
release notes in a gitnrepository and then building documentation from them.

Managing release notes for a complex project over a long period
of time with many releases can be time consuming and error prone. Reno
helps automate the hard parts.

%package -n     python2-%{pypi_name}
Summary:        RElease NOtes manager
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-babel
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires: 	PyYAML

Requires:	python-pbr
Requires:	python-babel
Requires:	PyYAML

%description -n python2-%{pypi_name}
Reno is a release notes manager for storing
release notes in a gitnrepository and then building documentation from them.

Managing release notes for a complex project over a long period
of time with many releases can be time consuming and error prone. Reno
helps automate the hard parts.

%if 0%{with_python3}
%package -n     python3-%{pypi_name}
Summary:        RElease NOtes manager
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-babel
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-PyYAML

Requires:	python3-pbr
Requires:	python3-babel
Requires:	python3-PyYAML

%description -n python3-%{pypi_name}
Reno is a release notes manager for storing
release notes in a gitnrepository and then building documentation from them.

Managing release notes for a complex project over a long period
of time with many releases can be time consuming and error prone. Reno
helps automate the hard parts.

%endif

%package -n python-%{pypi_name}-doc
Summary:        reno documentation
%description -n python-%{pypi_name}-doc
Documentation for reno

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build
%if 0%{with_python3}
%py3_build
%endif

%install
%if 0%{with_python3}
%py3_install
%endif

%py2_install

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%files -n python2-%{pypi_name} 
%doc doc/source/readme.rst README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{with_python3}
%files -n python3-%{pypi_name} 
%doc doc/source/readme.rst README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE 

%changelog
* Wed Sep 30 2015 Chandan Kumar <chkumar246@gmail.com> -0.1.0-2
- Some cosmetic changes in spec file

* Wed Sep 30 2015 Chandan Kumar <chkumar246@gmail.com> - 0.1.0-1
- Initial Package
