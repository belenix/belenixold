#
# spec file for package SUNWevolution-jescs
#
# includes module(s): evolution-jescs.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc
%use evojescs = evolution-jescs.spec
%define evo_major_version 2.26
%define evo_prefix /usr/lib/evolution

Name:          SUNWevolution-jescs
Summary:       Evolution connector for Sun JES Calendar Server
Version:       %{default_pkg_version}
SUNW_Category: EVO25,%{default_category}
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWevolution
Requires: SUNWjdsrm
Requires: SUNWgnome-base-libs
Requires: SUNWevolution-data-server
Requires: SUNWlibsoup
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SFEidnkit
Requires: SUNWdesktop-cache
BuildRequires: SUNWevolution-data-server-devel
BuildRequires: SUNWlibsoup-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SFEidnkit-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%evojescs.prep -d %name-%version

%build
#FIXME: symbol clash in the evo libraries means we can't use -Bdirect
#       should be re-enabled once these issues are fixed
export LD=/usr/ccs/bin/ld
export LDFLAGS="-z ignore %{?arch_ldadd} -L%{_libdir} -R%{_libdir} -L%{evo_prefix}/%{evo_major_version} -R%{evo_prefix}/%{evo_major_version}"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH="%_pkg_config_path"
%evojescs.build -d %name-%version

%install
%evojescs.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri icon-cache

%files
%doc -d evolution-jescs-%{evojescs.version} AUTHORS
%doc(bzip2) -d evolution-jescs-%{evojescs.version} ChangeLog
%doc(bzip2) -d evolution-jescs-%{evojescs.version} COPYING
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/*
%{_libdir}/evolution
%{_libdir}/evolution-data-server-*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/evolution-jescs
%{_datadir}/evolution
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Apr  4 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Nov 11 2008 - jedy.wang@sun.com
- Bump evo_major_version to 2.26.
* Fri Sep 19 2008 - christian.kelly@sun.com
- Set permissions on /usr/share/doc.
* Wed Sep 10 2008 - jedy.wang@sun.com
- Add new copyright files.
* Thu Aug 22 2008 - jedy.wang@sun.com
- Bump evo_major_version to 2.24.
  Update attribute of icon dirs.
* Tue Aug 19 2008 - jedy.wang@sun.com
- Add %post secion and ship new icons.
* Fri Oct  5 2007 - laca@sun.com
- add %{arch_ldadd} to LDFLAGS for GNU libiconv/libintl
* Fri May 18 2007 - damien.carbery@sun.com
- Shorten package name to fix WOS integration warning about pkg name length.
* Wed Nov 29 2006 - damien.carbery@sun.com
- Revert version to %{default_pkg_version} as this module has been integrated
  to Nevada with this version. Using the base module's version number (2.8.x)
  is lower than 2.16.x and will cause an integration error.
- Bump evo_major_version to 2.10 to match SUNWevolution.
* Mon Nov 27 2006 - jeff.cai@sun.com
- Use evolution-jescs's version information to replace default one. 
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Sun Jun 24 2006 - laca@sun.com
- change evo_major_version to 2.8.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - halton.huo@sun.com
- Change %defattr to (-, root, other).
- Remove unused -root package.
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Apr 13 2006 - halton.huo@sun.com
- Add /usr/lib/evolution/%{evo_major_version} to LDFLAGS, fix bug #6411728.
* Tue Apr 04 2006 - halton.huo@sun.com
- Alter remove .a/.la files part into linux spec.
* Thu Mar 30 2006 - halton.huo@sun.com
- Remove all *.a/*.la files.
* Thu Feb 23 2006 - damien.carbery@sun.com
- Use default pkg version to match other pkgs; add EVO25 to default category.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Jan 24 2006 - halton.huo@sun.com
- Remove hard code %{evojescs.eds_api_version}.
- Remove *.la under /usr/lib when install.
* Tue Jan 24 2006 - halton.huo@sun.com
- s/evolution-data-server-1.2/evolution-data-server-%evojescs.eds_api_version/g
* Wed Dec  7 2005 - laca@sun.com
- disable -Bdirect as due to symbol clashes
* Thu Dec  2 2005 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-base-libs/-devel-share for glib-gettextize.
* Thu Oct  6 2005 - damien.carbery@sun.com
- Add SUNWjdsrm dependency so that the obsolete SUNWevolution-socs-connect is 
  removed before this package is installed. They contain conflicting files.
* Tue Sep  6 2005 - halton.huo@sun.com
- Fix wrong Name.
- Fix evolution-jescs to evojescs.
- Change %files section.
* Fri Sep  2 2005 - halton.huo@sun.com
- Initial spec file

