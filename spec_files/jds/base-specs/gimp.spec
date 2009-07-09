#
# spec file for package gimp
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
%define subver 2.6
%define subver_install 2.0
%define microver 6

Name:         gimp
License:      GPL/LGPL
Group:        System/GUI/GNOME
Version:      %{subver}.%{microver}
Release:      2
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      The GIMP (GNU Image Manipulation Program)
Source:       ftp://ftp.gimp.org/pub/%{name}/v%{subver}/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
URL:          http://www.gimp.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       coreutils

%define glib2_version 2.4.1
%define gtk2_version 2.4.1
%define libmng_version 1.0.6
%define libgimpprint_version 4.2.6
%define libpng_version 1.2.5
%define libjpeg_version 6.2.0
%define libungif_version 4.1.0
%define slang_version 1.4.9
%define pygtk2_version 2.7.3

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgimpprint-devel >= %{libgimpprint_version}
BuildRequires: libmng-devel >= %{libmng_version}
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: libjpeg-devel >= %{libjpeg_version}
BuildRequires: libungif >= %{libungif_version}
BuildRequires: slang-devel >= %{slang_version}
BuildRequires: pygtk2-devel >= %{pygtk2_version}

Requires: glib2 >= %{glib2_version}
Requires: gtk2 >= %{gtk2_version}

%description
The GIMP (GNU Image Manipulation Program) is a powerful image
composition and editing program, which can be extremely useful for
creating logos and other graphics for webpages. The GIMP has many of
the tools and filters you would expect to find in similar commercial
offerings, and some interesting extras as well. The GIMP provides a
large image manipulation toolbox, including channel operations and
layers, effects, sub-pixel imaging and anti-aliasing, and conversions,
all with multi-level undo.

The GIMP includes a scripting facility, but many of the included
scripts rely on fonts that we cannot distribute. The GIMP FTP site
has a package of fonts that you can install by yourself, which
includes all the fonts needed to run the included scripts. Some of
the fonts have unusual licensing requirements; all the licenses are
documented in the package. Get
ftp://ftp.gimp.org/pub/gimp/fonts/freefonts-0.10.tar.gz and
ftp://ftp.gimp.org/pub/gimp/fonts/sharefonts-0.10.tar.gz if you are so
inclined. Alternatively, choose fonts which exist on your system
before running the scripts.

%package devel
Summary: The GIMP plug-in and extension development kit.
Group: Applications/Multimedia
Requires: 	gtk2-devel >= %{gtk2_version}
Requires:	%{name} = %{version}
Autoreqprov:  on

%description devel
The gimp-devel package contains the static libraries and header files
for writing GNU Image Manipulation Program (GIMP) plug-ins and
extensions.


%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif

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

CFLAGS="$RPM_OPT_FLAGS"			\
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
# Removing sierra driver on Solaris since it doesn't compile yet.
%ifos solaris
%define print_options "--disable-print"
%define mmx_options "--enable-mmx=no"
%else
%define print_options ""
%endif
./configure --prefix=%{_prefix} \
	    --sysconfdir=%{_sysconfdir} \
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
	    --libexecdir=%{_libexecdir} \
	    --localstatedir=/var/lib	\
	    --mandir=%{_mandir}		\
	    --enable-mp			\
	    %{gtk_doc_option}           \
	    --enable-default-binary	\
	    %{mmx_options}		\
	    %{print_options}
make munix=

%install
make DESTDIR=$RPM_BUILD_ROOT install
#clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/%{subver_install}/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/gimp/%{subver_install}/python/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/%{subver_install}/python/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/%{name}/%{subver_install}/python/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
rm -f %{_datadir}/mime-info/gimp-%{subver}.keys
/sbin/ldconfig

