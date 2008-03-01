#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use libxfcegui4 = libxfcegui4.spec

Name:			OSOLlibxfcegui4
Summary:		%{libxfcegui4.summary}
Version:		%{libxfcegui4.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:          OSOLxfce4-dev-tools
Requires:               OSOLlibxfce4util
BuildRequires:          OSOLlibxfce4util-devel

%package devel
Summary:		%{summary} - developer files
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
Requires:		%{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%libxfcegui4.prep -d %name-%version/%base_arch

%build
%libxfcegui4.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%libxfcegui4.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/lib*.so.*
%defattr(-,root,other)
%{_datadir}/locale*
%{_datadir}/icons*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/libxfcegui4
%{_datadir}/gtk-doc

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Wed Feb 21 2007 - Menno.Lageman@Sun.COM
- fix some gcc G_BEGIN_DECLS for Sun Studio build niceness
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
