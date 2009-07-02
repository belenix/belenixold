#
# spec file for package SFEgnokii.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)
%define postgres_version 8.3
%define mysql_version 5.0

Name:                   SFEgnokii
Summary:                Tools and user-space drivers for interfacing with mobiles phones esp. Nokia
Version:                0.6.27
License:                GPLv2
Source:                 http://www.gnokii.org/download/gnokii/gnokii-%{version}.tar.bz2
Patch1:                 gnokii-01-uint8.diff
Patch2:                 gnokii-02-utils.diff
Patch3:                 gnokii-03-strndup.diff
Patch4:                 gnokii-04-config.diff
Patch5:                 gnokii-05-mysql_config.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgtk2
BuildRequires: SUNWgtk2-devel
Requires: SUNWlibusb
Requires: SFEreadline
BuildRequires: SFEreadline-devel
Requires: SFElibical
BuildRequires: SFElibical-devel
Requires: SUNWpostgr-83-libs
BuildRequires: SUNWpostgr-83-devel
Requires: SUNWmysql5u
%if %option_with_gnu_iconv
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
BuildRequires: SFElibiconv-devel
Requires: SFEgettext
BuildRequires: SFEgettext-devel
%endif
%else
Requires: SUNWuiu8
%endif

%prep
%setup -q -n gnokii-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

%if %cc_is_gcc
#
# Mash up a mysql_config to not emit SUN Studio optimization flags
#
cp %{_prefix}/mysql/%{mysql_version}/bin/mysql_config .
%patch5 -p1
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} -I%{sfw_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lintl -liconv %{sfw_lib_path}"
export PGCONFIG="%{_prefix}/postgres/%{postgres_version}/bin/pg_config"
%if %cc_is_gcc
export MYSQLCONFIG=`pwd`/mysql_config
%else
export MYSQLCONFIG="%{_prefix}/mysql/%{mysql_version}/bin/mysql_config"
%endif

./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes		\
	    --enable-static=no		\
            --enable-libical            \
            --enable-security           \
            --with-libiconv-prefix=/usr/gnu \
            --with-libintl-prefix=/usr/gnu

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a
rm $RPM_BUILD_ROOT/%{_libdir}/smsd/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/smsd
%{_libdir}/smsd/*.so
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/xgnokii
%{_datadir}/xgnokii/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*

%changelog
* Thu Jul 02 2009 - moinakg(at)gmail<dot>com
- Major fix to build. Bump version.
* Sun Feb 24 2008 - moinakg@gmail.com
- Add check for gnu iconv option.
* Mon Jan 28 2008 - moinakg@gmail.com
- Add check for presence on SUNWgnu-iconv and SUNWgnu-gettext packages.
- Fixed a typo.
* Mon Jan 21 2008 - moinak.ghosh@sun.com
- Initial spec.
