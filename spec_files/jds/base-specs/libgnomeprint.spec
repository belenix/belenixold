#
# spec file for package libgnomeprint
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         libgnomeprint
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.18.6
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Print Library for the GNOME Desktop
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgnomeprint/2.18/libgnomeprint-%{version}.tar.bz2
# owner:gheet date:2006-04-23 type:bug bugster:6418204,6194525
Patch1:       libgnomeprint-01-papi-print-dialog.diff
# owner:gheet date:2006-08-10 type:bug bugster:6437235 bugzilla:345012
Patch2:       libgnomeprint-02-evince-crash.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define glib2_version 2.4.0
%define pango_version 1.4.0
%define libart_lgpl_version 2.3.16
%define gtk_doc_version 1.1
%define gnome_common_version 2.4.0
%define cups_version 1.1.20
%define openssl_devel_version 0.9.7

Requires:      glib2 >= %{glib2_version}
Requires:      pango >= %{pango_version}
Requires:      libart_lgpl >= %{libart_lgpl_version}
Requires:      cups >= %{cups_version}
Requires:      libgnomecups

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: libart_lgpl-devel >= %{libart_lgpl_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: cups-devel >= %{cups_version}
BuildRequires: gnome-common >= %{gnome_common_version}
BuildRequires: openssl-devel >= %{openssl_devel_version}
BuildRequires: libgnomecups-devel

%description
libgnomeprint is the printing library for the GNOME desktop, providing a simple and clean
API for GNOME applications to print documents.

%package devel
Summary:      Print Development Library for the GNOME Desktop
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     glib2-devel >= %{glib2_version}
Requires:     pango-devel >= %{pango_version}
Requires:     libart_lgpl-devel >= %{libart_lgpl_version}

%description devel
libgnomeprint is the printing library for the GNOME desktop, providing a simple and clean
API for GNOME applications to print documents.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"				\
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --mandir=%{_mandir}			\
	    --without-cups			\
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
rm $RPM_BUILD_ROOT%{_libdir}/libgnomeprint/*/modules/*.a
rm $RPM_BUILD_ROOT%{_libdir}/libgnomeprint/*/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libgnomeprint/*/modules/transports/*.a
rm $RPM_BUILD_ROOT%{_libdir}/libgnomeprint/*/modules/transports/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libgnomeprint/*/modules/filters/lib*a

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/libgnomeprint
%{_libdir}/libgnomeprint/*/modules/*so*
%{_libdir}/libgnomeprint/*/modules/*/*so*
%{_libdir}/*so.*

%files devel
%{_libdir}/pkgconfig/libgnomeprint-2.2.pc
%{_includedir}/libgnomeprint-2.2/libgnomeprint
%{_datadir}/gtk-doc
%{_libdir}/*so
%{_mandir}/man3/*

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.18.6
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.18.4. Remove upstream patch 03-pdf-search.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.18.3.
* Thu Oct 04 2007 - suresh.chandrasekharan@sun.com
- Add libgnomeprint-03-pdf-search.diff. Fixes 6347163.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Wed Aug 08 2007 - damien.carbery@sun.com
- Bump to 2.18.1. Remove upstream patch, 03-guchar-pointer.
* Wed Mar 14 2007 - damien.carbery@sun.com
- Add patch, 03-guchar-pointer, to fix incompatible type compiler error.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Thu Nov 23 2005 - damien.carbery@sun.com
- Remove upstream patch, 03-g11n-filename.
* Wed Nov 22 2005 - damien.carbery@sun.com
- Bump to 2.17.0. Remove upstream patch, 01-Wall. Renumber remainder.
* Thu Nov 16 2006 - takao.fujiwara@sun.com
- Add libgnomeprint-04-g11n-filename.diff. fixes 6452832 and 6245399
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Wed Aug 09 2006 - ghee.teo@sun.com
- Fixes 6437235 which also requires a patch in evince itself.
* Wed Apr 26 2006 - ghee.teo@sun.com
- Fixed 6418240 and also merged libgnomeprint-papi-crash.diff into
  libgnomeprint-papi-print-dialog.diff.
* Fri Oct 14 2005 - laca@sun.com
- fix crash in papi module when no printers are defined
* Tue Sep 27 2005 - glynn.foster@sun.com
- Bump to 2.12.1
* Tue Sep 20 2005 - laca@sun.com
- Add patch -Wall.diff to remove -Wall from a Makefile.am
* Sat Sep 17 2005 - laca@sun.com
- Add unpackaged files to %files
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.0.
* Wed Aug 03 2005 - laca@sun.com
- remove upstream patch PDF-landscape-*.diff
- remove patch use-older-cups.diff: no longer needed
* Thu Jun 02 2005 - suresh.chandrasekharan@sun.com
- Fix for 6263422. Added libgnomeprint-13-PDF-landscape-6263422.diff
* Mon May 16 2005 - arvind.samptur@wipro.com
- Port to 2.10
* Tue Mar 21 2005 - suresh.chandrasekharan@sun.com
- Fix for 6231341. Added libgnomeprint-12-ja-print-preview-6231341.diff
* Tue Dec 21 2004 - suresh.chandrasekharan@sun.com
- Fix for 5083233. Added libgnomeprint-11-gpdf-mixed-text-issue-5083233.diff
* Tue Dec 14 2004 - glynn.foster@sun.com
- Remove the $(datadir)/fonts/pfbs and $(datadir)/gnome-print from
  being created. No idea where this came from, but it's wrong.
* Thu Nov 04 2004 - takao.fujiwara@sun.com
- Updated libgnomeprint-08-g11n-i18n-ui.diff to fix 6188803
* Thu Oct 28 2004 - suresh.chandrasekharan@sun.com
- Fix for 5090546. Added libgnomeprint-10-chinese-ASCII-5090546.diff.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add libgnomeprint-2.2.3 man page
* Tue Oct 05 2004 - takao.fujiwara@sun.com
- Added libgnomeprint-08-g11n-i18n-ui.diff to i18n print dialogs.
  Fixed 4869747
- Added libgnomeprint-09-g11n-potfiles.diff
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.  Added patch to allow gtk-docs to build.
* Fri Aug 18 2004 - suresh.chandrasekharan@sun.com
- Modified libgnomeprint-05-ps-output.diff, a one line fix.
- Create libgnomeprint-06-broken-ttf-fix.diff (bugzilla #149858,
  bugtraq #5085669)
* Sat Jul 10 2004 - suresh.chandrasekharan@sun.com
- create libgnomeprint-05-ps-output.diff (bugzilla #148674,
  bugtraq #5065284, #5077052)
* Sat Jul 10 2004 - muktha.narayan@wipro.com
- Modified libgnomeprint-02-papi.diff to fix crash when there
  are no printers available. Patch by danek.duvall@sun.com.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeprint-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun 09 2004 - suresh.chandrasekharan@sun.com
- Add libgnomeprint-03-pdf-operator-fix.diff for correcting pdf
  output, backported from community's cvs HEAD
- Add libgnomeprint-04-TT-subsetting-4928658.diff to support
  TrueType font subsetting for PDF and PS
* Wed Jun 02 2004 - danek.duvall@sun.com
- Add PAPI support
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeprint-l10n-po-1.1.tar.bz2
* Fri Apr 02 2004 - ghee.teo@sun.com
- Updated to 2.6.0 tarball for 2.6
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeprint-l10n-po-1.0.tar.bz2
* Fri Mar 19 2004 - <glynn.foster@sun.com>
- Bump to 2.5.4 and remove a uninstalled, locale generation and potfiles
  patches.
* Tue Mar 09 2004 - <ghee.teo@sun.com>
- Hacked around with libgnomeprint-04-old-version-cups-hack.diff
  since the version of cups we have is just too old. This patch should be
  removed once CUPS 1.1.20 is made available.
* Thu Feb 19 2004 - <matt.keenan@sun.com>
- Bump to 2.5.2, re-apply patches, bump l10n to 0.8
* Thu Feb 12 2004 - <niall.power@sun.com>
- Add patch 03 to create a -uninstalled.pc file
- autotoolize the build stage
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.0.1
* Thu Oct 09 2003 - <ghee.teo@sun.com>
- Updated spec file to build for QS, since this CUPS stuff has not be
  integrated into GNOME 2.4. Still needs to use the same tarball as Mercury.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball
* Tue Jul 08 2003 - ghee.teo@sun.com
- Changed files section to include printer icons and also libraries 
  that import the cups printers into libgnomeprintui dialog.
* Mon Jun 30 2003 - ghee.teo@sun.com
- Added cups integration with a new version of tarball.
  libgnomeprint-2.3.0.cvs.9.tar.bz2
* Tue May 13 2003 - Laszlo.Kovacs@Sun.COM
- Initial Sun release
