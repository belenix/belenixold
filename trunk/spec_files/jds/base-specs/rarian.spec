#
# spec file for package rarian
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
# bugdb: bugzilla.freedesktop.org
#
Name:         rarian
License:      GPL
Group:        System/GUI/GNOME
Version:      0.8.1
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Documentation meta-data library
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.8/%{name}-%{version}.tar.bz2
#owner:gheet date:2008-02-20 type:bug bugzilla:11839 bugster:6639279
Patch1:       rarian-01-fix-sk-update.diff
#owner:gheet date:2008-09-03 type:bug bugzilla:17420 bugster:6646976
Patch2:       rarian-02-input-para.diff
#owner:mattman date:2008-10-02 type:bug bugzilla:17876 bugster:6702290
Patch3:       rarian-03-yelp-performance.diff
URL:          www.freedesktop.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on

%description
Rarian (formerly Spoon) is a documentation meta-data library, designed as a
replacement for Scrollkeeper.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1


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

#libtoolize --force
#glib-gettextize -f
#intltoolize --force --copy
#aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f
#autoconf

./configure \
    --prefix=%{_prefix} \
    --datadir=%{_datadir}       \
    --libexecdir=%{_libexecdir} \
    --localstatedir=/var        \
    --disable-skdb-update
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/librarian.*a

#%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Oct 02 2008 - matt.keenan@sun.com
- Fix bugster:6702290, yelp performance issue

* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 0.8.1.

* Wed Sep 03 2008 - ghee.teo@sun.com
- Added patch rarian-02-input-para.dif to fix 6646976.

* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 0.8.0.

* Thu Feb 21 2008 - ghee.teo@sun.com
- Added --disable-skdb-update to build successful for the patch
  rarian-02-fix-sk-update.diff.

* Wed Feb 20 2008 - ghee.teo@sun.com
- Added patch rarian-02-fix-sk-update.diff
* Tue Jan 08 2002 - damien.carbery@sun.com
- Bump to 0.7.1.

* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 0.7.0. Remove upstream patch 01-reg-return.

* Tue Oct 16 2007 - matt.keenan@sun.com
- Add patch 01-reg-return to fix 12279 crash bug.

* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 0.6.0. Remove upstream patches, 01-pc-newline and 02-memory-wua.

* Fri Aug 17 2007 - damien.carbery@sun.com
- Add patch 01-pc-newline to fix #12043, to add a newline to rarian.pc.in as
  the last line is lost during processing (a sed bug?).

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 0.5.8. Remove upstream patch, 01-solaris-build.

* Wed Aug 01 2007 - damien.carbery@sun.com
- Initial version.
