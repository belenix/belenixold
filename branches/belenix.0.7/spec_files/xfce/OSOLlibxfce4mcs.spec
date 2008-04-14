#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use libxfce4mcs = libxfce4mcs.spec

Name:			OSOLlibxfce4mcs
Summary:		%{libxfce4mcs.summary}
URL:			http://www.xfce.org/
Version:		%{libxfce4mcs.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools
Requires:		OSOLlibxfce4util
BuildRequires:		OSOLlibxfce4util-devel

%package devel
Summary:		%{summary} - developer files
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
Requires:		OSOLlibxfce4mcs

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%libxfce4mcs.prep -d %name-%version/%base_arch

%build
%libxfce4mcs.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%libxfce4mcs.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/libxfce4mcs
%{_datadir}/gtk-doc

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
