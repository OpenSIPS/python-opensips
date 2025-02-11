Summary:  A collection of Python packages for OpenSIPS.
Name:     python3-opensips
Version:  0.1.5
Release:  1%{?dist}
License:  GPL-3+
Group:    System Environment/Daemons
Source0:  Source0:  http://download.opensips.org/python/%{name}-%{version}.tar.gz
URL:      https://github.com/OpenSIPS/python-opensips

BuildArch: noarch

BuildRequires:  python%{python3_pkgversion}-setuptools, python%{python3_pkgversion}-devel
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

AutoReqProv: no

Requires: python3 >= 3.6

%description
A collection of Python packages for OpenSIPS.
These modules are designed to be as lightweight as possible and provide a
simple interface for interacting with OpenSIPS.
.
OpenSIPS is a very fast and flexible SIP (RFC3261)
server. Written entirely in C, OpenSIPS can handle thousands calls
per second even on low-budget hardware.
.
C Shell-like scripting language provides full control over the server's
behaviour. Its modular architecture allows only required functionality to be
loaded.
.
Among others, the following modules are available: Digest Authentication, CPL
scripts, Instant Messaging, MySQL support, Presence Agent, Radius
Authentication, Record Routing, SMS Gateway, Jabber/XMPP Gateway, Transaction
Module, Registrar and User Location, Load Balaning/Dispatching/LCR,
XMLRPC Interface.

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install
install -d %{buildroot}%{bash_completions_dir}/
install -Dpm 0644 utils/completion/python-opensips -t %{buildroot}%{bash_completions_dir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/opensips-event
%{_bindir}/opensips-mi
%{python3_sitelib}/opensips/*
%{python3_sitelib}/opensips-*.egg-info
%{bash_completions_dir}/python-opensips
%doc README.md
%doc docs/*
%license LICENSE

%changelog
* Tue Feb 11 2025 Darius Stefan <darius.stefan@opensips.org> - 0.1.5-1
- Set default communication type to fifo
- Set correct default values for fifo communication

* Mon Dec 09 2024 Razvan Crainea <razvan@opensips.org> - 0.1.4-1
- Fix logging of mi script
- Add completion

* Tue Nov 19 2024 Razvan Crainea <razvan@opensips.org> - 0.1.3-3
- Initial spec.
