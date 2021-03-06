#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define postgres_dir /usr/postgres/8.3

Name:                SFElibpqxx
Summary:             Official C++ client API for PostgreSQL.
Version:             3.0.2
URL:                 http://pqxx.org/development/libpqxx/
Source:              ftp://pqxx.org/software/libpqxx/libpqxx-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWpostgr-83-libs
BuildRequires:       SUNWpostgr-83-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:       SUNWpostgr-83-devel

%prep
%setup -q -n libpqxx-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{postgres_dir}/include"
export LDFLAGS="-L%{postgres_dir}/lib -R%{postgres_dir}/lib %_ldflags -L/lib -R/lib"
export PG_CONFIG=%{postgres_dir}/bin/pg_config
gnu_prefix=`dirname %{gnu_bin}`

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no  \

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Sep 28 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Bump version.
- Build with Postgres 8.3.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Initial spec.
