#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define xfce_version 4.4.0

Name:			%{xfce_banding}xfce4-verve-plugin
Summary:		Command line plugin for the Xfce panel
Version:		0.3.5
URL:			http://www.xfce.org/
Source0:		http://goodies.xfce.org/releases/verve-plugin/verve-plugin-%{version}.tar.bz2
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/verve-plugin-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWpcre
Requires:		SUNWgnome-base-libs
BuildRequires:		%{xfce_banding}libxfcegui4-devel
Requires:		%{xfce_banding}libxfcegui4
BuildRequires:		%{xfce_banding}xfce4-panel-devel
Requires:		%{xfce_banding}xfce4-panel
Requires:		SUNWpostrun
%prep
%setup -q -n verve-plugin-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -I%{_includedir}/pcre"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
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
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/xfce4
%{_datadir}/xfce4*
%defattr(-,root,other)
%{_datadir}/locale*

%changelog
* Sun Apr 22 2007 - sobotkap@students.zcu.cz
- small change in summary
* Mon Apr 16 2007 - laca@sun.com
- add missing defattr
* Tue Apr 10 2007 - dougs@truemail.co.th
- Fixed the summary
- Added SUNWpcre as a required - This could be a problem as SUNWpcre
- has been removed from JDS to in the future be added to SFW. If you don't 
- have it, you need to find an old JDS version
* Mon Apr  9 2007 - sobotkap@students.zcu.cz
- Initial Version
