#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define xfce_version 4.4.0
%define src_name notification-daemon-xfce

Name:			%{xfce_banding}notification-daemon
Summary:		Notification daemon for Xfce desktop.
Version:		0.3.7
URL:			http://www.xfce.org/
Source0:		http://goodies.xfce.org/releases/notification-daemon-xfce/%{src_name}-%{version}.tar.bz2
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/verve-plugin-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		%{xfce_banding}libxfcegui4-devel
Requires:		%{xfce_banding}libxfcegui4
Requires:		SUNWdbus
Requires:		SFElibsexy

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-gradient-look \
            --disable-static
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/notification-daemon-xfce
%dir %attr (0755, root, bin) %{_libdir}/xfce4
%{_libdir}/xfce4/*
%dir %attr (0755, root, other) %{_libdir}/notification-daemon-xfce-1.0
%{_libdir}/notification-daemon-xfce-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*
%defattr(0755, root, other)
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%defattr(-,root,other)
%{_datadir}/locale*

%changelog
* Mon Nov 5 2007 - sobotkap@centrum.cz
- Initial Version
