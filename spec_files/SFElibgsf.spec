#
# spec file for package SFElibgsf
#
# includes module(s): libgsf
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libgsf_64 = libgsf.spec
%endif

%include base.inc
%use libgsf = libgsf.spec
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:                    SFElibgsf
Summary:                 A library provide i/o abstraction for dealing with different structured file formats
Version:                 %{default_pkg_version}
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: %{name}-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-vfs
Requires: SUNWbzip
Requires: SUNWpostrun
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWlibms
Requires: SUNWdesktop-cache
Requires: SUNWgnome-python-libs
Requires: SUNWdesktop-cache
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-vfs-devel 
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWpython-setuptools
%if %option_with_gnu_iconv
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
BuildRequires: SFElibiconv-devel
Requires: SFEgettext
BuildRequires: SFEgettext-devel
%endif
%else
Requires: SUNWuiu8
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
Requires:                SUNWgnome-base-libs-devel
Requires:                SUNWlxml-devel
Requires:                SUNWgnome-component-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libgsf_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libgsf.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
if [ "x`basename $CC`" != xgcc ]
then
  FLAG64="-xarch=generic64"
else
  FLAG64="-m64"
fi

export CFLAGS="%optflags64"
%if %option_with_gnu_iconv
export CFLAGS="${CFLAGS} -I/usr/gnu/include -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"

if [ "%_ldflags64" = "%_ldflags64" ]
then
	export LDFLAGS="%_ldflags"
else
	export LDFLAGS="%_ldflags64"
fi
%if %option_with_gnu_iconv
export LDFLAGS="$LDFLAGS -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
%endif

%libgsf_64.build -d %name-%version/%{_arch64}
%endif


export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%if %option_with_gnu_iconv
export LDFLAGS="$LDFLAGS -L/usr/gnu/lib -R/usr/gnu/lib"
%endif

%libgsf.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%libgsf_64.install -d %name-%version/%{_arch64}
%endif

%libgsf.install -d %name-%version/%{base_arch}

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo 'retval=0';
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/gsf-office-thumbnailer.schemas || retval=1';
  echo 'exit $retval'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%preun root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo 'retval=0';
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/gsf-office-thumbnailer.schemas || retval=1';
  echo 'exit $retval'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%attr (-, root, bin) %{_libdir}/python*
%dir %attr (0755, root, sys) %{_datadir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libgsf-1
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gsf-office-thumbnailer.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Apr 18 2009 - moinakg@gmail.com
- Enable 64Bit build, add patches, deps and copyright from JDS gate.
* Mon jan 28 2008 - moinak.ghosh@sun.com
- Added a couple of missing dependencies.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Add check for presence on SUNWgnu-iconv and SUNWgnu-gettext packages.
* Thu Jan 03 2008 - nonsea@users.sourceforge.net
- Add gtk-doc check.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems.
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to CFLAGS/LDFLAGS
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Created.
