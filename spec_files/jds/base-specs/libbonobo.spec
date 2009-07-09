#
# spec file for package libbonobo
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         libbonobo
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.24.1
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Bonobo Base Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/libbonobo/2.24/libbonobo-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
#owner:padraig date:2006-10-06 type:bug bugster:6472900 bugzilla:359617
Patch1:       libbonobo-01-close-down.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_prefix}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define ORBit2_version 2.10.1
%define libxml2_version 2.6.7
%define gnome_common_version 2.4.0
%define pkgconfig_version 0.15.0
%define bonobo_activation_version 2.4.0
%define gtk_doc_version 1.1
%define glib2_version 2.3.2

Requires:      glib2 >= %{glib2_version}
Requires:      libxml2 >= %{libxml2_version}
Requires:      ORBit2 >= %{ORBit2_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: ORBit2-devel >= %{ORBit2_version}
BuildRequires: gnome-common >= %{gnome_common_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}

Obsoletes:	bonobo-activation < %{bonobo_activation_version}
Provides:	bonobo-activation = %{bonobo_activation_version}

%description
libbonobo is one of the base libraries for the GNOME Desktop, containing
convenient API for writing reusable components.

%package devel
Summary:      Bonobo Base Development Library
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}-%{release}
Requires:     glib2-devel >= %{glib2_version}
Requires:     pkgconfig >= %{pkgconfig_version}
Requires:     libxml2-devel >= %{libxml2_version}
Requires:     ORBit2-devel >= %{ORBit2_version}

Obsoletes:	bonobo-activation-devel < %{bonobo_activation_version}
Provides:	bonobo-activation-devel = %{bonobo_activation_version}

%description devel
libbonobo is one of the base libraries for the GNOME Desktop, containing
convenient API for writing reusable components.

%prep
%setup -q
%patch1 -p1

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

intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
libtoolize --force --copy
gtkdocize
autoheader
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --datadir=%{_datadir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir}	\
	    %{gtk_doc_option}

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/bonobo/monikers/*.a
rm $RPM_BUILD_ROOT%{_libdir}/bonobo/monikers/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.a
rm $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc COPYING ChangeLog NEWS README
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_libdir}/lib*.so*
%{_libdir}/orbit-2.0/*.so
%{_libdir}/bonobo/servers/*.server
%{_libdir}/bonobo/monikers/*.so
%dir %{_sysconfdir}/bonobo-activation
%config %{_sysconfdir}/bonobo-activation/*
%{_datadir}/man/man*/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-, root, root)
%{_includedir}/libbonobo-2.0/libbonobo.h
%{_includedir}/libbonobo-2.0/bonobo/*.h
%{_includedir}/bonobo-activation-2.0/bonobo-activation/*.h
%{_libdir}/bonobo-2.0/samples/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/idl/bonobo-2.0/*.idl
%{_datadir}/idl/bonobo-activation-2.0/*.idl
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.24.1
* Mon Sep 29 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.1
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.0.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.20.4. Remove upstream patch 02-fixcompile.
* Thu Jan 03 2008 - Brian.Cameron@sun.com
- Damien backed libbonobo back to 2.20.2 due to a build problem.  I
  fixed this with the libbonobo-02-fixcompile.diff patch, and Bump
  back to 2.20.3.
* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 2.20.3.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.20.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize calls to update intltool scripts.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Thu Mar 08 2007 - damien.carbery@sun.com
- Remove unnecessary patch, 02-popt. Renumber rest.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Wed Jan 24 2007 - damien.carbery@sun.com
- Add more autofoo because autoconf 2.61 used by maintainer, CBE has 2.60.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Fri Oct 06 2006 - padraig.obriain@sun.com
- Add patch libbonobo-03-close-down.diff to fix bug 6472900.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Mon Aug 14 2006 - damien.carbery@sun.com
- Bump to 2.15.3.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.2.
* Web Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.0.
  Delete patch 03 (upstream).
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Mar  7 2006 - damien.carbery@sun.com
- Bump to 2.13.93.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Remove patch, 04-undo-1.27, as issue is gone.
* Fri Feb  3 2006 - damien.carbery@sun.com
- Add patch, 03-add-newline, to fix .server.in.in so sed doesn't complain.
- Add patch, 04-undo-1.27, to undo commit to try fix libbonobo runtime issue.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.1
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 2.13.0. Remove upstream patch (01-forte).
* Thu Sep 15 2005 - brian.cameron@sun.com
- Added libbonobo-03-gthread.diff because building with uninstalled pc
  was causing the gthread configure test to fail.  
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.10.1.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.10.0.
* Wed Jun 29 2005 - balamurali.viswanathan@wipro.com
- Include popt in the .pc file
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.8.1
* Fri Feb 25 2005 - muktha.narayan@wipro.com
- Remove patch libbonobo-03-accessibility-support.diff since
  jdshelp does not come up when accessibility is on.
* Tue Feb 15 2005 - arvind.samptur@wipro.com
- Add patch to fix dhcp hostname change blocking
  login
* Wed Feb 09 2005 - vijaykumar.patwari@wipro.com
- Added libbonobo-03-accessibility-support.diff
  patch to set accessibility support.
* Mon Nov 29 2004 - vinay.mandyakoppal@wipro.com
- Remove patch libbonobo-03-change-of-hostname.diff. 
  It does not fix the scenario reported by user.
* Fri Nov 26 2004 - vinay.mandyakoppal@wipro.com
- Added patch libbonobo-03-change-of-hostname.diff to prevent hosing of
  system after changing hostname. Fixes #6193930.
* Sun Nov 14 2004 - laca@sun.com
- remove CPUS=$((CPUS*4)) because it seems to cause random build failures
  on multicpu systems (probably missing deps in some makefiles)
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add bonobo-slay.1, libbonobo-activation.3 man pages
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Tue Jul 27 2004 - arvind.samptur@wipro.com
- Add patch from  antonio.xu@sun.com to fix b-a-s
  quit on logout after evolution was run in the session
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libbonobo-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu May 27 2004 - arvind.samptur@wipro.com
- Update to 2.6.1 tarball, rework patch 01-forte
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libbonobo-l10n-po-1.1.tar.bz2
* Tue Apr 6 2004 - glynn.foster@sun.com
- Bump to 2.6.0
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libbonobo-l10n-po-1.0.tar.bz2
* Mon Mar 01 2004 - <niall.power@sun.com>
- define libexecdir in configure args
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Update to 2.5.4 tarball, remove patch 01-environ.diff
  Rename patch 02-forte -> 01-forte
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Update to 2.5.1 tarball
* Tue Oct 07 2003 - <markmc@sun.com> 2.4.0-1
- Update to 2.4.0. bonobo-activation has now been swallowed
  into this package.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Fri Aug 01 2003 - <markmc@sun.com> 2.2.3-1
- Update to 2.2.3
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Wed Apr 30 2003 - <niall.power@sun.com>
- Create new spec file for libbonobo
