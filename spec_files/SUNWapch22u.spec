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


SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWperl584core


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


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cd %{name}-%{version}

BLDDIR=`pwd`
TMP_HDR_DIR32=${BLDDIR}/Solaris/32/include
TMP_HDR_DIR64=${BLDDIR}/Solaris/64/include
TMP_HDR_DIR=${BLDDIR}/Solaris/include

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
export LD_OPTIONS PATH MAKE DESTDIR INSTALL PERL CXXFLAGS CPPFLAGS APR_USR_PREFIX APR_UTIL_USR_PREFIX ROOT SRC

. ./apache.build.env

mkdir -p ${RPM_BUILD_ROOT}/${APACHE_USR_PREFIX}
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_USR_PREFIX}/lib
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_VAR_PREFIX}
mkdir -p ${RPM_BUILD_ROOT}/${APACHE_VAR_PREFIX}/proxy
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
cat fcgid.conf | sed -e 's/::MACH64::/%{_arch64}/;' > ${APACHE_CONFD}/fcgid.conf

sh ./apxs-security2.ksh93 -b 64
(cd modsecurity-apache_%{modsecurity_version}-64
  sh ../install-module.ksh93 -b 64 -m security2)
cat security2.conf | sed -e 's/::MACH64::/%{_arch64}/;' > ${APACHE_SCONFD}/security2.conf

sh ./apxs-jk.ksh93 -b 64
(cd tomcat-connectors-%{connector_version}-src-64
  sh ../install-module.ksh93 -b 64 -m jk)
%endif

cd ${BLDDIR}/modules
PDIR=`pwd`
MACH64=""
LDFLAGS="${LDFLAGS32} -M ${PDIR}/mod_dtrace-%{mod_dtrace_version}-32/mapfile"
CFLAGS="-m32"
export ROOT MACH64 LDFLAGS CFLAGS
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
cd ..
 

%clean
rm -rf $RPM_BUILD_ROOT

%iclass preserve -f i.preserve

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/gnu
%dir %attr (0755, lp, lp) %{_sysconfdir}/lp
%dir %attr (0755, root, lp) %{_sysconfdir}/lp/fd
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/gnu/a2ps.cfg
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/gnu/a2ps-site.cfg
%attr (0755, root, lp) %{_sysconfdir}/lp/fd/a2ps.fd

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/a2ps
%dir %attr (0755, root, root) %{_datadir}/a2ps/afm
%dir %attr (0755, root, root) %{_datadir}/a2ps/encoding
%dir %attr (0755, root, root) %{_datadir}/a2ps/fonts
%dir %attr (0755, root, root) %{_datadir}/a2ps/ppd
%dir %attr (0755, root, root) %{_datadir}/a2ps/ps
%dir %attr (0755, root, root) %{_datadir}/a2ps/sheets
%dir %attr (0755, root, root) %{_datadir}/ogonkify
%dir %attr (0755, root, root) %{_datadir}/ogonkify/afm
%dir %attr (0755, root, root) %{_datadir}/ogonkify/fonts
%attr (0755, root, bin) %{_datadir}/a2ps/README
%attr (0755, root, bin) %{_datadir}/ogonkify/README
%attr (0755, root, bin) %{_datadir}/ogonkify/*.enc
%attr (0755, root, bin) %{_datadir}/ogonkify/*.ps
%{_datadir}/a2ps/afm/*
%{_datadir}/a2ps/encoding/*
%{_datadir}/a2ps/fonts/*
%{_datadir}/a2ps/ppd/*
%{_datadir}/a2ps/ps/*
%{_datadir}/a2ps/sheets/*
%{_datadir}/ogonkify/afm/*
%{_datadir}/ogonkify/fonts/*

%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%dir %attr (0755, root, bin) %{_basedir}/sfw
%dir %attr (0755, root, bin) %{_basedir}/sfw/bin
%{_basedir}/sfw/bin/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*

%changelog
* Fri Feb 06 2009 - moinakg@gmail.com
- Initial spec (migrated and merged from SFW gate). Incomplete and still work in progress.

