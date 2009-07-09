#
# spec file for package SUNWgnome-config-editor
#
# includes module(s): gconf-editor
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include Solaris.inc

%use gceditor = gconf-editor.spec

Name:                    SUNWgnome-config-editor
Summary:                 GNOME configuration database editor
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-config-editor-root
Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWlibpopt
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-config-devel
Requires: SUNWdesktop-cache

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

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
%gceditor.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"

%gceditor.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gceditor.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/var
rm -rf $RPM_BUILD_ROOT/var

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d gconf-editor-%{gceditor.version} README AUTHORS MAINTAINERS
%doc(bzip2) -d gconf-editor-%{gceditor.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gconf-editor/C
%{_datadir}/omf/gconf-editor/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/gconf-editor
%{_datadir}/gconf-editor/*
%attr (-, root, other) %{_datadir}/icons
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gconf-editor.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gconf-editor/[a-z][a-z]
%{_datadir}/gnome/help/gconf-editor/[a-z][a-z]_[A-Z][A-Z]
%{_datadir}/omf/gconf-editor/gconf-editor-[a-z][a-z].omf
%{_datadir}/omf/gconf-editor/gconf-editor-[a-z][a-z]_[A-Z][A-Z].omf
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Thu Oct 09 2008 - halton.huo@sun.com
- Remove %{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf if not use --with-l10n
* Tue Sep 30 2008 - padraig.obriain@sun.com
- Update copyright file.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Fix %files l10n.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Tue Dec 19 2006 - damien.carbery@sun.com
- Add l10n files to the l10n package.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Wed Aug 16 2006 - damien.carbery@sun.com
- Remove scrollkeeper files under /var. Remove missing help files from l10n 
  pkg.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables; set CFLAGS
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Jan 25 2006 - damien.carbery@sun.com
- Call gconf-merge-tree in %post to process /etc/gconf/gconf.xml.defaults in 
  root pkg. Add required SUNWpostrun dependency.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Add BuildRequires to avoid build errors.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Tue Sep 13 2005 - laca@sun.com
- define root subpkg, install gconf schemas, add unpackaged files to %files
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Wed Aug 25 2004  Kazuhiko.Maekawa@sun.com
- Added l10n help entries in files
* Tue Aug 24 2004  vinay.mandyakoppal@wipro.com
- Added %{_datadir}/gnome/help/gconf-editor/C to install help.
* Sun Jun 27 2004  shirley.woo@sun.com
- Added BuildRequires SUNWgnome-javahelp-convert
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Thu Feb 26 2004 - <niall.power@sun.com>
- define PERL5LIB for XML::Parser
- remove unnecessary CFLAGS definitions
- fix permissions of %{_mandir}
* Tue Feb 17 2004 - <niall.power@sun.com>
- Inital Solaris spec file created
