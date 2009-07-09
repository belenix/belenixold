#
# spec file for package SUNWgnome-config
#
# includes module(s): GConf
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use gconf_64 = GConf.spec
%endif

%include base.inc
%use gconf = GConf.spec

Name:                    SUNWgnome-config
Summary:                 GNOME configuration framework
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config-root
Requires: SUNWlxml
Requires: SUNWgnome-component
Requires: SUNWlibpopt
Requires: SUNWdbus
Requires: SUNWdbus-glib
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-glib-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-base-libs-devel

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

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%gconf_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gconf.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%ifarch amd64 sparcv9
%gconf_64.build -d %name-%version/%_arch64
%endif

export EXTRA_LDFLAGS=""
%gconf.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%gconf_64.install -d %name-%version/%_arch64
%endif

%gconf.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_datadir}/man
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%ifarch amd64 sparcv9
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gconfd-2
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gconf-sanity-check-2
%endif

rm -f $RPM_BUILD_ROOT%{_bindir}/gconf-merge-tree

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/GConf-%{gconf.version} README
%doc(bzip2) -d %{base_arch}/GConf-%{gconf.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gconftool-2
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgconf-2.so*
%{_libdir}/GConf/2/lib*.so
%{_libexecdir}/gconf-sanity-check-2
%{_libexecdir}/gconfd-2
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/gconf-merge-tree
%{_bindir}/%{_arch64}/gconftool-2
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libgconf-2.so*
%{_libdir}/%{_arch64}/GConf/2/lib*.so
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1
%{_datadir}/sgml/gconf/gconf-1.0.dtd
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%config %{_sysconfdir}/gconf

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Mar 24 2009 - jeff.cai@sun.com
- Since /usr/lib/amd64/pkgconfig/gconf-2.0.pc (SUNWgnome-config-devel)
  requires /usr/lib/amd64/pkgconfig/glib-2.0.pc which is found in
  SUNWgnome-base-libs-devel, add the dependency.
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Fri Sep 19 2008 - dave.lin@sun.com
- Set attribute of /usr/share/doc in base pkg %files section.
* Mon Sep 15 2008 - christian.kelly@sun.com
- Remove /usr/share/doc from %files.
* Wed Sep 10 2008 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Wed Aug 06 2008 - dermot.mccluskey@sun.com
- Bug 6703986 : Remove references to /usr/lib/ST/64
* Wed Jun 04 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWdbus and SUNWdbus-bindings for GConf 2.23.1. Update
  %files for dbus files.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Tue Jul 03 2007 - damien.carbery@sun.com
- Remove %{_datadir}/GConf from %files as it is no longer installed.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Thu Jun 29 2006 - laca@sun.com
- don't include gconf-merge-tree.  Now that we're only using the merged
  data, gconf-merge-tree can only cause trouble
* Thu Jun 22 2006 - damien.carbery@sun.com
- Correct LDFLAGS64 to use %{_arch64} and move sparc-specific settings to
  a %ifarch sparcv9 section.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Sep 20 2005 - laca@sun.com
- delete unpackaged files or add them to %files
* Tue Sep 06 2005 - laca@sun.com
- fix the 64-bit build
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : sman3/4 files should be in a separate devel package
* Tue Aug 24 2004 - laca@sun.com
- set all files in /etc/gconf to volatile, fixes 5090975
* Sun Aug 22 2004 - laca@sun.com
- fix dependencies: don't depend on -devel pkgs
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Mon Jul 05 2004 - damien.carbery@sun.com
- Add BuildRequires: SUNWgnome-base-libs-devel
* Sat Jun 26 2004 - shirley.woo@sun.com
- Changed install location to /usr/...
* Thu May 27 2004 - laca@sun.com
- added l10n subpkg
* Thu May 05 2004 - brian.cameron@sun.com
- removed aclocal files from share since they were already
  in devel-share.
* Sun Apr 04 2004 - laca@sun.com
- added some missing files to %files
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Jan 26 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
