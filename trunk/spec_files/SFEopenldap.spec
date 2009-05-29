#
# spec file for package SFEopenldap
#
# includes module(s): openldap
#
#
%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define maj_ver          2.4
Name:                    SFEopenldap
Summary:                 Lightweight Directory Access Protocol
Version:                 %{maj_ver}.16
License:                 BSD
URL:                     http://www.OpenLDAP.org/
Source:                  ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1:                 openldap.xml

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
License:                 GPLv2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEbdb
BuildRequires: SFEbdb-devel
Requires: SUNWopensslr
BuildRequires: SUNWopenssl-include
Requires: SFEcyrus-sasl
BuildRequires: SFEcyrus-sasl
Requires: SFEunixodbc

%description
OpenLDAP Software is an open source implementation of the Lightweight Directory Access Protocol.
The suite includes:

    * slapd - stand-alone LDAP daemon (server)
    * slurpd - stand-alone LDAP update replication daemon
    * libraries implementing the LDAP protocol, and
    * utilities, tools, and sample clients. 

%package devel
Summary:                 Development files for the openldap package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEbdb-devel
Requires: SUNWgnutls-devel
Requires: SFEcyrus-sasl


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp openldap-%{version} openldap-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
OPATH="${PATH}"

%ifarch amd64 sparcv9
cd openldap-%{version}-64

LOC_INC=`pwd`/include
export CPPFLAGS="-I${LOC_INC}"
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64}"
export PATH="%{_prefix}/bin/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}          \
            --sbindir=%{_sbindir}/%{_arch64}        \
            --libdir=%{_libdir}/%{_arch64}          \
            --libexecdir=%{_libexecdir}/%{_arch64}  \
            --sysconfdir=%{_sysconfdir}      \
            --includedir=%{_includedir}/openldap \
            --localstatedir=/var/openldap \
            --with-cyrus-sasl \
            --enable-bdb \
            --with-odbc=unixodbc \
            --with-openssl \
            --enable-overlays \
            --enable-crypt \
            --enable-null \
            --enable-passwd \
            --enable-shell \
            --with-threads \
            --without-gnutls \
            --with-tls=openssl \
            --disable-openssl-version-check \
            --enable-shared \
	    --disable-static

make -j$CPUS 
cd ..
%endif

cd openldap-%{version}

LOC_INC=`pwd`/include
export CPPFLAGS="-I${LOC_INC}"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -Wl,-z -Wl,muldefs -L/lib -R/lib"
export PATH="${OPATH}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --sbindir=%{_sbindir}            \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --includedir=%{_includedir}/openldap \
            --localstatedir=/var/openldap \
            --with-cyrus-sasl \
            --enable-bdb \
            --with-odbc=unixodbc \
            --with-openssl \
            --enable-overlays \
            --enable-crypt \
            --enable-null \
            --enable-passwd \
            --enable-shell \
            --with-threads \
            --without-gnutls \
            --with-tls=openssl \
            --disable-openssl-version-check \
            --enable-shared \
            --disable-static

cp servers/slapd/overlays/Makefile servers/slapd/overlays/Makefile.orig 
cat servers/slapd/overlays/Makefile.orig | sed '{
    s@\$(LD) -r@\$(LD) -z muldefs -r@
}'> servers/slapd/overlays/Makefile

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd openldap-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/libldap.so
(cd ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
 lib=""
 for l in libldap-%{maj_ver}.so.*
 do
   lib=${l}
 done
 ln -s ${lib} libldap-%{maj_ver}.so)
cd ..
%endif

cd openldap-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libldap.so
(cd ${RPM_BUILD_ROOT}%{_libdir}
 lib=""
 for l in libldap-%{maj_ver}.so.*
 do
   lib=${l}
 done
 ln -s ${lib} libldap-%{maj_ver}.so)
cd ..

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network/ldap
cp %{SOURCE1} ${RPM_BUILD_ROOT}/var/svc/manifest/network/ldap


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ldap*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/sla*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/slapd

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%{_libdir}/%{_arch64}/slapd
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/ldap*
%dir %attr (0755, root, bin) %{_sbindir}/%{_arch64}
%{_sbindir}/%{_arch64}/sla*
%endif

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/openldap
%{_sysconfdir}/openldap/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%dir %attr (0755, root, bin) %{_mandir}/man8
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%dir %attr (0755, root, sys) /var 
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/network
%dir %attr (0755, root, sys) /var/svc/manifest/network/ldap
%class(manifest) %attr(0444, root, sys) /var/svc/manifest/network/ldap/openldap.xml

%dir %attr (0755, root, bin) /var/openldap
%dir %attr (0755, root, bin) /var/openldap/run
%dir %attr (0755, root, bin) /var/openldap/openldap-data
/var/openldap/openldap-data/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
