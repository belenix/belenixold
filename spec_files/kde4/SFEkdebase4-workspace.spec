#
# spec file for package SFEkdebase-workspace
#
# includes module(s): kdebase-workspace
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdebase-workspace
%define python_version   2.6
%define _sessionsdir %{_datadir}/xsessions

Name:                    SFEkdebase4-workspace
Summary:                 Libraries for PIM data management in KDE4
Version:                 4.3.1
License:                 LGPLv2+
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdebase-workspace-%{version}.tar.bz2
Source1:                 kde.desktop
Source2:                 kdm.xml
Source3:                 kdmrc
Patch1:                  kdebase-workspace-01-kdm.diff
Patch2:                  kdebase-workspace-02-kwin.diff
Patch3:                  kdebase-workspace-03-startkde.diff
Patch4:                  kdebase-workspace-04-krdb.diff
Patch5:                  kdebase-workspace-05-ck-shutdown.diff
Patch6:                  kdebase-workspace-06-klipper-url.diff
Patch7:                  kdebase-workspace-07-plasma-konsole.diff
Patch8:                  kdebase-workspace-08-default_applets.diff
Patch9:                  kdebase-workspace-09-pykde4.diff
Patch13:                 kdebase-workspace-13-rootprivs.diff
Patch14:                 kdebase-workspace-14-timedate-kcm.diff
Patch15:                 kdebase-workspace-15-fadeeffect.cpp.diff
Patch16:                 kdebase-workspace-16-polkit_pid_t.diff
Patch17:                 kdebase-workspace-17-checkpass_pam.diff
# 
# Ksysguard port.
#
Patch18:                 kdebase-workspace-18-ksysguard.diff

# Fix screen unlocking issue.
Patch19:                 kdebase-workspace-19-lockdlg.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEqimageblitz
Requires:      SFEkdelibs4
Requires:      SFEkdepimlibs4
Requires:      SFEsoprano
Requires:      SFElibcaptury
Requires:      SFEgoogle-gadgets
Requires:      SUNWPython26
Requires:      SUNWglib2
Requires:      SUNWxwplt
Requires:      SFEkdebase4-runtime
Requires:      SFEqedje
Requires:      SFEpython26-pykde4
Requires:      SFElibxklavier
Requires:      SUNWdbus
Requires:      SUNWxorg-client-programs
Requires:      SUNWlibusb
Requires:      SFEconsolekit
Requires:      SFEpolicykit
Requires:      SFEpolkit-qt4
Requires:      SFEksysguard-daemon
BuildRequires: SFEqt4-devel
BuildRequires: SFEqimageblitz-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEsoprano-devel
BuildRequires: SFElibcaptury
BuildRequires: SUNWglib2-devel
BuildRequires: SFEgoogle-gadgets-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SFEkdebase4-runtime
BuildRequires: SFEqedje-devel
BuildRequires: SFEpython26-pykde4-devel
BuildRequires: SFElibxklavier-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWsfwhea
BuildRequires: SFEconsolekit-devel
BuildRequires: SFEpolicykit-devel
BuildRequires: SFEpolkit-qt4-devel
BuildRequires: SFExmms1-devel
Conflicts:     SFEkdebase3
BuildConflicts: SFEkdebase3-devel
Conflicts:     SFEkdmtheme

%description
The KDE Workspace is essentially the desktop of KDE 4.

%package -n SFEksysguard-daemon
Summary:                 KDE 4 System Monitoring Daemon.
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEqimageblitz-devel
Requires: SFEkdelibs4-devel
Requires: SFEkdepimlibs4-devel
Requires: SFEautomoc
Requires: SFEcmake
Requires: SFEsoprano-devel
Requires: SFElibcaptury
Requires: SUNWglib2-devel
Requires: SFEgoogle-gadgets-devel
Requires: SUNWPython26-devel
Requires: SFEkdebase4-runtime
Requires: SFEqedje-devel
Requires: SFEpython26-pykde4-devel
Requires: SFElibxklavier-devel
Requires: SUNWdbus-devel
Requires: SUNWsfwhea
Requires: SFEconsolekit-devel
Requires: SFEpolicykit-devel
Requires: SFExmms1-devel
Conflicts: SFEkdebase3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch13 -p1
%patch14 -p0
%patch15 -p1
%patch16 -p1
%patch17 -p0
%patch18 -p1
%patch19 -p1
cd ..

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
export JAVA_HOME=%{_prefix}/java
OPATH=${PATH}

mkdir -p kdebld
cd kdebld

#
# SFE paths are needed for libusb
#
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -DSOLARIS -DUSE_SOLARIS"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -DSOLARIS -DUSE_SOLARIS"
export LDFLAGS="-L%{_libdir}/polkit -R%{_libdir}/polkit %_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_libdir}/polkit/pkgconfig:%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{_libdir}/polkit:%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"

cmake   ../%{src_dir}-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DDBUS_INTERFACES_INSTALL_DIR=%{_datadir}/dbus-1/interfaces     \
        -DDBUS_SERVICES_INSTALL_DIR=%{_datadir}/dbus-1/services         \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DLIBUSB_INCLUDE_DIR:PATH=%{sfw_inc}                            \
        -DLIBUSB_LIBRARIES:FILEPATH=%{sfw_lib}/libusb.so                \
        -DBUILD_SHARED_LIBS=On                                          \
        -DKDE4_ENABLE_HTMLHANDBOOK=On                                   \
        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT
OPATH=${PATH}
cd kdebld
export PATH="%{qt4_bin_path}:${OPATH}"
make install DESTDIR=$RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages

