#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use mousepad = mousepad.spec

Name:			OSOLmousepad
Summary:		%{mousepad.summary}
Version:		%{mousepad.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibxfce4util-devel
Requires:		OSOLlibxfce4util
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
Requires:		SUNWpostrun

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%mousepad.prep -d %name-%version/%base_arch

%build
%mousepad.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%mousepad.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_bindir}/*
%defattr(-,root,other)
%{_datadir}/pixmaps*
%{_datadir}/applications*
%{_datadir}/locale*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
