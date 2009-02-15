#
# spec file for package SFEgdbm
#
# includes module(s): gdbm
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:         SFEgdbm
Summary:      GNU Database Routines
Group:        libraries/database
Version:      1.8.3
License:      GPL
Group:        Development/Libraries/C and C++
Release:      1
BuildRoot:    %{_tmppath}/gdbm-%{version}-build
Source0:      http://ftp.gnu.org/gnu/gdbm/gdbm-%{version}.tar.gz
URL:          http://directory.fsf.org/gdbm.html
Patch1:       gdbm-01-fixmake.diff
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%description
GNU database routines

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd gdbm-%{version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr gdbm-%{version} gdbm-%{version}-64
%endif


%build

%ifarch amd64 sparcv9
cd gdbm-%{version}-64
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64"
glib-gettextize -f
libtoolize --force
aclocal
autoconf
CFLAGS="$CFLAGS $RPM_OPT_FLAGS"         \
        ./configure                     \
                --prefix=%{_prefix}     \
                --infodir=%{_datadir}/info \
                --mandir=%{_mandir}     \
                --libdir=%{_libdir}/%{_arch64}     \
                --disable-static
make
cd ..
%endif

cd gdbm-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
glib-gettextize -f
libtoolize --force
aclocal
autoconf
CFLAGS="$CFLAGS $RPM_OPT_FLAGS"         \
        ./configure                     \
                --prefix=%{_prefix}     \
                --infodir=%{_datadir}/info \
                --mandir=%{_mandir}     \
                --libdir=%{_libdir}     \
                --disable-static
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd gdbm-%{version}-64
make INSTALL_ROOT=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.la
cd ..
%endif

cd gdbm-%{version}
make INSTALL_ROOT=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
cd ..

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sun Feb 15 2009 - moinakg@gmail.com
- Add 64Bit build.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgdbm
- delete -share subpkg
- update file attributes
* Fri May 05 2006 - damien.carbery@sun.com
- Remove unnecessary intltoolize call.
* Wed Mar 08 2006 - brian.cameron@sun.com
- Created.
