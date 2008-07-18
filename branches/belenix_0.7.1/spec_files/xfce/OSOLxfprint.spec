#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use xfprint = xfprint.spec

Name:			OSOLxfprint
Summary:		%{xfprint.summary}
Version:		%{xfprint.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
Requires:		SUNWa2psu
Requires:		SUNWpostrun

%package devel
Summary:                %{summary} - developer files
Group:                  Development/Libraries
SUNW_BaseDir:           %{_basedir}
Requires:               %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%xfprint.prep -d %name-%version/%base_arch

%build
%xfprint.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%xfprint.install -d %name-%version/%base_arch

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
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_bindir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.so.*
%{_libdir}/xfce4*
%{_datadir}/gtk-doc*
%{_datadir}/xfce4*
%defattr(-,root,other)
%{_datadir}/icons*
%{_datadir}/applications*
%{_datadir}/locale*

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
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
