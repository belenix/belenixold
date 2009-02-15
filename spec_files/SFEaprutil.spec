#
# spec file for package SFElibapr
#
#
%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define postgres_version 8.2
%define mysql_version 5.0


Name:			SFEaprutil
License:		Apache,LGPL,BSD
Version:		1.3.4
Summary:		Abstraction layer on top of Apache Portable Runtime
Source:			http://apache.mirrors.tds.net/apr/apr-util-%{version}.tar.gz
Patch1:                 aprutil-01-dbd.m4.diff

URL:			http://apr.apache.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SFEgawk
Requires: SFElibapr
Requires: SFEgdbm
BuildRequires: SFElibapr-devel
BuildRequires: SUNWpostgr-devel
BuildRequires: SUNWsqlite3-devel
BuildRequires: SUNWmysql5u
BuildRequires: SUNWsfwhea

%description
Apache Portable Runtime (APR) provides software libraries
that provide a predictable and consistent interface to
underlying platform-specific implementations.

APR-util provides a number of helpful abstractions on top of APR.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWhea
Requires:                SFElibapr-devel
Requires:                SUNWpostgr-devel
Requires:                SUNWsqlite3-devel
Requires:                SUNWsfwhea

%prep
%setup -q -c -n %name-%version

echo '# BeleniX Layout
<Layout BeleniX>
    prefix:        %{_basedir}/gnu
    exec_prefix:   ${prefix}
    bindir:        ${exec_prefix}/bin
    sbindir:       ${exec_prefix}/bin
    libdir:        ${exec_prefix}/lib
    libexecdir:    ${exec_prefix}/libexec
    mandir:        ${exec_prefix}/man
    sysconfdir:    %{_sysconfdir}/apr-util/1.3
    datadir:       %{_datadir}/apr-util/1.3
    includedir:    ${exec_prefix}/include
    localstatedir: ${prefix}
    installbuilddir: %{_datadir}/apr/build
    manualdir:     ${prefix}/manual
    runtimedir:    %{_datadir}/run/apr-util/1.3
</Layout>' >> apr-util-%{version}/config.layout

%ifarch amd64 sparcv9
cp -pr apr-util-%{version} apr-util-%{version}-64

echo '# BeleniX Layout
<Layout BeleniX>
    prefix:        %{_basedir}/gnu
    exec_prefix:   ${prefix}
    bindir:        ${exec_prefix}/bin/%{_arch64}
    sbindir:       ${exec_prefix}/bin/%{_arch64}
    libdir:        ${exec_prefix}/lib/%{_arch64}
    libexecdir:    ${exec_prefix}/libexec/%{_arch64}
    mandir:        ${exec_prefix}/man
    sysconfdir:    %{_sysconfdir}/apr-util/1.3
    datadir:       %{_datadir}/apr-util/1.3
    includedir:    ${exec_prefix}/include
    localstatedir: ${prefix}
    installbuilddir: %{_datadir}/apr/build/%{_arch64}
    manualdir:     ${prefix}/manual
    runtimedir:    %{_datadir}/run/apr-util/1.3
</Layout>' >> apr-util-%{version}/config.layout

(cd apr-util-%{version}-64
 %patch1 -p1
 cat apr-util.pc.in | \
   sed 's|Libs: -L${libdir}|Libs: -L${libdir} -R${libdir} -L%{_basedir}/lib/%{_arch64} -R%{_basedir}/lib/%{_arch64}|' \
   > apr-util.pc.in.new
 cp apr-util.pc.in.new apr-util.pc.in
 rm -f apr-util.pc.in.new)
%endif

(cd apr-util-%{version}
 %patch1 -p1
 cat apr-util.pc.in | \
   sed 's|Libs: -L${libdir}|Libs: -L${libdir} -R${libdir} -L%{_basedir}/lib -R%{_basedir}/lib|' \
   > apr-util.pc.in.new
 cp apr-util.pc.in.new apr-util.pc.in
 rm -f apr-util.pc.in.new)


%build

PG_DIR=/usr/postgres/%{postgres_version}
MYS_DIR=/usr/mysql/%{mysql_version}

%ifarch amd64 sparcv9
cd apr-util-%{version}-64

PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
CFLAGS="%optflags64 -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
CPPFLAGS="%optflags64 -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
LD=/usr/ccs/bin/ld
LDFLAGS="%_ldflags64 -L$RPM_BUILD_ROOT%{_libdir} -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
LIBS="-m64 -lgdbm"
PGSQL_CONFIG=${PG_DIR}/bin/%{_arch64}/pg_config
MYSQL_CONFIG=${MYS_DIR}/bin/%{_arch64}/mysql_config

