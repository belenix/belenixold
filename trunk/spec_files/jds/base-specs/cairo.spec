#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
# bugdb: bugzilla.freedesktop.org
#
Name:         cairo
License:      LGPL
Group:        System/Libraries
Version:      1.8.6
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Vector graphics library
Source:       http://cairographics.org/releases/%{name}-%{version}.tar.gz
#owner:erwannc date:2006-11-02 type:feature 
Patch1:       cairo-02-full-hinting.diff
#owner:erwannc date:2008-10-28 type:bug defect:4187
Patch2:       cairo-03-buggy-repeat.diff
URL:          http://www.cairographics.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Requires:     freetype2
BuildRequires:freetype2-devel
Requires:     fontconfig
BuildRequires:fontconfig-devel
Requires:     SUNWpixman

%description
Cairo is a vector graphics library with cross-device output
support. Currently supported output targets include the X Window
System and in-memory image buffers. Cairo is designed to produce 
identical output on all output media while taking advantage of 
display hardware acceleration when available (eg. through the 
X Render Extension).

Cairo provides a stateful user-level API with capabilities similar to
the PDF 1.4 imaging model. Cairo provides operations including
stroking and filling Bezier cubic splines, transforming and
compositing translucent images, and antialiased text rendering.


%package devel
Summary:      Vector graphics library
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description devel
Cairo is a vector graphics library with cross-device output
support. Currently supported output targets include the X Window
System and in-memory image buffers. Cairo is designed to produce
identical output on all output media while taking advantage of
display hardware acceleration when available (eg. through the
X Render Extension).

Cairo provides a stateful user-level API with capabilities similar to
the PDF 1.4 imaging model. Cairo provides operations including
stroking and filling Bezier cubic splines, transforming and
compositing translucent images, and antialiased text rendering.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PATH=`pwd`:$PATH

aclocal $ACLOCAL_FLAGS -I build
gtkdocize
autoheader
automake -a -c -f
autoconf
%if %option_with_debug
 export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS"
%else
  export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS -DNDEBUG"
%endif

