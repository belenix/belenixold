#
#
# spec file for package SUNWclutter-cairo
#
# includes module(s): clutter-cairo
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc
%use cluttercairo = clutter-cairo.spec

Name:                    SUNWclutter-cairo
Summary:                 clutter-cairo - An experimental clutter cairo 'drawable' actor.
Version:                 %{cluttercairo.version}
URL:                     http://www.clutter-project.org/
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 SUNWclutter-cairo.copyright

%ifnarch sparc
#packages are only for x86

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWclutter
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWclutter-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%cluttercairo.prep -d %name-%version/
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
export CFLAGS="%optflags -I/usr/include/pango-1.0 -I/usr/include/gtk-2.0 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include"
export LDFLAGS="%_ldflags -lglib-2.0 -lgobject-2.0 -lm"
%cluttercairo.build -d %name-%version/

%install

%cluttercairo.install -d %name-%version/
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d clutter-cairo-%{cluttercairo.version} AUTHORS README
%doc(bzip2) -d clutter-cairo-%{cluttercairo.version} ChangeLog COPYING NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%endif
%changelog
* Thu Mar 26 2009  Chris.wang@sun.com
- Correct copyright file in file section
* Fri Feb 20 2009  chris.wang@sun.com
- Add manpage
* Tue Jul  1 2008  chris.wang@sun.com 
- Initial build.
