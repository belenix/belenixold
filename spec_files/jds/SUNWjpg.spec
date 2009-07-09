#
# spec file for package SUNWjpg
#
# includes module(s): jpeg
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

%define tarball_version 6b

Name:                    SUNWjpg
Summary:                 jpeg - The Independent JPEG Groups JPEG software
Version:                 20.%{default_pkg_version}
Source:                  http://www.ijg.org/files/jpegsrc.v%{tarball_version}.tar.gz
Source1:                 %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -c -n %name-%version
gzcat %SOURCE1 | tar xf -
cd jpeg-%{tarball_version}

%ifarch amd64 sparcv9
cd ..
mv jpeg-%{tarball_version} jpeg-%{tarball_version}-64
gzcat %SOURCE0 | tar xf -
cd jpeg-%{tarball_version}
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="$RPM_OPT_FLAGS"
cd jpeg-%{tarball_version}
./configure --enable-shared --prefix=%{_prefix} --exec-prefix=%{_prefix}
sed -e "s%%^CC=\"/.*\"%%CC=\"$CC\"%%" `which libtool` > libtool
chmod a+x libtool
make -j$CPUS

%ifarch amd64 sparcv9
cd ../jpeg-%{tarball_version}-64
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags %optflags64"
export LD_RUN_PATH=%{_prefix}/lib/%{_arch64}
./configure --enable-shared --prefix=%{_prefix} --exec-prefix=%{_prefix}
sed -e "s%%^CC=\"/.*\"%%CC=\"$CC\"%%" `which libtool` > libtool
chmod a+x libtool
make -j$CPUS
%endif

%install
cd jpeg-%{tarball_version}
mkdir -p $RPM_BUILD_ROOT/dummy
mkdir -p $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
make install mandir=$RPM_BUILD_ROOT%{_mandir}/man1 bindir=$RPM_BUILD_ROOT%{_bindir} includedir=$RPM_BUILD_ROOT%{_includedir} libdir=$RPM_BUILD_ROOT%{_libdir}

%ifarch amd64 sparcv9
cd ../jpeg-%{tarball_version}-64
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
make install bindir=$RPM_BUILD_ROOT/dummy includedir=$RPM_BUILD_ROOT/dummy mandir=$RPM_BUILD_ROOT/dummy libdir=$RPM_BUILD_ROOT%{_libdir}/%{_arch64}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
%endif

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd ../sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT/dummy

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Apr 06 2006 - brian.cameron@sun.com
- Now use tarball-version
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 as the 64-bit C compiler, if defined
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : Include files and man3 files should be in separate devel package
* Thu Aug 12 2004 - shirley.woo@sun.com
- Updated Version to be 2.6.0 since delivering w/ G2.6
* Sun Feb 23 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
