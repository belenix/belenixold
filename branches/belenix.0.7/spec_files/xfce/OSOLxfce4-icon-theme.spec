#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use icontheme = xfce4-icon-theme.spec

Name:			OSOLxfce4-icon-theme
Summary:		%{icontheme.summary}
Version:		%{icontheme.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools

%package devel
Summary:                %{summary} - developer files
Group:                  Development/Libraries
SUNW_BaseDir:           %{_basedir}
Requires:               %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%icontheme.prep -d %name-%version/%base_arch

%build
%icontheme.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%icontheme.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce*
%defattr(-,root,other)
%{_datadir}/icons*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
