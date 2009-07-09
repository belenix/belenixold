#
# spec file for package gdesklets
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
# bugdb: https://bugs.launchpad.net/gdesklets/+bug/
#
%include l10n.inc
Name:		gdesklets
Version:	0.36.1
Release:        1
License:	GPL
Group:		Applications/Internet
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	System for bringing mini programs (desklets) onto the desktop
Source:         http://gdesklets.de/files/gdesklets-%{version}.tar.gz
%if %build_l10n
Source1:        l10n-configure.sh
Source2:        %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
# date:2007-02-05 owner:bewitche type:feature state:upstream
Patch1:         gdesklets-01-Solaris-support.diff
# date:2007-07-12 owner:bewitche type:feature 
Patch2:		gdesklets-02-session-manager-support.diff
# date:2007-11-21 owner:bewitche type:bug bugid:151880 bugster:6616731
Patch3:		gdesklets-03-starter.diff
# date:2008-05-12 owner:bewitche type:bug bugid:229506 bugster:6699649
Patch5:         gdesklets-05-manpage.diff
# date:2008-08-13 owner:jedy type:branding
Patch6:         gdesklets-06-menu-entry.diff
URL:		http://www.gdesklets.de/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Autoreqprov:	on


%prep
%setup -q -n gDesklets-%version
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1

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

libtoolize --force
intltoolize --copy --force

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS 
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--localstatedir=%{_localstatedir} \
	--disable-scrollkeeper

make -j $CPUS


%install
make DESTDIR=$RPM_BUILD_ROOT install 
rm $RPM_BUILD_ROOT%{_libdir}/gdesklets/utils/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gdesklets/libdesklets/system/*.la

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/gdesklets/*
%{_datadir}/locale/*/*/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/icons/*/*/*/*


%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Mon Apr 27 2009 - chris.wang@sun.com
- bump to 0.36.1 and remove upstreamed patch 04
* Wed Oct 29 2008 - takao.fujiwara@sun.com
- Remove incorrect indiana branding patch 07 #6765066
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Thu Sep 25 2008 - matt.keenan@sun.com
- Indiana branding, hide gdesklets menu option #6752376
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Wed Aug 13 2008 - jedy.wang@sun.com
- Add patch 06-dekstop.diff and reorder pathces.
* Wed Jul 30 2008 - chris.wang@sun.com
- Add patch gdesklets-06-manpage.diff to add ARC number and Attributes 
  to manpage
* Mon Jul 21 2008 - chris.wang@sun.com
- update bugdb to launchpad
* Fri Jul 11 2008 - chris.wang@sun.com
- Update orange bug status
* Mon May 12 2008 - chris.wang@sun.com
- added patch gdesklets-05-shift-f10.diff to fix bug 6699649, gdesklets 
  trayicon support shift-f10
* Mon May 12 2008 - chris.wang@sun.com
- Bump version to 0.36
* Wed Nov 22 2007 - chris.wang@sun.com
- Updated to build with new released gdesklets 0.36beta version
- Removed patch 3,4,5,6,7,9, which have been upstreamed and put into 0.36 beta
- Reorder patch gdesklets-08-session-manger-support.diff to 
  gdesklets-03-session-manager.diff due to removed patches
- Revised patch 1,2,3 due to the code change in 0.36beta
- Add patch gdesklets-04-starter.diff which fixed bugster bug 6616731
  gdesklets daemon trayicon menu don't pop-up if user put some desklets
  on the desktop
* Tue Aug 21 2007 - chris.wang@sun.com
- Add patch gdesklets-09-statusicon.diff which fixes bugster bug
  6575986 gdesklets crash on startup in gnome 2.19. This patch is
  from community, since gnome has statusicon since 2.10, they are 
  using it to replace eggicon.  
* Thu Jul 12 2007 - chris.wang@sun.com
- Add patch that fixed the gdesklets is not session aware
* Mon Apr 09 2007 - chris.wang@sun.com
- Add patch that can get proxy setting from gconf
* Mon Mar 12 2007 - laca@sun.com
- delete .la files
* Fri Feb 16 2007 - damien.carbery@sun.com
- Bump to 0.35.4. Update URL to gdesklets.de.
* Fri Feb 16 2007 - chris.wang@sun.com
- Add patch -06-tar, to solve the problem that the tar bundled with Solaris
  don't support -j and -z options.
* Thu Feb 15 2007 - chris.wang@sun.com
- Update the state of current patch
* Thu Feb 15 2007 - chris.wang@sun.com
- Add patch -05-performance, optimize the performance of gdesklets on Solaris
* Mon Feb 12 2007 - chris.wang@sun.com
- Add patch -03-number-of-cpu, to solve the problem that the number of cpu info cannot be
  retrieve correctly on Sparc bug:406957
*Mon Feb 12 2007 - chris.wang@sun.com
- Add patch -04-parse-args, to correct the args cannot be parsed correctly on 
  Sparc box  bug:406961
* Tue Feb  6 2007 - damien.carbery@sun.com
- Add patch, 02-rel-symlinks, to change absolute symlinks to relative. #405100.
* Mon Feb  5 2007 - damien.carbery@sun.com
- Remove the unnecessary reference to LD_LIBRARY_PATH.
* Thu Jan 29 2007 - <chris.wang@sun.com>
- initial creation
