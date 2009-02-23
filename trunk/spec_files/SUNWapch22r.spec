#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define APACHE_VERSION 2.2.9
%define APACHE_VERSION_DIR 2.2
%define APACHE_DIR httpd-%{APACHE_VERSION}
%define APACHE_PREFORK_DIR %{APACHE_DIR}-prefork
%define APACHE_WORKER_DIR %{APACHE_DIR}-worker

%ifarch amd64 sparcv9
%define APACHE_PREFORK_DIR64 %{APACHE_PREFORK_DIR}-64
%define APACHE_WORKER_DIR64 %{APACHE_WORKER_DIR}-64
%endif

%define APACHE_DIR_PREFIX apache2/%{APACHE_VERSION_DIR}
%define APACHE_USR_PREFIX %{_basedir}/%{APACHE_DIR_PREFIX}
%define APACHE_VAR_PREFIX %{_localstatedir}/%{APACHE_DIR_PREFIX}
%define APACHE_ETC_PREFIX %{_sysconfdir}/%{APACHE_DIR_PREFIX}
%define APACHE_LAYOUT Solaris-Apache2

%define APR_USR_PREFIX /usr/gnu
%define APR_UTIL_USR_PREFIX /usr/gnu

%define LD_OPTIONS "-M %{SOURCE51}"
%define CFLAGS_COMMON "-xchip=pentium -xspace -Xa  -xildoff -xc99=all -DSSL_EXPERIMENTAL -DSSL_ENGINE -xO4"
%define CPPFLAGS "-I%{sfw_inc} -I%{gnu_inc} -I%{_includedir}"
%define MAKE %{_basedir}/ccs/bin/make
%define INSTALL %{_basedir}/ucb/install
%define PERL %{_basedir}/perl5/bin/perl
%define CXXFLAGS "-norunpath"
%define LDFLAGS32 "-L%{sfw_lib} -R%{sfw_lib} -s  ${LD_OPTIONS} -L%{_libdir} -R%{_libdir} -L%{gnu_lib} -R%{gnu_lib}"
%define LDFLAGS64 "-L%{sfw_lib}/%{_arch64} -R%{sfw_lib}/%{_arch64} -s  ${LD_OPTIONS} -L%{_libdir}/%{_arch64} -R%{_libdir}/%{_arch64} -L%{gnu_lib}/%{_arch64} -R%{gnu_lib}/%{_arch64}"


%define src1    %{_sourcedir}/apache2/patches/mod_auth_gss_Makefile.patch.64
%define src2    %{_sourcedir}/apache2/patches/apachectl.patch
%define src3    %{_sourcedir}/apache2/patches/mod_proxy_ftp.patch
%define src4    %{_sourcedir}/apache2/patches/apr_common.m4.patch
%define src5    %{_sourcedir}/apache2/patches/apachectl.patch.64
%define src6    %{_sourcedir}/apache2/modules/fcgid.mk
%define src7    %{_sourcedir}/apache2/modules/apxs-fcgid.ksh93
%define src8    %{_sourcedir}/apache2/modules/dtrace.conf
%define src9    %{_sourcedir}/apache2/modules/workers.properties
%define src10   %{_sourcedir}/apache2/modules/jk.conf
%define src11   %{_sourcedir}/apache2/modules/install-module.ksh93
%define src12   %{_sourcedir}/apache2/modules/security2.mk
%define src13   %{_sourcedir}/apache2/modules/fcgid.conf
%define src14   %{_sourcedir}/apache2/modules/apxs-security2.ksh93
%define src15   %{_sourcedir}/apache2/modules/dtrace.mk
%define src16   %{_sourcedir}/apache2/modules/jk.mk
%define src17   %{_sourcedir}/apache2/modules/apxs-dtrace.ksh93
%define src18   %{_sourcedir}/apache2/modules/Makefile.sfw
%define src19   %{_sourcedir}/apache2/modules/apxs-jk.ksh93
%define src20   %{_sourcedir}/apache2/modules/security2.conf
%define src21   %{_sourcedir}/apache2/Solaris/apache2.1m.sunman
%define src22   %{_sourcedir}/apache2/Solaris/Makefile.in.patch
%define src23   %{_sourcedir}/apache2/Solaris/fix-config.nice.sed
%define src24   %{_sourcedir}/apache2/Solaris/sslconf.sed
%define src25   %{_sourcedir}/apache2/Solaris/http-apache22.xml
%define src26   %{_sourcedir}/apache2/Solaris/httpdconf.sed
%define src27   %{_sourcedir}/apache2/Solaris/httpd.conf.patch
%define src28   %{_sourcedir}/apache2/Solaris/modules-32.load
%define src29   %{_sourcedir}/apache2/Solaris/favicon.gif
%define src30   %{_sourcedir}/apache2/Solaris/template
%define src31   %{_sourcedir}/apache2/Solaris/template/configure.patch
%define src32   %{_sourcedir}/apache2/Solaris/template/http-apache22
%define src33   %{_sourcedir}/apache2/Solaris/template/loadmodules.sed
%define src34   %{_sourcedir}/apache2/Solaris/template/special.mk.patch
%define src35   %{_sourcedir}/apache2/Solaris/template/src.patch
%define src36   %{_sourcedir}/apache2/Solaris/template/apxs.patch
%define src37   %{_sourcedir}/apache2/Solaris/template/rules.mk.patch
%define src38   %{_sourcedir}/apache2/Solaris/modules-64.load
%define src39   %{_sourcedir}/apache2/Solaris/favicon.ico
%define src40   %{_sourcedir}/apache2/Solaris/fix-config_vars.sed
%define src41   %{_sourcedir}/apache2/Solaris/envvars.sed
%define src42   %{_sourcedir}/apache2/mod_auth_gss
%define src43   %{_sourcedir}/apache2/mod_auth_gss/mod_auth_gss.html
%define src44   %{_sourcedir}/apache2/mod_auth_gss/mod_auth_gss.c
%define src45   %{_sourcedir}/apache2/mod_auth_gss/README
%define src46   %{_sourcedir}/apache2/mod_auth_gss/Makefile
%define src55   %{_sourcedir}/apache2/tools/post_process_so
%define src56   %{_sourcedir}/apache2/tools/post_process

