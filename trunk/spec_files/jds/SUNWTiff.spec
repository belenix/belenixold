#
# spec file for package SUNWTiff
#
# includes module(s): tiff
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

%define _prefix /usr

%define tarball_version 3.8.2

Name:                    SUNWTiff
Summary:                 libtiff - library for reading and writing TIFF
Version:                 20.%{default_pkg_version}
Source:                  ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{tarball_version}.tar.gz
Source1:                 %{name}-manpages-0.1.tar.gz
# date:2006-11-22 owner:laca type:bug bugster:6451119 state:upstream
# patch for vulnerabilities identified by Tavis Ormandy, Google Security Team
# upstream, taken from Fedora
Patch1:                  libtiff-01-ormandy.diff
# date:2006-11-22 owner:laca type:bug bugster:6451119 state:upstream
# upstream, taken from Fedora
Patch2:                  libtiff-02-CVE-2006-2193.diff
# date:2008-09-03 owner:johnf type:bug bugster:6743799 state:upstream
# upstream, taken from RHEL by Even Rouault
Patch3:                  libtiff-03-CVE-2008-2327.diff
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWzlib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SUNWTiff
Requires: SUNWman

%prep
%setup -c -n %name-%version
cd tiff-%{tarball_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
gzcat %SOURCE1 | tar -xf -

%ifarch amd64 sparcv9
cd ..
mv tiff-%{tarball_version} tiff-%{tarball_version}-64
gzcat %SOURCE0 | tar xf -
cd tiff-%{tarball_version}
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="%_ldflags"

cd tiff-%{tarball_version}

%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

./configure \
	--prefix=%{_prefix} \
	--libexecdir=%{_libexecdir} \
	--disable-cxx
make -j$CPUS

%ifarch amd64 sparcv9
cd ../tiff-%{tarball_version}-64
export CFLAGS="%optflags64"
./configure \
	--prefix=%{_prefix} \
	--libexecdir=%{_libexecdir}/%{_arch64} \
	--libdir=%{_libdir}/%{_arch64} \
	--disable-cxx
make -j$CPUS
%endif

%install
%ifarch amd64 sparcv9
cd tiff-%{tarball_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd tiff-%{tarball_version}
make install DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

mkdir -p $RPM_BUILD_ROOT%{_mandir}/entities
touch $RPM_BUILD_ROOT%{_mandir}/entities/booktitles.ent
touch $RPM_BUILD_ROOT%{_mandir}/entities/gnomecommon.ent
touch $RPM_BUILD_ROOT%{_mandir}/entities/smancommon.ent
cd $RPM_BUILD_ROOT%{_mandir}/man3tiff
ln -s ../entities/booktitles.ent .
ln -s ../entities/gnomecommon.ent .
ln -s ../entities/smancommon.ent .
rm $RPM_BUILD_ROOT%{_mandir}/entities/booktitles.ent
rm $RPM_BUILD_ROOT%{_mandir}/entities/gnomecommon.ent
rm $RPM_BUILD_ROOT%{_mandir}/entities/smancommon.ent
rmdir $RPM_BUILD_ROOT%{_mandir}/entities
cd -
chmod 0755 $RPM_BUILD_ROOT%{_mandir}/man3tiff
chmod 0755 $RPM_BUILD_ROOT%{_mandir}/man1
chmod 0755 $RPM_BUILD_ROOT%{_mandir}/man3
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libtiff.so.3

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -rf $RPM_BUILD_ROOT%{_prefix}/man

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%attr (0755, root, bin) %{_libdir}/%{_arch64}/lib*.so*
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
%dir %attr(0755, root, bin) %{_mandir}/man3tiff
%{_mandir}/man3tiff/*

%changelog
* Thu Sep  4 2008 - john.fischer@sun.com
- add patch CVE-2008-2327.diff
* Mon Mar 24 2008 - laca@sun.com
- add copyright file
* Thu Apr 26 2007 - laca@sun.com
- add SUNWman dependency, fixes 6511213
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Wed Nov 22 2006 - laca@sun.com
- add patches ormandy.diff and CVE-2006-2193.diff, fixes 6451119
* Fri Sep 01 2006 - matt.keenan@sun.com
- Add new man page tarball
* Fri Jul 28 2006 - laca@sun.com
- bump to 3.8.2
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Apr 06 2006 - brian.cameron@sun.com
- Now use tarball_version.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Dec 19 2005 - damien.carbery@sun.com
- Bump to 3.7.4.
* Thu Sep 22 2005 - laca@sun.com
- make install the 64-bit bits first so the executables in %{_bindir}
  get overwritten by the 32-bit ones and not the other way around.
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Tue Apr 26 2004 - laca@sun.com
- updated to version 3.7.2, fixes CR6203747
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 as the 64-bit C compiler, if defined
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Sun Sep 12 2004 - laca@sun.com
- Added %defattr for devel-share pkg
* Fri Sep 10 2004 - shirley.woo@sun.com
- Added Requires: SUNWTiff for devel and devel-share packages
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : include files and sman3 files should be in a separate devel
  package
* Wed Aug 18 2004 - damien.carbery@sun.com
- Update libtiff.so.3 perms for Solaris integration.
* Tue Aug 17 2004 - shirley.woo@sun.com
- Another Update mandir perms for Solaris integration.
* Tue Aug 17 2004 - damien.carbery@sun.com
- Update mandir perms for Solaris integration.
* Tue Aug 17 2004 - laca@sun.com
- update mandir permissions for Solaris integration
* Fri Aug 13 2004 - damien.carbery@sun.com
- Create symlinks to *.ent in ../entities. Fixes 5085622.
* Thu Aug 12 2004 - shirley.woo@sun.com
- Updated Version to be 2.6.0 since delivering w/ G2.6
* Thu Aug 12 2004 - damien.carbery@sun.com
- Add symlinks to ../entities/*.ent in the sman3tiff dir. Fixes 5085622.
* Sun Feb 23 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
