# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: libbpf
Epoch: 100
Version: 0.8.0
Release: 1%{?dist}
Summary: Libbpf library
License: LGPL-2.1+
URL: https://github.com/sudipm-mukherjee/libbpf/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: elfutils-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: zlib-devel

%description
libbpf is a library for loading eBPF programs and reading and
manipulating eBPF objects from user-space.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%make_build -C ./src CFLAGS="%{optflags}"

%install
%make_install -C ./src CFLAGS="%{optflags}"

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libbpf0
Summary: C library for managing eBPF programs and maps

%description -n libbpf0
libbpf is a C library which provides API for managing eBPF programs and maps.

%package -n libbpf-devel
Summary: eBPF helper library (development files)
Requires: elfutils-devel
Requires: elfutils-libelf-devel
Requires: libbpf0 = %{epoch}:%{version}-%{release}
Requires: zlib-devel

%description -n libbpf-devel
This package is needed to compile programs against libbpf.

%package -n libbpf-devel-static
Summary: eBPF helper library (development files)
Requires: libbpf-devel = %{epoch}:%{version}-%{release}

%description -n libbpf-devel-static
The libbpf-static package contains static library for developing
applications that use libbpf.

%post -n libbpf0 -p /sbin/ldconfig
%postun -n libbpf0 -p /sbin/ldconfig

%files -n libbpf0
%license LICENSE
%{_libdir}/*.so.*

%files -n libbpf-devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%files -n libbpf-devel-static
%{_libdir}/*.a
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n libbpf-devel
Summary: eBPF helper library (development files)
Requires: elfutils-devel
Requires: elfutils-libelf-devel
Requires: libbpf = %{epoch}:%{version}-%{release}
Requires: zlib-devel

%description -n libbpf-devel
This package is needed to compile programs against libbpf.

%package -n libbpf-static
Summary: eBPF helper library (development files)
Requires: libbpf-devel = %{epoch}:%{version}-%{release}

%description -n libbpf-static
The libbpf-static package contains static library for developing
applications that use libbpf.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so.*

%files -n libbpf-devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%files -n libbpf-static
%{_libdir}/*.a
%endif

%changelog
