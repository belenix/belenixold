#
# spec file for package SUNWlibvisual.spec
#
# include module(s): libvisual, libvisual-plugins
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#
%include Solaris.inc

%use libvisual = libvisual.spec
%use libvisual_plugins = libvisual-plugins.spec

Name:                   SUNWlibvisual
Summary:                Libvisual provides a convenient API for writing visualization plugins
Version:                0.4.0
SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:		%{name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWlibmsr
%ifarch i386
BuildRequires: SUNWxorg-mesa
%endif
%ifarch sparc
# uncomment the following if we decide to deliver
# plugins which need OpenGL support.
# BuildRequires: SUNWglh
%endif
Requires: SUNWgnome-base-libs
Requires: SUNWlibmsr

%if %build_l10n
%package l10n
Summary:       %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-common-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%libvisual.prep -d %name-%version
%libvisual_plugins.prep -d %name-%version

%build

export CFLAGS="-features=extensions -D__volatile=__volatile__"
export LDFLAGS="%{_ldflags} -Wl,-Mmap.remove_all"
%libvisual.build -d %name-%version
export PKG_CONFIG_PATH=%{_builddir}/%name-%version/libvisual-%{libvisual.version}:%{_pkg_config_path}
export CFLAGS="$CFLAGS -I%{_builddir}/%name-%version/libvisual-%{libvisual.version}"
export LDFLAGS="%_ldflags -L%{_builddir}/%name-%version/libvisual-%{libvisual.version}/libvisual/.libs"
%libvisual_plugins.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%libvisual.install -d %name-%version
%libvisual_plugins.install -d %name-%version

rm $RPM_BUILD_ROOT%{_libdir}/libvisual-0.4/actor/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libvisual-0.4/input/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libvisual-0.4/morph/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/libvisual*
%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_datadir}
%doc libvisual-%{libvisual.version}/AUTHORS
%doc libvisual-%{libvisual.version}/README
%doc(bzip2) libvisual-%{libvisual.version}/COPYING
%doc(bzip2) libvisual-%{libvisual.version}/NEWS
%doc(bzip2) libvisual-%{libvisual.version}/ChangeLog
%doc(bzip2) libvisual-%{libvisual.version}/po/ChangeLog
%doc libvisual-plugins-%{libvisual_plugins.version}/AUTHORS
%doc libvisual-plugins-%{libvisual_plugins.version}/NEWS
%doc libvisual-plugins-%{libvisual_plugins.version}/README
%doc libvisual-plugins-%{libvisual_plugins.version}/po/ChangeLog
%doc(bzip2) libvisual-plugins-%{libvisual_plugins.version}/COPYING
%doc(bzip2) libvisual-plugins-%{libvisual_plugins.version}/ChangeLog
%ifarch sparc
# those are plugin - madspin relative files, which need
# OpenGL support.
# %{_datadir}/libvisual-plugins-0.4/actor/actor_madspin/*
%else
%{_datadir}/libvisual-plugins-0.4/actor/actor_madspin/*
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other)	%{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Feb 19 2009 - brian.cameron@sun.com
- Remove -xarch=sse2 since it was not being implemented properly.  When
  building with sse2 specific flags you have to install to a directory
  specific to the architecture.
* Fri Jan 16 2009 - christian.kelly@sun.com
- Fixed %files.
* Fri Jan 09 2009 - brian.cameron@sun.com
- Add SUNWlibmsr and SUNWgnome-base-libs as dependencies.  Fixes bug 
  #6791253.
* Fri Jan 09 2009 - christian.kelly@sun.com
- Fix up %files section.
* Mon Dec 22 2008 - takao.fujiwara@sun.com
- add l10n package.
* Tue Nov 25 2008 - jim.li@sun.com
- add copyright file
- add license tag
- combine SFElibvisual and SFElibvisual-plugin to SUNWlibvisual
- use sun compiler 12 instead of gcc
* Sun Jun 29 2008 - river@wikimedia.org
- force /usr/sfw/bin/gcc, use gcc cflags instead of studio
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Initial spec.
