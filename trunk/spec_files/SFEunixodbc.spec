%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                   SFEunixodbc
Summary:                ODBC Driver Manager
Version:                2.2.12
URL:                    http://www.unixodbc.org
Source:                 http://www.unixodbc.org/unixODBC-%{version}.tar.gz

License:                GPLv2&LGPLv2|GPLv3&LGPLv3
SUNW_BaseDir:           /
SUNW_Copyright:         %{name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SFEreadline
Requires:               SFEncurses
BuildRequires:          SFEreadline-devel
BuildRequires:          SFEncurses-devel

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp unixODBC-%{version} unixODBC-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd unixODBC-%{version}-64
CFLAGS="%optflags64 -D_REENTRANT -D__EXTENSIONS__ -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_POSIX_PTHREAD_SEMANTICS -DSOLARIS -DSOLARIS10 -DNDEBUG -DNO_DEBUG"
export CFLAGS

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir}/%{_arch64} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir}/%{_arch64} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir}/%{_arch64} \
        --sysconfdir=%{_sysconfdir} \
        --with-libiconv-prefix=%{_prefix} \
        --with-x --x-includes=/usr/X11/include --x-libraries=/usr/X11/lib/%{_arch64} \
        --enable-shared \
        --with-pic \
        --enable-rpath \
        --enable-threads \
        --enable-stats \
        --enable-drivers \
        --enable-inicaching \
        --enable-rtldgroup \
        --enable-readline \
        --enable-inicaching \
        --enable-iconv \
        --disable-gui --disable-qt --without-qt

make -j $CPUS
cd ..
%endif