Name:                    SUNWapch22r
Summary:                 The Apache HTTP Server Version 2.2 (root components)
Version:                 %{APACHE_VERSION}
%define mod_dtrace_version 0.3a
%define mod_fcgid_version 2.2
%define modsecurity_version 2.1.5
%define connector_version 1.2.25
%define mod_perl_version 2.0.2
URL:                     http://www.apache.org/
Source:                  http://www.belenix.org/binfiles/apache/httpd-%{version}.tar.gz
Source47:                http://www.belenix.org/binfiles/apache/mod_dtrace-%{mod_dtrace_version}.tar.gz
Source48:                http://www.belenix.org/binfiles/apache/mod_fcgid.%{mod_fcgid_version}.tgz
Source49:                http://www.belenix.org/binfiles/apache/modsecurity-apache_%{modsecurity_version}.tar.gz
Source50:                http://www.belenix.org/binfiles/apache/tomcat-connectors-%{connector_version}-src.tar.gz
Source51:                mapfile_noexstk
Source52:                install-apache2
Source53:                install-apache2-64
Source54:                install.subr
Source57:                http://www.belenix.org/binfiles/apache/mod_perl-%{mod_perl_version}.tar.gz


SUNW_PkgType:            root
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWperl584core
BuildRequires: SFElibapr-devel
BuildRequires: SFEaprutil-devel


%package -n SUNWapch22u
Summary:                 The Apache HTTP Server Version 2.2 (usr components)
Version:                 %{APACHE_VERSION}
SUNW_BaseDir:            /
SUNW_PkgType:            usr
%include default-depend.inc
Requires: %name
Requires: SUNWopensslr
Requires: SFElibapr
Requires: SFElibapr-devel
Requires: SFEaprutil
Requires: SFEaprutil-devel
Requires: SFEgawk

%package -n SUNWapch22d
Summary:                 The Apache HTTP Server Version 2.2 (documentation)
Version:                 %{APACHE_VERSION}
SUNW_BaseDir:            /
SUNW_PkgType:            usr
%include default-depend.inc
Requires: SUNWapch22u

%package -n SUNWapch22m-dtrace
Summary:                 DTrace plugin for Apache Web Server V2.2
Version:                 %{mod_dtrace_version}
SUNW_BaseDir:            /
SUNW_PkgType:            usr
%include default-depend.inc
Requires: SUNWapch22u

%package -n SUNWapch22r-dtrace
Summary:                 DTrace plugin for Apache Web Server V2.2 (root components)
Version:                 %{mod_dtrace_version}
SUNW_BaseDir:            /
SUNW_PkgType:            root
%include default-depend.inc
Requires: SUNWapch22u
Requires: SUNWapch22m-dtrace

%package -n SUNWapch22m-fcgid
Summary:                 FastCGI plugin for Apache Web Server V2.2
Version:                 %{mod_fcgid_version}
SUNW_BaseDir:            /
SUNW_PkgType:            usr
%include default-depend.inc
Requires: SUNWapch22u

%package -n SUNWapch22r-fcgid
Summary:                 FastCGI plugin for Apache Web Server V2.2 (root components)
Version:                 %{mod_fcgid_version}
SUNW_BaseDir:            /
SUNW_PkgType:            root
%include default-depend.inc
Requires: SUNWapch22u
Requires: SUNWapch22m-fcgid

%package -n SUNWapch22m-jk
Summary:                 Tomcat Connector plugin for Apache Web Server V2.2
Version:                 %{connector_version}
SUNW_BaseDir:            /
SUNW_PkgType:            usr
%include default-depend.inc
Requires: SUNWapch22u

%package -n SUNWapch22r-jk
Summary:                 Tomcat Connector plugin for Apache Web Server V2.2 (root components)
Version:                 %{connector_version}
SUNW_BaseDir:            /
SUNW_PkgType:            root
%include default-depend.inc
Requires: SUNWapch22u
Requires: SUNWapch22m-jk

