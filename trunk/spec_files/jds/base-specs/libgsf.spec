#
# spec file for package libgsf
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#
%define pythonver 2.4

Name:			libgsf
License:		LGPL 2.1
Group:			System/Libraries
Version:		1.14.11
Release:	 	1	
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		The GNOME Structured File Library
Source:			http://ftp.gnome.org/pub/gnome/sources/libgsf/1.14/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# date:2004-04-12 owner:yippi type:feature
Patch0:			libgsf-01-uninstalled-pc.diff
# date:2008-09-17 owner:rickju type:branding
Patch1:			libgsf-02-gio.diff
URL:			http://ftp.gnome.org/pub/gnome/sources/libgsf/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

#####################################
##     Package Defines Section     ##
#####################################

%define			glib2_version	2.6.0
%define			zlib_version	1.2.1
%define			libxml2_version	2.6.7
%define			bzip2_version	1.0.2
%define			libbonobo_version	2.6.0
%define			gnome_vfs_version	2.6.0

#####################################
##  Package Requirements Section   ##
#####################################

Requires:		glib2	>=	%{glib2_version}
Requires:		libxml2	>=	%{libxml2_version}
Requires:		zlib	>=	%{zlib_version}
Requires:		bzip2	>=	%{bzip2_version}
Requires:		libbonobo	>=	%{libbonobo_version}
Requires:		gnome-vfs	>=	%{gnome_vfs_version}
BuildRequires:		glib2-devel >= %{glib2_version}
BuildRequires:		libxml2-devel	>=	%{libxml2_version}
BuildRequires:		zlib-devel	>=	%{zlib_version}
BuildRequires:		bzip2	>=	%{bzip2_version}
BuildRequires:		libbonobo-devel	>=	%{libbonobo_version}
BuildRequires:		gnome-vfs-devel	>=	%{gnome_vfs_version}

#####################################
##   Package Description Section   ##
#####################################

%description
libgsf project aims to provide an efficient extensible i/o abstraction for
dealing with different structured file formats.

#####################################
##   Package Development Section   ##
#####################################

%package devel
Summary:		libgsf development headers
Group:			Development/Libraries
Requires:		%{name} = %{version}
Requires:		glib2-devel >= %{glib2_version}
Requires:		libxml2-devel	>=	%{libxml2_version}
Requires:		zlib-devel	>=	%{zlib_version}
Requires:		bzip2	>=	%{bzip2_version}
Requires:		libbonobo-devel	>=	%{libbonobo_version}
Requires:		gnome-vfs-devel	>=	%{gnome_vfs_version}

%description devel
libgsf development headers

#####################################
##   Package Preparation Section   ##
#####################################

%prep
%setup -q
%patch0 -p1
%patch1 -p1

#####################################
##      Package Build Section      ##
#####################################


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
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS  -I ./m4
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}            \
      --bindir=%{_bindir}                  \
      --libdir=%{_libdir}                  \
      --includedir=%{_includedir}          \
      --sysconfdir=%{_sysconfdir}          \
      --mandir=%{_mandir}                  \
      --with-gnome                         \
      --with-bz2                           \
      --with-gnome-vfs                     \
      --with-gio                           

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
#Clean up unpackaged files
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Move to vendor-packages
if [ -x $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages ]; then
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
fi


%clean
rm -rf $RPM_BUILD_ROOT

#########################################
##  Package Post[Un] Install Section   ##
#########################################

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gsf-office-thumbnailer.schemas >/dev/null


%postun
/sbin/ldconfig

%preun
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gsf-office-thumbnailer.schemas >/dev/null

#####################################
##      Package Files Section      ##
#####################################

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sysconfdir}/gconf/schemas
%{_libdir}/*.so.*
%{_datadir}/locale
%{_mandir}/man1

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/libgsf/*

%changelog
* Fri Feb 6 2009  - jerry.tan@sun.com
- move python binding from site-packges to vendor-packages
* Sun Sep 21 2008 - christian.kelly@sun.com
- Remove %gtk_doc_option as it's breaking the build on x86.
* Wed Sep 17 2008 - rick.ju@sun.com
- Use gio and support 64bit build
* Mon Sep 01 2008 - halton.huo@sun.com
- Bump to 1.14.9.
* Thu Mar 06 2008 - damien.carbery@sun.com
- Bump to 1.14.8.
* Wed Feb 20 2008 - halton.huo@sun.com
- Add comment for uninstalled-pc.diff.
- Unremove gtk-doc when gtk_doc is false
* Fri Sep 14 2007 - nonsea@users.sourceforge.net
- Add libtoolize and intltoolize to fix build fail.
* Mon Sep 10 2007 - nonsea@users.sourceforge.net
- Bump to 1.14.7.
* Mon Aug 13 2007 - nonsea@users.sourceforge.net
- Bump to 1.14.5.
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Bump to 1.14.3.
- use %gtk_doc_option in configure so that it can be
  disabled using --without-gtk-doc
* Fri Jun 09 2006 - damien.carbery@sun.com
- Bump to 1.14.1.
* Fri Mar 10 2006 - damien.carbery@sun.com
- Bump to 1.14.0.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 1.13.3
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 1.12.3
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 1.12.1
* Tue May 24 2005 - brian.cameron@sun.com
- Turn on --enable-gtk-doc on Solaris since it works now.
* Tue May 24 2005 - laszlo.kovacs@sun.com
- libgsf-02-gtkdoc.diff removed
* Thu May 19 2005 - laszlo.kovacs@sun.com
- ported to 2.10
* Fri Nov 12 2004 - laca@sun.com
- added --libdir and --bindir to configure opts so they can be redirected
  on Solaris
* Mon Sep 20 2004 - dermot.mccluskey@sun.com
- added patch 01 (gtkdoc) back - it's needed to build on linux
* Mon Sep 13 2004 - damien.carbery@sun.com
- Disable gtk-doc on Solaris to get module to build.
* Wed Sep 01 2004 - laszlo.kovacs@sun.com
- fixed gtk-doc path problem
* Tue Aug 24 2004 - brian.cmaeron@sun.com
- Enabling gtk-docs and setting with-html-dir to place them in
  the standard gtk-doc location.
* Thu Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Apr 12 2004 - <brian.cameron@sun.com
- Added patch 1 to add uninstalled.pc file for Solaris build.
* Tue Feb 24 2004 - <michael.twomey@sun.com>
- Fixed distro typo
* Tue Feb 24 2004 - <matt.keenan@sun.com>
- Update Distro
* Tue Oct 21 2003 - <michael.twomey@sun.com>
- Updated to 1.8.2.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Thu Jul 17 2003 - michael.twomey@sun.com
- Initial package
