#
# spec file for package SUNWlibffi
#
# includes module(s): libffi
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libffi_64 = libffi.spec
%endif

%include base.inc
%use libffi = libffi.spec

Name:                    SUNWlibffi
Summary:                 %{libffi.summary}
Version:                 %{libffi.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libffi.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%libffi.prep -d %name-%version/%base_arch

%build
%if %cc_is_gcc
%else
export CXX="$CXX -norunpath"
%endif

%ifarch amd64 sparcv9
%libffi_64.build -d %name-%version/%_arch64
%endif

%libffi.build -d %name-%version/%base_arch

%install
%ifarch amd64 sparcv9
%libffi_64.install -d %name-%version/%_arch64
%endif

%libffi.install -d %name-%version/%base_arch

rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%ifarch amd64 sparcv9
rm $RPM_BUILD_ROOT%{_libdir}/%_arch64/lib*.la
%endif

# FIXME
rm -r $RPM_BUILD_ROOT%{_datadir}/info

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch sparcv9 amd64
%{_libdir}/%_arch64/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man3/*.3

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libffi-%{libffi.version}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch sparcv9 amd64
%{_libdir}/%_arch64/libffi-%{libffi.version}
%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
%{_libdir}/%_arch64/pkgconfig/*
%endif

%changelog
* Fri May 23 2008 - laca@sun.com
- create