export PATH CFLAGS CPPFLAGS LD LDFLAGS PGSQL_CONFIG MYSQL_CONFIG

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}/%{_arch64} \
    --enable-layout=BeleniX \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-threads \
    --with-apr=%{_prefix}/bin/%{_arch64}/apr-1-config \
    --with-dbm=gdbm \
    --with-gdbm=yes \
    --with-pgsql=${PG_DIR} \
    --with-mysql=${MYS_DIR} \
    --with-sqlite3 \
    --with-ldap

# Unfortunate steps to work around a broken configure script
# that does not honour CFLAGS/CPPFLAGS/LDFLAGS when generating
# the Makefile
# configure is broken in other wasy as well. We need to specify
# *both* --with-dbm=gdbm and --with-gdbm... otherwise gdbm support
# is compiled with missing symbols due to config flags not being
# set properly!
#
[ ! -f Makefile.orig ] && cp Makefile Makefile.orig
cat Makefile | sed 's|INCLUDES =|INCLUDES = -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server|' > Makefile.new
cp Makefile.new Makefile
rm -f Makefile.new
cat Makefile | sed 's|APRUTIL_LIBS =|APRUTIL_LIBS = -m64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -liconv -lintl -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}|' > Makefile.new
cp Makefile.new Makefile
rm -f Makefile.new
[ ! -f build/rules.mk.orig ] && cp build/rules.mk build/rules.mk.orig
cat build/rules.mk | sed "s|^CFLAGS=.*|CFLAGS=${CFLAGS}|" > build/rules.mk.new
cp build/rules.mk.new build/rules.mk
rm -f build/rules.mk.new 

LDFLAGS="-L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
cat apu-1-config | \
  sed "s|^LDFLAGS=|LDFLAGS=\"${LDFLAGS}\"|" > apu-1-config.new
cp apu-1-config.new apu-1-config
rm -f apu-1-config.new

make
cd ..
%endif

cd apr-util-%{version}
PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
CPPFLAGS="-I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server"
LD=/usr/ccs/bin/ld
LDFLAGS="%_ldflags -L$RPM_BUILD_ROOT%{_libdir} -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"
PGSQL_CONFIG=${PG_DIR}/bin/pg_config
MYSQL_CONFIG=${MYS_DIR}/bin/mysql_config

export PATH CFLAGS CPPFLAGS LD LDFLAGS PGSQL_CONFIG MYSQL_CONFIG

./configure \
    --prefix=%{_prefix} \
    --enable-layout=BeleniX \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-threads \
    --with-apr=%{_prefix}/bin/apr-1-config \
    --with-dbm=gdbm \
    --with-gdbm=/usr \
    --with-pgsql=${PG_DIR} \
    --with-mysql=${MYS_DIR} \
    --with-sqlite3 \
    --with-ldap

# Unfortunate steps to work around a broken configure script
# that does not honour CFLAGS/CPPFLAGS/LDFLAGS when generating
# the Makefile
# configure is broken in other wasy as well. We need to specify
# *both* --with-dbm=gdbm and --with-gdbm... otherwise gdbm support
# is compiled with missing symbols due to config flags not being
# set properly!
#
[ ! -f Makefile.orig ] && cp Makefile Makefile.orig
cat Makefile | sed 's|INCLUDES =|INCLUDES = -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server|' > Makefile.new
cp Makefile.new Makefile
rm -f Makefile.new
cat Makefile | sed 's|APRUTIL_LIBS =|APRUTIL_LIBS = -L/usr/gnu/lib -R/usr/gnu/lib -liconv -lintl -L/usr/sfw/lib -R/usr/sfw/lib|' > Makefile.new
cp Makefile.new Makefile
rm -f Makefile.new

LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"
cat apu-1-config | \
  sed "s|^LDFLAGS=|LDFLAGS=\"${LDFLAGS}\"|" > apu-1-config.new
cp apu-1-config.new apu-1-config
rm -f apu-1-config.new

make

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd apr-util-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.exp
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/apr-util-1/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_infodir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/apu-1-config $RPM_BUILD_ROOT%{_bindir}/%{_arch64}

(cd $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/
 ln -s libaprutil.so.0 libaprutil-1.so.0)
cd ..
%endif

cd apr-util-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp
rm -f $RPM_BUILD_ROOT%{_libdir}/apr-util-1/*.la
(cd $RPM_BUILD_ROOT%{_libdir}
 ln -s libaprutil.so.0 libaprutil-1.so.0)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/apu-1-config
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/apr-util-1
%{_libdir}/apr-util-1/*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/apu-1-config
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/apr-util-1
%{_libdir}/%{_arch64}/apr-util-1/*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Feb 15 2009 - moinakg@gmail.com
- Major fixes.
* Tue Feb 10 2009 - moinakg@gmail.com
- Bump version to 1.3.4.
- Add 64Bit build support.
* Sun Feb 24 2008 - moinakg@gmail.com
- Update sqlite dependency.
* Tue Jan 22 2008 - moinakg@gmail.com
- Initial spec.
