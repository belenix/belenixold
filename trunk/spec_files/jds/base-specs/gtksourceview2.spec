#
# spec file for package gtksourceview
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: hawklu
#
Name:			gtksourceview
License:		GPL
Group:			System/Libraries
Version:		2.6.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Syntax highlighting text widget
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.6/%{name}-%{version}.tar.bz2
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

gtkdocize
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
intltoolize --force

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif


CFLAGS="$RPM_OPT_FLAGS"				\
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
%{_datadir}/gtksourceview-2.0
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
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.6.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.5.6
* Mon Feb 17 2009 - dave.lin@sun.com
- Bump to 2.5.5.
- Add patch 01-gtkdoc-rebase.diff to fix GTKDOC_REBASE issue.
* Thu Jan 08 2009 - christian.kelly@sun.com
- Bump to 2.5.2.
* Sun Sep 28 2008 - patrick.ale@gmail.com
- Correct download URL

* Sun Sep 21 2008 - christian.kelly@sun.com
- Bump to 2.4.0.

* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.3.3.

* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.3.2.

* Mon Aug 11 2008 - damien.carbery@sun.com
- Bump to 2.3.1.

* Mon Jun 23 2008 - damien.carbery@sun.com
- Bump to 2.2.2.

* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.2.1.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.2.0.

* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.1.3.

* Tue Feb 05 2008 - damien.carbery@sun.com
- Bump to 2.1.2. Remove upstream patch 01-212.

* Mon Feb 04 2008 - damien.carbery@sun.com
- Add patch 01-212 to bump module to 2.1.2 while waiting for tarball release.

* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.1.1.

* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.1.0.

* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.0.2.

* Mon Oct 22 2007 - damien.carbery@sun.com
- Bump to 2.0.1.

* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.0.0.

* Tue Sep 11 2007 - damien.carbery@sun.com
- Bump to 1.90.5.

* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 1.90.4.

* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 1.90.3.

* Wed Jul 04 2007 - damien.carbery@sun.com
- Bump to 1.90.2.

* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 1.90.1.

* Wed May 30 2007 - damien.carbery@sun.com
- Initial spec file.
