#
# spec file for package libgksuui
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: lin
#
%include l10n.inc
Name:         libgksuui
License:      LGPL v2
Group:        Applications/Utilities
Version:      1.0.5
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Shows dialogs for asking passwords
Source:       http://people.debian.org/~kov/gksu/old_stuff/libgksuui1.0/libgksuui1.0-%{version}.tar.gz
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Source2:      l10n-configure.sh
# date:2006-10-21 owner:lin type:feature
Patch1:	      libgksuui1.0-01-Makefile.diff
# date:2006-10-21 owner:lin type:feature
Patch2:	      libgksuui1.0-02-GUI-update.diff
# date:2009-04-06 owner:fujiwara type:bug state:upstreamed
Patch3:	      libgksuui1.0-03-build.diff
URL:          http://savannah.nongnu.org/projects/gksu/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf


BuildRequires: gettext, bison, gtk-doc, pkgconfig, gtk2-devel

%description
Libgksuui uses the Gtk+2 library to show the dialog asking for the target
user's password when needed. It is used by gksu.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -n libgksuui1.0-%{version}
sh -x %SOURCE2 --enable-sun-linguas
/bin/rm -f po/stamp-po
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
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

# libtoolize --force
# aclocal $ACLOCAL_FLAGS
autoheader
autoconf
# automake -a -c -f

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
	--disable-scrollkeeper
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
# rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING INSTALL
%{_libdir}/libgksuui*.so.*
%{_datadir}/gtk-doc/html/libgksuui*/
%{_datadir}/libgksuui*/gksu-auth.png
%{_datadir}/locale/*/*/libgksuui*

%files devel
%defattr(-, root, root)
%{_includedir}/*.h
%{_libdir}/libgksuui*.a
%{_libdir}/libgksuui*.so
# %exclude %{_libdir}/*.la
%{_libdir}/pkgconfig/libgksuui*.pc

%changelog
* Mon Apr 06 2009 - takao.fujiwara@sun.com
- Add l10n tarball.
- Add patch build.diff for autoconf
- Update patch GUI-update.diff for SUN_BRANDING.
* Tue Mar 10, 2009 - harry.lu@sun.com
- Change owner to Lin Ma
* Sun Jan 28 2007 - laca@sun.com
- fix download url
* Sat Oct 21 2006 Jim Li <jim.li@sun.com>
- Add patch GUI-update.diff to support accessibility.
* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 1.0.7-1.2
- Rebuild for Fedora Core 5.
* Thu Jan 05 2006 Dries Verachtert <dries@ulyssis.org> - 1.0.7-1
- Initial package.
