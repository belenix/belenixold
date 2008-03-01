#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use thunar = thunar.spec

Name:			OSOLthunar
Summary:		%{thunar.summary}
Version:		%{thunar.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools
Requires:		OSOLlibexo
BuildRequires:		OSOLlibexo-devel
Requires:		OSOLxfce4-panel
BuildRequires:		OSOLxfce4-panel-devel
Requires:		SUNWgamin
BuildRequires:		SUNWgamin-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                %{summary} - developer files
Group:                  Development/Libraries
SUNW_BaseDir:           %{_basedir}
Requires:               %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%thunar.prep -d %name-%version/%base_arch

%build
%thunar.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%thunar.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/xfce4
%{_libdir}/thunarx-1
%{_libdir}/thunar-vfs-*
%{_libdir}/thunar-sendto-email
%{_libdir}/ThunarBulkRename
%{_libdir}/ThunarHelp
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce4
%{_datadir}/thumbnailers
%{_datadir}/dbus-1
%{_datadir}/Thunar
%{_datadir}/gtk-doc
%defattr(-,root,other)
%{_datadir}/icons
%{_datadir}/pixmaps
%{_datadir}/locale
%{_datadir}/doc
%{_datadir}/applications

%files root
%defattr(-,root,sys)
%{_sysconfdir}

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}

%changelog
* Sun Dec  9 2007 - sobotkap@centrum.cz
- Bumped to 0.9.0
* Sun Apr 15 2007 - dougs@truemail.co.th
- Added OSOLgamin as a required package
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  9 2007 - dougs@truemail.co.th
- Added SUNWpcre requirement
* Thu Feb  2 2007 - dougs@truemail.co.th
- Initial version