cd unixODBC-%{version}
CFLAGS="%optflags -D_REENTRANT -D__EXTENSIONS__ -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_POSIX_PTHREAD_SEMANTICS -DSOLARIS -DSOLARIS10 -DNDEBUG -DNO_DEBUG"
export CFLAGS

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --with-libiconv-prefix=%{_prefix} \
        --with-x --x-includes=/usr/X11/include --x-libraries=/usr/X11/lib \
        --enable-shared \
        --with-pic \
        --enable-rpath \
        --enable-threads \
        --enable-stats \
        --enable-drivers \
        --enable-inicaching \
        --enable-rtldgroup \
        --enable-readline \
        --enable-inicaching \
        --enable-iconv \
        --disable-gui --disable-qt --without-qt

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd unixODBC-%{version}-64
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd unixODBC-%{version}
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/iusql
%{_bindir}/odbc_config
%{_bindir}/odbcinst
#
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%_arch64
%{_bindir}/%_arch64/dltest
%{_bindir}/%_arch64/isql
%{_bindir}/%_arch64/iusql
%{_bindir}/%_arch64/odbc_config
%{_bindir}/%_arch64/odbcinst
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/autotest.h
%{_includedir}/odbcinst.h
%{_includedir}/odbcinstext.h
%{_includedir}/sql.h
%{_includedir}/sqlext.h
%{_includedir}/sqltypes.h
%{_includedir}/sqlucode.h
%{_includedir}/uodbc_extras.h
%{_includedir}/uodbc_stats.h

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libboundparam.so
%{_libdir}/libboundparam.so.1
%{_libdir}/libboundparam.so.1.0.0
%{_libdir}/libesoobS.so
%{_libdir}/libesoobS.so.1
%{_libdir}/libesoobS.so.1.0.0
%{_libdir}/libgtrtst.so
%{_libdir}/libgtrtst.so.1
%{_libdir}/libgtrtst.so.1.0.0
%{_libdir}/libmimerS.so
%{_libdir}/libmimerS.so.1
%{_libdir}/libmimerS.so.1.0.0
%{_libdir}/libnn.so
%{_libdir}/libnn.so.1
%{_libdir}/libnn.so.1.0.0
%{_libdir}/libodbc.so
%{_libdir}/libodbc.so.1
%{_libdir}/libodbc.so.1.0.0
%{_libdir}/libodbccr.so
%{_libdir}/libodbccr.so.1
%{_libdir}/libodbccr.so.1.0.0
%{_libdir}/libodbcdrvcfg1S.so
%{_libdir}/libodbcdrvcfg1S.so.1
%{_libdir}/libodbcdrvcfg1S.so.1.0.0
%{_libdir}/libodbcdrvcfg2S.so
%{_libdir}/libodbcdrvcfg2S.so.1
%{_libdir}/libodbcdrvcfg2S.so.1.0.0
%{_libdir}/libodbcinst.so
%{_libdir}/libodbcinst.so.1
%{_libdir}/libodbcinst.so.1.0.0
%{_libdir}/libodbcminiS.so
%{_libdir}/libodbcminiS.so.1
%{_libdir}/libodbcminiS.so.1.0.0
%{_libdir}/libodbcmyS.so
%{_libdir}/libodbcmyS.so.1
%{_libdir}/libodbcmyS.so.1.0.0
%{_libdir}/libodbcnnS.so
%{_libdir}/libodbcnnS.so.1
%{_libdir}/libodbcnnS.so.1.0.0
%{_libdir}/libodbcpsql.so
%{_libdir}/libodbcpsql.so.1
%{_libdir}/libodbcpsql.so.1.0.0
%{_libdir}/libodbcpsql.so.2
%{_libdir}/libodbcpsql.so.2.0.0
%{_libdir}/libodbcpsqlS.so
%{_libdir}/libodbcpsqlS.so.1
%{_libdir}/libodbcpsqlS.so.1.0.0
%{_libdir}/libodbctxt.so
%{_libdir}/libodbctxt.so.1
%{_libdir}/libodbctxt.so.1.0.0
%{_libdir}/libodbctxtS.so
%{_libdir}/libodbctxtS.so.1
%{_libdir}/libodbctxtS.so.1.0.0
%{_libdir}/liboplodbcS.so
%{_libdir}/liboplodbcS.so.1
%{_libdir}/liboplodbcS.so.1.0.0
%{_libdir}/liboraodbcS.so
%{_libdir}/liboraodbcS.so.1
%{_libdir}/liboraodbcS.so.1.0.0
%{_libdir}/libsapdbS.so
%{_libdir}/libsapdbS.so.1
%{_libdir}/libsapdbS.so.1.0.0
%{_libdir}/libtdsS.so
%{_libdir}/libtdsS.so.1
%{_libdir}/libtdsS.so.1.0.0
%{_libdir}/libtemplate.so
%{_libdir}/libtemplate.so.1
%{_libdir}/libtemplate.so.1.0.0
#
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/libboundparam.so
%{_libdir}/%_arch64/libboundparam.so.1
%{_libdir}/%_arch64/libboundparam.so.1.0.0
%{_libdir}/%_arch64/libesoobS.so
%{_libdir}/%_arch64/libesoobS.so.1
%{_libdir}/%_arch64/libesoobS.so.1.0.0
%{_libdir}/%_arch64/libgtrtst.so
%{_libdir}/%_arch64/libgtrtst.so.1
%{_libdir}/%_arch64/libgtrtst.so.1.0.0
%{_libdir}/%_arch64/libmimerS.so
%{_libdir}/%_arch64/libmimerS.so.1
%{_libdir}/%_arch64/libmimerS.so.1.0.0
%{_libdir}/%_arch64/libnn.so
%{_libdir}/%_arch64/libnn.so.1
%{_libdir}/%_arch64/libnn.so.1.0.0
%{_libdir}/%_arch64/libodbc.so
%{_libdir}/%_arch64/libodbc.so.1
%{_libdir}/%_arch64/libodbc.so.1.0.0
%{_libdir}/%_arch64/libodbccr.so
%{_libdir}/%_arch64/libodbccr.so.1
%{_libdir}/%_arch64/libodbccr.so.1.0.0
%{_libdir}/%_arch64/libodbcdrvcfg1S.so
%{_libdir}/%_arch64/libodbcdrvcfg1S.so.1
%{_libdir}/%_arch64/libodbcdrvcfg1S.so.1.0.0
%{_libdir}/%_arch64/libodbcdrvcfg2S.so
%{_libdir}/%_arch64/libodbcdrvcfg2S.so.1
%{_libdir}/%_arch64/libodbcdrvcfg2S.so.1.0.0
%{_libdir}/%_arch64/libodbcinst.so
%{_libdir}/%_arch64/libodbcinst.so.1
%{_libdir}/%_arch64/libodbcinst.so.1.0.0
%{_libdir}/%_arch64/libodbcminiS.so
%{_libdir}/%_arch64/libodbcminiS.so.1
%{_libdir}/%_arch64/libodbcminiS.so.1.0.0
%{_libdir}/%_arch64/libodbcmyS.so
%{_libdir}/%_arch64/libodbcmyS.so.1
%{_libdir}/%_arch64/libodbcmyS.so.1.0.0
%{_libdir}/%_arch64/libodbcnnS.so
%{_libdir}/%_arch64/libodbcnnS.so.1
%{_libdir}/%_arch64/libodbcnnS.so.1.0.0
%{_libdir}/%_arch64/libodbcpsql.so
%{_libdir}/%_arch64/libodbcpsql.so.1
%{_libdir}/%_arch64/libodbcpsql.so.1.0.0
%{_libdir}/%_arch64/libodbcpsql.so.2
%{_libdir}/%_arch64/libodbcpsql.so.2.0.0
%{_libdir}/%_arch64/libodbcpsqlS.so
%{_libdir}/%_arch64/libodbcpsqlS.so.1
%{_libdir}/%_arch64/libodbcpsqlS.so.1.0.0
%{_libdir}/%_arch64/libodbctxt.so
%{_libdir}/%_arch64/libodbctxt.so.1
%{_libdir}/%_arch64/libodbctxt.so.1.0.0
%{_libdir}/%_arch64/libodbctxtS.so
%{_libdir}/%_arch64/libodbctxtS.so.1
%{_libdir}/%_arch64/libodbctxtS.so.1.0.0
%{_libdir}/%_arch64/liboplodbcS.so
%{_libdir}/%_arch64/liboplodbcS.so.1
%{_libdir}/%_arch64/liboplodbcS.so.1.0.0
%{_libdir}/%_arch64/liboraodbcS.so
%{_libdir}/%_arch64/liboraodbcS.so.1
%{_libdir}/%_arch64/liboraodbcS.so.1.0.0
%{_libdir}/%_arch64/libsapdbS.so
%{_libdir}/%_arch64/libsapdbS.so.1
%{_libdir}/%_arch64/libsapdbS.so.1.0.0
%{_libdir}/%_arch64/libtdsS.so
%{_libdir}/%_arch64/libtdsS.so.1
%{_libdir}/%_arch64/libtdsS.so.1.0.0
%{_libdir}/%_arch64/libtemplate.so
%{_libdir}/%_arch64/libtemplate.so.1
%{_libdir}/%_arch64/libtemplate.so.1.0.0
%endif

%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/odbc.ini
%{_sysconfdir}/odbcinst.ini
%{_sysconfdir}/ODBCDataSources

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial version
