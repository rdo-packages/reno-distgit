# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name reno

# Currently, we cannot generate reno docs from a tarball due to
# https://bugs.launchpad.net/reno/+bug/1520096
%global with_docs 0

%global common_desc \
Reno is a release notes manager for storing \
release notes in a git repository and then building documentation from them. \
\
Managing release notes for a complex project over a long period \
of time with many releases can be time consuming and error prone. Reno \
helps automate the hard parts.

Name:           python-%{pypi_name}
Version:        2.11.3
Release:        1%{?dist}
Summary:        Release NOtes manager

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        RElease NOtes manager
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-dulwich
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-babel
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  git

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  PyYAML
%else
# Until https://src.fedoraproject.org/rpms/python-dulwich/pull-request/3 is merged, we need this
BuildRequires:  python%{pyver}-certifi
BuildRequires:  python%{pyver}-PyYAML
%endif

Requires:  python%{pyver}-pbr
Requires:  python%{pyver}-babel
Requires:  python%{pyver}-dulwich
Requires:  python%{pyver}-six
Requires:  git

# Handle python2 exception
%if %{pyver} == 2
Requires:  PyYAML
%else
Requires:  python%{pyver}-PyYAML
# Until https://src.fedoraproject.org/rpms/python-dulwich/pull-request/3 is merged, we need this
Requires:  python%{pyver}-certifi
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%package -n python-%{pypi_name}-doc
Summary:        reno documentation
%description -n python-%{pypi_name}-doc
Documentation for reno

%prep
%autosetup -n %{pypi_name}-%{upstream_version}

%build
%{pyver_build}

%install
%{pyver_install}

%if 0%{?with_docs}
# generate html docs
sphinx-build-%{pyver} doc/source html
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-*.egg-info

%files -n python-%{pypi_name}-doc
%if 0%{?with_docs}
%doc html
%endif
%license LICENSE

%changelog
* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 2.11.3-1
- Update to 2.11.3

