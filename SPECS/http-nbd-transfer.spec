Name:           http-nbd-transfer
Version:        1.0.0
Release:        1%{?dist}
Summary:        Set of tools to transfer NBD requests to a HTTP server
License:        GPLv3
URL:            https://github.com/xcp-ng/http-nbd-lib
Source0:        https://github.com/xcp-ng/http-nbd-lib/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: libcurl-devel
BuildRequires: make
BuildRequires: nbdkit-devel

Requires: libcurl
Requires: nbd
Requires: nbdkit

%description
Set of tools to transfer NBD requests to a HTTP server.

%prep
%autosetup -p1

%build
make

%install
%make_install PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT

%files
%{_bindir}/http-disk-server
%{_bindir}/nbd-http-server
%{_libdir}/nbdkit/plugins/nbdkit-multi-http-plugin.so

%changelog
* Tue May 3 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.0-1
- Initial package
