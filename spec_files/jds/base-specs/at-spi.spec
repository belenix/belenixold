#
# spec file for package at-spi
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#

Name:         at-spi
License:      LGPL v2
Group:        System/Libraries
Version:      1.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Assistive Technology Service Provider Interface
Source:       http://ftp.gnome.org/pub/GNOME/sources/at-spi/1.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:          http://developer.gnome.org/projects/gap/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:	      /sbin/ldconfig

%define gtk2_version 2.4.0
%define libbonobo_version 2.6.0
%define atk_version 1.7.2
%define gail_version 1.6.3

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: gail-devel >= %{gail_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      libbonobo >= %{libbonobo_version}
Requires:      gail >= %{gail_version}

%{?!pythonver:%define pythonver 2.4}

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package devel
Summary:	Assistive Technology Service Provider Developer Interface
Group:		Development/Libraries/GNOME
Requires:	%{name} = %{version}
Requires:       libbonobo-devel >= %{libbonobo_version}
Requires:       atk-devel >= %{atk_version}

%description devel
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

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

intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

export PYTHON=/usr/bin/python%{pythonver}

libtoolize -f
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
CFLAGS="%optflags"
LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --bindir=%{_bindir}			\
            --sysconfdir=%{_sysconfdir}		\
	    --mandir=%{_mandir}			\
	    --libexecdir=%{_libexecdir}		\
	    --enable-xevie=no			\
	    %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Move to vendor-packages
if [ -x $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages ]; then
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
rm -rf $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/*
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libspi*.so.*
%{_libdir}/libcspi*.so.*
%{_libdir}/libloginhelper*.so.*
%{_libdir}/gtk-2.0/modules/*.so
%{_libdir}/bonobo/servers/*.server
%{_libdir}/orbit-2.0/*.so
%{_libexecdir}/at-spi-registryd
%{_datadir}/locale/*

%files devel
%defattr(-, root, root)
%{_includedir}/at-spi-1.0/cspi/*.h
%{_includedir}/at-spi-1.0/libspi/*.h
%{_includedir}/at-spi-1.0/login-helper/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html
%{_datadir}/idl
%{_libdir}/libspi*.so
%{_libdir}/libcspi*.so
%{_libdir}/libloginhelper*.so
%{_mandir}/man3/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 1.26.0
* Fri Mar 06 2009 - li.yuan@sun.com
- Bump to 1.25.92.
* Fri Feb 27 2009 - li.yuan@sun.com
- Add support for multi versions of python.
* Fri Feb 06 2009 - li.yuan@sun.com
- Install pyatspi in vendor-packages.
* Thu Feb 05 2009 - li.yuan@sun.com
- Disable xevie. Bug 6801596.
* Thu Jan 22 2009 - li.yuan@sun.com
- Bump to 1.25.5. Removed at-spi-01-build.diff.
* Thu Jan 08 2009 - li.yuan@sun.com
- Bump to 1.25.4. Added at-spi-01-build.diff.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 1.25.2
* Wed Nov 05 2008 - li.yuan@sun.com
- Change copyright information.
* Mon Sep 29 2008 - christian.kelly@sun.com
- Take out mv site-packages to vendor-packages.
* Sun Sep 28 2008 - patrick.ale@gmail.com
- Correct download URL
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 1.24.0.
* Thu Sep 11 2008 - christian.kelly@sun.com
- Bump to 1.23.92, add libtoolize -f to fix build issue.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 1.23.91.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 1.23.6.
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 1.23.5. Remove upstream patch 01-uninstalled.
* Wed Jul 09 2008 - damien.carbery@sun.com
- Add patch 01-uninstalled to fix bugzilla #542217.
* Mon Jul 07 2008 - li.yuan@sun.com
- Fix 6697334. Add 64 bit libraries support.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 1.23.3.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 1.22.0.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 1.21.92.
* Mon Jan 14 2008 - damien.carbery@sun.com
- Bump to 1.21.5.
* Thu Jan 10 2008 - li.yuan@sun.com
- change owner to liyuan.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 1.21.3.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 1.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 1.20.1.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Move files from site-packages to vendor-packages. Fixes 6615442.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.20.0.
* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 1.19.5.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 1.19.3.
* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 1.19.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 1.18.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 1.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 1.17.2.
* Wed Feb 28 2007 - li.yuan@sun.com
- Remove upstream patch, at-spi-01-get-attributes-crash.diff
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 1.17.0.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 1.7.16.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 1.7.15.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 1.7.14. Remove upstream patch, at-spi-01-fix-leak.diff.
* Fri Dec 08 2006 - damien.carbery@sun.com
- Bump to 1.7.13.
* Fri Nov 10 2006 - padraig.obriain@sun.com
- Remove patch 01-define-symbols.diff; move patch 02-fix-leak.diff to
  01-fix-leak.diff
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Wed Oct 11 2006 - padraig.obriain@sun.com
- Add patch 02-fix-leak to fix bug 6457388
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 1.7.12.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 1.7.11.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 1.7.10.
* Wed Jul 19 2006 - dermot.mccluskey@sun.com
- Bump to 1.7.9
* Mon Apr 01 2006 - padraig.obriain@sun.com
- Add patch 01-define-symbols so that gok builds.
* Fri Mar 31 2006 - damien.carbery@sun.com
- Bump to 1.7.7.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 1.7.6.
* Thu Feb 23 2006 - damien.carbery@sun.com
- Remove 'make clean' hack as 1.7.5 tarball fixed the issue.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 1.7.5.
* Thu Feb 16 2006 - brian.cameron@sun.com
- Add "make clean" hack to ensure that the bonobo
  registry server file is built with the right
  sysconfdir.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 1.7.4.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 1.7.3.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 1.7.2.
* Thu Sep 08 2005 - damien.carbery@sun.com
- Bump to 1.6.6.
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 1.6.5.
* Tue Aug 23 2005 - damien.carbery@sun.com
- Move CFLAGS setting as it was useless in original location.
* Tue Jun 14 2005 - brian.cameron@sun.com
- Added aclocal/automake/autoconf, needed for Solaris build.
* Mon May 16 2005 - balamurali.viswanathan@wipro.com
- Bump to 1.6.4 
* Mon May 16 2005 - balamurali.viswanathan@wipro.com
- Bump to 1.6.3 
* Tue Apr 5 2005 - bill.haneman@sun.com
- Added patch at-spi-01-leakfix.diff to fix leak in bounds-change events.
* Thu Dec 9 2004 - bill.haneman@sun.com
- Revved to 1.6.2, to get fixes for 6192693, 6205004, others.
* Wed Sep 1 2004 - bill.haneman@sun.com
- Bumped to version 1.5.4, to include fixes for 
- activation issues with DISPLAY env, and gnopernicus
- dependencies.
* Tue Aug 31 2004 - bill.haneman@sun.com
- Removed patch since #5088625 has been fixed, and
- the patch is incompatible with the fix.
* Wed Aug 18 2004 - bill.haneman@sun.com
- added patch from Padraig to work around P1/S2 bug #5088625.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - dermot.mccluskey@sun.com
- add login-helper headers and lib to %files
* Wed Jun 02 2004 - <padraig.obriain@sun.com>
- Bump version to 1.5.2
* Fri Apr 30 2004 - <padraig.obriain@sun.com>
- Bump version to 1.5.1
* Tue Mar 23 2004 - <brian.cameron@sun.com>
- Remove "patch -p1" from the %prep section since
  the patch was removed, and this is causing an
  error on Solaris build.
* Tue Mar 23 2004 - <padraig.obriain@sun.com>
- Bump version to 1.4.0, remove reference to 
  at-spi-01-uninstalled-idldir.diff
* Mon Mar 22 2004 - <laca@sun.com>
- backport idldir fix in uninstalled.pc files from HEAD
* Tue Mar 16 2004 - <glynn.foster@sun.com>
- Remove the uninstalled-pc patch as it's 
  upstream now.
* Thu Mar 11 2004 - <damien.carbery@sun.com>
- Reset release to 1.
* Wed Mar 10 2004 - <damien.carbery@sun.com>
- Bump to 1.3.15
* Mon Feb 23 2004 - damien.carbery@sun.com
- Add '--libexecdir=%{_libexecdir}' to install files to correct dir on Solaris.
* Wed Feb 18 2004 - matt.keenan@sun.com
- tarball upgrade to 1.3.12, add manpages, update %files
* Wed Dec 16 2003 - glynn.foster@sun.com
- tarball upgrade to 1.3.9
* Fri Oct 10 2003 - Laszlo.Kovacs@sun.com
- tarball upgrade
* Thu Aug 14 2003 - <laca@sun.com>
- move *.so to -devel, remove *.a and *.al
* Thu May 08 2003 - ghee.teo@Sun.COM
- Created new spec file for at-spi
