#
# spec file for package libgnomeprintui
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         libgnomeprintui
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.18.4
Release:      1 
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Print User Interface Library for the GNOME Desktop
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgnomeprintui/2.18/libgnomeprintui-%{version}.tar.bz2
# owner:gheet date:2006-04-23 type:bug bugster:6418204
Patch1:	      libgnomeprintui-01-papi-print-dialog.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.6.0
%define libgnomeprint_version 2.12.1
%define libgnomecanvas_version 2.6.0
%define gnome_icon_theme_version 1.1.92
%define XFree86_version 4.3.99

Requires:  gtk2 >= %{gtk2_version}
Requires:  libgnomeprint >= %{libgnomeprint_version}
Requires:  libgnomecanvas >= %{libgnomecanvas_version}
Requires:  libgnomeui
Requires:  gnome-icon-theme >= %{gnome_icon_theme_version} 

BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:  libgnomeprint-devel >= %{libgnomeprint_version}
BuildRequires:  libgnomecanvas-devel >= %{libgnomecanvas_version}
BuildRequires:  libgnomeui-devel
BuildRequires:  gnome-icon-theme >= %{gnome_icon_theme_version} 

%description
libgnomeprintui is the printing user interface library for the GNOME desktop, providing 
the user interface elements for GNOME applications eg. print dialog

%package devel
Summary:      Print User Interface Development Library for the GNOME Desktop
Group:        Development/Libraries/GNOME
Autoreqprov:  on
Requires:     %{name} >= %{version}
Requires:     gtk2-devel >= %{gtk2_version}
Requires:     libgnomeprint-devel >= %{libgnomeprint_version}
Requires:     libgnomecanvas-devel >= %{libgnomecanvas_version}

%description devel
libgnomeprintui is the printing user interface library for the GNOME desktop, providing 
the user interface elements for GNOME applications eg. print dialog

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

libtoolize --force --copy
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir} \
	    --libexecdir=%{_libexecdir} \
	    --mandir=%{_mandir}		\
	    %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc AUTHORS ChangeLog NEWS README COPYING
%{_datadir}/locale/*/LC_MESSAGES/libgnomeprintui*.mo
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/*
%{_datadir}/libgnomeprintui/%{version}/*
%{_mandir}/man3/*

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.18.4
* Thu Jan 31 2008 - damien.carbery@sun.com
- Bump to 2.18.2. Remove upstream patch, 02-layout-button-crash.
* Wed Nov 07 2007 - ghee.teo@sun.com
- Added patch libgnomeprintui-02-layout-button-crash.diff
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Mon Mar 12 2005 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2005 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Thu Nov 23 2005 - damien.carbery@sun.com
- Bump to 2.17.0.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Wed Apr 26 2006 - ghee.teo@sun.com
- Fixed 6418240 with libgnomeprintui-01-papi-print-dialog.diff.
* Tue Sep 27 2005 - glynn.foster@sun.com
- Bump to 2.12.1
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.12.0.
* Thu May 19 2005 - brian.cameron@sun.com
- Replace libgnomeprintui-01-g11n-potfiles.diff and remove 
  libgnomeprintui-01-printing-in-nautilus.diff since it breaks the
  build.
* Thu May 19 2005 - arvind.samptur@wipro.com
-  port to 2.10
* Tue May 17 2005 - laszlo.kovacs@sun.com
- ported to 2.10
* Wed Mar 30 2005 - vinay.mandyakoppal@wipro.com
- Added libgnomeprintui-05-read-page-word.diff patch to make sure
  that 'Page' word is read once in print preview window by screen
  reader. Fixes bug #6224958.
* Fri Feb 11 2005 - srirama.sharma@wipro.com
- Added libgnomeprintui-04-read-subheadings.diff to make sure that
  gnopernicus reads the subheadings of the "print dialog".
  Fixes bug #6192634.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add libgnomeprintui-2.2.3 man page
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.  Added patch to allow gtk-docs to build.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeprintui-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeprintui-l10n-po-1.1.tar.bz2
* Fri Apr 02 2004 - ghee.teo
- Updated to 2.6.0 tarball
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeprintui-l10n-po-1.0.tar.bz2
* Fri Mar 19 2004 - <glynn.foster@sun.com>
- Bump to 2.5.4, and rename the potfiles patch.
* Fri Mar 12 2004 - <ghee.teo@sun.com>
- Dropping the iconlist-dialog patch and goes for the HEAD. Will review this
  with HCI before final feature freeze.
* Wed Mar 03 2004 - <ghee.teo@sun.com>
- Fixed the print dialog crashing due to a back port of 
  libgnomeprintui-02-iconlist-dialog.diff
* Tue Feb 24 2004 - <ghee.teo@sun.com>
- Fixed a symbol typo in libgnomeprintui-02-iconlist-dialog.diff
* Mon Feb 23 2004 - <ghee.teo@sun.com>
- Ported patches libgnomeprintui-02-iconlist-dialog.diff and
  libgnomeprintui-03-printing-in-nautilus.diff for cinnabar.
* Thu Feb 19 2004 - <matt.keenan@sun.com>
- Bump to 2.5.2, l10n to 0.8
- Remove libgnomeprintui-01-doc-makefile.diff patch, in new tarball
- Ported potfiles_in patch from QS
* Thu Feb 12 2004 - <niall.power@sun.com>
- add ACLOCAL_FLAGS to aclocal invocation
* Wed Jan 07 2004 - <matt.keenan@sun.com>
- Patch for doc/Makefile.am do not include GTKDOC_CC/GTKDOC_LD as already
  got from gtk-doc.make in toplevel dir.
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.0.1
* Tue Oct 21 2003 - <ghee.teo@sun.com>
- Port printing-in-nautilus patch to QS.
* Thu Oct 09 2003 - <ghee.teo@sun.com>
- Updated spec file rev to build for QS. Since this tarball is not in the 
  community yet. Stick to the same tarball as in Mercury.
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball
* Mon Jun 30 2003 - ghee.teo@sun.com
- Added cups integration with a new tarball and a patch
  libgnomeprintui-2.3.0.tar.bz2, libgnomeprintui-01-iconlist-dialog.diff
* Wed May 14 2003 - matt.keenan@sun.com
- Initial Sun release
