#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use session = xfce4-session.spec

Name:			OSOLxfce4-session
Summary:		%{session.summary}
Version:		%{session.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLlibxfce4mcs-devel
Requires:		OSOLlibxfce4mcs
BuildRequires:		OSOLxfce-mcs-manager-devel
Requires:		OSOLxfce-mcs-manager
Requires:		SUNWpostrun

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
%session.prep -d %name-%version/%base_arch

%build
%session.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%session.install -d %name-%version/%base_arch

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
%{_libexecdir}/balou-export-theme
%{_libexecdir}/balou-install-theme
%{_libexecdir}/xfsm-shutdown-helper
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce4*
%{_datadir}/themes*
%defattr(-,root,other)
%{_datadir}/icons*
%{_datadir}/applications*
%{_datadir}/locale*

%files root
%defattr(-,root,sys)
%{_sysconfdir}

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_includedir}/*
%{_libdir}/pkgconfig/*


%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
