#
# spec file for package SUNWlibdaemon
#
# includes module(s): libdaemon
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include Solaris.inc

%use libdaemon = libdaemon.spec 

Name:                    SUNWlibdaemon
Summary:                 Lightweight C library for UNIX daemons
Version:                 %{libdaemon.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:          %{name}.copyright

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libdaemon.prep -d %name-%version

%build
PKG_CONFIG_DISABLE_UNISTALLED=
unset PKG_CONFIG_DISABLE_UNISTALLED
export PKG_CONFIG_PATH=../libdaemon-%{libdaemon.version}:%{_pkg_config_path}

export PKG_CONFIG_PATH32="$PKG_CONFIG_PATH"

export PKG_CONFIG_PATH64=../libdaemon-%{libdaemon.version}-64:%{_pkg_config_path64}


export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%libdaemon.build -d %name-%version

%install
%libdaemon.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d libdaemon-%{libdaemon.version} LICENSE README
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libdaemon*.so*

%files devel
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Thu Sep 18 2008 - dave.lin@sun.com
- Fix the attribute conflict of the dir %{_datadir}
* Wed Sep 10 2008 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Mon May 29 2006 - padraig.obriain@sun.com
- Initial spec file created.
