%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
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
Version:        XXX
Release:        XXX
Summary:        Release NOtes manager

License:        Apache-2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        RElease NOtes manager
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:  git-core

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python-%{pypi_name}-doc
Summary:        reno documentation
%description -n python-%{pypi_name}-doc
Documentation for reno

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version}

sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
for reqfile in doc/requirements.txt test-requirements.txt; do
if [ -f $reqfile ]; then
sed -i /^${pkg}.*/d $reqfile
fi
done
done
# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_docs}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.dist-info

%files -n python-%{pypi_name}-doc
%if 0%{?with_docs}
%doc doc/build/html
%endif
%license LICENSE

%changelog