%files
%defattr (-, root, root)
%{_bindir}/gimp
%{_bindir}/gimp-%{subver}
%{_bindir}/gimp-console*
%{_bindir}/gimp-remote*
%{_libdir}/lib*-%{subver_install}.so.*
%dir %{_datadir}/gimp/%{subver_install}
%dir %{_libdir}/gimp/%{subver_install}
%dir %{_libdir}/gimp/%{subver_install}/environ
%dir %{_libdir}/gimp/%{subver_install}/modules
%dir %{_libdir}/gimp/%{subver_install}/plug-ins
%{_libdir}/gimp/%{subver_install}/environ/*
%{_libdir}/gimp/%{subver_install}/modules/*.so
%{_libdir}/gimp/%{subver_install}/plug-ins/*
%{_libdir}/gimp/%{subver_install}/interpreters
%{_libdir}/gimp/%{subver_install}/python
%{_datadir}/gimp/%{subver_install}/brushes/
%{_datadir}/gimp/%{subver_install}/fractalexplorer/
%{_datadir}/gimp/%{subver_install}/gfig/
%{_datadir}/gimp/%{subver_install}/gflare/
%{_datadir}/gimp/%{subver_install}/gimpressionist/
%{_datadir}/gimp/%{subver_install}/gradients/
%{_datadir}/gimp/%{subver_install}/images/
%{_datadir}/gimp/%{subver_install}/palettes/
%{_datadir}/gimp/%{subver_install}/patterns/
%{_datadir}/gimp/%{subver_install}/scripts/
%{_datadir}/gimp/%{subver_install}/themes/
%{_datadir}/gimp/%{subver_install}/tips/
%{_datadir}/gimp/%{subver_install}/menus/
%{_datadir}/applications/gimp.desktop
%{_datadir}/application-registry/gimp.applications
%{_datadir}/mime-info/gimp.keys
%{_datadir}/locale
%{_datadir}/icons
%{_sysconfdir}/gimp/%{subver_install}/gimprc
%{_sysconfdir}/gimp/%{subver_install}/gtkrc
%{_sysconfdir}/gimp/%{subver_install}/ps-menurc
%{_sysconfdir}/gimp/%{subver_install}/sessionrc
%{_sysconfdir}/gimp/%{subver_install}/templaterc
%{_sysconfdir}/gimp/%{subver_install}/unitrc
%{_sysconfdir}/gimp/%{subver_install}/controllerrc
%{_mandir}/man1/gimp-%{subver}.1*
%{_mandir}/man1/gimp-remote*
%{_mandir}/man1/gimptool*
%{_mandir}/man5/gimprc-%{subver}.5*

%files devel
%defattr (-, root, root)
%{_includedir}/gimp-%{subver_install}/
%{_bindir}/gimptool-%{subver_install}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_libdir}/gimp/%{subver_install}/modules
%{_datadir}/aclocal/gimp-2.0.m4
%{_datadir}/gtk-doc/html/
%{_mandir}/man1/gimptool-%{subver_install}.1*

%changelog
* Thu Jun 05 2008 - damien.carbery@sun.com
- Revert to 2.4.6 because 2.5.0 requires gegl and babl, both GPL v3 modules.
* Wed May 28 2008 - brian.cameron@sun.com
- Bump to 2.5.0.
* Thu Mar 06 2008 - brian.cameron@sun.com
- Bump to 2.4.5.
* Mon Feb 04 2008 - brian.cameron@sun.com
- Bump to 2.4.4.
* Fri Jan 11 2008 - laca@sun.com
- remove help -- moved to a separate spec file and package
* Wed Dec 19 2007 - brian.cameron@sun.com
- Bump to 2.4.3.
* Mon Dec 03 2007 - brian.cameron@sun.com
- Bump to 2.4.2.  Bump gimp-help to 2.4.0
* Wed Nov 07 2007 - brian.cameron@sun.com
- Bump to 2.4.1.
* Fri Oct 26 2007 - damien.carbery@sun.com
- Bump to 2.4.0.
* Thu Oct  2 2007 - damien.carbery@sun.com
- Bump gimp-help to 2.0.13.
* Wed Sep 25 2007 - damien.carbery@sun.com
- Bump to 2.4.0-rc3.
* Thu Sep 06 2007 - damien.carbery@sun.com
- Bump to 2.4.0-rc2.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Replace 05-iconv-solaris patch with call to intltoolize.
* Mon Aug 20 2007 - damien.carbery@sun.com
- Bump to 2.4.0-rc1. Add patch 05-iconv-solaris to fix #467309. Modify
  intltool-merge.in to allow use of non-GNU iconv.
* Thu Aug 02 2007 - damien.carbery@sun.com
- Bump to 2.3.19.
* Sat Jul 14 2007 - damien.carbery@sun.com
- Bump to 2.3.18.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.3.17. Remove upstream patch, 02-void-return.
* Sun May 06 2007 - damien.carbery@sun.com
- Bump to 2.3.16. Add patch 02-void-return to fix 433339. Removes 'return'
  keyword from void function code.
* Wed Mar 14 2007 - damien.carbery@sun.com
- Bump to 2.3.15.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Thu Feb  8 2007 - damien.carbery@sun.com
- Bump to 2.3.14.
* Thu Jan 25 2006 - brian.cameron@sun.com
- Remove gimp-02-fixcompile.  Fixed upstream.
* Thu Dec 21 2006 - brian.cameron@sun.com
- Bump help version to 2.0.11.  Add --without-gimp to help 
  configure so the help docs build.
* Tue Nov 28 2006 - damien.carbery@sun.com
- Bump to 2.3.13. Remove upstream patches 02-Xext and 04-null-char. Renumber 
  remainder.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Tue Oct 17 2006 - matt.keenan@sun.com
- Created bugzilla : #362877, attached patch gimp-02-Xext.diff,
  to get this upstream
* Tue Oct 17 2006 - damien.carbery@sun.com
- Add patch, 04-null-char, to remove a null char that is breaking the build.
  Bugzilla #362832.
- Bump to 2.3.12.
* Fri Oct 13 2006 - damien.carbery@sun.com
- Delete .a and .la files.
* Thu Sep 28 2006 - damien.carbery@sun.com
- Bump to 2.3.11. Remove upstream patch, 03-hidden, and renumber rest.
* Mon Aug 14 2006 - damien.carbery@sun.com
- Bump to 2.3.10.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.3.9.  Set --enable-mmx=no when building on Solaris since
  this compiler option doesn't work on Solaris
* Tue May 30 2006 - damien.carbery@sun.com
- Add patch, 04-hidden, for new G_GNUC_INTERNAL usage.
* Wed May 03 2006 - damien.carbery@sun.com
- Bump help version to 2.0.10.
* Tue Apr 25 2006 - damien.carbery@sun.com
- Add patch, 03-void-return, to fix build issues. Bugzilla: 339698.
* Mon Apr 24 2006 - damien.carbery@sun.com
- Bump to 2.3.8.
- Bump help version to 2.0.9.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 2.3.7.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.3.6.
* Fri Sep 30 2005 - brian.cameron@sun.com
- Bump to 2.3.4
* Tue Sep 20 2005 - laca@sun.com
- add patch Xext.diff: add -lXext to a Makefile.am
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.3.3.
* Fri Jun 10 2005 - matt.keenan@sun.com
- Bump to 2.2.7, reapply patches
* Tue Feb 01 2005 - laca@sun.com
- add a symlink called gimp to bindir that points to gimp-%subver, fixes
  #6221126
* Fri Jan 21 2005 - damien.carbery@sun.com
- %ifos linux the PKG_CONFIG_PATH so Solaris one can be different.
* Sun Jan 16 2005 - damien.carbery@sun.com
- Set PKG_CONFIG_PATH to build with gimp-help tarball.
* Tue Jan 11 2005 - matt.keenan@sun.com
- #6199103 : Add gimp-help tarball
* Fri Nov 12 2004 - laca@sun.com
- Added --libdir and --bindir to configure opts so they can be redirected
  on Solaris
* Tue Sep 14 2004 - yuriy.kuznetsov@sun.com
- Added gimp-03-g11n-potfiles.diff 
* Wed Aug 25 2004 - laszlo.kovacs@sun.com
- changed header file permissions
* Wed Aug 18 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since it doesn't make sense to include both
  this and --enable-gtk-doc.
* Fri Jul 16 2004 - niall.power@sun.com
- Finally bumped to 2.0.x series (2.0.2)
- packaging fixes for rpm4 and remove upstream patches
* Tue Jul 13 2004 - damien.carbery@sun.com
- Remove '-j $CPUS' from 'make' because of failures on Solaris and intermittent
  failures on Linux.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gimp-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri May 21 2004 - brian.cameron@sun.com
- Added patch 4 to support building on x86 Solaris.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gimp-l10n-po-1.1.tar.bz2
* Wed Apr 28 2004 - vijaykumar.patwari@wipro.com
- Remove unwanted keys from gimp.keys.
* Sun Apr 03 2004 - brian.cameron@sun.com
- Use #ifdef to set --disable-print for Solaris.
* Thu Apr 01 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar.  Now pass ACLOCAL_FLAGS into
  aclocal.  Added EXTRA_CONFIGURE_OPTIONS to allow Solaris
  to pass in --disable-print.  Fixed a few defattr lines.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gimp-l10n-po-1.0.tar.bz2 l10n content
* Fri Jan 09 2004 - <niall.power@sun.com>
- Patch configure.in to enable deprecated widgets
* Mon Oct 20 2003 - <ghee.teo@sun.com>
- Updated version of glib2 and gtk2 dependency to build for QS.
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Tue Aug 11 2003 - niall.power@sun.com
- Move mime, .desktop and keys files into proper location
  instead of just sym-linking them
* Mon Aug 10 2003 - glynn.foster@sun.com
- Bump tarball
* Thu Jul 17 2003 - glynn.foster@sun.com
- Correct menu entry
* Mon Jul 14 2003 - Niall.Power@sun.com
- initial spec file created
