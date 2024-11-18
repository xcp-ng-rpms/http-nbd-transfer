Name:           http-nbd-transfer
Version:        1.5.0
Release:        1%{?dist}
Summary:        Set of tools to transfer NBD requests to a HTTP server
License:        GPLv3
URL:            https://github.com/xcp-ng/http-nbd-lib
Source0:        https://github.com/xcp-ng/http-nbd-lib/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: libcurl-devel
BuildRequires: make
BuildRequires: nbdkit-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: libcurl
Requires: nbd
Requires: nbdkit
Requires: python3

%description
Set of tools to transfer NBD requests to a HTTP server.

%prep
%autosetup -p1

%build
make
PYTHON=%{__python3} %{__python3} ./setup.py build

%install
%make_install PREFIX=%{_prefix} DESTDIR=%{buildroot}
PYTHON=%{__python3} %{__python3} ./setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

%files -f INSTALLED_FILES
%{_libdir}/nbdkit/plugins/nbdkit-multi-http-plugin.so

%changelog
* Tue Nov 19 2024 Ronan Abhamon <ronan.abhamon@vates.tech> - 1.5.0-1
- Prevent stacktrace during SIGTERM signal and open_device call
- Robustify nbdkit startup: always wait for sockpath to be created
- Handle broken pipe errors for python 3
- Fix nbdkit plugin location for python 3
- Don't force stdout/stderr flush
- Fix libs import using underscores instead of dashes

* Wed Jul 31 2024 Ronan Abhamon <ronan.abhamon@vates.tech> - 1.4.0-1
- Try to open device and start HTTP server before notifying the user
- Install pyc and pyo files

* Wed Jul 12 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.3.0-1
- Handle invalid buffer usage in nbdkit plugin
- Compatible with both versions of Python: 2 and 3

* Fri Feb 17 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.2.0-1
- Remove open/close calls to read/write disk

* Mon Jan 09 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.1.0-1
- HTTP server can reuse binding address now
- Notify when HTTP server is ready
- Better error handling and command logs
- SIGTERM can be safely sent to NBD server

* Tue May 03 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.0-1
- Initial package
