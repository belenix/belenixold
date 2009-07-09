#
#
# spec file for package SUNWgtkmm
#
# includes module(s): gtkmm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc

%use gtkmm = gtkmm.spec

Name:                    SUNWgtkmm
Summary:                 gtkmm - C++ Wrapper for the Gtk+ Library
Version:                 %{gtkmm.version}
Source:			 %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWglibmm
Requires: SUNWcairomm
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWsigcpp
Requires: SUNWlibC
Requires: SUNWpangomm
BuildRequires: SUNWsigcpp-devel
BuildRequires: SUNWglibmm-devel
BuildRequires: SUNWcairomm-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWpangomm-devel

%package devel
Summary:                 gtkmm - C++ Wrapper for the Gtk+ Library - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWglibmm-devel
Requires: SUNWsigcpp-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%gtkmm.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export CXXFLAGS="%cxx_optflags"
%if %cc_is_gcc
export CFLAGS=`echo ${CFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS=`echo ${CXXFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="${LDFLAGS} ${LDFLAGS_EXTRA}"
export CFLAGS="${CFLAGS} ${CFLAGS_EXTRA}"
%endif
%gtkmm.build -d %name-%version

%install
%gtkmm.install -d %name-%version

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT
# Move demo to demo directory
#
install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
mv $RPM_BUILD_ROOT%{_bindir}/gtkmm-demo $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
rm -r $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d gtkmm-%{gtkmm.version} AUTHORS README
%doc(bzip2) -d gtkmm-%{gtkmm.version} ChangeLog COPYING NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/gtkmm*
%{_libdir}/gdkmm*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtkmm-2.4/demo
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/gtkmm*
%{_datadir}/devhelp
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_prefix}/demo
%dir %attr (0755, root, bin) %{_prefix}/demo/jds
%dir %attr (0755, root, bin) %{_prefix}/demo/jds/bin
%{_prefix}/demo/jds/bin/gtkmm-demo


%changelog
* Fri Sep 19 2008 - dave.lin@sun.com
- Fix file conflicts in /usr/share/doc/* between base pkg and devel pkg.
* Wed Sep 18 2008 - chris.wang@sun.com
- Update copyright
* Mon Aug 18 2008 - chris.wang@sun.com
- Add manpage
* Thu Jul 30 2008 - chris.wang@sun.com
- Add SUNWpangomm as dependency
* Thu Mar 27 2008 - simon.zheng@sun.com
- Add file SUNWgtkmm.copyright.
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version number.
* Thu Feb 14 2008 - chris.wang@sun.com
- Move gtkmm-demo to /usr/demo/jds/bin per requested by ARC
* Tue Jan 29 2008 - chris.wang@sun.com
- create
