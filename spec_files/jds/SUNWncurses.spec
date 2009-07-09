#
# spec file for package SUNWncurses
#
# includes module(s): ncurses
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:yuntong.jin 
#
%include Solaris.inc

# Relegating to /usr/gnu to avoid name collisions with regular curses files
%define _basedir    /usr
%define _subdir     gnu
%define _prefix     %{_basedir}/%{_subdir}

%use ncurses = ncurses.spec 

Name:                    SUNWncurses
Summary:                 A CRT screen handling and optimization package.
Version:                 %{ncurses.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:          %{name}.copyright

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ncurses.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"

export LDFLAGS="%_ldflags"
%ncurses.build -d %name-%version

%install
%ncurses.install -d %name-%version

# install man page
#rm -rf $RPM_BUILD_ROOT%{_mandir}
#cd %{_builddir}/%name-%version/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/terminfo
%dir %attr (0755, root, bin) %{_datadir}/tabset
%{_bindir}/*
%{_libdir}/*
%{_datadir}/terminfo/*
%{_datadir}/tabset/*
#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Mar 30 2009 - yuntong.jin@sun.com
- change the owner to yuntong.jin
* Thu Feb 26 2009 - elaine.xiong@sun.com
- correct basedir setting to fix CR6760759.
* Mon Aug 18 2008 - rick.ju@sun.com
- use /usr/gnu as prefix
* Sat Aug 16 2008 - halton.huo@sun.com
- Add (0755, root, sys) %{_datadir} to fix conflict issue.
* Tur Jul 17 2008 - rick.ju@sun.com
- Initial spec file created.
