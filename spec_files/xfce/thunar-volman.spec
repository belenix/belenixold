#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define xfce_version 4.4.0

%define src_name thunar-volman
Name:			OSOLthunar-volman
Summary:		Thunar Volume manager
Version:		svn
URL:			http://www.xfce.org/
#Source0:		thunar-volman.tar.bz2
Patch1:			thunar-volman-01-fixgccism.diff
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLthunar-devel
Requires:		OSOLthunar
BuildRequires:		SUNWgamin-devel
Requires:		SUNWgamin
Requires:		SUNWpostrun

%prep
if [ ! -d %{src_name} ]
then
mkdir %{src_name}
cd %{src_name}
svn co http://svn.xfce.org/svn/goodies/%{src_name}/trunk %{src_name}

else
cd %{src_name}
fi

if [ ! -f .patched ]
then
%patch1 -p0
touch .patched
fi

%build
cd %{src_name}/%{src_name}

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

[ -f Makefile ] && make distclean
./autogen.sh --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-gtk-doc \
            --enable-debug=no \
            --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

cd %{src_name}/%{src_name}
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
%{_libdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%defattr(-,root,other)
%{_datadir}/icons
%{_datadir}/locale

%changelog
* Sun Apr 15 2007 - dougs@truemail.co.th
- Added OSOLgamin requirement
* Sat Apr 14 2007 - dougs@truemail.co.th
- Initial version