%package -n SUNWapch22m-security
Summary:                 Mod Security plugin for Apache Web Server Version 2.2
Version:                 %{modsecurity_version}
SUNW_BaseDir:            /
SUNW_PkgType:            usr
%include default-depend.inc
Requires: SUNWapch22u
Requires: SUNWapch22m-security

%package -n SUNWapch22r-security
Summary:                 Mod Security plugin for Apache Web Server Version 2.2 (root components)
Version:                 %{modsecurity_version}
SUNW_BaseDir:            /
SUNW_PkgType:            root
%include default-depend.inc
Requires: SUNWapch22u
Requires: SUNWapch22m-security



%prep
if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

PATH=/usr/bin:/usr/sfw/bin:/usr/X11/bin:/opt/SUNWspro/bin
export PATH

rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}

cp -r %{_sourcedir}/apache2/* .

#
# We are using patches copied from SFW gate here which expect APR and APU in
# proto area. However we use the system's APR and APU so we just substitute
# __dummy__ for the APR and APU patterns. We do not want them to be translated
# into the build directory.
#
(cd Solaris/template
mkdir -p ../32 ../64
for i in `ls *.sed *.patch http-apache22`; do
      sed -e 's/::ISAINFO:://g' \
           -e 's/::BITNESS::/32/g' \
           -e 's!::APR_PREFIX::!/__dummy__!g' \
           -e 's!::APU_PREFIX::!/__dummy__!g' \
      < $i > ../32/$i
      sed -e 's/::ISAINFO::/\/%{_arch64}/g' \
           -e 's/::BITNESS::/64/g' \
           -e 's!::APR_PREFIX::!/__dummy_!g' \
           -e 's!::APU_PREFIX::!/__dummy__!g' \
      < $i > ../64/$i
done)

gunzip -c %{SOURCE} | tar xopf -
mv %{APACHE_DIR} %{APACHE_PREFORK_DIR}
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../Solaris/32/configure.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../Solaris/32/apxs.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../Solaris/32/src.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../Solaris/httpd.conf.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../Solaris/Makefile.in.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../patches/apachectl.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../patches/apr_common.m4.patch)
(cd %{APACHE_PREFORK_DIR}; gpatch -p1 < ../patches/mod_proxy_ftp.patch)

gunzip -c %{SOURCE} | tar xopf -
mv %{APACHE_DIR} %{APACHE_WORKER_DIR}
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../Solaris/32/configure.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../Solaris/32/apxs.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../Solaris/32/src.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../Solaris/httpd.conf.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../Solaris/Makefile.in.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../patches/apachectl.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../patches/apr_common.m4.patch)
(cd %{APACHE_WORKER_DIR}; gpatch -p1 < ../patches/mod_proxy_ftp.patch)

echo "
APACHE_VERSION=%{APACHE_VERSION}
APACHE_VERSION_DIR=%{APACHE_VERSION_DIR}
APACHE_DIR=%{APACHE_DIR}
APACHE_PREFORK_DIR=%{APACHE_PREFORK_DIR}
APACHE_WORKER_DIR=%{APACHE_WORKER_DIR}

APACHE_DIR_PREFIX=%{APACHE_DIR_PREFIX}
APACHE_USR_PREFIX=%{APACHE_USR_PREFIX}
APACHE_VAR_PREFIX=%{APACHE_VAR_PREFIX}
APACHE_ETC_PREFIX=%{APACHE_ETC_PREFIX}
APACHE_LAYOUT=%{APACHE_LAYOUT}" > apache.build.env

cd modules
gunzip -c %{SOURCE47} | tar xf -
gunzip -c %{SOURCE48} | tar xf -
gunzip -c %{SOURCE49} | tar xf -
gunzip -c %{SOURCE50} | tar xf -
find modsecurity-apache_%{modsecurity_version} -type d | xargs chmod go+rx
cd ..

chmod +x %{src55}
chmod +x %{src56}


%ifarch amd64 sparcv9
gunzip -c %{SOURCE} | tar xopf -
mv %{APACHE_DIR} %{APACHE_PREFORK_DIR64}
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../Solaris/64/configure.patch)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../Solaris/64/apxs.patch)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../Solaris/64/src.patch)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../Solaris/httpd.conf.patch)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../Solaris/Makefile.in.patch)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../patches/apachectl.patch.64)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../patches/apr_common.m4.patch)
(cd %{APACHE_PREFORK_DIR64}; gpatch -p1 < ../patches/mod_proxy_ftp.patch)

gunzip -c %{SOURCE} | tar xopf -
mv %{APACHE_DIR} %{APACHE_WORKER_DIR64}
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../Solaris/64/configure.patch)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../Solaris/64/apxs.patch)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../Solaris/64/src.patch)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../Solaris/httpd.conf.patch)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../Solaris/Makefile.in.patch)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../patches/apachectl.patch.64)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../patches/apr_common.m4.patch)
(cd %{APACHE_WORKER_DIR64}; gpatch -p1 < ../patches/mod_proxy_ftp.patch)

mkdir mod_auth_gss-64
cp -r mod_auth_gss/* mod_auth_gss-64

mkdir modules-64
cp -r modules/* modules-64
mv modules-64/mod_dtrace-%{mod_dtrace_version} modules-64/mod_dtrace-%{mod_dtrace_version}-64
mv modules-64/mod_fcgid.%{mod_fcgid_version} modules-64/mod_fcgid.%{mod_fcgid_version}-64
mv modules-64/modsecurity-apache_%{modsecurity_version} modules-64/modsecurity-apache_%{modsecurity_version}-64
mv modules-64/tomcat-connectors-%{connector_version}-src modules-64/tomcat-connectors-%{connector_version}-src-64

cd mod_auth_gss-64
gpatch -p1 < ../patches/mod_auth_gss_Makefile.patch.64
cd ..

echo "
APACHE_PREFORK_DIR64=%{APACHE_PREFORK_DIR64}
APACHE_WORKER_DIR64=%{APACHE_WORKER_DIR64}
" >> apache.build.env

%endif

mv modules/mod_dtrace-%{mod_dtrace_version} modules/mod_dtrace-%{mod_dtrace_version}-32
mv modules/mod_fcgid.%{mod_fcgid_version} modules/mod_fcgid.%{mod_fcgid_version}-32
mv modules/modsecurity-apache_%{modsecurity_version} modules/modsecurity-apache_%{modsecurity_version}-32
mv modules/tomcat-connectors-%{connector_version}-src modules/tomcat-connectors-%{connector_version}-src-32
(cd modules
  gunzip -c %{SOURCE57} | tar xf -)


%build
cd %{name}-%{version}
BLDDIR=`pwd`

PATH=/usr/bin:/usr/sfw/bin:/usr/X11/bin:/opt/SUNWspro/bin
export PATH

HTTPD_COMMON_CONFIGURE_OPTIONS="\
    --prefix=%{APACHE_USR_PREFIX} \
    --enable-layout=%{APACHE_LAYOUT} \
    --enable-mods-shared=all \
    --enable-so \
    --enable-suexec \
    --with-suexec-caller=webservd \
    --enable-proxy \
    --enable-proxy-connect \
    --enable-proxy-ftp \
    --enable-proxy-http \
    --enable-proxy-ajp \
    --enable-proxy-balancer \
    --enable-cache \
    --enable-file-cache \
    --enable-disk-cache \
    --enable-mem-cache \
    --enable-deflate \
    --enable-cgid \
    --enable-cgi \
    --enable-authnz-ldap \
    --enable-ldap \
    --enable-ssl"

LD_OPTIONS=%{LD_OPTIONS}
CFLAGS_COMMON=%{CFLAGS_COMMON}
CPPFLAGS=%{CPPFLAGS}
MAKE=%{MAKE}
INSTALL=%{INSTALL}
PERL=%{PERL}
CXXFLAGS=%{CXXFLAGS}
LDFLAGS32=%{LDFLAGS32}
LDFLAGS64=%{LDFLAGS64}
DESTDIR=${RPM_BUILD_ROOT}
PATH=${PATH}:%{sfw_bin}
APR_USR_PREFIX=%{APR_USR_PREFIX}
APR_UTIL_USR_PREFIX=%{APR_UTIL_USR_PREFIX}
export LD_OPTIONS PATH MAKE DESTDIR INSTALL PERL CXXFLAGS CPPFLAGS APR_USR_PREFIX APR_UTIL_USR_PREFIX

. ./apache.build.env

#
# First run all the configure scripts
#
%ifarch amd64 sparcv9
cd %{APACHE_PREFORK_DIR64}
CFLAGS="-m64 ${CFLAGS_COMMON}"
LDFLAGS="-m64 ${LDFLAGS64}"
export CFLAGS LDFLAGS

./configure ${HTTPD_COMMON_CONFIGURE_OPTIONS} \
     --with-apr=%{gnu_bin}/%{_arch64}/apr-1-config \
     --with-apr-util=%{gnu_bin}/%{_arch64}/apu-1-config \
     --with-mpm=prefork

cd ${BLDDIR}/%{APACHE_WORKER_DIR64}

./configure ${HTTPD_COMMON_CONFIGURE_OPTIONS} \
     --with-apr=%{gnu_bin}/%{_arch64}/apr-1-config \
     --with-apr-util=%{gnu_bin}/%{_arch64}/apu-1-config \
     --with-mpm=worker
%endif

cd ${BLDDIR}/%{APACHE_PREFORK_DIR}
CFLAGS="-m32 ${CFLAGS_COMMON}"
LDFLAGS="-m32 ${LDFLAGS32}"
export CFLAGS LDFLAGS
./configure ${HTTPD_COMMON_CONFIGURE_OPTIONS} \
     --with-apr=%{gnu_bin}/apr-1-config \
     --with-apr-util=%{gnu_bin}/apu-1-config \
     --with-mpm=prefork

cd ${BLDDIR}/%{APACHE_WORKER_DIR}

./configure ${HTTPD_COMMON_CONFIGURE_OPTIONS} \
     --with-apr=%{gnu_bin}/apr-1-config \
     --with-apr-util=%{gnu_bin}/apu-1-config \
     --with-mpm=worker


#
# Now run all the makes
#
%ifarch amd64 sparcv9
cd ${BLDDIR}/%{APACHE_PREFORK_DIR64}
CFLAGS="-m64 ${CFLAGS_COMMON}"
LDFLAGS="-m64 ${LDFLAGS64}"
export CFLAGS LDFLAGS

${MAKE} -e

cd ${BLDDIR}/%{APACHE_WORKER_DIR64}
${MAKE} -e

%endif

cd ${BLDDIR}/%{APACHE_PREFORK_DIR}
CFLAGS="-m32 ${CFLAGS_COMMON}"
LDFLAGS="-m32 ${LDFLAGS32}"
export CFLAGS LDFLAGS

${MAKE} -e

cd ${BLDDIR}/%{APACHE_WORKER_DIR}
${MAKE} -e


#
# INSTALL Section
#
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cd %{name}-%{version}

BLDDIR=`pwd`
TMP_HDR_DIR32=${BLDDIR}/Solaris/32/include
TMP_HDR_DIR64=${BLDDIR}/Solaris/64/include
TMP_HDR_DIR=${BLDDIR}/Solaris/include

. ./apache.build.env

LD_OPTIONS=%{LD_OPTIONS}
CFLAGS_COMMON=%{CFLAGS_COMMON}
CPPFLAGS=%{CPPFLAGS}
MAKE=%{MAKE}
INSTALL=%{INSTALL}
PERL=%{PERL}
CXXFLAGS=%{CXXFLAGS}
LDFLAGS32=%{LDFLAGS32}
LDFLAGS64=%{LDFLAGS64}
DESTDIR=${RPM_BUILD_ROOT}
PATH=${PATH}:%{sfw_bin}
APR_USR_PREFIX=/usr/gnu
APR_UTIL_USR_PREFIX=/usr/gnu
ROOT=${RPM_BUILD_ROOT}
SRC=%{_sourcedir}/apache2
AP_PERL5LIB=${APACHE_USR_PREFIX}/lib/perl
AP_PERL5BIN=${APACHE_USR_PREFIX}/bin
PERLMAN=${APACHE_USR_PREFIX}/man
export LD_OPTIONS PATH MAKE DESTDIR INSTALL PERL CXXFLAGS CPPFLAGS APR_USR_PREFIX APR_UTIL_USR_PREFIX ROOT SRC
export AP_PERL5LIB AP_PERL5BIN PERLMAN

mkdir -p ${RPM_BUILD_ROOT}/${APACHE_USR_PREFIX}
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_USR_PREFIX}/lib
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_VAR_PREFIX}
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_VAR_PREFIX}/proxy
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_VAR_PREFIX}/libexec
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_ETC_PREFIX}
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_ETC_PREFIX}/conf.d
mkdir -p ${RPM_BUILD_ROOT}/lib/svc/method
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network
mkdir -p ${RPM_BUILD_ROOT}/%{_basedir}/bin
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1m

%ifarch amd64 sparcv9
cd ${APACHE_WORKER_DIR64}
CFLAGS="-m64 ${CFLAGS_COMMON}"
LDFLAGS="-m64 ${LDFLAGS64}"
export CFLAGS LDFLAGS

mkdir -p ${RPM_BUILD_ROOT}/%{_basedir}/bin/%{_arch64}
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_USR_PREFIX}/lib/%{_arch64}

${MAKE} -e install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${TMP_HDR_DIR64}
cp ${DESTDIR}${APACHE_USR_PREFIX}/include/ap_config_layout.h ${TMP_HDR_DIR64}

cd ${BLDDIR}/${APACHE_PREFORK_DIR64}
${MAKE} -e install DESTDIR=${RPM_BUILD_ROOT}
cp ${DESTDIR}${APACHE_ETC_PREFIX}/original/httpd.conf ../Solaris/64

cd ${BLDDIR}/mod_auth_gss-64
${MAKE} install DESTDIR=${RPM_BUILD_ROOT} ROOT=${RPM_BUILD_ROOT}

%endif


cd ${BLDDIR}/${APACHE_WORKER_DIR64}
CFLAGS="-m32 ${CFLAGS_COMMON}"
LDFLAGS="-m32 ${LDFLAGS32}"
export CFLAGS LDFLAGS

${MAKE} -e install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${TMP_HDR_DIR32}
cp ${DESTDIR}${APACHE_USR_PREFIX}/include/ap_config_layout.h ${TMP_HDR_DIR32}

cd ${BLDDIR}/${APACHE_PREFORK_DIR}
${MAKE} -e install DESTDIR=${RPM_BUILD_ROOT}
cp ${DESTDIR}${APACHE_ETC_PREFIX}/original/httpd.conf ../Solaris/32

cd ${BLDDIR}/mod_auth_gss
${MAKE} install DESTDIR=${RPM_BUILD_ROOT} ROOT=${RPM_BUILD_ROOT}

%ifarch amd64 sparcv9
MACH64=%{_arch64}
SRCDIR=%{_sourcedir}
export MACH64 BLDDIR SRCDIR

#
# Run some custom install scripts
#
cd ${BLDDIR}
sh %{SOURCE53}
%endif

unset MACH64
cd ${BLDDIR}
sh %{SOURCE52}
mkdir -p ${TMP_HDR_DIR}

#
# We use a custom install sequence here to unify 32bit and 64bit includes
# since we can only ship one set of includes. Therefore we use
# "/usr/bin/diff -D <64bit>" (and for some exceptions a manual path) to
# generate an unified version of the include files (and add a boilerplate text
# which explains the interface stability status).
# Define the symbol used to distinguish between 32bit and 64bit parts of the
# include file. We cannot use |_LP64| here because not every compiler (like
# Studio 10/11/12) sets it by default (this doesn't harm because the AST
# includes are OS- and platform-specific anyway) and we can't rely on the
# system includes like <sys/isa_defs.h> because "/usr/bin/diff -D<symbol>"
# adds the "#ifdef <symbol>" before any other content and "injecting" an
# "#include <sys/isa_defs.h>" will alter the behaviour of the AST code
# in unpredictable ways (e.g. the resulting code will not longer work).
# Sun-Bug #6524070 ("RFE: Please set |_LP64| for 64bit platforms by default
# (like gcc does)") has been filed against the Sun Studio compiler as RFE
# to set |_LP64| for 64bit targets.
#
for hdr in ap_config_layout.h
do
%ifarch amd64
INTEL_64BITCPPSYMBOL=__amd64
set +e; /usr/bin/diff -D ${INTEL_64BITCPPSYMBOL} \
    ${TMP_HDR_DIR32}/${hdr} ${TMP_HDR_DIR64}/${hdr} > ${TMP_HDR_DIR}/${hdr}
%endif

%ifarch sparcv9
SPARC_64BITCPPSYMBOL=__sparcv9
set +e; /usr/bin/diff -D ${SPARC_64BITCPPSYMBOL} \
    ${TMP_HDR_DIR32}/${hdr} ${TMP_HDR_DIR64}/${hdr} > ${TMP_HDR_DIR}/${hdr}
%endif
cp ${TMP_HDR_DIR}/${hdr} ${RPM_BUILD_ROOT}/%{APACHE_USR_PREFIX}/include
done

#
# Make and Install all the modules
#
APACHE_CONFD=${RPM_BUILD_ROOT}/${APACHE_ETC_PREFIX}/conf.d
APACHE_SCONFD=${RPM_BUILD_ROOT}/${APACHE_ETC_PREFIX}/samples-conf.d

%ifarch amd64 sparcv9
cd ${BLDDIR}/modules-64
PDIR=`pwd`
MACH64=%{_arch64}
LDFLAGS="${LDFLAGS64} -M ${PDIR}/mod_dtrace-%{mod_dtrace_version}-64/mapfile"
CFLAGS="-m64"
export ROOT MACH64 LDFLAGS CFLAGS
sh ./apxs-dtrace.ksh93 -b 64
(cd mod_dtrace-%{mod_dtrace_version}-64
  sh ../install-module.ksh93 -b 64 -m dtrace)
cat dtrace.conf | sed -e 's/::MACH64::/%{_arch64}/;' > ${APACHE_CONFD}/dtrace.conf

LDFLAGS="${LDFLAGS64}"
export LDFLAGS
sh ./apxs-fcgid.ksh93 -b 64
(cd mod_fcgid.%{mod_fcgid_version}-64
  sh ../install-module.ksh93 -b 64 -m fcgid)
cat fcgid.conf | sed -e 's/::MACH64::/%{_arch64}/;' > ${APACHE_SCONFD}/fcgid.conf

sh ./apxs-security2.ksh93 -b 64
(cd modsecurity-apache_%{modsecurity_version}-64
  sh ../install-module.ksh93 -b 64 -m security2)
cat security2.conf | sed -e 's/::MACH64::/%{_arch64}/;' > ${APACHE_SCONFD}/security2.conf

sh ./apxs-jk.ksh93 -b 64
(cd tomcat-connectors-%{connector_version}-src-64
  sh ../install-module.ksh93 -b 64 -m jk)
cat jk.conf | sed -e 's/::MACH64::/%{_arch64}/;' > ${APACHE_CONFD}/jk.conf
cp workers.properties ${APACHE_CONFD}/workers.properties

%endif

cd ${BLDDIR}/modules
PDIR=`pwd`
MACH64=""
LDFLAGS="${LDFLAGS32} -M ${PDIR}/mod_dtrace-%{mod_dtrace_version}-32/mapfile"
CFLAGS="-m32"
export MACH64 LDFLAGS CFLAGS
sh ./apxs-dtrace.ksh93 -b 32
(cd mod_dtrace-%{mod_dtrace_version}-32
  sh ../install-module.ksh93 -b 32 -m dtrace)

LDFLAGS="${LDFLAGS32}"
export LDFLAGS
sh ./apxs-fcgid.ksh93 -b 32
(cd mod_fcgid.%{mod_fcgid_version}-32
  sh ../install-module.ksh93 -b 32 -m fcgid)

sh ./apxs-security2.ksh93 -b 32
(cd modsecurity-apache_%{modsecurity_version}-32
  sh ../install-module.ksh93 -b 32 -m security2)

sh ./apxs-jk.ksh93 -b 32
(cd tomcat-connectors-%{connector_version}-src-32
  sh ../install-module.ksh93 -b 32 -m jk)

(cd mod_perl-%{mod_perl_version}
  PATH="/opt/SUNWspro/bin:/usr/perl5/bin:${PATH}"
  CFLAGS="-xO3"
  MODPERL_AP_INCLUDEDIR=${APACHE_USR_PREFIX}/include
  MODPERL_AP_LIBEXECDIR=${APACHE_USR_PREFIX}/libexec
  export PATH CFLAGS MODPERL_AP_INCLUDEDIR MODPERL_AP_LIBEXECDIR

  perl Makefile.PL \
      MP_APU_CONFIG=${APR_UTIL_USR_PREFIX}/bin/apu-1-config \
      MP_APR_CONFIG=${APR_USR_PREFIX}/bin/apr-1-config \
      MP_APXS=${ROOT}${APACHE_USR_PREFIX}/bin/apxs \
      INSTALLDIRS=perl \
      INSTALLSITELIB=${AP_PERL5LIB} \
      INSTALLARCHLIB=${AP_PERL5LIB} \
      INSTALLSITEARCH=${AP_PERL5LIB} \
      INSTALLPRIVLIB=${AP_PERL5LIB} \
      SITEARCHEXP=${AP_PERL5LIB} \
      SITELIBEXP=${AP_PERL5LIB} \
      INSTALLMAN1DIR=${PERLMAN}/man1 \
      INSTALLMAN3DIR=${PERLMAN}/man3 \
      INSTALLSCRIPT=${AP_PERL5BIN}
      for i in `find . -name Makefile`
      do
      sed -e '/^CC/s;CC = cc;CC = ${CC};' \
          -e '/^LD =/s;LD = cc;LD = ${CC};' \
          -e '/^CCFLAGS/s;CCFLAGS = ;CCFLAGS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64;' \
          -e '/^MODPERL_CCOPTS/s;MODPERL_CCOPTS = ;MODPERL_CCOPTS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64;' \
          -e '/^MODPERL_INC/s;-I'${APACHE_USR_PREFIX}'/include;-I'${ROOT}${APACHE_USR_PREFIX}'/include;g' \
          -e '/^MODPERL_AP_INCLUDEDIR =/s;'${ROOT}${APACHE_USR_PREFIX}';'${APACHE_USR_PREFIX}';g' \
          -e '/^MODPERL_AP_LIBEXECDIR =/s;'${ROOT}${APACHE_USR_PREFIX}';'${APACHE_USR_PREFIX}';g' \
          -e '/^INC/s;-I${APACHE_USR_PREFIX}/include;-I'${ROOT}${APACHE_USR_PREFIX}'/include;g' \
          -e '/^LDDLFLAGS =/s;-[LR]'${ROOT}${APACHE_USR_PREFIX}'/lib;;g;s; \( *\); ;g' \
          -e '/^LD_RUN_PATH =/s;'${ROOT}${APACHE_USR_PREFIX}'/lib\(:*\);;g;s; \( *\); ;g' $i > $i.1
          mv $i.1 $i
      done
      grep D_LARGEFILE_SOURCE Makefile || for i in `find . -name Makefile`
      do
      sed -e '/^MODPERL_CCOPTS/s;MODPERL_CCOPTS = ;MODPERL_CCOPTS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64;' \
          -e '/^CCFLAGS/s;CCFLAGS = ;CCFLAGS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64;' \
          -e '/^MODPERL_INC/s;-I'${APACHE_USR_PREFIX}'/include;-I'${ROOT}${APACHE_USR_PREFIX}'/include;g' \
          -e '/^INC/s;-I${APACHE_USR_PREFIX}/include;-I${ROOT}${APACHE_USR_PREFIX}/include;g' \
          $$i > $$i.1
          mv $$i.1 $$i
      done
  ${MAKE} -e install

  PREFIX=${ROOT}/${APACHE_USR_PREFIX}
  cd ${PREFIX}/lib
  find . -type d -exec chmod 755 {} \;
  find . -type f -exec chmod 555 {} \;

  cd ${PREFIX}/man
  find . -type d -exec chmod 755 {} \;
  find . -type f -exec chmod 644 {} \;

  cd ${PREFIX}/include
  find . -type d -exec chmod 755 {} \;
  find . -type f -exec chmod 644 {} \;

  cd ${PREFIX}/bin
  sed -e 's/\/usr\/perl5\/5\.8\.4\/bin/\/usr\/perl5\/bin/g' mp2bug > mp2bug.1
  mv -f mp2bug.1 mp2bug
  chmod 555 mp2bug

  cd ${PREFIX}/libexec
  chmod 555 mod_perl.so
)
cd ..
 

%clean
rm -rf $RPM_BUILD_ROOT

%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/original
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/samples-conf.d
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/envvars
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/mime.types
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/magic
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/httpd.conf
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d/modules-32.load
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d/modules-64.load
%attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/original/httpd.conf
%attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/samples-conf.d/*
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/http-apache22
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/network
%class(manifest) %attr (0444, root, bin) %{_localstatedir}/svc/manifest/network/http-apache22.xml
%dir %attr (0755, root, bin) %{_localstatedir}/apache2
%dir %attr (0755, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/htdocs
%dir %attr (0755, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/error
%dir %attr (0755, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/icons
%dir %attr (0755, webservd, webservd) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/logs
%dir %attr (0755, webservd, webservd) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/proxy
%dir %attr (0755, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/cgi-bin
%dir %attr (0755, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/libexec
%attr (0644, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/htdocs/*
%attr (0644, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/error/*
%attr (0644, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/icons/*
%attr (0555, root, bin) %{_localstatedir}/apache2/%{APACHE_VERSION_DIR}/cgi-bin/*

%files -n SUNWapch22u
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/apache2
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/build
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/lib
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/lib/perl
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/bin
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/include
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/build/*
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/lib/perl/*
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/bin/*
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/include/*
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_rewrite.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_mem_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_file_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_disk_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_dir.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_speling.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_env.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authz_groupfile.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_cern_meta.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authz_host.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authn_file.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_headers.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_dav.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authz_default.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_cgi.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_cgid.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_imagemap.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_ssl.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authn_dbd.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authn_default.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_dumpio.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authn_anon.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_perl.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authz_dbm.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authnz_ldap.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_proxy_connect.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_userdir.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_vhost_alias.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_auth_gss.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_dav_fs.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_suexec.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_actions.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authz_user.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_alias.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_proxy.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_asis.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_proxy_balancer.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_info.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_autoindex.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_ldap.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_logio.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_auth_digest.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_unique_id.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_auth_basic.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_deflate.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_ident.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_log_forensic.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_filter.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_negotiation.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_proxy_http.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authn_dbm.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_mime_magic.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_dbd.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_ext_filter.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_version.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_usertrack.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_authz_owner.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_mime.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_include.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_log_config.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_status.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_proxy_ftp.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_proxy_ajp.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_expires.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_setenvif.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_substitute.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/httpd.exp

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/lib/%{_arch64}
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_rewrite.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_mem_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_file_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_disk_cache.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_dir.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_speling.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_env.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authz_groupfile.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_cern_meta.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authz_host.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authn_file.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_headers.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_dav.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authz_default.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_cgi.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_cgid.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_imagemap.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_ssl.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authn_dbd.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authn_default.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_dumpio.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authn_anon.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authz_dbm.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authnz_ldap.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_proxy_connect.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_userdir.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_vhost_alias.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_auth_gss.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_dav_fs.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_suexec.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_actions.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authz_user.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_alias.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_proxy.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_asis.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_proxy_balancer.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_info.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_autoindex.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_ldap.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_logio.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_auth_digest.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_unique_id.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_auth_basic.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_deflate.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_ident.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_log_forensic.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_filter.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_negotiation.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_proxy_http.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authn_dbm.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_mime_magic.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_dbd.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_ext_filter.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_version.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_usertrack.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_authz_owner.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_mime.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_include.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_log_config.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_status.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_proxy_ftp.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_proxy_ajp.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_expires.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_setenvif.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_substitute.so
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/httpd.exp
%endif


%files -n SUNWapch22d
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/apache2
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/man
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/man/man1
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/man/man3
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/man/man8
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/manual
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/man/man1/*
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/man/man3/*
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/man/man8/*
%{_basedir}/apache2/%{APACHE_VERSION_DIR}/manual/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*


%files -n SUNWapch22m-dtrace
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/apache2
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_dtrace.so

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_dtrace.so
%endif

%files -n SUNWapch22r-dtrace
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d/dtrace.conf

%files -n SUNWapch22m-fcgid
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/apache2
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec
%attr (0555,  root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_fcgid.so

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_fcgid.so
%endif

%files -n SUNWapch22r-fcgid
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/samples-conf.d
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/samples-conf.d/fcgid.conf

%files -n SUNWapch22m-jk
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/apache2
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec
%attr (0555,  root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_jk.so

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_jk.so
%endif

%files -n SUNWapch22r-jk
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d/jk.conf
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/conf.d/workers.properties

%files -n SUNWapch22m-security
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/apache2
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec
%attr (0555,  root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/mod_security2.so

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}
%attr (0555, root, bin) %{_basedir}/apache2/%{APACHE_VERSION_DIR}/libexec/%{_arch64}/mod_security2.so
%endif

%files -n SUNWapch22r-security
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}
%dir %attr (0755, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/samples-conf.d
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/apache2/%{APACHE_VERSION_DIR}/samples-conf.d/security2.conf

%changelog
* Mon Feb 23 2009 - moinakg@gmail.com
- Add mod_perl and many other fixes.
- Fixup packaging information.
* Fri Feb 06 2009 - moinakg@gmail.com
- Initial spec (migrated and merged from SFW gate). Incomplete and still work in progress.

