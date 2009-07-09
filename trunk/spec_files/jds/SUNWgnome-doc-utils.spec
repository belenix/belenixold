#
# spec file for package SUNWgnome-doc-utils
#
# includes module(s): gucharmap
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

%use gnomedocutils = gnome-doc-utils.spec

Name:                    SUNWgnome-doc-utils
Summary:                 GNOME documentation utilities
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-common-devel
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWPython
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWlxsl-devel

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
%gnomedocutils.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
%gnomedocutils.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnomedocutils.install -d %name-%version

# HACK.
if [ -d $RPM_BUILD_ROOT%{_libdir}/locale ]; then
  mv $RPM_BUILD_ROOT%{_libdir}/locale $RPM_BUILD_ROOT%{_datadir}
fi

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnome-doc-prepare
%{_bindir}/gnome-doc-tool
%{_bindir}/xml2po
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-doc-utils
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help
%{_datadir}/omf
%{_datadir}/xml
%{_datadir}/xml2po
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- stop using postrun
* Wed Jul 23 2008 - damien.carbery@sun.com
- Modify hack because %{_libdir}/locale is installed on svn_91 but not snv_93.
* Sun Mar 16 2008 - damien.carbery@sun.com
- Add hack back in to get build going again. Will split 'glib' out of
  SUNWgnome-base-specs.spec at a later date.
* Fri Mar 14 2008 - damien.carbery@sun.com
- Remove hack - call aclocal/automake/autoconf in the base spec file.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Add hack to move locale files from %{_libdir} to %{_datadir}.
* Thu Nov 15 2007 - damien.carbery@sun.com
- Add BuildRequires SUNWlxml-devel and SUNWlxsl-devel.
* Thu Oct 11 2007 - damien.carbery@sun.com
- Remove duplicate %{_datadir} line and second %defattr.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Move -devel package into base package as the module is only used during
  building.
* Thu Aug 23 2007 - laca@sun.com
- don't delete lib/locale in %install -- this is now fixed in the base spec
- delete $RPM_BUILD_ROOT in %install
* Mon May 14 2007 - damien.carbery@sun.com
- Add SUNWgnome-common-devel dependency for pkg-config.
* Fri May 11 2007 - damien.carbery@sun.com
- Remove unnecessary SUNWgnome-libs dependency. Builds okay without it.
* Wed Apr 11 2007 - damien.carbery@sun.com
- Add l10n package after bumping tarball.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Add %{_bindir}/gnome-doc-tools from new tarball.
* Fri Sep 08 2006 - Matt.Keenan@sun.com
- Remove "rm" of _mandir during %install, deliver xml2po.1 community man page
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Fri Aug 11 2006 - damien.carbery@sun.com
- Remove %{_libdir}/locale files because I don't want to create a l10n pkg.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Wed Oct 19 2005 - damien.carbery@sun.com
- Add SUNWPython dependency as xml2po uses python.
* Wed Jul 06 2005 - laca@sun.com
- remove mandir from %files, it's not there
- remove l10n subpkg, there's no l10n content
* Mon Jul 04 2005 - matt.keenan@sun.com
- Initial spec file needed by SUNWgnome-help-viewer (yelp)
