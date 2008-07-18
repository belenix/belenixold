#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use xfcalendar = orage.spec

Name:			OSOLxfcalendar
Summary:		Xfce Calendar
Summary:                %{xfcalendar.summary}
Version:                %{xfcalendar.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLlibxfce4util-devel
Requires:		OSOLlibxfce4util
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLxfce4-panel-devel
Requires:		OSOLxfce4-panel
Requires:		SUNWpostrun

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%xfcalendar.prep -d %name-%version/%base_arch


%build
%xfcalendar.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%xfcalendar.install -d %name-%version/%base_arch

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
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/orage
%{_datadir}/xfce4
%defattr(-,root,other)
%{_datadir}/icons
%{_datadir}/applications
%{_datadir}/locale

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Fri Feb  9 2007 - dougs@truemail.co.th
- Fixed zoneinfo lookup
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
