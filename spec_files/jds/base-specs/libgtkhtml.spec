#
# spec file for package libgtkhtml
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         libgtkhtml
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.11.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Library for HTML support in GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgtkhtml/2.11/libgtkhtml-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/libgtkhtml
Autoreqprov:  on

%define gtk2_version 2.2.4
%define libxml2_version 2.4.23
%define gail_version 1.8.0

Requires: gtk2 >= %{gtk2_version}
Requires: libxml2 >= %{libxml2_version}
Requires: gail >= %{gail_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: gail-devel >= %{gail_version}

%description
libgtkhtml is a library to provide extensions for GTK+ to handle HTML format.

%package devel
Summary:      Development Library for HTML support in GNOME
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     gtk2-devel >= %{gtk2_version}
Requires:     libxml2-devel >= %{libxml2_version}
Requires:     gail-devel >= %{gail_version}

%description devel
libgtkhtml is a library to provide extensions for GTK+ to handle HTML format.

%prep
%setup -q 

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

libtoolize --copy --force
aclocal -I %{_datadir}/aclocal
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"				\
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/%{_libdir}/libgtkhtml-2.a
rm $RPM_BUILD_ROOT/%{_libdir}/libgtkhtml-2.la

#%check
make check

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files 
%defattr(-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gtkhtml-2.0

%changelog
* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.

* Thu Sep 20 2007 - damien.carbery@sun.com
- Bump to 2.11.1.

* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.11.0. Remove upstream patch, 01-keynav-crash.

* Wed Jun 15 2005 - laca@sun.com
- Add patch pkgconfig.diff to add glib-2.0 to the list of dependent modules
- autotoolize

* Wed May 18 2005 - glynn.foster@sun.com
- Bump to 2.6.3

* Wed Mar 23 2005 - vinay.mandyakoppal@wipro.com
- Add patch libgtkhtml-07-keynav-crash.diff fixes the issue of yelp
  crashing with keynav/mouse highlighting. Fixes #6229854.

* Fri Dec 13 2004 - padraig.obriain@sun.com
- Add patch libgtkhtml-06-toggle-cursor.diff for bugzilla #160705.

* Thu Nov 25 2004 - padraig.obriain@sun.com
- Add patch libgtkhtml-05-link-focus.diff for bug #6190671.

* Fri Nov 05 2004 - matt.keenan@sun.com
- Add patch -04-hand-symbol.diff : #5032857

* Thu Nov 04 2004 - padraig.obriain@sun.com
- Add patch libgtkhtml-03-fix-move.diff for bug #6190222.

* Wed Oct 27 2004 - padraig.obriain@sun.com
- Add patch libgtkhtml-02-fix-crash.diff for bug #6185204.

* Fri Jul 23 2004 - padraig.obriain@sun.com
- Add patch libgtkhtml-01-fix-speech.diff for bugzilla #143502

* Mon Jul 12 2004 - stephen.browne@sun.com
- ported to rpm4

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Tue Jun 08 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.6.2

* Thu May 06 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.6.1

* Mon Apr 05 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.6.0

* Thu Mar 18 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.5.6

* Tue Feb 24 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.5.5

* Thu Feb 05 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.5.3

* Tue Dec 16 2003 - <glynn.foster@sun.com>
- Upgrade tarball to 2.5.1

* Tue Oct 14 2003 - <matt.keenan@sun.com>
- Upgrade tarball to 2.4.1 for QS

* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la

* Tue May 13 2003 - matt.keenan@sun.com
- Initial Sun release
