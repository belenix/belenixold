#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use mcsplugins = xfce-mcs-plugins.spec

Name:			OSOLxfce-mcs-plugins
Summary:		%{mcsplugins.summary}
URL:			%{mcsplugins.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLxfce4-dev-tools
Requires:		OSOLxfce-mcs-manager
BuildRequires:		OSOLxfce-mcs-manager-devel
Requires:		SUNWpostrun

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%mcsplugins.prep -d %name-%version/%base_arch

%build
%mcsplugins.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%mcsplugins.install -d %name-%version/%base_arch

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
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/xfce4*
%{_datadir}/xfce4*
%{_datadir}/xfce-mcs-plugins*
%defattr(-,root,other)
%{_datadir}/locale*
%{_datadir}/applications*
%{_datadir}/icons*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Sat Jan 10 2007 - dougs@truemail.co.th
- Added fix to find Xorg extensions
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
