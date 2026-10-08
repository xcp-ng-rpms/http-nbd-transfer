Name:           http-nbd-transfer
Version:        1.7.0
Release:        2~XCPNG3564.2%{?dist}
Summary:        Set of tools to transfer NBD requests to a HTTP server
License:        GPLv3
URL:            https://github.com/xcp-ng/http-nbd-transfer
Source0:        https://github.com/xcp-ng/http-nbd-transfer/archive/v%{version}/%{name}-%{version}.tar.gz

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

%package tests
Summary:        Test suite for http-nbd-transfer
Requires:       %{name} = %{version}-%{release}
Requires:       pytest
Requires:       lsof

%description tests
Test suite for http-nbd-transfer tools, it requires root privileges and uses nbd kernel module.

Usage:
py.test /usr/*/http-nbd-transfer/tests

%prep
%autosetup -p1

%build
make
PYTHON=%{__python3} %{__python3} ./setup.py build

%check
# Skip tests as root is required, so tests are packaged for integration purpose
# py.test tests

%install
%make_install PREFIX=%{_prefix} DESTDIR=%{buildroot}
PYTHON=%{__python3} %{__python3} ./setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

# Package upstream's testsuite for integration tests
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/tests
install -m 0644 tests/*.py %{buildroot}%{_libdir}/%{name}/tests/

# Adapt tests's paths to use system's files
# and write to temp dir to prevent filesystem pollution
sed -i \
    -e "s|WORKING_DIR + 'bin/'|'%{_bindir}/'|" \
    -e "s|'/{}/{}.socket'.format(WORKING_DIR, volume_name)|'/tmp/%{name}-{}.socket'.format(volume_name)|" \
    -e "s|backing_path = WORKING_DIR + 'image-'|backing_path = '/tmp/%{name}-image-'|" \
    %{buildroot}%{_libdir}/%{name}/tests/conftest.py

%files -f INSTALLED_FILES
%{_libdir}/nbdkit/plugins/nbdkit-multi-http-plugin.so

%files tests
%{_libdir}/%{name}/tests/__init__.py
%{_libdir}/%{name}/tests/conftest.py
%{_libdir}/%{name}/tests/test_mirroring.py
%{_libdir}/%{name}/tests/test_requests.py
%exclude %{_libdir}/%{name}/tests/*.pyc
%exclude %{_libdir}/%{name}/tests/*.pyo

%changelog
* Thu Oct 8 2026 Philippe Coval <philippe.coval@vates.tech> - 1.7.0-2
- Add tests subpackage that adapt upstream's test suite,

* Thu Jul 10 2025 Mathieu Labourier <mathieu.labourier@vates.tech> - 1.7.0-1
- Fix missing import exceptions in log files.
- Fix a potential HA startup failure with LINSTOR.

* Tue Jun 17 2025 Mathieu Labourier <mathieu.labourier@vates.tech> - 1.6.0-1
- Reduce logs by adding a debug log feature

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
