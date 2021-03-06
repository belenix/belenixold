#
# spec file for package SFElibvisual.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                   SFElibvisual
Summary:                Libvisual provides a convenient API for writing visualization plugins
Version:                0.4.0
URL:                    http://localhost.nl/~synap/libvisual-wiki/index.php/Main_Page
Source:                 %{sf_download}/libvisual/libvisual-%{version}.tar.bz2
Patch1:                 libvisual-01-lv_types.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-common-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-common-devel

%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n libvisual-%{version}
%patch1 -p1

%build
if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes		\
	    --enable-static=no


make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other)  %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Sun Feb 24 2008 - moinakg@gmail.com
- Add l10n package.
* Thu Jan 24 2008 - moinakg@gmail.com
- Initial spec.