export LDFLAGS="%_ldflags"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --bindir=%{_bindir} \
    %{gtk_doc_option}

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/gtk-doc/*
%{_libdir}/pkgconfig/*

%changelog
* Web Feb 25 2009 - chris.wang@sun.com
- bump to version 1.8.6
* Thu Feb 12 2009 - jedy.wang@sun.com
- Fix broken download link.
* Fri Dec 12 2008 - chris.wang@sun.com
- Add NDEBUG macro in CFLAGS
* Wed Dec 10 2008 - dave.lin@sun.com
- Removed upstreamed patch -uninstalled-pc.diff.
* Mon Dec 08 2008 - dave.lin@sun.com
- Bump to 1.8.4.
* Tue Nov 18 2008 - darren.kenny@sun.com
- Remove unneeded patch cairo-03-no-pixman-dep.diff, since we pixman should
  now be on the system (delivered by X). Renumber remaining patches.
- Add Requires statement for SUNWpixman.
* Wed Aug 13 2008 - damien.carbery@sun.com
- Reenable patch2 (02-full-hinting) because the build machine is on snv_92 or
  greater.
* Tue Aug 12 2008 - damien.carbery@sun.com
- Bump to 1.7.4.
* Fri Jul 11 2008 - damien.carbery@sun.com
- Disable 02-full-hinting patch as build machines use snv_91. freetype fix is
  in snv_92.
* Thu Jul 10 2008 - erwann.chenede@sun.com
- re-enabled cairo-02-full-hinting.diff patch as freetype is fixed now.
* Thu Jun 12 2008 - damien.carbery@sun.com
- Comment out patch2 because of change to Freetype in snv_91 breaks build.
* Sun Apr 20 2008 - damien.carbery@sun.com
- Add -D_POSIX_PTHREAD_SEMANTICS to CFLAGS to fix sparc build (ctime_r error).
* Fri Apr 18 2008 - darren.kenny@sun.com
- Temporarily remove depenency on pixman in pkg-config file since it's
  directly linked into libcairo until pixman is delivered by X.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Revert to 1.4.14 as 1.5.6 requires pixman and this will be delivered by X
  Server group in the future. Remove obsolete patch 05-ctime_r: only an issue in
  1.5.6.
* Thu Jan 17 2008 - patrick.ale@gmail.com
- Someone bumped up to snapshot 1.5.6.
- Changed URL to fetch from snapshot dir rather than releases 
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 1.4.14.
* Tue Nov 27 2007 - brian.cameron@sun.com
- Bump to 1.4.12
* Fri Aug 3  2007 - chris.wang@sun.com
- merge patch cairo-02-8bit-fix.diff and cairo-05-null-struct-pointer.diff, and
  remove cairo-05-null-struct-pointer.diff from repository. revised patch 
  cairo-02-8bit-fix.diff, added code to support 8bit Truecolor. This fixed bug
  6555333, xscreensaver-demo crash when display set to 8 bit.
* Mon Jul 23 2007 - chris.wang@sun.com
- add patch cairo-05-null-struct-pointer.diff which fixed the bug nautilus
  crash when D&D files
* Tue Jul 03 2007 - damien.carbery@sun.com
- Bump to 1.4.10.
* Wed May  9 2007 - elaine.xiong@sun.com
- Removed obsolete buggy_repeat path for Xsun.
* Wed May  2 2007 - brian.cameron@sun.com
- Bump to 1.4.6.
* Sun Apr  1 2007 - laca@sun.com
- add missing aclocal calls
* Thu Mar 15 2007 - laca@sun.com
- convert to new style of building multiple ISAs as per docs/multi-ISA.txt
* Wed Mar 15 2007 - dougs@truemail.co.th
- Changed source URL from snapshots to releases for 1.4.0
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Wed Mar 14 2007 - damien.carbery@sun.com
- Bump to 1.4.0. Remove upstream patch, 04-endian-search. Renumber remainder.
* Fri Feb 16 2007 - brian.cameron@sun.com
- Add mediaLib patch and autoheader call needed for this patch.
* Thu Dec 14 2006 - damien.carbery@sun.com
- Correct url for unstable builds: s/releases/snapshots/.
* Tue Dec 12 2006 - damien.carbery@sun.com
- Readd a patch to fix bug 9124 (called 04-endian-search this time).
* Mon Dec 11 2006 - damien.carbery@sun.com
- Bump to 1.3.6. Remove upstream patch 04-float-word.
* Fri Dec 08 2006 - brian.cameron@sun.com
- Add patch description for 8-bit patch since I noticed the bugzilla bug.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Bump to 1.3.2. Add patch 04-float-word to fix configure issue. Fixes #9124.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Oct 16 2006  brian.cameron@sun.com
- Enable gtk-docs.  This required adding gtkdocize and automake
  before calling configure
* Mon Aug 28 2006  harry.lu@sun.com
- Bumped to 1.2.4.
* Fri Aug 11 2006  damien.carbery@sun.com
- Remove upstream patch, 02-buggyx. Renumber others.
* Fri Aug 11 2006  damien.carbery@sun.com
- Bumped to 1.2.2.
* Thu Jul 20 2006  damien.carbery@sun.com
- Bumped to 1.2.0.
* Wed Jun 14 2006  yandong.yao@sun.com
- Fix bug 6434250: cairo will crash when access 0x0 bitmap image glyph
  Add patch cairo-04-g11n-0x0glyph-fix.diff
* Wed Oct 26 2005  damien.carbery@sun.com
- Bumped to 1.0.2.
* Tue Oct 25 2005  brian.cameron@sun.com
- Add patch 2 to workaround the buggy Xserver shipped with
  Solaris 10.  This fixes the problem that the background
  would not get repainted when you would move an icon, view
  the root menu, etc.  The same workaround is used in the
  code to resolve this problem on other platforms using an
  Xorg server older than 2.8.2 (we use 2.8.0 on Solaris 10).
* Tue Sep 13 2005  brian.cameron@sun.com
- Bumped to 1.0.0
* Fri Aug 26 2005  laca@sun.com
- add 64-bit bits
* Tue Aug 16 2005  laca@sun.com
- add some missing dependencies
* Mon Aug 15 2005  glynn.foster@sun.com
- Bump to 0.9.2
* Mon Feb 28 2004  brian.cameron@sun.com
- Add patch 01 so that we can build libsvg and libsvg-cairo.
* Tue Feb 22 2004  brian.cameron@sun.com
- created
