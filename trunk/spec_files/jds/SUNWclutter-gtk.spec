#
#
# spec file for package SUNWclutter-gtk
#
# includes module(s): clutter-gtk
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc
%use cluttergtk = clutter-gtk.spec

Name:                    SUNWclutter-gtk
Summary:                 clutter-gtk - GTK+ integration library for clutter
Version:                 %{cluttergtk.version}
URL:                     http://www.clutter-project.org/
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 SUNWclutter-gtk.copyright

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
%cluttergtk.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%cluttergtk.build -d %name-%version

%install
%cluttergtk.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d clutter-gtk-%{cluttergtk.version} AUTHORS README
%doc(bzip2) -d clutter-gtk-%{cluttergtk.version} ChangeLog COPYING NEWS
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
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
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
