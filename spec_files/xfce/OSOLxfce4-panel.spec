#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use xfce4panel = xfce4-panel.spec

Name:			OSOLxfce4-panel
Summary:		%{xfce4panel.summary}
Version:		%{xfce4panel.version}
URL:			http://www.xfce.org/
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibxfce4util-devel
Requires:		OSOLlibxfce4util
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4

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
%xfce4panel.prep -d %name-%version/%base_arch

%build
%xfce4panel.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%xfce4panel.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

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

%files root
%defattr(-,root,sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
