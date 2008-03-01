#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use devtools = xfce4-dev-tools.spec

Name:			OSOLxfce4-dev-tools
Summary:		%{devtools.summary}
Version:		%{devtools.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%devtools.prep -d %name-%version/%base_arch

%build
%devtools.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%devtools.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_bindir}/*
%{_datadir}/xfce4*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Apr  5 2007 - dougs@truemail.co.th
- Initial version
