#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define xfce_version 4.4.0

%define _localedir %{_libdir}/locale

%define src_name xfce4-cpugraph-plugin
Name:			OSOLxfce4-cpugraph-plugin
Summary:		CPU Graph Plugin
Version:		0.4.0
URL:			http://www.xfce.org/
Source0:		http://goodies.xfce.org/releases/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:			xfce4-cpugraph-plugin-01-solaris_support.diff
Patch2:         xfce4-cpugraph-plugin-02-fixmaxcpu.diff
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLxfce4-panel-devel
Requires:		OSOLxfce4-panel
Requires:		SUNWpostrun
%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
#%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

autoconf --force

./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
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
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xfce4
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce4

%defattr(-,root,other)
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%changelog
* Thu Nov 22 2007 - Petr Sobotka sobotkap@centrum.cz
- Bump to 0.4
- New code for multiple cpus/cores
* Tue Apr 12 2007 - dougs@truemail.co.th
- Initial version
