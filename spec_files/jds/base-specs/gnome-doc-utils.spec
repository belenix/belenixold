#
# spec file for package gnome-doc-utils
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			gnome-doc-utils
License:		GPL
Group:			System/Libraries
Version:		0.16.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Documentation utilities for GNOME
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.16/%{name}-%{version}.tar.bz2
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

%define libxml2_version 2.6.12
%define libxslt_version 1.1.8

Requires:	libxml2 >= %{libxml2_version}
Requires:	libxslt >= %{libxslt_version}

BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:	libxslt-devel >= %{libxslt_version}

%description
This package contains a selection of utilities for managing documents 
in the GNOME desktop.

The xml2po program is used to convert between PO files and XML documents.
Within gnome-doc-utils, it is used primarily to translate documentation
written in the DocBook format. 

The gnome-doc-prepare script is used to initialize your source tree for 
using the gnome-doc-utils build utilities.  It can also be used to 
create a template document and the necessary supporting files and folders.

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

./configure $MYARCH_FLAGS \
        --prefix=%{_prefix} \
        --datadir=%{_datadir} \
        --sysconfdir=%{_sysconfdir} \
	--localstatedir=%{_localstatedir}/lib \
        --mandir=%{_mandir} \
	--disable-scrollkeeper

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/gnome-doc-prepare
%{_bindir}/xml2po
%{_libdir}/pkgconfig/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*
%{_datadir}/gnome-doc-utils/*
%{_datadir}/gnome/help/*
%{_datadir}/omf/*
%{_datadir}/xml/*
%{_datadir}/xml2po/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 0.16.0
* Mon Mar 02 2009 - dave.lin@sun.com
- Bump to 0.15.2
* Fri Feb 06 2009 - christian.kelly@sun.com
- Bump to 0.15.1.
* Tue Aug 09 2008 - patrick.ale@gmail.com
- Correct download URL

* Thu Aug 29 2008 - dave.lin@sun.com
- Bump to 0.13.1
- Remove the unsupported configure option --localedir
* Sun Mar 16 2008 - damien.carbery@sun.com
- Add hack back in to get build going again. Will split 'glib' out of
  SUNWgnome-base-specs.spec at a later date.
* Fri Mar 14 2008 - damien.carbery@sun.com
- Call aclocal/automake/autoconf to install locale files into correct dir.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Specify --datadir and --localedir to correct install dir of locale files.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 0.12.2.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 0.12.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Remove the --host parameter from configure because it breaks the build.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 0.12.0.
* Thu Aug 23 2007 - laca@sun.com
- delete patch 01-gettext
- use DESTDIR in %install
- don't autotoolize
- add --mandir and --host options
* Mon Aug 20 2007 - damien.carbery@sun.com
- Add patch 01-gettext to fix 6329710. Add appropriate autofoo. Remove moving
  of manpage dir as it is not installed under %{_prefix}/man.
* Mon Aug 20 2007 - damien.carbery@sun.com
- Bump to 0.11.2.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 0.11.1.
* Tue Apr 10 2007 - damien.carbery@sun.com
- Bump to 0.10.3. Remove upstream patch 01-nawk-w.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 0.10.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 0.10.0.
* Wed Feb 28 2007 - halton.huo@sun.com
- Fix source url error.
- Remove old comments about upgarde from 0.8.x to 0.9.x 
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 0.9.2. Add patch, 01-nawk-w, to remove '-W compat' switch that breaks
  on Solaris.
* Fri Jan 26 2007 - damien.carbery@sun.com
- Bump to 0.9.1, but, because it doesn't build, leave at 0.8.0.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 0.8.0.
* Tue Aug 08 2006 - brian.cameron@sun.com
- Bump to 0.7.2.
* Wed Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 0.7.1.
* Mon Jul 10 2006 - brian.cameron@sun.com
- Bump to 0.6.1.
* Sun Mar 12 2006 - damien.carbery@sun.com
- Bump to 0.6.0.
* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 0.5.7.
* Sun Feb 19 2006 - damien.carbery@sun.com
- Bump to 0.5.6.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 0.5.5.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 0.5.4.
* Thu Dec 22 2005 - damien.carbery@sun.com
- Bump to 0.5.2.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 0.4.4.
* Wed Oct 26 2005 - damien.carbery@sun.com
- Bump to 0.4.3.
* Thu Sep 29 2005 - brian.cameron@sunc.om
- Bump to 0.4.2.
* Thu Sep 08 2005 - brian.cameron@sun.com
- Bump to 0.4.1 since this contains some fixes that cause things
  to break for Solaris in 0.4.0. 
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.3.2.
* Thu Jun 09 2005 - matt.keenan@sun.com
- Update so that builds
* Wed May 18 2005 - glynn.foster@sun.com
- Initial spec of gnome-doc-utils