install -d $RPM_BUILD_ROOT%{_sessionsdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sessionsdir}

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/application/graphical-login
cp %{SOURCE2} $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/application/graphical-login

install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kapplications-merged
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_datadir}/config/kdm/

export PATH="${OPATH}"
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin) %{_bindir}/genkdmconf
%attr (0755, root, bin) %{_bindir}/kaccess
%attr (0755, root, bin) %{_bindir}/kapplymousetheme
%attr (0755, root, bin) %{_bindir}/kblankscrn.kss
%attr (0755, root, bin) %{_bindir}/kcheckrunning
%attr (0755, root, bin) %{_bindir}/kcminit
%attr (0755, root, bin) %{_bindir}/kcminit_startup
%attr (0755, root, bin) %{_bindir}/kdm
%attr (0755, root, bin) %{_bindir}/kdmctl
%attr (0755, root, bin) %{_bindir}/kdostartupconfig4
%attr (0755, root, bin) %{_bindir}/kfontinst
%attr (0755, root, bin) %{_bindir}/kfontview
%attr (0755, root, bin) %{_bindir}/klipper
%attr (0755, root, bin) %{_bindir}/kmenuedit
%attr (0755, root, bin) %{_bindir}/krandom.kss
%attr (0755, root, bin) %{_bindir}/krandrtray
%attr (0755, root, bin) %{_bindir}/krdb
%attr (0755, root, bin) %{_bindir}/krunner
%attr (0755, root, bin) %{_bindir}/ksmserver
%attr (0755, root, bin) %{_bindir}/ksplashsimple
%attr (0755, root, bin) %{_bindir}/ksplashx
%attr (0755, root, bin) %{_bindir}/ksplashx_scale
%attr (0755, root, bin) %{_bindir}/kstartupconfig4
%attr (0755, root, bin) %{_bindir}/ksysguard
%attr (0755, root, bin) %{_bindir}/ksystraycmd
%attr (0755, root, bin) %{_bindir}/kwin
%attr (0755, root, bin) %{_bindir}/kwin_killer_helper
%attr (0755, root, bin) %{_bindir}/kwin_rules_dialog
%attr (0755, root, bin) %{_bindir}/kwrited
%attr (0755, root, bin) %{_bindir}/kxkb
%attr (0755, root, bin) %{_bindir}/plasma-desktop
%attr (0755, root, bin) %{_bindir}/plasma-overlay
%attr (0755, root, bin) %{_bindir}/plasmaengineexplorer
%attr (0755, root, bin) %{_bindir}/plasmawallpaperviewer
%attr (0755, root, bin) %{_bindir}/plasmoidviewer
%attr (0755, root, bin) %{_bindir}/polkit-kde-authorization
%attr (0755, root, bin) %{_bindir}/safestartkde
%attr (0755, root, bin) %{_bindir}/setscheduler
%attr (0755, root, bin) %{_bindir}/solid-action-desktop-gen
%attr (0755, root, bin) %{_bindir}/startkde
%attr (0755, root, bin) %{_bindir}/systemsettings
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*.so
%dir %attr (0755, root, bin) %{_libdir}/kde4/plugins
%{_libdir}/kde4/plugins/*
%dir %attr (0755, root, bin) %{_libdir}/kde4/libexec
%attr (4755, root, bin) %{_libdir}/kde4/libexec/kcheckpass
%attr (0755, root, bin) %{_libdir}/kde4/libexec/kcmdatetimehelper
%attr (0755, root, bin) %{_libdir}/kde4/libexec/kdm_config
%attr (0755, root, bin) %{_libdir}/kde4/libexec/kdm_greet
%attr (0755, root, bin) %{_libdir}/kde4/libexec/kfontprint
%attr (0755, root, bin) %{_libdir}/kde4/libexec/kio_fonts_helper
%attr (0755, root, bin) %{_libdir}/kde4/libexec/krootimage
%attr (0755, root, bin) %{_libdir}/kde4/libexec/kscreenlocker
%attr (0755, root, bin) %{_libdir}/kde4/libexec/polkit-kde-manager
%attr (0755, root, bin) %{_libdir}/kde4/libexec/test_kcm_xinerama
%dir %attr (0755, root, bin) %{_libdir}/strigi
%{_libdir}/strigi/*
%dir %attr (0755, root, bin) %{_libdir}/KDE4Workspace-%{version}
%{_libdir}/KDE4Workspace-%{version}/*
%dir %attr (0755, root, other) %{_libdir}/kconf_update_bin
%{_libdir}/kconf_update_bin/*

%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages/PyKDE4
%{_libdir}/python%{python_version}/vendor-packages/PyKDE4/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*
%dir %attr (0755, root, bin) %{_datadir}/sounds
%{_datadir}/sounds/*
%dir %attr (0755, root, bin) %{_datadir}/xsessions
%{_datadir}/xsessions/*

%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*rc
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/menus
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/menus/kapplications-merged

%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/graphical-login
%class(manifest) %{_localstatedir}/svc/manifest/application/graphical-login/kdm.xml

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/wallpapers
%{_datadir}/wallpapers/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*

%files -n SFEksysguard-daemon
%attr (4755, root, bin) %{_bindir}/ksysguardd
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Nov 08 2009 - Moinak Ghosh
- Fix screen unlocking issue.
* Mon Sep 28 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial port of Ksysguard.
- make ksysguardd set-uid.
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Make some executables set-uid.
- Fix policykit dependency and add PAM patch from KDE-Solaris repo.
- Update KDM configuration.
* Sat Sep 19 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Changes for upreving to KDE 4.3.1
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Rebuild with Solaris build flags.
- Add KDM SMF Manifest.
- Add dependency on ConsoleKit.
* Wed Jun 17 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
