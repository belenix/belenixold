#
# spec file for package gthumb
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner: jerrytan
#
%include l10n.inc
Name:		gthumb
License:	GPL v2
Group:		Applications/Multimedia
Version:	2.10.11
Release:	1
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	An image viewer and browser for GNOME.
Source:		http://ftp.gnome.org/pub/GNOME/sources/gthumb/2.10/%{name}-%{version}.tar.bz2
Source1:	%{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:jerrytan date:2006-03-22 type:branding
Patch1:         gthumb-01-menu-entry.diff
#owner:jerrytan date:2008-07-31 type:branding
Patch2:         gthumb-02-man.diff
#owner:fujiwara date:2008-08-26 type:bug bugster:6738015 bugzilla:489922 state:upsteam
Patch3:         gthumb-03-g11n-locale-dir.diff
#owner:jerrytan date:2008-11-20 type:bug bugster:6718848 bugzilla:561632 
Patch4:         gthumb-04-zh-ja-locale.diff 
URL:		http://gthumb.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_docdir}/doc
Autoreqprov:	on

BuildRequires:	libpng-devel
BuildRequires:	glib2-devel >= 2.4.0
BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:	libxml2-devel >= 2.6.7
BuildRequires:	libgnome-devel >= 2.6.0
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	gnome-vfs-devel >= 2.6.0
BuildRequires:	libglade-devel >= 2.3.6
BuildRequires:	libgnomeprint-devel >= 2.6.0
BuildRequires:	libgnomeprintui-devel >= 2.6.0
BuildRequires:	libbonobo-devel >= 2.6.0
BuildRequires:	libbonoboui-devel >= 2.6.0
Requires:	libpng
Requires:       glib2 >= 2.4.0
Requires:       gtk2 >= 2.4.0
Requires:	libxml2 >= 2.6.7
Requires:	libgnome >= 2.6.0
Requires:	libgnomeui >= 2.6.0
Requires:	gnome-vfs >= 2.6.0
Requires:	libglade >= 2.3.6
Requires:	libgnomeprint >= 2.6.0
Requires:	libgnomeprintui >= 2.6.0
Requires:	libbonobo >= 2.6.0
Requires:	libbonoboui >= 2.6.0

%description
gThumb lets you browse your hard disk, showing you thumbnails of image files. 
It also lets you view single files (including GIF animations), add comments to
images, organize images in catalogs, print images, view slideshows, set your
desktop background, and more. 

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" 			\
  ./configure --prefix=%{_prefix} 		\
              --bindir=%{_bindir}               \
              --libdir=%{_libdir}               \
	      --mandir=%{_mandir}		\
	      --sysconfdir=%{_sysconfdir}	\
              --disable-scrollkeeper            \
	      --disable-schemas-install	        \
	      --libexecdir=%{_libexecdir}
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#Clean up unpackage files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gthumb/modules/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gthumb/modules/*.la


# Remove omf file(s) so that does not appear in yelp
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/gthumb
rmdir $RPM_BUILD_ROOT%{_datadir}/omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gthumb.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done


%postun

%files
%defattr(-,root,root)
%{_bindir}/gthumb
%{_libdir}/gthumb/libgthumb.so
%{_libexecdir}/gthumb-image-viewer
%{_libexecdir}/gthumb-catalog-view
%{_datadir}/applications/gthumb.desktop
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/gthumb/glade/*
%{_datadir}/gthumb/icons/*
%{_datadir}/gthumb/albumthemes/*
%{_datadir}/locale/*/LC_MESSAGES/gthumb.mo
%{_datadir}/application-registry/gthumb.applications
%{_libdir}/bonobo/servers/*.server
%{_libdir}/gthumb/modules/*.so
%{_datadir}/pixmaps/gthumb.png
%{_sysconfdir}/gconf/schemas/*.schemas
%doc AUTHORS NEWS README COPYING
%doc %{_datadir}/man/man1/gthumb.1*
%doc %{_datadir}/gnome/help/gthumb

%changelog
* Thu Feb 26 2009 - dave.lin@sun.com
- Bump to 2.10.11
- Remove upstreamed patch 05-libumem-check.diff.
* Wed Feb 04 2009 - jerry.tan@sun.com
- Add gthumb-05-libumem-check.diff to fix bug 6647918
* Wed Dec 03 2008 - jerry.tan@sun.com
- Bump to 2.10.10
* Thu Nov 20 2008 -xin.lai@sun.com
- Add gthumb-04-zh-ja-locale.diff to fix the core dumped bug 6718848
* Tue Aug 26 2008 - takao.fujiwara@sun.com
- Add gthumb-03-g11n-locale-dir.diff to show none UTF-8 filenames.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.10.9. Remove upstream patch 02-uninstd_h.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Add upstream patch 02-uninstd_h to fix 543584.
* Thu 25 Apr 2008 - jerry.tan@sun.com
- Bump to 2.10.8.
* Thu Nov 22 2007 - matt.keenan@sun.com
- Add Patch 02-threads.diff resolves bugs 6631422/498995
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.10.7.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.10.6.
* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 2.10.5. Remove upstream patch, 02-html-page-begin.
* Fri Jun 22 2007 - damien.carbery@sun.com
- Add patch, 02-html-page-begin, to fix 450110.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.10.4.
* Thu May 17 2007 - damien.carbery@sun.com
- Bump to 2.10.3. Remove upstream patch, 02-fix-photo-import.
* Wed May 16 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.10.2.
* Wed Mar 28 2007 - damien.carbery@sun.com
- Bump to 2.10.1.
* Tue Mar 20 2007 - damien.carbery@sun.com
- Bump to 2.10.0.
* Wed Mar 14 2007 - laca@sun.com
- add --disable-scrollkeeper configure option
* Wed Mar 07 2007 - daymobrew@users.sourceforge.net
- Bump to 2.9.3.
* Mon Feb 19 2007 - damien.carbery@sun.com
- Bump to 2.9.2. Minor change to deletion of *.a & *.la.
* Thu Nov 20 2006 - laca@sun.com
- bump to 2.7.9
* Sat May 13 2006 - laca@sun.com
- Move to /usr
* Thu Apr 20 2006 - damien.carbery@sun.com
- Bump to 2.7.6.
* Tue Mar 21 2006 - damien.carbery@sun.com
- Bump to 2.7.5.1.
* Mon Mar  6 2006 - damien.carbery@sun.com
- Bump to 2.7.4.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.7.3.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.7.2
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.7.1
* Fri Dec 02 2005 - srirama.sharma@wipro.com
- Added gthumb-04-sfw-path.diff to use the absolute path of the 
  executable in the .desktop file as usr/sfw/bin should not be 
  included in $PATH.
  Fixes bug #6345489.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 2.6.8.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.6.6.
* Fri Jan 28 2005 - Matt.keenan@sun.com
- #6222302 - Remove from yelp
* Sun Nov 14 2004 - laca@sun.com
- added --libdir=%{_libdir} and --bindir=%{_bindir} to configure opts
* Wed Oct 20 2004 - alvaro.lopez@sun.com
- Added patch6. It fixes bug #5101957
* Wed Oct 20 2004 - alvaro.lopez@sun.com
- "Source" entry updated
* Wed Sep 15 2004 - yuriy.kuznetsov@sun.com
- Added gthumb-04-g11n-potfiles.diff
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gthumb-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Jun 14 2004 - kaushal.kumar@wipro.com
- Fix gthumb omf file installation.
* Thu Jun 10 2004 - vijaykumar.patwari@wipro.com
- Fixes search pattern.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gthumb-l10n-po-1.1.tar.bz2
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Fri Apr 09 2004 - brian.cameron@sun.com
- Change the way the build directory is cleaned so that eog and
  gthumb can be built into the same Solaris package.
* Thu Apr 01 2004 - brian.cameron@sun.com
- Added patch02, now use ACLOCAL_FLAGS in aclocal call, and
  added --libexecdir to the configure line.
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion, fix BuildRoot location
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gthumb-l10n-po-1.0.tar.bz2 l10n content
* Mon Feb 23 2004 - <stephen.browne@sun.com>
- uprevd to 2.3.1, removed patch 02
* Fri Jan 09 2004 - <matt.keenan@sun.com>
- Deprecated patch for compile
* Mon Oct 20 2003 - <stephen.browne@sun.com>
- upreved to 2.1.7
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Mon Aug 11 2003 - stephen.browne@sun.como
- new tarball, reset release
* Sat Aug 01 2003 - glynn.foster@sun.com
- Update menu entry.
* Mon Jul 14 2003 - Ghee.Teo@sun.com
- Initial Sun Release
