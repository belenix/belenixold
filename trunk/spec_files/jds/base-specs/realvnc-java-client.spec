#
# spec file for package realvnc-java-client
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
Name:			realvnc-java-client
License:		GPL v2
Group:			System/GUI/GNOME
Version:		4.1
%define tarball_version  4_1
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		RealVNC Java Viewer
URL:            http://www.realvnc.com
# download the source manually from http://www.realvnc.com/cgi-bin/download.cgi
Source:			vnc-%{tarball_version}-javasrc.tar.gz
# date:2007-06-22 owner:halton type:branding
Patch1:         %{name}-01-makefile.diff
# date:2007-06-22 owner:halton type:branding
Patch2:         %{name}-02-applet-html.diff
# date:2007-06-28 owner:halton type:bug bugster:6574150,6574964 state:unmaintained
Patch3:         %{name}-03-use-listener.diff
# date:2007-07-21 owner:halton type:bug bugster:6578118 state:unmaintained
Patch4:         %{name}-04-highcolor.diff
# date:2008-01-16 owner:fujiwara type:bug bugster:6650387 state:unmaintained
Patch5:         %{name}-05-g11n-use-remote-im.diff
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%description
A VNC client written in Java, can be used as applet.


%prep
%setup -q -n vnc-%{tarball_version}-javasrc
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
cd java
make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Wed Jan 16 2008 - takao.fujiwara@sun.com
- Add g11n-use-remote-im.diff to use remote IM. bugster 6650387
* Fri Nov 02 2007 - halton.huo@sun.com
- Remove patch add-wrapper and reorder.
* Sat Jul 21 2007 - halton.huo@sun.com
- Add patch highcolor.diff to fix bugster #6578118
* Thu Jun 28 2007 - halton.huo@sun.com
- Add patch use-listener.diff
* Fri Jun 22 2007 - halton.huo@sun.com
- Initial spec file
