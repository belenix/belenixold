#
# spec file for package libgnomeui 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: alo
#
Name:         libgnomeui 
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.24.1
Release:      3
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      GNOME User Interface Library  
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgnomeui/2.24/libgnomeui-%{version}.tar.bz2
# date:2004-10-28 bugzilla:129668 owner:padraig type:bug
Patch1:       libgnomeui-01-icon-a11y.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk_doc_version 1.1
%define gtk2_version 2.4.0
%define gail_version 1.5.7
%define libbonoboui_version 2.6.0
%define libglade_version 2.3.6
%define libbonobo_version 2.6.0
%define libgnome_version 2.6.0
%define gnome_keyring_version 0.2.0

Requires: gtk2 >= %{gtk2_version}
Requires: libbonoboui >= %{libbonoboui_version}
Requires: libglade >= %{libglade_version}
Requires: gnome-keyring >= %{gnome_keyring_version}
Requires: gail >= %{gail_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libbonoboui-devel >= %{libbonoboui_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: gnome-keyring-devel >= %{gnome_keyring_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}

%description
libgnomeui is the GNOME User Interface Library, containing many widgets and 
convenient API used to developer GNOME applications that is not in GTK+ 
eg. About Dialog, Session Manager support

%package devel
Summary:      GNOME User Interface Development Library
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     libgnome-devel >= %{libgnome_version}
Requires:     libbonoboui-devel >= %{libbonoboui_version}

%description devel
libgnomeui is the GNOME User Interface Library, containing many widgets and 
convenient API used to developer GNOME applications that is not in GTK+ 
eg. About Dialog, Session Manager support

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoconf
autoheader
automake -a -c -f

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --datadir=%{_datadir}       \
	    --sysconfdir=%{_sysconfdir}	\
	    --mandir=%{_mandir}		\
	    --libexecdir=%{_libexecdir}	\
	    %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/libglade/*/*.a
rm $RPM_BUILD_ROOT%{_libdir}/libglade/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

#%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_datadir}/locale/*/LC_MESSAGES/libgnomeui-2.0.mo
%{_datadir}/pixmaps/*.png
%{_libexecdir}/*
%{_libdir}/libglade/2.0/libgnome*so*
%{_libdir}/lib*.so.*
%{_libdir}/gtk-2.0/2.4.0/filesystems/*.so

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libgnomeui-2.0/libgnomeui/*.h
%{_includedir}/libgnomeui-2.0/*.h
%{_libdir}/lib*.so
%{_datadir}/gtk-doc/html/libgnomeui
%{_mandir}/man3/*

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.24.1
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.90
- Removed the upstreamed patch libgnomeui-02-gtk-deprecated.diff
- Update the patch libgnomeui-01-icon-a11y.diff to fix hunk failure
* Thu Jul 10 2008 - damien.carbery@sun.com
- Add 03-gtk-deprecated to update files for the new gtk+ tarball.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4. Remove obsolete patch, 02-gio-critical.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.
* Thu Apr 10 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Tue Mar 18 2008 - alvaro.lopez@sun.com
- Added patch: libgnomeui-02-gio-critical.diff
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.01.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.1. Remove obsolete patch, 02-crash-no-bugbuddy.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.0.
* Wed Mar 14 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.1.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 2.17.0. Change patch2 to -p1 while reworking the patch contents.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Thu Oct 05 2006 - damien.carbery@sun.com
- Bump to 2.16.1. Remove upstream patch, 03-hang-on-mutex.
* Wed Sep 27 2006 - padraig.obriain@sun.com
- Add libgnomeui-03-hang-on-mutex.diff to fix 6475663.
* Wed Sep 13 2006 - harry.lu@sun.com
- Add libgnomeui-02-crash-no-bugbuddy.diff to fix 6463604.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
- Remove upstream patch, 02-hidden.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Fri Jul 21 2006 - padraig.obriain@sun.com
- Bump to 2.15.2.
* Mon May 29 2006 - damien.carbery@sun.com
- Add patch, 02-hidden, to remove G_GNUC_INTERNAL to build.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Thu Jan 26 2006 - damien.carbery@sun.com
- Bump to 2.13.3
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.2
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.13.0
* Thu Sep 15 2005 - brian.cameron@sun.com
- Bump to 2.12.0
* Wed Aug 24 2005 - laca@sun.com
- merge/remove patches
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.2.
* Wed Aug 03 2005 - laca@sun.com
- remove upstream patch (cancel-rename.diff)
* Wed Jun 15 2005 - laca@sun.com
- Add more libs to LDADD so that it builds with the new pkgconfig
* Fri May 13 2005 - vijaykumar.patwari@wipro.com
- Added patch libgnomeui-10-cancel-rename.diff, fixes
  nautilus crash for rename operation in smb.
  Fixes bug#6264644.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.0
* Wed Mar 16 2005 - balamurali.viswanathan@wipro.com
- Added patch libgnomeui-09-disconnect-close.diff. Don't connect the close
  signal in the authentication dialog. Fixes bug #6237403
* Thu Dec 23 2004 - vinay.mandyakoppal@wipro.com
- Added libgnomeui-08-disable-crash-dialog.diff to make
  --disable-crash-dialog option work. Fixes bug #6210518.
* Fri Dec 17 2004 - glynn.foster@sun.com
- Bump to 2.6.2, so that we pick up a bunch of file chooser
  fixes.
* Fri Nov 12 2004 - padraig.obriain@sun.com
- Add patch libgnomeui-08-a11y-children.diff. Fixes bug #5080627
* Fri Nov 5 2004 - archana.shah@wipro.com
- Added patch libgnomeui-07-sftp.diff.
  Fixes bug# 5088520
* Thu Oct 28 2004 - balamurali.viswanathan@wipro.com
- Modified patch libgnomeui-06 so that the selected icon have 
  SPI_STATE_FOCUSED
* Tue Oct 19 2004 - balamurali.viswanathan@wipro.com
- Added patch libgnomeui-06 to make the icon list accessible.
* Tue Oct 5 2004 - srirama.sharma@wipro.com
- Added patch libgnomeui-05-file-chooser.diff to
  canonicalize the URI before looking it up in the 
  folder's hash table. Fixes Bug #5103163.
* Tue Sep 14 2004 - muktha.narayan@wipro.com
- Added patch libgnomeui-04-druid-theming.diff to make
  'Add a printer' dialog theme compliant.
  Fixes bug #5035846.
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc
* Wed Jul 28 2004 - glynn.foster@sun.com
- Bump to 2.6.1.1
* Wed Jul 28 2004 - glynn.foster@sun.com
- Add patch to unfocus the widgets on the previous page
  of the GnomeDruid widget. Patch from Eric Zhao.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeui-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu Jun 24 2004 - takao.fujiwara@sun.com
- Updated libgnomeui-01-g11n-i18n-ui.diff to i18n Filesystem in gtkdialog.
  bugzilla #144529
* Thu Jun 17 2004 - ghee.teo@sun.com
- Added libgnomeui-03-mount-crashed-gedit.diff. The patch is taken from
  HEAD (also included in 2.6.1.1 tarball release). bugzilla id#139063.
  Bugtraq id 5055273. Since we are at Beta, so have to keep this patch
  for the time being and uprev after Beta, this patch can then be removed.
* Tue May 25 2004 - yuriy.kuznetsov@sun.com
- Added libgnomeui-02-g11n-potfiles.diff
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeui-l10n-po-1.1.tar.bz2
* Wed May 05 2004 - niall.power@sun.com
- Add missing gtk file selector plug-in to %files.
  Add gtk2 to requirements
* Wed May 04 2004 - glynn.foster@sun.com
- Remove auth manager patch, it was wrong and rejected in
  bugzilla.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomeui-l10n-po-1.0.tar.bz2
* Mon Mar 22 2004 - takao.fujiwara@sun.com
- Added libgnomeui-02-g11n-i18n-ui.diff to fix 4995208
* Mon Mar 22 2004 - glynn.foster@sun.com
- Bump to 2.6.0 and remove broken file entry patch that doesn't
  fix anything.
* Sun Feb 15 2004 - laca@sun.com
- Add --libexecdir to the configure options so we get the correct path
  on Solaris
* Mon Feb 02 2004 - niall.power@sun.com
- Bump to 2.5.3
- Add ACLOCAL_FLAGS env to aclocal invocation
* Thu Jan 08 2004 - niall.power@sun.com
- Update to 2.5.2 to make nautilus build
* Mon Dec 15 2003 - glynn.foster@sun.com
- Update to 2.5.1
* Mon Oct 13 2003 - stephen.browne@sun.com
- added auth manager patch (moved from nautilus)
* Thu Oct 09 2003 - stephen.browne@sun.com
- Updated for 2.4
* Thu Sep 25 2003 - stephen.browne@sun.com
- Fix icon theming for icons with full paths
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Thu Aug 07 2003 - glynn.foster@sun.com
- Remove the evil activate signal on file entry 
  browse ok button callback. Stops browse dialog
  being displayed twice, when user selects stuff.
* Thu Aug 07 2003 - glynn.foster@sun.com
- Update tarball, bump version, reset release.
* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball
* Tue May 13 2003 - Laszlo.Kovacs@Sun.COM
- Initial Sun release.
