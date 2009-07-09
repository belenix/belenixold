#
# spec file for package SUNWgnome-a11y-mousetweaks
#
# includes module(s): mousetweaks
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#
# We have removed mousetweaks from our builds since it is GPLv3.
# For now, leave in the following comment so that our ARC scripts
# recognize that we are not shipping this module starting with
# the 2.24 release.  When we re-integrate this package, remove
# the following line:
# PACKAGE NOT INCLUDED IN GNOME UMBRELLA ARC
#

%include Solaris.inc
%use mousetweaks = mousetweaks.spec

Name:                    SUNWgnome-a11y-mousetweaks
Summary:                 provided mouse accessibility enhancements
Version:                 %{mousetweaks.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-applets
Requires: SUNWgnome-panel
Requires: SUNWgnome-a11y-libs
Requires: SUNWdbus-glib
Requires: SUNWgnome-libs
Requires: SUNWdesktop-cache
Requires: %{name}-root

BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-a11y-libs-devel
BuildRequires: SUNWdbus-glib-devel
BuildRequires: SUNWgnome-libs-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n content
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%mousetweaks.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%mousetweaks.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%mousetweaks.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/mousetweaks
%doc -d mousetweaks-%{mousetweaks.version} README AUTHORS
%doc(bzip2) -d mousetweaks-%{mousetweaks.version} COPYING.GPL COPYING.FDL NEWS ChangeLog src/mt-pidfile.c
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/*
%{_datadir}/omf/mousetweaks/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/mousetweaks.schemas
%{_sysconfdir}/gconf/schemas/pointer-capture-applet.schemas

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Thu Oct 30 2008 - yue.wang@sun.com
- Remove the original manpages, and add new manpages.
* Thu Oct 30 2008 - li.yuan@sun.com
- Add copyright information.
* Fri Sep 05 2008 - christian.kelly@sun.com
- Fixed %files, added /usr/share/omf/mousetweaks dir. 
* Thu Jun 12 2008 - li.yuan@sun.com
- Add missing dependency on the %{name}-root pacakge.
* Mon Mar 31 2008 - li.yuan@sun.com
- Add copyright file
* Mon Feb 04 2008 Li Yuan <li.yuan@sun.com>
- Remove mfversion patch and use autoconf/automake to avoid
  build errors. Remove some unnecessary script.
* Tue Jan 29 2008 Li Yuan <li.yuan@sun.com>
- Initial version.
