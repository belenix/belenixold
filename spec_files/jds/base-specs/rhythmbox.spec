#
# spec file for package rhythmbox
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:         rhythmbox
License:      GPL v2, MIT, BSD
Group:        System/GUI/GNOME
Version:      0.12.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Rhythmbox Multimedia Player
Source:       http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/0.12/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
#owner:jerrytan date:2008-01-16 type:bug bugzilla:509846
Patch1:       rhythmbox-01-playcd.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define	libgnomeui_version			2.6.0
%define	gstreamer_version               	0.8.1
%define gstreamer_plugins_version       	0.8.1
%define gnome_desktop_version                   2.6.1

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       gstreamer >= %{gstreamer_version}
Requires:       gstreamer-plugins >= %{gstreamer_plugins_version}
Requires:       gnome-desktop >= %{gnome_desktop_version}
Requires:       iso-codes
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-devel >= %{gstreamer_plugins_version}
BuildRequires:  gnome-desktop-devel >= %{gnome_desktop_version}

%description
Rhythmbox is an integrated music management application

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

export PYTHON=/usr/bin/python%{pythonver}

if test "x$x_includes" = "x"; then
 x_includes="/usr/X11/include"
fi

if test "x$x_libraries" = "x"; then
 x_libraries="/usr/X11/lib"
fi

intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

libtoolize --force
## FIXME: Swap aclocal dir order to pick up gnome-doc-utils.m4 in 'macros'.
##aclocal $ACLOCAL_FLAGS -I ./macros
aclocal -I ./macros $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

export MOZILLA_PLUGINDIR="%{_libdir}/firefox/plugins"
# --with-ipod requires that gtkpod be installed or configure will fail.
CFLAGS="$RPM_OPT_FLAGS"	\
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
	--libexecdir=%{_libexecdir} \
	--mandir=%{_mandir}         \
	--localstatedir=/var/lib    \
	--disable-daap              \
	--disable-browser-plugin    \
	--enable-gstreamer
#FIXME -j is breaking the build removing for now.
#make -j $CPUS
make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
rm $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins/*/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="totem.schemas totem-video-thumbnail.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_bindir}/*
%{_sysconfdir}/gconf/schemas
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/applications
%{_datadir}/gnome/help/totem/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/pixmaps/*

%changelog
* Thu Mar 12 2009 - brian.cameron@sun.com
- Set PYTHON environment variable in %build section.
* Wed Jan 07 2009 - takao.fujiwara@sun.com
- Add patch po.diff for zh_CN. SVN revision 6121.
* Thu Aug 21 2008 - jijun.yu@sun.com
- add --disable-browser-plugin option at configuring.
* Wed Jul 09 2008 - damien.carbery@sun.com
- Bump to 0.11.6.
* Wed Mar 26 2008 - brian.cameron@sun.com
- Bump to 0.11.5.
* Wed Mar 05 2008 - brian.cameron@sun.com
- Patch to fix linking with soup to avoid crash on startup.  Fixes #6671873.
* Thu Jan 31 2008 - damien.carbery@sun.com
- Add patch 05-libsoup to allow building with libsoup 2.3.x. Fixes #509701.
* Wed Jan 16 2008 - jerry.tan@sun.com
- Add patch for fix the bug that rhythmbox can not play CD. Fixes bugzilla
  509846.
* Thu Jan 10 2008 - damien.carbery@sun.com
- Add patch 03-mozilla-plugindir to allow specifying of mozilla plugin dir via
  MOZILLA_PLUGINDIR env var. Code copied from totem. Bug 508499.
* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 0.11.4. Remove upstream patch, 03-empty-dialog.
* Tue Dec 11 2007 - Irene.huang@sun.com
- Added patch rhythmbox-03-empty-dialog.diff
* Fri Nov 09 2007 - damien.carbery@sun.com
- Bump to 0.11.3.
* Wed Sep 26 2007 - brian.cameron@sun.com
- Call intltoolize so that the desktop file gets built.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Bump to 0.11.2.
* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 0.11.1.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 0.11.0.
* Mon May 28 2007 - irene.huang@sun.com	
- change patch -02-null-title to be branding
* Fri May 25 2007 - damien.carbery@sun.com
- Bump to 0.10.90.
* Tue Apr 24 2007 - irene.huang@sun.com
- Modify bug number for patch null-title.diff
* Mon Apr 02 2007 - damien.carbery@sun.com
- Bump to 0.10.0. Remove upstream patch, 03-wronglocking.
* Wed Mar 22 2007 - irene.huang@sun.com
- add patch rhythmbox-03-wronglocking.diff
* Wed Mar 14 2007 - irene.huang@sun.com
- add patch rhythmbox-02-null-title.diff.
* Mon Mar 12 2007 - laca@sun.com
- delete .la files
* Wed Feb 28 2007 - halton.huo@sun.com
- Remove patch 02-gnome-doc-utils since g-d-u is upgrade to 0.9.x.
* Thu Feb 22 2007 - damien.carbery@sun.com
- Add patch, 02-gnome-doc-utils, to create gnome-doc-utils.m4 in macros subdir.
  This is needed because g-d-u is too old (it's blocked waiting for docbook
  update). The dir order in the aclocal call is also reversed to pick up the
  new gnome-doc-utils.m4 before the (older) system one. When g-d-u is updated
  the patch can be removed and aclocal call restored.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 0.9.7. Remove upstream patch, rhythmbox-02-audiocd.diff.
- Remove code that deletes the .la/.a files as none are generated.
* Wed Oct 18 2006 - brian.cameron@sun.com
- Add rhythmbox-02-audiocd.diff to fix linking of audiocd plugin
  to include nautilus-burn library.  Without this, rhythmbox fails
  to start.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Remove 'rm' line from %install as the files listed are not installed.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 0.9.6.
- Remove '-f' from 'rm' calls to force failure when source changes need
  attention.
* Fri Sep 15 2006 - brian.cameron@sun.com
- Remove patch 2, no longer needed.
* Wed Jun 21 2006 - brian.cameron@sun.com
- Bump to 0.9.5.
* Mon May 01 2006 - brian.cameron@sun.com
- Add patch to fix compile issue that appears when building with HAL.
* Wed Apr 26 2006 - damien.carbery@sun.com
- Removed upstream patch rhythmbox-01-fixcompile.diff.
* Tue Apr 25 2006 - damien.carbery@sun.com
- Bump to 0.9.4.1.
* Tue Apr 18 2006 - damien.carbery@sun.com
- Bump to 0.9.4.
* Wed Apr  5 2006 - damien.carbery@sun.com
- Remove --with-ipod option as gtkpod is not in build.
* Mon Mar 20 2006 - Brian.Cameron@sun.com
- Created
