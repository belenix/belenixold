#
# spec file for package SUNWgksu
#
# includes module(s): gksu libgksu libgksuui
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include Solaris.inc

%use gksu = gksu.spec
%use libgksu = libgksu.spec
%use libgksuui = libgksuui.spec
Name:                    SUNWgksu
Summary:                 Gksu CLI and libraries
Version:                 1.3.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-component-devel
Requires: SUNWgtk2
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-config
Requires: SUNWgnome-component

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files 
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

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
%libgksu.prep -d %name-%version
%libgksuui.prep -d %name-%version
%gksu.prep -d %name-%version

%build
export PKG_CONFIG_PATH=../libgksu1.2-%{libgksu.version}/libgksu:../libgksuui1.0-%{libgksuui.version}/libgksuui:%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir} -I%{_builddir}/%name-%version/libgksu1.2-%{libgksu.version}/libgksu -I%{_builddir}/%name-%version/libgksuui1.0-%{libgksuui.version}/libgksuui"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -L/usr/X11/lib -R/usr/X11/lib -L%{_builddir}/%name-%version/libgksu1.2-%{libgksu.version}/libgksu -L%{_builddir}/%name-%version/libgksuui1.0-%{libgksuui.version}/libgksuui"
%libgksu.build -d %name-%version
%libgksuui.build -d %name-%version
%gksu.build -d %name-%version

%install
%libgksu.install -d %name-%version
%libgksuui.install -d %name-%version
%gksu.install -d %name-%version

# -f used because charset alias doesn't seem to be created when using
# gnu libiconv/libintl
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm $RPM_BUILD_ROOT%{_bindir}/gksuexec
rm $RPM_BUILD_ROOT%{_bindir}/gksudo
rm $RPM_BUILD_ROOT%{_mandir}/man1/gksuexec.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/gksudo.1
rm $RPM_BUILD_ROOT%{_libdir}/libgksu1.2.a
rm $RPM_BUILD_ROOT%{_libdir}/libgksu1.2.la
rm $RPM_BUILD_ROOT%{_libdir}/libgksuui1.0.a
rm $RPM_BUILD_ROOT%{_libdir}/libgksuui1.0.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgksu1.2.so*
%{_libdir}/libgksu1.2/gksu-run-helper
%{_libdir}/libgksuui1.0.so*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/gksu*.1
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gksu*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/libgksuui1.0/gksu-auth.png
%attr (0755, root, other) %dir %{_datadir}/pixmaps
%{_datadir}/pixmaps/gksu*.png
%attr (0755, root, other) %dir %{_datadir}/applications
%{_datadir}/applications/gksu*.desktop
%doc gksu-%{gksu.version}/AUTHORS
%doc gksu-%{gksu.version}/README
%doc(bzip2) gksu-%{gksu.version}/COPYING
%doc(bzip2) gksu-%{gksu.version}/ChangeLog
%doc(bzip2) gksu-%{gksu.version}/po/ChangeLog
%doc libgksu1.2-%{libgksu.version}/AUTHORS
%doc(bzip2) libgksu1.2-%{libgksu.version}/COPYING
%doc(bzip2) libgksu1.2-%{libgksu.version}/ChangeLog
%doc(bzip2) libgksu1.2-%{libgksu.version}/po/ChangeLog
%doc libgksuui1.0-%{libgksuui.version}/AUTHORS
%doc(bzip2) libgksuui1.0-%{libgksuui.version}/COPYING
%doc(bzip2) libgksuui1.0-%{libgksuui.version}/ChangeLog
%doc(bzip2) libgksuui1.0-%{libgksuui.version}/po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0644, root, root) %{_sysconfdir}/gksu.conf

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libgksu1.2.pc
%{_libdir}/pkgconfig/libgksuui1.0.pc
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/libgksu1.2/gksu*.h
%{_includedir}/libgksuui1.0/gksuui*.h

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Sep 17 2008 - jim.li@sun.com
- Revised new format copyright file
* Wed Oct  3 2007 - laca@sun.com
- use rm -f to delete charset.alias/locale.alias because they do not get
  created in the indiana build
* Wed May 03 2007 - darren.kenny@sun.com
- Restore correct permissons on /etc/gksu.conf to be root:root
* Tue Apr 24 2007 - laca@sun.com
- fix default attributes
* Thu Sep 18 2006 - darren.kenny@sun.com
- Change the group for /etc/gksu.conf to be as the app expects (i.e. root:root)
* Fri Aug 30 2006 - damien.carbery@sun.com
- Delete %{_datadir}/locale/locale.alias as it caused a packaging conflict.
* Thu Aug 10 2006 - Jim.li@sun.com
- initial Sun release.

