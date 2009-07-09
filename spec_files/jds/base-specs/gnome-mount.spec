#
# spec file for package gnome-volume-manager
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen
Name:         gnome-mount
License:      GPL
Group:        System/GUI/GNOME
# Note: HAL may need to be bumped before gnome-mount.
Version:      0.4
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Programs for mounting, unmounting and ejecting storage devices.
Source:       http://people.freedesktop.org/~david/dist/gnome-mount-%{version}.tar.gz
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# This patch addresses two separate Sun-specific bugs which are both upstream.
# Note that bugster bug #6790821 is not fully resolved with the patch, so that
# bug is not yet fixed.  However, backporting some code from upstream did
# improve the situation significantly so this patch partially addresses this
# bug.
#owner:yippi date:2006-06-20 type:bug bugzilla:400499 bugster:6790821 state:upstream
Patch1:       gnome-mount-01-sun-patch.diff
URL:          www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}
Autoreqprov:  on
Prereq:       /usr/sbin/groupadd
Prereq:       /usr/sbin/useradd
Prereq:       /sbin/nologin
Prereq:       sed
Prereq:       coreutils

%description
Handles mount/umount/eject by using HAL.

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

export CFLAGS="$RPM_OPT_FLAGS"
autoheader
autoconf
libtoolize --force
glib-gettextize -c -f
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -a -c -f
%ifos solaris
ENABLE_MULTIUSER=--enable-multiuser=no
%else
ENABLE_MULTIUSER=--enable-multiuser=yes
%endif 

./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=/var/lib \
	--mandir=%{_mandir} \
	--libexecdir=%{_libexecdir} $ENABLE_MULTIUSER
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

cd $RPM_BUILD_ROOT%{_bindir}

# Build symlinks as relative instead of full path.
#
rm -rf gnome-umount
rm -fr gnome-eject
ln -s gnome-mount gnome-umount
ln -s gnome-mount gnome-eject

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-volume-manager.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%config %attr(-,gdm,gdm) %{_sysconfdir}/X11/gdm
%config %attr(-,root,root) %{_sysconfdir}/X11/dm
%{_datadir}/locale/*/LC_MESSAGES/gdm*.mo
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/gtk-2.0/modules/*.so
%{_libexecdir}/*
%{_datadir}/gdm
%{_datadir}/applications/*
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/faces/*.jpg
%{_datadir}/pixmaps/faces/*.png
%{_datadir}/icons
%{_datadir}/gnome/help/*
%{_datadir}/xsessions/*
%{_mandir}/man1/*
%{_datadir}/omf/*
%attr(-,gdm,gdm) /var/lib/gdm
%config /etc/pam.d/*
%config /etc/security/*

%changelog
* Wed Apr 01 2009 - brian.cameron@sun.com
- Merge both upstream Sun-specific patches into one patch.
* Fri Feb 20 2009 - brian.cameron@sun.com
- Add patch gnome-mount-02-fixdelay.diff.  This patch is from upstream, and
  helps to ensure that gnome-mount waits for mount operations to complete.
* Tue Jun 20 2006 - <brian.cameron@sun.com>
- Bump to 0.4 and add patch needed for Solaris support
* Wed May 03 2006 - <brian.cameron@sun.com>
- Created
