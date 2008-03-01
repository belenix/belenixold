#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use gtkxfceengine = gtk-xfce-engine.spec

Name:			OSOLgtk-xfce-engine
Summary:		%{gtkxfceengine.summary}
Version:		%{gtkxfceengine.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%gtkxfceengine.prep -d %name-%version/%base_arch

%build
%gtkxfceengine.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%gtkxfceengine.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/gtk-2.0*
%{_datadir}/themes*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
