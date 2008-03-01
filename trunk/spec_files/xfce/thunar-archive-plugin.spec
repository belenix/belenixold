#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define xfce_version 4.4.0

%define src_name thunar-archive-plugin
Name:			OSOLthunar-archive-plugin
Summary:		Thunar archive plugin
Version:		0.2.4
URL:			http://www.xfce.org/
#Source:			http://download.berlios.de/xfce-goodies/%{src_name}-%{version}.tar.bz2
Patch1:			thunar-archive-plugin-01-fixgccism.diff
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		OSOLlibxfcegui4-devel
Requires:		OSOLlibxfcegui4
BuildRequires:		OSOLthunar-devel
Requires:		OSOLthunar
Requires:		SUNWpostrun

%prep
if [ ! -d %{src_name}-%{version} ]
then
mkdir %{src_name}-%{version}
cd %{src_name}-%{version}
svn co http://svn.xfce.org/svn/goodies/%{src_name}/trunk %{src_name}

else
cd %{src_name}-%{version}
fi

if [ ! -f .patched ]
then
%patch1 -p0
touch .patched
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

cd %{src_name}-%{version}/%{src_name}

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

[ -f Makefile ] && make distclean
./autogen.sh --prefix=%{_prefix}	\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --datadir=%{_datadir}	\
            --mandir=%{_mandir}		\
            --sysconfdir=%{_sysconfdir}	\
            --enable-gtk-doc		\
            --enable-debug=no		\
            --disable-static
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd %{src_name}-%{version}/%{src_name}
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
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%defattr(-,root,other)
%{_datadir}/icons
%{_datadir}/locale

%changelog
* Wed Apr 19 2007 - dougs@truemail.co.th
- Initial version
