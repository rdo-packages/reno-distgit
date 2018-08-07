%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name reno

%if 0%{?fedora}
%global with_python3 1
%endif

# Currently, we cannot generate reno docs from a tarball due to
# https://bugs.launchpad.net/reno/+bug/1520096
%global with_docs 0

# Only reason to choose 24 is that that's what was in development when we made
# the switch for this package.  Fedora Policy was to have made this switch for
# Fedora 22.
%if 0%{?fedora} >= 24
%global default_python 3
%else
%global default_python 2
%endif

%global common_desc \
Reno is a release notes manager for storing \
release notes in a git repository and then building documentation from them. \
\
Managing release notes for a complex project over a long period \
of time with many releases can be time consuming and error prone. Reno \
helps automate the hard parts.

Name:           python-%{pypi_name}
Version:        2.9.2
Release:        1%{?dist}
Summary:        Release NOtes manager

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        RElease NOtes manager
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-dulwich
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-babel
BuildRequires:  python2-sphinx
%if 0%{?fedora} > 0
BuildRequires:  python2-pyyaml
# Until https://src.fedoraproject.org/rpms/python-dulwich/pull-request/3 is merged, we need this
BuildRequires:  python2-certifi
%else
BuildRequires:  PyYAML
%endif
BuildRequires:  git

Requires:	python2-pbr
Requires:	python2-babel
Requires:   python2-dulwich
%if 0%{?fedora} > 0
Requires:   python2-pyyaml
# Until https://src.fedoraproject.org/rpms/python-dulwich/pull-request/3 is merged, we need this
Requires:  python2-certifi
%else
Requires:   PyYAML
%endif
Requires:	python2-six
Requires:   git

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}

%package -n     python3-%{pypi_name}
Summary:        RElease NOtes manager
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-dulwich
# Until https://src.fedoraproject.org/rpms/python-dulwich/pull-request/3 is merged, we need this
BuildRequires:  python3-certifi
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-babel
BuildRequires:  python3-sphinx
BuildRequires:  python3-PyYAML
BuildRequires:  git

Requires:	python3-pbr
Requires:	python3-babel
Requires:   python3-dulwich
# Until https://src.fedoraproject.org/rpms/python-dulwich/pull-request/3 is merged, we need this
Requires:   python3-certifi
Requires:	python3-PyYAML
Requires:	python3-six
Requires:   git

%description -n python3-%{pypi_name}
%{common_desc}

%endif

%package -n python-%{pypi_name}-doc
Summary:        reno documentation
%description -n python-%{pypi_name}-doc
Documentation for reno

%prep
%autosetup -n %{pypi_name}-%{upstream_version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%if 0%{?default_python} >= 3
mv %{buildroot}%{_bindir}/%{pypi_name} ./%{pypi_name}.py3
%endif
%endif

%py2_install

%if 0%{?default_python} >= 3
mv %{pypi_name}.py3 %{buildroot}%{_bindir}/%{pypi_name}
%endif

%if 0%{?with_docs}
# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%if 0%{?default_python} <= 2
%{_bindir}/%{pypi_name}
%endif
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%if 0%{?default_python} >= 3
%{_bindir}/%{pypi_name}
%endif
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%files -n python-%{pypi_name}-doc
%if 0%{?with_docs}
%doc html
%endif
%license LICENSE

%changelog
* Tue Aug 07 2018 RDO <dev@lists.rdoproject.org> 2.9.2-1
- Update to 2.9.2

