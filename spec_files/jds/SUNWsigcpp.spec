#
# spec file for package SUNWsigcpp
#
# includes module(s): libsigc++
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#

%include Solaris.inc
%use sigcpp = sigcpp.spec

Name:                    SUNWsigcpp
Summary:                 Libsigc++ - a library that implements typesafe callback system for standard C++ 
Version:                 %{sigcpp.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%if %cc_is_gcc
Requires: SFEgccruntime
%else
Requires: SUNWlibC
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%sigcpp.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%if %cc_is_gcc
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS=`echo ${CFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS=`echo ${CXXFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export CFLAGS="${CFLAGS} ${CFLAGS_EXTRA}"
%else
export CFLAGS="%optflags"
export CXX="${CXX} -norunpath"
export CXXFLAGS="%cxx_optflags"
%endif
export LDFLAGS="%_ldflags"
%sigcpp.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%sigcpp.install -d %name-%version
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d libsigc++-%{sigcpp.version} AUTHORS README
%doc(bzip2) -d libsigc++-%{sigcpp.version} COPYING NEWS
%doc(bzip2) -d libsigc++-%{sigcpp.version} ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/sigc++*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/libsigc*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Thu Sep 18 2008 - elaine.xiong@sun.com
- Fix install files conflict. 
* Tue Sep 16 2008 - elaine.xiong@sun.com
- Add %doc to %files for new copyright.
* Mon Aug 04 2008 - elaine.xiong@sun.com
- Add manpage.
* Thu Mar 27 2008 - elaine.xiong@sun.com
- Add file SUNWsigcpp.copyright.
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version number.
* Fri Feb 01 2008 - elaine.xiong@sun.com
- create, split from SFEsigcpp.spec
