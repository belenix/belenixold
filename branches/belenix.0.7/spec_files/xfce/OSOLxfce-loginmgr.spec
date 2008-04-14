#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:			OSOLxfce-loginmgr
Summary:		gdm and dtlogin files to support Xfce
URL:			http://www.opensolaris.org/
Version:		4.4.0
Source0:		Xinitrc.xfce
Source1:		Xsession.xfce
Source2:		Xsession2.xfce
Source3:		Xresources.xfce
Source4:		xfce.desktop
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
cp %{SOURCE0} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE1} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE2} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE3} $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
mkdir -p $RPM_BUILD_ROOT/usr/share/xsessions
cp %{SOURCE4} $RPM_BUILD_ROOT/usr/share/xsessions

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) /usr/dt
%dir %attr (0755, root, bin) /usr/dt/config
%dir %attr (0755, root, bin) /usr/dt/config/C
%dir %attr (0755, root, bin) /usr/dt/config/C/Xresources.d
/usr/dt/config/C/Xresources.d/*
%attr (0755, root, bin) /usr/dt/config/Xinitrc.xfce
%attr (0755, root, bin) /usr/dt/config/Xsession.xfce
%attr (0755, root, bin) /usr/dt/config/Xsession2.xfce
%{_datadir}/*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Fri Feb  9 2007 - dougs@truemail.co.th
- Changed from tar archives to normal files
- Changed startup script in xfce.desktop from Xinitrc.xfce to Xsession.xfce
* Thu Feb  2 2007 - dougs@truemail.co.th
- Initial version
