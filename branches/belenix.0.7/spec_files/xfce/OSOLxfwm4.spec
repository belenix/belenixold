#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use xfwm4 = xfwm4.spec
%use themes = xfwm4-themes.spec

Name:			OSOLxfwm4
Summary:		%{xfwm4.summary}
Version:		%{xfwm4.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibxfce4mcs-devel
Requires:		OSOLlibxfce4mcs
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLxfce-mcs-manager-devel
Requires:		OSOLxfce-mcs-manager
Requires:		SUNWpostrun

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%xfwm4.prep -d %name-%version/%base_arch
%themes.prep -d %name-%version/%base_arch

%build
%xfwm4.build -d %name-%version/%base_arch
%themes.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%xfwm4.install -d %name-%version/%base_arch
%themes.install -d %name-%version/%base_arch

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
%{_libdir}/*
%{_datadir}/xfce4*
%{_datadir}/xfwm4*
%{_datadir}/themes*
%defattr(-,root,other)
%{_datadir}/icons*
%{_datadir}/applications*
%{_datadir}/locale*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
- Combined with xfwm4-themes
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Sat Jan 10 2007 - dougs@truemail.co.th
- Added fix to find Xorg extensions
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
