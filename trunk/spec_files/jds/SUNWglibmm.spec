#
# spec file for package SUNWglibmm
#
# includes module(s): glibmm
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
%include Solaris.inc
%use glibmm = glibmm.spec

Name:                    SUNWglibmm
Summary:                 glibmm - C++ Wrapper for the Glib2 Library
Version:                 %{glibmm.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWsigcpp
BuildRequires: SUNWsigcpp-devel
Requires: SUNWperl584core
Requires: SUNWdesktop-cache

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%if %build_l10n
%package l10n
Summary:		 %{summary} - l10n files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires:		 %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%glibmm.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CXXFLAGS="%cxx_optflags"
%if %cc_is_gcc
export CFLAGS=`echo ${CFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS=`echo ${CXXFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="${LDFLAGS} ${LDFLAGS_EXTRA}"
%else
export CXX="${CXX} -norunpath"
%endif
export PERL_PATH=/usr/perl5/bin/perl
%glibmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%glibmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc/m4
rm -rf $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc/pm
rm -rf $RPM_BUILD_ROOT%{_libdir}/libglibmm_generate_extra_defs*.so*
rm -rf $RPM_BUILD_ROOT%{_includedir}/glibmm-2.4/glibmm_generate_extra_defs

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d glibmm-%{glibmm.version} README AUTHORS
%doc(bzip2) -d glibmm-%{glibmm.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/glibmm*
%{_libdir}/giomm*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/glibmm*
%dir %attr (0755, root, bin) %{_datadir}/devhelp
%{_datadir}/devhelp/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/lib/glibmm-2.4/proc/beautify_docs.pl (SUNWglibmm) requires
  /usr/perl5/5.8.4/bin/perl5.8.4 which is found in SUNWperl584core, add
  the dependency.
* Mon Nov 10 2008 - chris.wang@sun.com
- Change the owner of the spec to chris wang
* Thu Sep 18 2008 - dave.lin@sun.com
- Fix the conflicts in /usr/share/doc between base & devel pkgs
* Wed Jul 20 2008 - simon.zheng@sun.com
- Add manpage.
* Thu Mar 27 2008 - simon.zheng@sun.com
- Add SUNWglibmm.copyright.
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version number.
* Fri 29 2008 - simon.zheng@sun.com
- Pack devhelp index file. 
* Wed Feb 15 2008 - simon.zheng@sun.com
- Pack file /usr/lib/giomm-2.4/giommconfig.h.
* Thu Feb 14 2008 - simon.zheng@sun.com
- Remove useless m4, pm and extra_gen_defs files.
* Mon Jau 28 2008 - simon.zheng@sun.com
- Split into SUNWglibmm.spec and glibmm.spec.
- Change download URL to GNOME official website.
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.12.10
* Tue Apr 17 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.8.
* Fri Mar 16 2007 - laca@sun.com
- bump to 2.12.7
* Wed Jan 03 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.4
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEglibmm
- update permissions
- bump to 2.10.4
* Fri May 12 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Fri Mar 10 2006 - damien.carbery@sun.com
- Bump to 2.10.0.
* Thu Nov 17 2005 - laca@sun.com
- create
