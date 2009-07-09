#
# spec file for package SUNWcheese
#
# includes module(s): cheese
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine 
#

%include Solaris.inc
%define source_name cheese

Name:                    SUNWcheese
Summary:                 Cheese - GNOME application for taking photos and videos from a webcam
#### DO NOT BUMP TO 2.24.x AS IT DEPENDS ON HAL v4l backend
#### NOT YET READY FOR SOLARIS
Version:                 2.23.90
Source:                  http://ftp.gnome.org/pub/GNOME/sources/cheese/2.23/cheese-%{version}.tar.gz

# owner:elaine date:2008-09-01 type:bug bugster:6657549
Patch1:                  cheese-01-lack-hal-backend.diff

# owner:elaine date:2008-09-01 type:bug bugster:6743364
Patch2:                  cheese-02-lack-uvc-framerate.diff

# owner:elaine date:2008-09-01 type:bug bugzilla:549804
Patch3:                  cheese-03-thumbnail-create.diff

URL:                     http://live.gnome.org/Cheese
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Source1:                 %{name}-manpages-0.1.tar.gz

Requires: SUNWgnome-base-libs
Requires: SUNWgnome-media
Requires: SUNWgnome-vfs
Requires: SUNWcheese-root
Requires: SUNWdbus
Requires: SUNWevolution-data-server
Requires: SUNWgnome-config
Requires: SUNWhal
Requires: SUNWlibrsvg
Requires: SUNWxwrtl
Requires: SUNWdesktop-cache
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWevolution-data-server-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWhal
BuildRequires: SUNWlibrsvg-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWgnome-config

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd %{source_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
cd %{source_name}-%{version}

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} 

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{source_name}-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/cheese/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/cheese/cheese-[a-z]*.omf
%endif

#install man page
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT


%post
%restart_fmri gconf-cache desktop-mime-cache icon-cache mime-types-cache

%postun
%restart_fmri desktop-mime-cache mime-types-cache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/cheese
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/cheese
%{_libdir}/cheese/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/cheese
%{_datadir}/cheese/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/cheese/C
%{_datadir}/omf/cheese/cheese-C.omf
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/org.gnome.Cheese.service
%doc -d cheese-%{version} AUTHORS
%doc(bzip2) -d cheese-%{version} ChangeLog NEWS COPYING
%dir %attr (0755, root, other) %{_datadir}/doc


%files root
%defattr (-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/cheese.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/cheese/[a-z]*
%{_datadir}/omf/cheese/cheese-[a-z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Feb 10 2009 - halton.huo@sun.com
- Add dependency on SUNWlibrsvg, CR #6755918
* Sun Sep 21 2008 - christian.kelly@sun.com
- Fix typo from previous.
* Sat Sep 20 2008 - christian.kelly@sun.com
- Added BuildRequires SUNWlibsrvg-devel.
* Fri Sep 19 2008 - elaine.xiong@sun.com
- Assign attribute to shared folders.
* Tue Sep 16 2008 - elaine.xiong@sun.com
- Add %doc to %files for new copyright.
* Mon Sep 08 2008 - elaine.xiong@sun.com
- Create from SFEcheese.spec. Upgrade to 2.23.90.
- Add patch cheese-01-lack-hal-backend.diff.
- Add patch cheese-02-lack-uvc-framerate.diff
- Add patch cheese-03-thumbnail-create.diff
