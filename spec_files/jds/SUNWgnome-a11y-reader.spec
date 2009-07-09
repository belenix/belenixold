#
# spec file for package SUNWgnome-a11y-reader
#
# includes module(s): orca
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dcarbery
#
%include Solaris.inc
%use orca = orca.spec

Name:              SUNWgnome-a11y-reader
Summary:           Orca screen reader/magnifier
Version:           %{default_pkg_version}
Source:            %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
# obsoletes SUNWgnome-orca:
Requires: SUNWgnome-python-libs
Requires: SUNWjdsrm
Requires: SUNWPython
Requires: SUNWgnome-base-libs
Requires: SUNWbash
Requires: SUNWdesktop-cache
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-python-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%orca.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export PYTHON="/usr/bin/python"
export CPPFLAGS="-I/usr/include/python2.4"
export CFLAGS="%optflags -I%{_includedir} -I/usr/include/python2.4"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%orca.build -d %name-%version

%install
%orca.install -d %name-%version
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
%restart_fmri icon-cache desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d orca-%{orca.version} README AUTHORS
%doc(bzip2) -d orca-%{orca.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/orca
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/orca.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/orca.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/orca.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/orca.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/orca.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/orca.svg
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/orca.desktop
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Apr  4 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Sep 19 2008 - li.yuan@sun.com
- Added %doc to %files for copyright.
* Thu Apr 03 2008 - damien.carbery@sun.com
- Add SUNW_Copyright.
* Mon Nov 05 2007 - li.yuan@sun.com
- Use icon-cache.script for %post
* Thu Sep 27 2007 - laca@sun.com
- delete some unnecessary env variables
* Wed Aug 01 2007 - damien.carbery@sun.com
- Add new icons to %files.
* Mon Feb 05 2007 - damien.carbery@sun.com
- Add Requires SUNWbash after check-deps.pl run.
* Tue Dec 12 2006 - takao.fujiwara@sun.com
- Uncomment out l10n locale dir. Fixes 6499543.
* Wed Nov 15 2006 - damien.carbery@sun.com
- Use %{default_pkg_version} instead of orca.version.
* Mon Sep 11 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Tue Aug 22 2006 - damien.carbery@sun.com
- Update %files after bump to 0.9.0.
* Wed Aug 16 2006 - damien.carbery@sun.com
- Comment out 'orca' dir until build issues with 0.2.[5-8] are resolved.
* Fri Jun 16 2006 - damien.carbery@sun.com
- Add %{_datadir}/orca to %files for new tarball.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu Feb 23 2006 - william.walker@sun.com
- Update to orca-0.2.1
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Nov 30 2005 - william.walker@sun.com
- Update to orca-0.2.0
* Thu Oct 27 2005 - laca@sun.com
- rename to SUNWgnome-a11y-orca
- move to vendor-packages from site-packages
* Tue Sep 20 2005 - laca@sun.com
- move to /usr as Python was also moved there
* Thu Sep 15 2005 - laca@sun.com
- define l10n subpkg; update to keep locale stuff in /usr/share
* Mon Aug 29 2005 - rich.burridge@sun.com
- Adjusted to put files under /usr/sfw
* Thu Aug 25 2005 - rich.burridge@sun.com
- Removed the 'export CC="/opt/SUNWspro/bin/cc"' line. No longer needed.
* Mon Aug 15 2005 - rich.burridge@sun.com
- initial version
