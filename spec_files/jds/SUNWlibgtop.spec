#
# 
# spec file for package SUNWlibgtop  
#
# includes module(s): libgtop
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: niall
#
%include Solaris.inc
%use libgtop = libgtop.spec

Name:              SUNWlibgtop
Summary:           Library to get system specific data 
Version:           %{default_pkg_version}
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
Source:            %{name}-manpages-0.1.tar.gz


%include default-depend.inc
Requires: SUNWgnome-component
Requires: SUNWgnome-print
Requires: SUNWgnome-libs
Requires: SUNWjdsrm
Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWmlib
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel


%package devel
Summary:           Library to get system specific data - developer files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires: %name

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
%libgtop.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -


%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I /usr/share/aclocal"

%libgtop.build -d %name-%version
export PATH=%{_builddir}/%name-%version:$PATH
export CFLAGS="`echo %optflags | sed -e 's/-xregs=no.frameptr//'`"

%install
%libgtop.install -d %name-%version
# Remove the libgtop2.info file. No other modules install .info files.
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
# delete files don't need
rm -rf $RPM_BUILD_ROOT%{_bindir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}
# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d libgtop-%{libgtop.version} README AUTHORS
%doc(bzip2) -d libgtop-%{libgtop.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/html/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Mon Mar 23 2009 - Niall Power <niall.power@sun.com>
- Take ownership of spec file
* Wed Sep 17 2008 - Henry Zhang <hua.zhang@sun.com>
- Add  %doc to %files for copyright
* Mon July 28 2008 - hua.zhang@sun.com
- Add manpage
* Thu Jan 10 2008 - damien.carbery@sun.com
- Set ACLOCAL_FLAGS to pick up the modified intltool.m4.
* Fri Sep 28 2007 - laca@sun.com
- delete some unnecessary env variables that break the indiana build
* Wed Dec 06 2006 - damien.carbery@sun.com
- Add gtk-docs to the devel package.
* Fri Sep 22 2006 - hua.zhang@sun.com
-  Shorten the summary according to Shirley comments.
-  Delete unuseful binary files from /usr/bin
* Thu Aug 23 2006 - damien.carbery@sun.com
- Remove the %{_datadir}/info dir as no other modules install .info files.
* Thu May 11 2006 - hua.zhang@sun.com
- initial version
