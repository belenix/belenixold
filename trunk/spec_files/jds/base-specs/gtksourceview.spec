#
# spec file for package gtksourceview
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: hawklu
#
Name:			gtksourceview
License:		GPL
Group:			System/Libraries
Version:		1.8.5
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Syntax highlighting text widget
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.8/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:			http://www.gnome.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define libxml_version 2.5.0
%define gtk2_version 2.2.0
%define libgnomeprint_version 2.2.0
%define gnome_vfs_version 2.2.0

BuildRequires: gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeprint-devel >= %{libgnomeprint_version}
BuildRequires: libxml2-devel >= %{libxml_version}
BuildRequires: libgnomeprintui
Requires: gnome-vfs >= %{gnome_vfs_version}
Requires: gtk2 >= %{gtk2_version}
Requires: libgnomeprint >= %{libgnomeprint_version}
Requires: libxml2 >= %{libxml_version}
Requires: libgnomeprintui

%description
GtkSourceView is a text widget that extends the standard gtk+ 2.x text widget
GtkTextView.
 
It improves GtkTextView by implementing syntax highlighting and other features
typical of a source editor.

%package devel
Summary:		gtksourceview development files
Group:			Development/Libraries/X11
Requires:		%{name} = %{version}

%description devel
Development files for gtksourceview

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

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
intltoolize --force

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif


export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lgailutil"
./configure --prefix=%{_prefix}			\
	    --datadir=%{_datadir}       	\
	    --sysconfdir=%{_sysconfdir}		\
	    %{gtk_doc_option}
./config.status
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog MAINTAINERS NEWS README TODO
%{_libdir}/*.so.*
%{_datadir}/gtksourceview-1.0
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/gtk-doc/html/gtksourceview

%files devel
%defattr(-,root,root)
%{_includedir}/gtksourceview-*
%{_libdir}/pkgconfig
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man3/*

%changelog
* Wed Jun 04 2008 - damien.carbery@sun.com
- Add "-lgailutil" to LIBS so that libgailutil is linked in when libgnomecanvas
  is linked. libgnomecanvas.so includes some gail functions.
* Wed May 30 2007 - damien.carbery@sun.com
- Unbump from 1.90.0 to 1.8.5. Version 1.90.0 is a move toward version 2.0
  which is incompatible with 1.x. This breaks gedit and gnome-python-desktop.
  There is a new module forthcoming, pygtksourceview, which will help. See
  bugzilla bugs 442283 and 442272.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 1.90.0.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 1.8.5.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 1.8.4.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 1.8.3.
* Wed Dec 13 2006 - damien.carbery@sun.com
- Bump to 1.8.2.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 1.8.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 1.8.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 1.7.2.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 1.6.1.
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 1.6.1.
* Sun Mar 12 2006 - damien.carbery@sun.com
- Bump to 1.6.0.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 1.5.6
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 1.5.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 1.5.2
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 1.3.93.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 1.3.91.
* Thu May 19 2005 - brian.cameron@sun.com
- Add aclocal and automake, needed for Solaris.
* Wed Jan 12 2005 - takao.fujiwara@sun.com
- Added gtksourceview-01-g11n-ai.diff for autoindent with localized chars
  Fixed 4937266
* Fri Dec 12 2004 - vinay.mandyakoppal@wipro.com
- Replacing the gtksourceview-02-gedit-undo-sun-keyboard.diff
  patch with the one eventually got into cvs head.
* Tue Nov 09 2004 - hidetoshi.tajima@sun.com
- Removed gtksourceview-01-g11n-ai.diff that causes #6191240, gedit hangs when
  typing RETURN key.
* Sat Oct 30 2004 - vinay.mandyakoppal@wipro.com
- Added gtksourceview-02-gedit-undo-sun-keyboard.diff to make undo key in
  sun keyboard work for gedit application. Fixes bug #6178291.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add libgtksourceview-1.0.3 man page
* Tue Oct 05 2004 - takao.fujiwara@sun.com
- Added gtksourceview-01-g11n-ai.diff for autoindent with localized chars
  Fixed 4937266
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc
* Tue Jul 20 2004 - glynn.foster@sun.com
- Bump to 1.0.1
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gtksourceview-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gtksourceview-l10n-po-1.1.tar.bz2
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gtksourceview-l10n-po-1.0.tar.bz2 l10n content
* Mon Feb 23 2004 - <matt.keenan@sun.com>
- Bump to 0.9.0 tarball, update %files
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- Add dependency on libgnomeprintui
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 0.7.0 tarball
* Tue Oct 21 2003 - <michael.twomey@sun.com> 0.6.0-2
- Fixed missing Requires and BuildRequires, comments
  and license.
* Mon Oct 20 2003 - <michael.twomey@sun.com> 0.6.0-1
- Initial spec file.

