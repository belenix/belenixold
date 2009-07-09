#
# spec file for package SUNWlibpopt
#
# includes module(s): popt
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
# bugdb: bugzilla.redhat.com
#
%include Solaris.inc

%define _prefix /usr

Name:                    SUNWlibpopt
Summary:                 Command line parsing library
Version:                 1.7
Source:                  ftp://ftp.mirrorservice.org/sites/ftp.rpm.org/pub/rpm/dist/rpm-4.1.x/popt-%{version}.tar.gz
Source1:                 %{name}-manpages-0.1.tar.gz
Source2:                 l10n-configure.sh
# date:2007-12-21 owner:fujiwara type:bug bugster:6186542 bugzilla:178413 state:upstream
Patch1:                  popt-01-g11n-i18n-stdio.diff
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
cd popt-%version
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp popt-%version popt-%version-64
%endif

cd popt-%version
bash -x %SOURCE2 --enable-sun-linguas

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

CONFLAGS="--prefix=%{_prefix} --mandir=%{_mandir} --disable-nls"
export LDFLAGS="%_ldflags"

%ifarch amd64 sparcv9
cd popt-%version-64
CFLAGS32="$RPM_OPT_FLAGS"
RPM_OPT_FLAGS="%optflags64"
export RPM_OPT_FLAGS
CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS

libtoolize -f
aclocal-1.9 $ACLOCAL_FLAGS
autoconf
automake-1.9 -a -c -f

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

./configure $CONFLAGS					\
            --libdir=%{_libdir}/%{_arch64}		\
            --libexecdir=%{_libexecdir}/%{_arch64}	\
            --sysconfdir=%{_sysconfdir}/%{_arch64}

make -j $CPUS
cd ..
%endif

cd popt-%version
libtoolize -f
aclocal-1.9 $ACLOCAL_FLAGS
autoconf
automake-1.9 -a -c -f

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

CFLAGS="$CFLAGS32"	\
./configure $CONFLAGS
make -j $CPUS


%install
%ifarch amd64 sparcv9
cd popt-%version-64
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
%endif

cd popt-%version
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd ../sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

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
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Mon Jun 30 2008 - laca@sun.com
- call automake/aclocal 1.9 explicitely
* Fri Dec 21 2007 - takao.fujiwara@sun.com
- Add popt-01-g11n-i18n-stdio.diff. Fixes '--help' option on none UTF-8.
  CR 6186542
* Wed Dec 19 2007 - patrick.ale@gmail.com
- Change FTP location to ftp.mirrorservices.org.
  ftp.rpm.org does not longer seem available/to exist
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed CC64 and CC32. They are not needed anymore
* Sun Feb 11 2007 - laca@sun.com
- delete PATH changes in the 64-bit build: not needed anymore and break
  the build on SXDE
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sun Jun 11 2006 - laca@Sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 as the 64-bit C compiler, if defined
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : include files should be in a separate devel package
  		renamed SUNWlibpopt-share to SUNWlibpopt-devel-share
	        removed SUNWlibpopt depend on SUNWlibpopt-share
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Wed May 19 2004 - Brian.Cameron@sun.com
- added man page.
* Fri Feb 13 2004 - Laszlo.Peter@sun.com
- added 64-bit version
* Mon Jan 28 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
