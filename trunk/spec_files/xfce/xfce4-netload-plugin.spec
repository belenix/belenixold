#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define xfce_version 4.4.0

Name:			%{xfce_banding}xfce4-netload-plugin
Summary:		Network load applet for Xfce
Version:		0.4.0
URL:			http://www.xfce.org/
Source0:		http://goodies.xfce.org/releases/xfce4-netload-plugin/xfce4-netload-plugin-%{version}.tar.bz2
Patch1:			xfce4-netload-plugin-01-libnsl.diff
Patch2:			xfce4-netload-plugin-02-os-def.diff
Patch3:			xfce4-netload-plugin-03-localedir.diff
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-component-devel
Requires:		SUNWgnome-component
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		SUNWgnome-panel-devel
Requires:		SUNWgnome-panel
BuildRequires:		%{xfce_banding}libxfcegui4-devel
Requires:		%{xfce_banding}libxfcegui4
BuildRequires:		%{xfce_banding}libxfce4util-devel
Requires:		%{xfce_banding}libxfce4util
BuildRequires:		%{xfce_banding}xfce4-panel-devel
Requires:		%{xfce_banding}xfce4-panel
Requires:		SUNWpostrun

%prep
%setup -q -n xfce4-netload-plugin-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

autoconf

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-locales-dir=%{_datadir}/locale \
            --enable-gtk-doc \
            --disable-static
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xfce4
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce4
%defattr(-,root,other)
%{_datadir}/locale

%changelog
* Sun Mar 2 2007 - dougs@truemail.co.th
- Initial version
