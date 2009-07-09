#
# spec file for package intltool 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			intltool 
License:		GPL
Group:			Development/Tools/Other 
BuildArchitectures:	noarch
Version:		0.40.6
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Translation Tools for GNOME Internationalization
Source:			http://ftp.gnome.org/pub/GNOME/sources/intltool/0.40/intltool-%{version}.tar.bz2
# owner:laca date:2007-12-18 bugzilla:490845 type:bug
Patch1:                 intltool-01-msgfmt.diff
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir: 		%{_defaultdocdir}/doc
Autoreqprov:		on

%description
intltool is a collection of tools for the GNOME Internationalization Developer
Framework. Data available in XML files (.oaf, .desktop, .sheet, etc.) can be 
extracted into PO files and, after translating, the new info will be written back
into the XML files.

%define INSTALL install -m755 -s
%define INSTALL_SCRIPT install -m755
%define INSTALL_DIR install -d -m755
%define INSTALL_DATA install -m644

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

./configure --prefix=%{_prefix} 	\
	    --mandir=%{_mandir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%defattr(0555, root, root)
%{_prefix}/bin
%defattr (0444, root, root)
%{_mandir}/man1/*
%{_mandir}/man8/*
%defattr(0755,root,root) 
%{_datadir}/%{name}
%{_datadir}/aclocal/

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 0.40.6
* Mon Dec 15 2008 - dave.lin@sun.com
- Bump to 0.40.5.
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 0.40.4.
* Fri Aug 01 2008 - christian.kelly@sun.com
- Bump to 0.40.3.
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 0.40.1.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 0.40.0.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 0.37.1.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 0.37.0.
* Tue Dec 18 2007 - laca@sun.com
- add patch msgfmt.diff: do not verify if msgfmt is GNU
* Mon Dec 17 2007 - laca@sun.com
- bump to 0.36.3 and remove upstream patch
* Mon Dec 03 2007 - takao.fujiwara@sun.com
- Add intltool-01-g11n-merge-linugas.diff to read LINGUAS file correctly.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 0.36.2. Remove upstream patch, 01-path-check.
* Wed Aug 29 2007 - damien.carbery@sun.com
- Remove upstream patch, 01-g11n-path-failure; add patch 01-path-check to fix
  464846.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 0.36.1.
* Sat Aug 04 2007 - damien.carbery@sun.com
- Unbump back to 0.35.5 and add 01-g11n-path-failure patch as 0.36.0 is
  breaking other modules.
* Fri Aug 03 2007 - damien.carbery@sun.com
- Bump to 0.36.0. Remove upstream patch, 01-g11n-path-failure.
* Thu Apr 12 2007 - takao.fujiwara@sun.com
- Add intltool-01-g11n-path-failure.diff to work intltool-update. bugzilla
  #413461.
* Tue Feb 27 2007 - brian.cameron@sun.com
- Bump to 0.35.5.  Remove upstream patch.
* Fri Jan 12 2007 - takao.fujiwara@sun.com
- Added intltool-01-g11n-desktop-comment.diff to extract comment. bugzilla
  390271.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 0.35.4.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 0.35.3.
* Thu Dec 21 2006 - damien.carbery@sun.com
- Bump to 0.35.2.
* Thu Dec  7 2006 - damien.carbery@sun.com
- Bump to 0.35.1. Remove upstream patches, 01-intltoolize-exit-1 and 
  02-ALL_LINGUAS.
* Thu Jul 13 2006 - laca@sun.com
- add patch ALL_LINGUAS.diff that removes the \n's from ALL_LINGUAS in
  IT_PROG_INTLTOOL
* Wed Jul 12 2006 - laca@sun.com
- bump to 0.35.0
* Wed Feb  8 2006 - damien.carbery@sun.com
- Bump to 0.34.2.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.34.1.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 0.33
* Fri Nov 05 2004 - takao.fujiwara@sun.com
- Added intltool-01-g11n-icon.diff to support .icon files. Fix CR 6191220
- Added intltool-02-g11n-space.diff to fix space attributes. bugzilla 151017.
* Thu Oct 21 2004 - alvaro.lopez@sun.com
- Updated "Source" to current version.
* Thu Oct 21 2004 - matt.keenan@sun.com
- Bump to 0.31, remove patch-01 , #6179699
* Wed Jul 07 2004 - niall.power@sun.com
- Ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue Mar 16 2004 - takao.fujiwara@sun.com
- Added intltool-01-g11n-handle-blacket.diff to fix 4996253
* Thu Feb 05 2004 - Matt Keenan <matt.keenan@sun.com>
- Bump to 0.30
* Mon Dec 15 2003 - Glynn Foster <glynn.foster@sun.com>
- Bump to 0.28
* Mon Oct 13 2003 - Matt Keenan  <matt.keenan@sun.com>
- Man pages update
* Thu Oct 09 2003 - Matt Keenan  <matt.keenan@sun.com>
- Man pages
* Fri Jul 04 2003 - Ghee Teo  <ghee.teo@sun.com>
- Fixes a directory permission for %{_datadir}/aclocal because of
  an incorrect macros being used under files section
* Tue May 13 2003 - Laszlo.Kovacs@Sun.COM
- Initial release
