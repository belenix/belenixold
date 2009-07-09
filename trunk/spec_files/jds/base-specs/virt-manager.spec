#
# spec file for package virt-manager
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
# bugdb: bugzilla.redhat.com
#
Name:         virt-manager
Summary:      Virtual Machine Manager
Version:      0.4.0
Release:      1
License:      GPL v2, FDL v1.1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Group:        System/GUI/GNOME
Source:       http://virt-manager.et.redhat.com/download/sources/virt-manager/%{name}-%{version}.tar.gz
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://virt-manager.et.redhat.com

# date:2006-12-08 owner:dermot type:bug bugster:6530450
Patch1:       virt-manager-01-build-flags.diff

# date:2007-03-09 owner:dermot type:bug bugster:6530453 state:upstream into new version in Fedora
Patch2:       virt-manager-02-serial-console.diff

# date:2007-08-16 owner:fujiwara type:bug bugster:6526323 bugzilla:229324
Patch3:       virt-manager-03-g11n-desktop.diff

# This patch is mainly including some temporary patch to make virt-manager run with current xVM
# date:2008-02-15 owner:henryz type:feature
Patch4:       virt-manager-04-temporary-patch.diff

# date:2008-02-16 owner:henryz type:bug bugster:6664159 state:upstream into new version in Fedora
Patch5:       virt-manager-05-host-about.diff

# date:2008-03-04 owner:henryz type:bug bugster:6665415 state:upstream into new version in Fedora
# this fix has been in the trunk.
Patch6:       virt-manager-06-delete-button.diff

# date:2008-11-05 owner:fujiwara type:feature
Patch7:       virt-manager-07-build.diff
%description
Virtual Machine Manager

%prep
%setup -q -n %name-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1


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

intltoolize --automake -c -f
# for intltool 0.40.4
touch po/POTFILES.in

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I ./m4
libtoolize --force
automake
autoconf
./configure   --prefix=%{_prefix}          \
              --sysconfdir=%{_sysconfdir}  \
              --libexecdir=%{_libexecdir}
make -j $CPUS


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
rm $RPM_BUILD_ROOT%{_libdir}/virt-manager/*.la
rm $RPM_BUILD_ROOT%{_libdir}/virt-manager/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_libdir}/virt-manager
%{_libdir}/virt-manager/*
%{_datadir}/virt-manager
%{_datadir}/virt-manager/*
%{_datadir}/locale/*
%{_bindir}/virt-manager
%{_libexecdir}/virt-manager-launch

%changelog
* Tue Mar 24 2009 - dave.lin@sun.com
- Use automake, aclocal 1.10 instead of 1.9 to fix undefined macro _AM_SUBST_NOTMAKE issue.
* Wed Nov 05 2008 - takao.fujiwara@sun.com
- Add virt-manager-07-build.diff. GNU Makefile is used.
* Fri May 16 2008 - hua.zhang@sun.com
- Change the patch state to upstream
* Fri Mar 21 2008 - hua.zhang@sun.com
- Add new patches to make it run at Solaris
* Thu Aug 16 2007 - takao.fujiwara@sun.com
- Add virt-manager-03-g11n-i18n-desktop.diff to localize .desktop file.
  Fixes 6526323
* Tue May 22 2007 - dermot.mccluskey@sun.com
- bump to version 0.4.0
* Mon Apr  2 2007 - laca@sun.com
- add missing aclocal call and force using automake 1.9
* Mon Mar 12 2007 - laca@sun.com
- delete .la file
* Fri Mar 09 2007 - dermot.mccluskey@sun.com
- added patch 2 for Serial Console on Solaris
* Mon Mar 05 2007 - dermot.mccluskey@sun.com
- Bump to ver 0.3.1
* Fri Man 02 2007 - dermot.mccluskey@sun.com
- Add bug id for patch #1
* Fri Jan 12 2007 - dermot.mccluskey@sun.com
- Use libtool to set PIC option
* Wed Jan 10 2007 - dermot.mccluskey@sun.com
- fixes from code review:
  handle GConf schemas properly;
  use %{_libexecdir};
  move patch 01 to linux spec file
* Fri Dec 8 2006 - dermot.mccluskey@sun.com
- Initial version.
