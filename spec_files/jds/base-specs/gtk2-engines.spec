#
# spec file for package gtk2-engines
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         gtk2-engines
License:      GPL
Group:        System/GUI/GNOME
Version:      2.18.0
Release:      2
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Engines for GTK2 Themes
Source:       http://ftp.gnome.org/pub/GNOME/sources/gtk-engines/2.18/gtk-engines-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define       gtk2_version 2.4.0

BuildRequires: gtk2-devel >= %{gtk2_version}
Requires:      gtk2 >= %{gtk2_version}

%description
This packages contains Theme-Engine libraries for GTK2

%prep
%setup -q -n gtk-engines-%{version}

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
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --libdir=%{_libdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/gtk-2.0/*/engines/*.so
%{_datadir}/themes/*
%{_libdir}/pkgconfig/*.pc

%changelog -n gtk2-engines
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.18.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.17.4
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.17.3
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.17.1
* Fri Sep 26 2008 - brian.cameron@sun.com
- Bump to 2.16.0.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.15.4.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.15.3
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.15.2. Remove upstream patch 01-remove-cast.
* Thu May 29 2008 - damien.carbery@sun.com
- Add patch, 01-remove-cast, to fix 535456. Removes unnecessary cast.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.15.1.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.14.2.
* Wed Apr 08 2008 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.13.6.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.13.5.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.13.4.
* Mon Jan 07 2007 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.13.2.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.13.1.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.13.0.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.12.2. Removed upstream patch, 01-iconv-solaris.
* Tue Sep 25 2007 - damien.carbery@sun.com
- Bump to 2.12.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.12.0.
* Fri Aug 24 2007 - damien.carbery@sun.com
- Bump to 2.11.7.
* Wed Aug 22 2007 - damien.carbery@sun.com
- Add patch 01-iconv-solaris to fix #467309. Modify intltool-merge.in to allow
  use of non-GNU iconv.
* Mon Aug 20 2007 - damien.carbery@sun.com
- Bump to 2.11.6.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.11.4.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.11.3.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.11.1.
* Fri May 18 2007 - laca@sun.com
- set CFLAGS/LDFLAGS and configure options such that we can use this spec
  file for the 64-bit build too
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.11.0. Remove upstream patch, 01-remove-cast.
* Wed Apr 11 2007 - damien.carbery@sun.com
- Bump to 2.10.1. Add patch 01-remove-cast to remove casts that were breaking
  build. Bugzilla #428772.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.10.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.9.4.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.9.3.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.9.2.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.9.1.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 2.9.0.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.8.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.8.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.7.7.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.7.6.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.7.5. Add patch, 01-hidden, for G_GNUC_INTERNAL.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.7.4.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.7.2
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.7.1. Remove upstream patch, 01-crux-theme-crash.
* Thu Dec 08 2005 - muktha.narayan@wipro.com
- Added patch gtk-engines-01-crux-theme-crash.diff
  to fix the crash when theme is changed from Crux.
  Fixes bug #6359039.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.6.6.
* Sun Sep 18 2005 - glynn.foster@sun.com
- Bump to 2.6.5
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.6.4.
* Sat May 14 2005 - glynn.foster@sun.com
- Update to 2.6.3
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu Feb 26 2004 - michael.twomey@sun.com
- Uprevved release to 230 so there is a clean upgrade from quicksilver.
* Wed Jan 07 2004 - glynn.foster@sun.com
- Remove pixbuf static patch since it's upstream
* Tue Oct 20 2003 - glynn.foster@sun.com
- remove the thinice engine, since it's part of gnome-themes now
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Tue Jul 15 2003 - <markmc@sun.com>
- Make pixbuf_cache static so it doesn't conflict with other
  global symbols of the same name.
* Thu Jul 02 2003 - <glynn.foster@sun.com>
- Make sure that we install the thinice engine
* Tue May 13 2003 - <Stephen.Browne@sun.com>
- initial release
