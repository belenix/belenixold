#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use terminal = terminal.spec

Name:			OSOLterminal
Summary:		%{terminal.summary}
Version:		%{terminal.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		SUNWgnome-terminal-devel
Requires:		SUNWgnome-terminal
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibexo
Requires:		OSOLlibexo-devel

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%terminal.prep -d %name-%version/%base_arch

%build
%terminal.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%terminal.install -d %name-%version/%base_arch

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
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/TerminalHelp
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/Terminal
%defattr(-,root,other)
%{_datadir}/locale
%{_datadir}/pixmaps
%{_datadir}/doc
%{_datadir}/applications
%{_datadir}/icons

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
