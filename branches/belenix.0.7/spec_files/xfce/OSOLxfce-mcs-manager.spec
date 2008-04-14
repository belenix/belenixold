#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use  mcsmanager = xfce-mcs-manager.spec

Name:			OSOLxfce-mcs-manager
Summary:		%{mcsmanager.summary}
Version:		%{mcsmanager.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
Requires:		OSOLlibxfce4mcs
BuildRequires:		OSOLlibxfce4mcs-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		SUNWpostrun

%package devel
Summary:		%{summary} - developer files
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
Requires:		%{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%mcsmanager.prep -d %name-%version/%base_arch

%build
%mcsmanager.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%mcsmanager.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || {';
  echo '  echo "ERROR: gtk-update-icon-cache not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo '/usr/bin/gtk-update-icon-cache -f -t %{datadir}/icons/hicolor || retval=1';
  echo 'done';
  echo 'exit $retval'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%postun
( echo 'test -x /usr/bin/gtk-update-icon-cache || {';
  echo '  echo "ERROR: gtk-update-icon-cache not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo '/usr/bin/gtk-update-icon-cache -f -t %{datadir}/icons/hicolor || retval=1';
  echo 'done';
  echo 'exit $retval'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/xfce4
%{_bindir}/*
%{_datadir}/xfce4/*
%defattr(-,root,other)
%{_datadir}/locale*
%{_datadir}/applications*
%{_datadir}/icons*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/xfce-mcs-manager

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
