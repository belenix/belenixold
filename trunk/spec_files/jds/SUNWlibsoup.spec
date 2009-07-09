#
# spec file for package SUNWlibsoup
#
# includes module(s): libsoup
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: wangke
#
%include Solaris.inc
%use libsoup = libsoup.spec

Name:          SUNWlibsoup
Summary:       Libsoup is an HTTP client/server library for GNOME.
Version:       %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_Category: EVO25,%{default_category}
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright: %{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlibgcrypt
Requires: SUNWgnutls
Requires: SUNWlxml
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWlibproxy
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWlibgcrypt-devel
BuildRequires: SUNWgnutls-devel
BuildRequires:	SUNWlibproxy-devel

%package devel
Summary:		%{summary} - development files
SUNW_BaseDir:		%{_basedir}
%include default-depend.inc
Requires:      SUNWlibsoup

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libsoup.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export LDFLAGS="%_ldflags -L%{_libdir} -R%{_libdir}"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PKG_CONFIG_PATH=%{_pkg_config_path}
%libsoup.build -d %name-%version

%install
%libsoup.install -d %name-%version

# Verbose deletion to show the dirs being targetted.
rm -r $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/libsoup-*
rmdir $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html
rmdir $RPM_BUILD_ROOT%{_datadir}/gtk-doc
rmdir $RPM_BUILD_ROOT%{_datadir}


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d libsoup-%{libsoup.version} README AUTHORS
%doc(bzip2) -d libsoup-%{libsoup.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Mar 10 2009 - harry.lu@sun.com
- change owner to Ke Wang.
* Wed Feb 18 2009 - ke.wang@sun.com
- Add dependency on libproxy

* Wed Jul 30 2008 - simon.zheng@sun.com
- Add manpage.

* Thu Mar 27 2008 - simon.zheng@sun.com
- Add SUNWlibsoup.copyright.

* Thu Mar 06 2008 - damien.carbery@sun.com
- Remove unnecessary code left over from SUNWevolution-libs.spec.

* Tue Mar 04 2008 - <jedy.wang@sun.com>
- Initial version created. Splited from SUNWevolution-libs.
